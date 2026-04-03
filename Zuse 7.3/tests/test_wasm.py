# FILE: tests/test_wasm.py
# Tests für das WASM-Backend (Phase 5.3)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transpiler import transpile


def transpiliere(code):
    return transpile(code, source_lang="deutsch", target_backend="wasm", include_stdlib=False)["code"]


# ─── Grundstruktur ────────────────────────────────────────────────────────

class TestGrundstruktur:
    def test_hat_module(self):
        code = transpiliere('AUSGABE 42')
        assert "(module" in code
        assert code.strip().endswith(")")

    def test_hat_memory(self):
        code = transpiliere('AUSGABE 42')
        assert "(memory" in code

    def test_hat_start_funktion(self):
        code = transpiliere('AUSGABE 42')
        assert "$main" in code or "_start" in code

    def test_hat_imports(self):
        code = transpiliere('AUSGABE 42')
        assert "import" in code
        assert "print" in code

    def test_hat_header_kommentar(self):
        code = transpiliere('AUSGABE 42')
        assert "Zuse Transpiler" in code
        assert "WAT" in code or "WebAssembly" in code


# ─── Ausgabe ──────────────────────────────────────────────────────────────

class TestAusgabe:
    def test_ausgabe_zahl(self):
        code = transpiliere("AUSGABE 42")
        assert "f64.const 42" in code
        assert "call $print_f64" in code

    def test_ausgabe_string(self):
        code = transpiliere('AUSGABE "Hallo"')
        assert "call $print_str" in code
        assert "Hallo" in code

    def test_string_in_data_section(self):
        code = transpiliere('AUSGABE "Welt"')
        assert "(data" in code
        assert "Welt" in code


# ─── Variablen ────────────────────────────────────────────────────────────

class TestVariablen:
    def test_zuweisung_und_ausgabe(self):
        code = transpiliere("x = 10\nAUSGABE x")
        assert "local.set $x" in code
        assert "local.get $x" in code

    def test_lokale_deklaration(self):
        code = transpiliere("x = 5")
        assert "(local $x f64)" in code

    def test_pi_konstante(self):
        code = transpiliere("AUSGABE PI")
        assert "3.14159" in code

    def test_e_konstante(self):
        code = transpiliere("AUSGABE E")
        assert "2.71828" in code


# ─── Arithmetik ───────────────────────────────────────────────────────────

class TestArithmetik:
    def test_addition(self):
        code = transpiliere("AUSGABE 1 + 2")
        assert "f64.add" in code

    def test_subtraktion(self):
        code = transpiliere("AUSGABE 5 - 3")
        assert "f64.sub" in code

    def test_multiplikation(self):
        code = transpiliere("AUSGABE 3 * 4")
        assert "f64.mul" in code

    def test_division(self):
        code = transpiliere("AUSGABE 10 / 2")
        assert "f64.div" in code

    def test_vergleich(self):
        code = transpiliere("x = 1 == 1\nAUSGABE x")
        assert "f64.eq" in code


# ─── Kontrollfluss ────────────────────────────────────────────────────────

class TestKontrollfluss:
    def test_wenn(self):
        code = transpiliere("WENN 1 DANN\n    AUSGABE 42\nENDE WENN")
        assert "(if" in code
        assert "(then" in code

    def test_solange(self):
        code = transpiliere("x = 0\nSOLANGE x < 5 MACHE\n    x = x + 1\nENDE SCHLEIFE")
        assert "(loop" in code
        assert "(block" in code
        assert "br_if" in code

    def test_fur_bereich(self):
        code = transpiliere("F\u00dcR i IN BEREICH(10) MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert "(loop" in code
        assert "local.set $i" in code


# ─── Funktionen ───────────────────────────────────────────────────────────

class TestFunktionen:
    def test_funktion_definition(self):
        code = transpiliere("DEFINIERE quadrat(n):\n    ERGEBNIS IST n * n\nENDE FUNKTION")
        assert "(func $quadrat" in code
        assert "(param $n f64)" in code
        assert "(result f64)" in code
        assert "f64.mul" in code

    def test_funktion_aufruf(self):
        code = transpiliere("DEFINIERE f(x):\n    ERGEBNIS IST x\nENDE FUNKTION\nAUSGABE f(5)")
        assert "call $f" in code


# ─── Mathe-Funktionen ────────────────────────────────────────────────────

class TestMatheFunktionen:
    def test_wurzel(self):
        code = transpiliere("AUSGABE WURZEL(16)")
        assert "f64.sqrt" in code

    def test_absolut(self):
        code = transpiliere("AUSGABE ABSOLUT(-5)")
        assert "f64.abs" in code

    def test_boden(self):
        code = transpiliere("AUSGABE BODEN(3.7)")
        assert "f64.floor" in code

    def test_decke(self):
        code = transpiliere("AUSGABE DECKE(3.2)")
        assert "f64.ceil" in code

    def test_min_max_helfer(self):
        code = transpiliere("AUSGABE 1")
        assert "$min_f64" in code
        assert "$max_f64" in code


# ─── Backend-Registrierung ───────────────────────────────────────────────

class TestRegistrierung:
    def test_wasm_in_backends(self):
        from transpiler import BACKENDS
        assert "wasm" in BACKENDS

    def test_dateiendung(self):
        result = transpile("AUSGABE 1", source_lang="deutsch",
                          target_backend="wasm", include_stdlib=False)
        assert result['extension'] == ".wat"

    def test_backend_name(self):
        result = transpile("AUSGABE 1", source_lang="deutsch",
                          target_backend="wasm", include_stdlib=False)
        assert "WebAssembly" in result['backend'] or "WAT" in result['backend']
