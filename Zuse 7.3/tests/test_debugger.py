# FILE: tests/test_debugger.py
# Tests für den Zuse Debugger (Phase 5.5)

import sys, os, threading
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from debugger import ZuseDebugger, CallFrame, RUNNING, PAUSED, STEPPING_INTO, STEPPING_OVER, STOPPED
from interpreter import Interpreter
from language_loader import lade_sprache
from lexer import tokenize
from parser import Parser


# ─── Hilfsfunktionen ────────────────────────────────────────────────────

def _debug_run(code, debugger, sprache="deutsch"):
    """Führt Code mit Debugger aus und gibt Ausgaben zurück."""
    config = lade_sprache(sprache)
    tokens = tokenize(code, config)
    ast = Parser(tokens).parse()
    ausgaben = []
    interp = Interpreter(output_callback=lambda t: ausgaben.append(str(t)))
    interp._debugger = debugger
    interp.interpretiere(ast)
    return ausgaben


def _debug_run_threaded(code, debugger, sprache="deutsch", timeout=5):
    """Führt Code mit Debugger in einem Thread aus."""
    config = lade_sprache(sprache)
    tokens = tokenize(code, config)
    ast = Parser(tokens).parse()
    ausgaben = []
    error = [None]
    interp = Interpreter(output_callback=lambda t: ausgaben.append(str(t)))
    interp._debugger = debugger

    def run():
        try:
            interp.interpretiere(ast)
        except Exception as e:
            error[0] = e

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(timeout=timeout)
    return ausgaben, error[0]


# ─── Breakpoints ─────────────────────────────────────────────────────────

class TestBreakpoints:
    def test_set_remove_breakpoint(self):
        dbg = ZuseDebugger()
        dbg.set_breakpoint(5)
        dbg.set_breakpoint(10)
        assert dbg.get_breakpoints() == {5, 10}
        assert dbg.has_breakpoint(5)
        dbg.remove_breakpoint(5)
        assert dbg.get_breakpoints() == {10}
        assert not dbg.has_breakpoint(5)

    def test_remove_nonexistent_breakpoint(self):
        dbg = ZuseDebugger()
        dbg.remove_breakpoint(99)  # Kein Fehler

    def test_breakpoint_pauses_execution(self):
        code = "x = 1\nAUSGABE x\ny = 2"
        paused_lines = []

        def on_pause(dbg):
            paused_lines.append(dbg._current_line)
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)
        _debug_run(code, debugger)
        assert 2 in paused_lines

    def test_continue_after_breakpoint(self):
        code = "x = 10\nAUSGABE x\ny = 20\nAUSGABE y"

        def on_pause(dbg):
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)
        ausgaben = _debug_run(code, debugger)
        assert "10" in ausgaben
        assert "20" in ausgaben

    def test_multiple_breakpoints(self):
        code = "x = 1\ny = 2\nz = 3\nAUSGABE x + y + z"
        paused_lines = []

        def on_pause(dbg):
            paused_lines.append(dbg._current_line)
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)
        debugger.set_breakpoint(4)
        _debug_run(code, debugger)
        assert 2 in paused_lines
        assert 4 in paused_lines


# ─── Einzelschritt ───────────────────────────────────────────────────────

class TestStepping:
    def test_step_into(self):
        code = "x = 1\ny = 2\nAUSGABE x + y"
        visited_lines = []

        def on_pause(dbg):
            visited_lines.append(dbg._current_line)
            dbg.do_step_into()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger._state = STEPPING_INTO
        _debug_run(code, debugger)
        assert len(visited_lines) >= 3  # Mindestens 3 Zeilen

    def test_step_over_skips_function(self):
        code = "DEFINIERE f():\n    x = 1\n    y = 2\nENDE FUNKTION\nf()\nAUSGABE 42"
        visited_lines = []

        def on_pause(dbg):
            visited_lines.append(dbg._current_line)
            dbg.do_step_over()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger._state = STEPPING_INTO
        _debug_run(code, debugger)
        # Bei step-over sollten die internen Zeilen 2,3 NICHT einzeln besucht werden
        assert 1 in visited_lines  # DEFINIERE
        assert 6 in visited_lines  # AUSGABE 42
        # Interne Funktionszeilen sollten nicht als separate Stops auftauchen
        assert 2 not in visited_lines
        assert 3 not in visited_lines

    def test_step_into_enters_function(self):
        code = "DEFINIERE f():\n    AUSGABE 99\nENDE FUNKTION\nf()"
        visited_lines = []

        def on_pause(dbg):
            visited_lines.append(dbg._current_line)
            dbg.do_step_into()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger._state = STEPPING_INTO
        _debug_run(code, debugger)
        assert 2 in visited_lines  # AUSGABE 99 innerhalb der Funktion


# ─── Variablen-Inspektion ───────────────────────────────────────────────

class TestVariableInspection:
    def test_get_variables_at_breakpoint(self):
        code = "x = 42\ny = 10\nAUSGABE x"
        captured_vars = {}

        def on_pause(dbg):
            captured_vars.update(dbg.get_variables())
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(3)
        _debug_run(code, debugger)
        assert captured_vars.get("x") == 42
        assert captured_vars.get("y") == 10

    def test_variables_in_function_scope(self):
        code = "DEFINIERE f(a, b):\n    summe = a + b\n    AUSGABE summe\nENDE FUNKTION\nf(3, 7)"
        captured_vars = {}

        def on_pause(dbg):
            captured_vars.update(dbg.get_local_variables())
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(3)  # AUSGABE summe
        _debug_run(code, debugger)
        assert captured_vars.get("a") == 3
        assert captured_vars.get("b") == 7
        assert captured_vars.get("summe") == 10

    def test_local_variables_in_function(self):
        """In einem Funktions-Scope sieht get_local_variables nur lokale Vars."""
        code = "DEFINIERE f(a):\n    b = a * 2\n    AUSGABE b\nENDE FUNKTION\nf(5)"
        captured_local = {}

        def on_pause(dbg):
            captured_local.update(dbg.get_local_variables())
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(3)  # AUSGABE b
        _debug_run(code, debugger)
        assert "a" in captured_local
        assert "b" in captured_local
        assert captured_local["b"] == 10
        # Globale Stdlib-Funktionen nicht in lokalen Variablen
        assert "str" not in captured_local
        assert "BEREICH" not in captured_local


# ─── Aufruf-Stapel ──────────────────────────────────────────────────────

class TestCallStack:
    def test_call_stack_in_function(self):
        code = "DEFINIERE f():\n    AUSGABE 1\nENDE FUNKTION\nf()"
        captured_stack = []

        def on_pause(dbg):
            captured_stack.extend(dbg.get_call_stack())
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)
        _debug_run(code, debugger)
        assert len(captured_stack) == 1
        assert captured_stack[0]["name"] == "f"

    def test_nested_call_stack(self):
        code = "DEFINIERE a():\n    AUSGABE 1\nENDE FUNKTION\nDEFINIERE b():\n    a()\nENDE FUNKTION\nb()"
        captured_stack = []

        def on_pause(dbg):
            captured_stack.extend(dbg.get_call_stack())
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)  # AUSGABE 1 in a()
        _debug_run(code, debugger)
        assert len(captured_stack) == 2
        names = [f["name"] for f in captured_stack]
        assert "b" in names
        assert "a" in names

    def test_call_stack_empty_at_top_level(self):
        code = "x = 1\nAUSGABE x"
        captured_stack = []

        def on_pause(dbg):
            captured_stack.extend(dbg.get_call_stack())
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(1)
        _debug_run(code, debugger)
        assert len(captured_stack) == 0


# ─── Quellcode-Anzeige ──────────────────────────────────────────────────

class TestSourceContext:
    def test_get_source_line(self):
        dbg = ZuseDebugger(source_code="Zeile 1\nZeile 2\nZeile 3")
        assert dbg.get_source_line(1) == "Zeile 1"
        assert dbg.get_source_line(2) == "Zeile 2"
        assert dbg.get_source_line(3) == "Zeile 3"
        assert dbg.get_source_line(99) == ""

    def test_get_source_context(self):
        code = "\n".join(f"Zeile {i}" for i in range(1, 11))
        dbg = ZuseDebugger(source_code=code)
        dbg._current_line = 5
        ctx = dbg.get_source_context(context=2)
        lines = [num for num, text, is_cur in ctx]
        assert 3 in lines
        assert 5 in lines
        assert 7 in lines
        # Aktuelle Zeile markiert
        current = [c for c in ctx if c[2]]
        assert len(current) == 1
        assert current[0][0] == 5


# ─── Integration ─────────────────────────────────────────────────────────

class TestIntegration:
    def test_debugger_is_optional(self):
        """Interpreter funktioniert ohne Debugger."""
        from conftest import zuse_ausfuehren
        result = zuse_ausfuehren("AUSGABE 42")
        assert "42" in result

    def test_no_debugger_by_default(self):
        interp = Interpreter()
        assert interp._debugger is None

    def test_full_debug_session(self):
        """Kompletter Debugging-Ablauf: Breakpoint, inspizieren, weiter."""
        code = "x = 10\ny = 20\nz = x + y\nAUSGABE z"
        events = []

        def on_pause(dbg):
            line = dbg._current_line
            variables = dbg.get_variables()
            events.append({"line": line, "vars": dict(variables)})
            if line == 2:
                dbg.do_step_into()  # Zum nächsten Schritt
            else:
                dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)
        ausgaben = _debug_run(code, debugger)

        # Mindestens 2 Pausen: Zeile 2 (BP) und Zeile 3 (Step)
        assert len(events) >= 2
        assert events[0]["line"] == 2
        assert events[0]["vars"].get("x") == 10
        assert events[1]["line"] == 3
        assert events[1]["vars"].get("y") == 20
        assert "30" in ausgaben

    def test_debugger_does_not_break_output(self):
        """Debugger verändert die Programmausgabe nicht."""
        code = "AUSGABE 1\nAUSGABE 2\nAUSGABE 3"

        def on_pause(dbg):
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(2)
        ausgaben = _debug_run(code, debugger)
        assert ausgaben == ["1", "2", "3"]

    def test_debugger_with_loop(self):
        """Debugger funktioniert mit Schleifen."""
        code = "x = 0\nSOLANGE x < 3 MACHE\n    x = x + 1\nENDE SCHLEIFE\nAUSGABE x"
        pause_count = [0]

        def on_pause(dbg):
            pause_count[0] += 1
            dbg.do_continue()

        debugger = ZuseDebugger(source_code=code, on_pause=on_pause)
        debugger.set_breakpoint(3)  # x = x + 1
        ausgaben = _debug_run(code, debugger)
        assert "3" in ausgaben
        assert pause_count[0] == 3  # 3 Schleifendurchläufe
