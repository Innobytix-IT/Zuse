# FILE: tests/test_mathe.py
# Tests für die Mathe-Bibliothek (Phase 4.1)

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren
from transpiler import transpile


def ausfuehren(code):
    return zuse_ausfuehren(code)


def transpiliere(code, backend="python"):
    return transpile(code, source_lang="deutsch", target_backend=backend, include_stdlib=False)["code"]


# ─── Konstanten ──────────────────────────────────────────────────────────────

class TestKonstanten:
    def test_pi(self):
        r = ausfuehren("AUSGABE PI")
        assert abs(float(r[0]) - math.pi) < 0.0001

    def test_e(self):
        r = ausfuehren("AUSGABE E")
        assert abs(float(r[0]) - math.e) < 0.0001


# ─── Grundfunktionen ────────────────────────────────────────────────────────

class TestGrundfunktionen:
    def test_wurzel(self):
        r = ausfuehren("AUSGABE WURZEL(16)")
        assert float(r[0]) == 4.0

    def test_absolut_positiv(self):
        r = ausfuehren("AUSGABE ABSOLUT(5)")
        assert float(r[0]) == 5

    def test_absolut_negativ(self):
        r = ausfuehren("AUSGABE ABSOLUT(-7)")
        assert float(r[0]) == 7

    def test_potenz(self):
        r = ausfuehren("AUSGABE POTENZ(2, 10)")
        assert float(r[0]) == 1024

    def test_runden(self):
        r = ausfuehren("AUSGABE RUNDEN(3.14159)")
        assert float(r[0]) == 3.0

    def test_runden_mit_stellen(self):
        r = ausfuehren("AUSGABE RUNDEN(3.14159, 2)")
        assert float(r[0]) == 3.14

    def test_boden(self):
        r = ausfuehren("AUSGABE BODEN(3.7)")
        assert r[0] == '3'

    def test_decke(self):
        r = ausfuehren("AUSGABE DECKE(3.2)")
        assert r[0] == '4'


# ─── Trigonometrie ───────────────────────────────────────────────────────────

class TestTrigonometrie:
    def test_sinus_null(self):
        r = ausfuehren("AUSGABE SINUS(0)")
        assert float(r[0]) == 0.0

    def test_cosinus_null(self):
        r = ausfuehren("AUSGABE COSINUS(0)")
        assert float(r[0]) == 1.0

    def test_tangens_null(self):
        r = ausfuehren("AUSGABE TANGENS(0)")
        assert float(r[0]) == 0.0

    def test_sinus_pi_halbe(self):
        r = ausfuehren("AUSGABE SINUS(PI / 2)")
        assert abs(float(r[0]) - 1.0) < 0.0001


# ─── Aggregation ─────────────────────────────────────────────────────────────

class TestAggregation:
    def test_minimum_args(self):
        r = ausfuehren("AUSGABE MINIMUM(3, 1, 4, 1, 5)")
        assert float(r[0]) == 1

    def test_maximum_args(self):
        r = ausfuehren("AUSGABE MAXIMUM(3, 1, 4, 1, 5)")
        assert float(r[0]) == 5

    def test_summe_liste(self):
        r = ausfuehren("AUSGABE SUMME([1, 2, 3, 4, 5])")
        assert float(r[0]) == 15

    def test_logarithmus(self):
        r = ausfuehren("AUSGABE LOGARITHMUS(E)")
        assert abs(float(r[0]) - 1.0) < 0.0001


# ─── Zufall ──────────────────────────────────────────────────────────────────

class TestZufall:
    def test_zufall_bereich(self):
        r = ausfuehren("AUSGABE ZUFALL()")
        val = float(r[0])
        assert 0.0 <= val <= 1.0

    def test_zufall_bereich_int(self):
        r = ausfuehren("AUSGABE ZUFALL_BEREICH(1, 10)")
        val = int(r[0])
        assert 1 <= val <= 10


# ─── Transpiler ──────────────────────────────────────────────────────────────

class TestTranspiler:
    def test_python_wurzel(self):
        code = transpiliere("AUSGABE WURZEL(16)")
        assert "math.sqrt" in code

    def test_python_pi(self):
        code = transpiliere("AUSGABE PI")
        assert "math.pi" in code

    def test_js_wurzel(self):
        code = transpiliere("AUSGABE WURZEL(16)", backend="javascript")
        assert "Math.sqrt" in code

    def test_js_pi(self):
        code = transpiliere("AUSGABE PI", backend="javascript")
        assert "Math.PI" in code

    def test_java_wurzel(self):
        code = transpiliere("AUSGABE WURZEL(16)", backend="java")
        assert "Math.sqrt" in code

    def test_csharp_wurzel(self):
        code = transpiliere("AUSGABE WURZEL(16)", backend="csharp")
        assert "Math.Sqrt" in code

    def test_alle_backends_kompilieren(self):
        """Alle Backends transpilieren Mathe-Code ohne Fehler."""
        zuse_code = "x = WURZEL(PI)\nAUSGABE RUNDEN(x, 2)"
        for backend in ['python', 'javascript', 'java', 'csharp']:
            code = transpiliere(zuse_code, backend=backend)
            assert len(code) > 0, f"Backend {backend} hat leeren Code erzeugt"


# ─── Python-Ausführbar ──────────────────────────────────────────────────────

class TestPythonAusfuehrbar:
    def test_transpilierter_code_laeuft(self):
        """Generierter Python-Code läuft korrekt."""
        import subprocess
        code = transpiliere("AUSGABE WURZEL(25)")
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert '5.0' in result.stdout

    def test_pi_berechnung(self):
        import subprocess
        code = transpiliere("AUSGABE RUNDEN(PI, 4)")
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert '3.1416' in result.stdout
