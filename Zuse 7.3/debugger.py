# FILE: debugger.py
# Zuse Debugger — Breakpoints und Einzelschritt-Ausführung (Phase 5.5)
# Wird optional an den Interpreter angehängt.

import threading


# ─── Debug-Zustände ──────────────────────────────────────────────────────

RUNNING = "RUNNING"
PAUSED = "PAUSED"
STEPPING_INTO = "STEPPING_INTO"
STEPPING_OVER = "STEPPING_OVER"
STOPPED = "STOPPED"


# ─── Call Frame ──────────────────────────────────────────────────────────

class CallFrame:
    """Ein Eintrag im Aufruf-Stapel."""
    __slots__ = ('func_name', 'line', 'env')

    def __init__(self, func_name, line, env=None):
        self.func_name = func_name
        self.line = line
        self.env = env

    def __repr__(self):
        return f"CallFrame({self.func_name!r}, Zeile {self.line})"


# ─── Debugger ────────────────────────────────────────────────────────────

class ZuseDebugger:
    """
    Debugger für die Zuse-Programmiersprache.

    Funktionen:
    - Breakpoints setzen/entfernen
    - Einzelschritt (step into, step over)
    - Variablen inspizieren
    - Aufruf-Stapel anzeigen

    Verwendung:
        debugger = ZuseDebugger(source_code=code, on_pause=callback)
        debugger.set_breakpoint(5)
        interpreter._debugger = debugger
        interpreter.interpretiere(ast)
    """

    def __init__(self, source_code="", on_pause=None):
        self._breakpoints = set()
        self._state = RUNNING
        self._call_stack = []
        self._step_depth = 0
        self._current_line = 0
        self._current_env = None
        self._source_lines = source_code.splitlines() if source_code else []
        self._on_pause = on_pause
        self._pause_event = threading.Event()
        self._pause_event.set()  # Nicht blockiert am Anfang

    # ─── Breakpoints ─────────────────────────────────────────────────

    def set_breakpoint(self, line):
        """Setzt einen Breakpoint auf eine Zeilennummer."""
        self._breakpoints.add(line)

    def remove_breakpoint(self, line):
        """Entfernt einen Breakpoint."""
        self._breakpoints.discard(line)

    def get_breakpoints(self):
        """Gibt alle Breakpoints zurück."""
        return set(self._breakpoints)

    def has_breakpoint(self, line):
        """Prüft ob auf dieser Zeile ein Breakpoint liegt."""
        return line in self._breakpoints

    # ─── Interpreter-Hooks ───────────────────────────────────────────

    def on_statement(self, line, env):
        """
        Wird vom Interpreter vor jeder Anweisung aufgerufen.
        Entscheidet ob die Ausführung pausiert werden soll.
        """
        if self._state == STOPPED:
            return

        self._current_line = line
        self._current_env = env

        should_pause = False
        if line in self._breakpoints:
            should_pause = True
        elif self._state == STEPPING_INTO:
            should_pause = True
        elif self._state == STEPPING_OVER and len(self._call_stack) <= self._step_depth:
            should_pause = True

        if should_pause:
            self._state = PAUSED
            self._pause_event.clear()
            if self._on_pause:
                self._on_pause(self)
            self._pause_event.wait()

    def on_call(self, func_name, line, env=None):
        """Wird aufgerufen wenn eine Zuse-Funktion betreten wird."""
        self._call_stack.append(CallFrame(func_name, line, env))

    def on_return(self):
        """Wird aufgerufen wenn eine Zuse-Funktion verlassen wird."""
        if self._call_stack:
            self._call_stack.pop()

    # ─── Steuerung ───────────────────────────────────────────────────

    def do_continue(self):
        """Weiter bis zum nächsten Breakpoint."""
        self._state = RUNNING
        self._pause_event.set()

    def do_step_into(self):
        """Einen Schritt ausführen, in Funktionen hineinspringen."""
        self._state = STEPPING_INTO
        self._pause_event.set()

    def do_step_over(self):
        """Einen Schritt ausführen, Funktionsaufrufe überspringen."""
        self._step_depth = len(self._call_stack)
        self._state = STEPPING_OVER
        self._pause_event.set()

    def do_stop(self):
        """Debugger-Sitzung beenden."""
        self._state = STOPPED
        self._pause_event.set()

    # ─── Inspektion ──────────────────────────────────────────────────

    def get_variables(self, env=None):
        """Gibt sichtbare Variablen im aktuellen Scope zurück."""
        env = env or self._current_env
        if env is None:
            return {}
        result = {}
        all_syms = env.all_symbols(local_only=False)
        for name, sym in all_syms.items():
            if sym.scope_type == 'builtin':
                continue
            if name.startswith('__'):
                continue
            result[name] = sym.value
        return result

    def get_local_variables(self, env=None):
        """Gibt nur lokale Variablen zurück (ohne Parent-Scopes)."""
        env = env or self._current_env
        if env is None:
            return {}
        result = {}
        all_syms = env.all_symbols(local_only=True)
        for name, sym in all_syms.items():
            if sym.scope_type == 'builtin':
                continue
            if name.startswith('__'):
                continue
            result[name] = sym.value
        return result

    def get_call_stack(self):
        """Gibt den Aufruf-Stapel zurück."""
        return [{"name": f.func_name, "line": f.line} for f in self._call_stack]

    def get_source_line(self, line):
        """Gibt den Quellcode einer Zeile zurück."""
        idx = line - 1
        if 0 <= idx < len(self._source_lines):
            return self._source_lines[idx]
        return ""

    def get_source_context(self, line=None, context=3):
        """
        Gibt umgebende Zeilen zurück.
        Returns: Liste von (zeilennr, text, ist_aktuelle_zeile) Tupeln
        """
        if line is None:
            line = self._current_line
        result = []
        start = max(1, line - context)
        end = min(len(self._source_lines), line + context)
        for i in range(start, end + 1):
            text = self._source_lines[i - 1] if i - 1 < len(self._source_lines) else ""
            result.append((i, text, i == line))
        return result

    @property
    def is_paused(self):
        return self._state == PAUSED

    @property
    def is_running(self):
        return self._state in (RUNNING, STEPPING_INTO, STEPPING_OVER)

    @property
    def is_stopped(self):
        return self._state == STOPPED
