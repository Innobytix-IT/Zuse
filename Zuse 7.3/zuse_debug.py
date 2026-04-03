# FILE: zuse_debug.py
# Zuse Debugger — Interaktive Kommandozeile (Phase 5.5)
# Benutzung: python zuse_debug.py <datei.zuse> [sprache]

import sys
import os
import io
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Windows-Konsole auf UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from debugger import ZuseDebugger
from interpreter import Interpreter
from language_loader import lade_sprache
from lexer import tokenize
from parser import Parser


class ZuseDebugCLI:
    """Interaktiver Kommandozeilen-Debugger für Zuse."""

    def __init__(self, filename, sprache="deutsch"):
        if not os.path.exists(filename):
            print(f"Fehler: Datei '{filename}' nicht gefunden.")
            sys.exit(1)

        with open(filename, 'r', encoding='utf-8') as f:
            self.source = f.read()

        self.filename = filename
        self.sprache = sprache
        self.debugger = ZuseDebugger(source_code=self.source, on_pause=self._on_pause)
        self._prompt_event = threading.Event()
        self._quit = False
        self._interp_done = False
        self._interp_error = None

    def _on_pause(self, dbg):
        """Callback: Wird aufgerufen wenn der Debugger pausiert."""
        self._show_current_line()
        self._prompt_event.set()

    def _show_current_line(self):
        """Zeigt die aktuelle Zeile an."""
        line = self.debugger._current_line
        text = self.debugger.get_source_line(line)
        bp = "*" if self.debugger.has_breakpoint(line) else " "
        print(f">{bp}{line:4d} | {text}")

    def run(self):
        """Startet den Debugger."""
        print(f"Zuse Debugger — {self.filename}")
        print(f"Tippe 'h' fuer Hilfe.\n")

        # Code parsen
        try:
            config = lade_sprache(self.sprache)
            tokens = tokenize(self.source, config)
            ast = Parser(tokens).parse()
        except Exception as e:
            print(f"Fehler beim Parsen: {e}")
            sys.exit(1)

        # Interpreter vorbereiten
        interp = Interpreter(output_callback=print, sprache=self.sprache)
        interp.working_dir = os.path.dirname(os.path.abspath(self.filename))
        interp._debugger = self.debugger

        # Am Anfang anhalten
        self.debugger._state = "STEPPING_INTO"

        # Interpreter im Hintergrund starten
        def run_interpreter():
            try:
                interp.interpretiere(ast)
            except Exception as e:
                self._interp_error = str(e)
            finally:
                self._interp_done = True
                self._prompt_event.set()

        thread = threading.Thread(target=run_interpreter, daemon=True)
        thread.start()

        # REPL
        while not self._quit:
            self._prompt_event.wait(timeout=1.0)
            if self._interp_done:
                if self._interp_error:
                    print(f"\nFehler: {self._interp_error}")
                else:
                    print("\nProgramm beendet.")
                break
            if self._prompt_event.is_set():
                self._prompt_event.clear()
                self._command_loop()

        self.debugger.do_stop()

    def _command_loop(self):
        """Liest und verarbeitet Debug-Befehle."""
        while not self._quit and not self._interp_done:
            try:
                cmd = input("(zuse-debug) ").strip()
            except (EOFError, KeyboardInterrupt):
                self._quit = True
                break
            if not cmd:
                continue
            parts = cmd.split(None, 1)
            command = parts[0].lower()
            arg = parts[1].strip() if len(parts) > 1 else ""
            if not self._dispatch(command, arg):
                break  # Ausführung wurde fortgesetzt

    def _dispatch(self, command, arg):
        """Verarbeitet einen Befehl. Gibt False zurück wenn die Ausführung fortgesetzt wird."""
        cmds = {
            'b': self._cmd_break, 'break': self._cmd_break,
            'c': self._cmd_continue, 'continue': self._cmd_continue,
            'weiter': self._cmd_continue,
            's': self._cmd_step, 'step': self._cmd_step,
            'schritt': self._cmd_step,
            'n': self._cmd_next, 'next': self._cmd_next,
            'p': self._cmd_print, 'print': self._cmd_print,
            'ausgabe': self._cmd_print,
            'l': self._cmd_list, 'list': self._cmd_list,
            'w': self._cmd_where, 'where': self._cmd_where,
            'stapel': self._cmd_where,
            'q': self._cmd_quit, 'quit': self._cmd_quit,
            'beenden': self._cmd_quit,
            'h': self._cmd_help, 'help': self._cmd_help,
            'hilfe': self._cmd_help,
        }
        handler = cmds.get(command)
        if handler:
            return handler(arg)
        print(f"Unbekannter Befehl: '{command}'. Tippe 'h' fuer Hilfe.")
        return True  # Weiter im Befehlsmodus

    def _cmd_break(self, arg):
        """Breakpoint setzen/entfernen/anzeigen."""
        if not arg:
            bps = sorted(self.debugger.get_breakpoints())
            if bps:
                print("Breakpoints:")
                for bp in bps:
                    text = self.debugger.get_source_line(bp)
                    print(f"  Zeile {bp}: {text}")
            else:
                print("Keine Breakpoints gesetzt.")
            return True
        if arg.startswith('-'):
            try:
                line = int(arg[1:])
                self.debugger.remove_breakpoint(line)
                print(f"Breakpoint auf Zeile {line} entfernt.")
            except ValueError:
                print("Benutzung: b <zeile> oder b -<zeile>")
        else:
            try:
                line = int(arg)
                self.debugger.set_breakpoint(line)
                text = self.debugger.get_source_line(line)
                print(f"Breakpoint auf Zeile {line}: {text}")
            except ValueError:
                print("Benutzung: b <zeile> oder b -<zeile>")
        return True

    def _cmd_continue(self, arg):
        """Weiter bis zum nächsten Breakpoint."""
        self.debugger.do_continue()
        return False

    def _cmd_step(self, arg):
        """Einzelschritt (hineinspringen)."""
        self.debugger.do_step_into()
        return False

    def _cmd_next(self, arg):
        """Nächster Schritt (überspringen)."""
        self.debugger.do_step_over()
        return False

    def _cmd_print(self, arg):
        """Variable(n) anzeigen."""
        if not arg:
            variables = self.debugger.get_variables()
            if not variables:
                print("Keine Variablen im aktuellen Scope.")
            else:
                for name, value in sorted(variables.items()):
                    print(f"  {name} = {_format_value(value)}")
        else:
            variables = self.debugger.get_variables()
            if arg in variables:
                print(f"  {arg} = {_format_value(variables[arg])}")
            else:
                print(f"  Variable '{arg}' nicht gefunden.")
        return True

    def _cmd_list(self, arg):
        """Quellcode um aktuelle Zeile anzeigen."""
        context = 5
        if arg:
            try:
                context = int(arg)
            except ValueError:
                pass
        lines = self.debugger.get_source_context(context=context)
        for num, text, is_current in lines:
            marker = ">" if is_current else " "
            bp = "*" if self.debugger.has_breakpoint(num) else " "
            print(f"{marker}{bp}{num:4d} | {text}")
        return True

    def _cmd_where(self, arg):
        """Aufruf-Stapel anzeigen."""
        stack = self.debugger.get_call_stack()
        if not stack:
            print(f"  <hauptprogramm> Zeile {self.debugger._current_line}")
        else:
            print(f"  <hauptprogramm>")
            for i, frame in enumerate(stack):
                indent = "  " * (i + 1)
                print(f"  {indent}{frame['name']}() Zeile {frame['line']}")
            print(f"  {'  ' * (len(stack) + 1)}-> Zeile {self.debugger._current_line}")
        return True

    def _cmd_quit(self, arg):
        """Debugger beenden."""
        self._quit = True
        return False

    def _cmd_help(self, arg):
        """Hilfe anzeigen."""
        print("""
Zuse Debugger — Befehle:
  b [zeile]     Breakpoint setzen (b), anzeigen (b), entfernen (b -zeile)
  c / weiter    Weiter bis zum naechsten Breakpoint
  s / schritt   Einzelschritt (in Funktionen hineinspringen)
  n / next      Naechster Schritt (Funktionen ueberspringen)
  p [variable]  Variable(n) anzeigen
  l [n]         Quellcode anzeigen (n Zeilen Kontext)
  w / stapel    Aufruf-Stapel anzeigen
  q / beenden   Debugger beenden
  h / hilfe     Diese Hilfe anzeigen
""".strip())
        return True


def _format_value(value):
    """Formatiert einen Wert für die Anzeige."""
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, list):
        if len(value) > 10:
            return f"[{', '.join(str(v) for v in value[:10])}, ... ({len(value)} Elemente)]"
        return str(value)
    return str(value)


def main():
    if len(sys.argv) < 2:
        print("Benutzung: python zuse_debug.py <datei.zuse> [sprache]")
        print("Beispiel:  python zuse_debug.py mein_programm.zuse deutsch")
        sys.exit(1)

    filename = sys.argv[1]
    sprache = sys.argv[2] if len(sys.argv) > 2 else "deutsch"

    cli = ZuseDebugCLI(filename, sprache)
    cli.run()


if __name__ == "__main__":
    main()
