# FILE: tests/test_semantik.py
# Tests für die semantische Analyse (Phase 3.2)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ast
from semantic_analyzer import SemanticAnalyzer, SemanticError, SemanticWarning


def analysiere(code, sprache="deutsch"):
    """Hilfsfunktion: Zuse-Code → (errors, warnings)."""
    ast = zuse_ast(code, sprache)
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(ast)


# ─── Undefinierte Variablen ──────────────────────────────────────────────────

class TestUndefinierteVariablen:
    def test_definierte_variable_ok(self):
        errors, warnings = analysiere("x = 5\nAUSGABE x")
        assert len(errors) == 0
        # x ist definiert, keine Warnung dafür
        var_warnings = [w for w in warnings if "x" in w.nachricht]
        assert len(var_warnings) == 0

    def test_undefinierte_variable_warnung(self):
        errors, warnings = analysiere("AUSGABE x")
        var_warnings = [w for w in warnings if "'x'" in w.nachricht]
        assert len(var_warnings) == 1
        assert "bevor sie definiert" in var_warnings[0].nachricht

    def test_variable_in_bedingung_undefiniert(self):
        errors, warnings = analysiere("WENN y == 5 DANN\nAUSGABE 1\nENDE WENN")
        var_warnings = [w for w in warnings if "'y'" in w.nachricht]
        assert len(var_warnings) == 1

    def test_builtins_immer_definiert(self):
        errors, warnings = analysiere("AUSGABE wahr\nAUSGABE falsch")
        assert len(errors) == 0
        var_warnings = [w for w in warnings if "definiert" in w.nachricht]
        assert len(var_warnings) == 0

    def test_funktion_definiert_variablen(self):
        code = "DEFINIERE foo(x)\nAUSGABE x\nENDE FUNKTION\nfoo(5)"
        errors, warnings = analysiere(code)
        var_warnings = [w for w in warnings if "'x'" in w.nachricht]
        assert len(var_warnings) == 0

    def test_for_schleife_definiert_variable(self):
        code = "SCHLEIFE FÜR i IN BEREICH(5) MACHE\nAUSGABE i\nENDE SCHLEIFE"
        errors, warnings = analysiere(code)
        var_warnings = [w for w in warnings if "'i'" in w.nachricht]
        assert len(var_warnings) == 0

    def test_mehrfach_zuweisung_definiert(self):
        code = "a, b = 1, 2\nAUSGABE a\nAUSGABE b"
        errors, warnings = analysiere(code)
        var_warnings = [w for w in warnings if "definiert" in w.nachricht]
        assert len(var_warnings) == 0


# ─── Break/Continue außerhalb von Schleifen ──────────────────────────────────

class TestAbbruchWeiter:
    def test_abbruch_in_schleife_ok(self):
        code = "SCHLEIFE SOLANGE wahr MACHE\nABBRUCH\nENDE SCHLEIFE"
        errors, warnings = analysiere(code)
        assert len(errors) == 0

    def test_abbruch_ausserhalb_fehler(self):
        code = "ABBRUCH"
        errors, warnings = analysiere(code)
        assert len(errors) == 1
        assert "ABBRUCH" in errors[0].nachricht
        assert "Schleife" in errors[0].nachricht

    def test_weiter_in_schleife_ok(self):
        code = "SCHLEIFE FÜR i IN BEREICH(5) MACHE\nWEITER\nENDE SCHLEIFE"
        errors, warnings = analysiere(code)
        assert len(errors) == 0

    def test_weiter_ausserhalb_fehler(self):
        code = "WEITER"
        errors, warnings = analysiere(code)
        assert len(errors) == 1
        assert "WEITER" in errors[0].nachricht

    def test_abbruch_in_verschachtelter_schleife_ok(self):
        code = "SCHLEIFE SOLANGE wahr MACHE\nSCHLEIFE SOLANGE wahr MACHE\nABBRUCH\nENDE SCHLEIFE\nENDE SCHLEIFE"
        errors, warnings = analysiere(code)
        assert len(errors) == 0


# ─── Return außerhalb von Funktionen ─────────────────────────────────────────

class TestErgebnis:
    def test_ergebnis_in_funktion_ok(self):
        code = "DEFINIERE foo()\nERGEBNIS IST 42\nENDE FUNKTION"
        errors, warnings = analysiere(code)
        ergebnis_errors = [e for e in errors if "ERGEBNIS" in e.nachricht]
        assert len(ergebnis_errors) == 0

    def test_ergebnis_ausserhalb_fehler(self):
        code = "ERGEBNIS IST 42"
        errors, warnings = analysiere(code)
        assert len(errors) == 1
        assert "ERGEBNIS" in errors[0].nachricht
        assert "Funktion" in errors[0].nachricht


# ─── Builtin-Shadowing ──────────────────────────────────────────────────────

class TestShadowing:
    def test_builtin_shadowing_warnung(self):
        code = "DEFINIERE len()\nERGEBNIS 0\nENDE FUNKTION"
        errors, warnings = analysiere(code)
        shadow_warnings = [w for w in warnings if "überschattet" in w.nachricht]
        assert len(shadow_warnings) == 1

    def test_normale_funktion_ok(self):
        code = "DEFINIERE meine_funktion(x)\nERGEBNIS x\nENDE FUNKTION"
        errors, warnings = analysiere(code)
        shadow_warnings = [w for w in warnings if "überschattet" in w.nachricht]
        assert len(shadow_warnings) == 0


# ─── Klassen ─────────────────────────────────────────────────────────────────

class TestKlassen:
    def test_klasse_definiert_ok(self):
        code = "KLASSE Hund:\nDEFINIERE bellen()\nAUSGABE 1\nENDE FUNKTION\nENDE KLASSE"
        errors, warnings = analysiere(code)
        assert len(errors) == 0

    def test_methoden_parameter_ok(self):
        code = "KLASSE Tier:\nDEFINIERE sag(text)\nAUSGABE text\nENDE FUNKTION\nENDE KLASSE"
        errors, warnings = analysiere(code)
        var_warnings = [w for w in warnings if "'text'" in w.nachricht]
        assert len(var_warnings) == 0


# ─── Komplexprogramm ────────────────────────────────────────────────────────

class TestKomplex:
    def test_korrektes_programm_keine_fehler(self):
        code = """x = 10
y = 20
DEFINIERE addiere(a, b)
    ERGEBNIS a + b
ENDE FUNKTION
summe = addiere(x, y)
AUSGABE summe
SCHLEIFE FÜR i IN BEREICH(5) MACHE
    WENN i == 3 DANN
        ABBRUCH
    ENDE WENN
    AUSGABE i
ENDE SCHLEIFE"""
        errors, warnings = analysiere(code)
        assert len(errors) == 0

    def test_try_catch_analyse(self):
        code = """VERSUCHE
    x = 10
    AUSGABE x
FANGE
    AUSGABE 0
ENDE VERSUCHE"""
        errors, warnings = analysiere(code)
        assert len(errors) == 0


# ─── Mehrsprachig ───────────────────────────────────────────────────────────

class TestMehrsprachig:
    def test_english_break_outside_loop(self):
        code = "BREAK"
        errors, warnings = analysiere(code, sprache="english")
        assert len(errors) == 1
        assert "ABBRUCH" in errors[0].nachricht or "Schleife" in errors[0].nachricht

    def test_english_correct_program(self):
        code = "x = 5\nPRINT x"
        errors, warnings = analysiere(code, sprache="english")
        assert len(errors) == 0
