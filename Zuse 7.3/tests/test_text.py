# FILE: tests/test_text.py
# Tests für die Text-Bibliothek (Phase 4.2)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren
from transpiler import transpile


def ausfuehren(code):
    return zuse_ausfuehren(code)


def transpiliere(code, backend="python"):
    return transpile(code, source_lang="deutsch", target_backend=backend, include_stdlib=False)["code"]


# ─── GROSSBUCHSTABEN / KLEINBUCHSTABEN ─────────────────────────────────────

class TestGrossKlein:
    def test_grossbuchstaben(self):
        r = ausfuehren('AUSGABE GROSSBUCHSTABEN("hallo")')
        assert r[0] == "HALLO"

    def test_kleinbuchstaben(self):
        r = ausfuehren('AUSGABE KLEINBUCHSTABEN("WELT")')
        assert r[0] == "welt"

    def test_grossbuchstaben_gemischt(self):
        r = ausfuehren('AUSGABE GROSSBUCHSTABEN("Hallo Welt")')
        assert r[0] == "HALLO WELT"

    def test_kleinbuchstaben_gemischt(self):
        r = ausfuehren('AUSGABE KLEINBUCHSTABEN("Hallo Welt")')
        assert r[0] == "hallo welt"


# ─── ERSETZE ───────────────────────────────────────────────────────────────

class TestErsetze:
    def test_ersetze_einfach(self):
        r = ausfuehren('AUSGABE ERSETZE("Hallo Welt", "Welt", "Zuse")')
        assert r[0] == "Hallo Zuse"

    def test_ersetze_mehrfach(self):
        r = ausfuehren('AUSGABE ERSETZE("aabaa", "a", "x")')
        assert r[0] == "xxbxx"

    def test_ersetze_nicht_gefunden(self):
        r = ausfuehren('AUSGABE ERSETZE("hallo", "xyz", "abc")')
        assert r[0] == "hallo"


# ─── TEILE ─────────────────────────────────────────────────────────────────

class TestTeile:
    def test_teile_mit_trenner(self):
        r = ausfuehren('AUSGABE TEILE("a,b,c", ",")')
        assert "a" in r[0]
        assert "b" in r[0]
        assert "c" in r[0]

    def test_teile_ohne_trenner(self):
        r = ausfuehren('AUSGABE TEILE("eins zwei drei")')
        assert "eins" in r[0]
        assert "zwei" in r[0]
        assert "drei" in r[0]


# ─── TRIMME ────────────────────────────────────────────────────────────────

class TestTrimme:
    def test_trimme_leerzeichen(self):
        r = ausfuehren('AUSGABE TRIMME("  hallo  ")')
        assert r[0] == "hallo"

    def test_trimme_kein_effekt(self):
        r = ausfuehren('AUSGABE TRIMME("hallo")')
        assert r[0] == "hallo"


# ─── ENTHAELT ──────────────────────────────────────────────────────────────

class TestEnthaelt:
    def test_enthaelt_wahr(self):
        r = ausfuehren('AUSGABE ENTHAELT("Hallo Welt", "Welt")')
        assert r[0] == "True"

    def test_enthaelt_falsch(self):
        r = ausfuehren('AUSGABE ENTHAELT("Hallo Welt", "xyz")')
        assert r[0] == "False"


# ─── LAENGE ────────────────────────────────────────────────────────────────

class TestLaenge:
    def test_laenge_string(self):
        r = ausfuehren('AUSGABE LAENGE("hallo")')
        assert int(r[0]) == 5

    def test_laenge_liste(self):
        r = ausfuehren("AUSGABE LAENGE([1, 2, 3])")
        assert int(r[0]) == 3

    def test_laenge_leer(self):
        r = ausfuehren('AUSGABE LAENGE("")')
        assert int(r[0]) == 0


# ─── FINDE ─────────────────────────────────────────────────────────────────

class TestFinde:
    def test_finde_vorhanden(self):
        r = ausfuehren('AUSGABE FINDE("Hallo Welt", "Welt")')
        assert int(r[0]) == 6

    def test_finde_nicht_vorhanden(self):
        r = ausfuehren('AUSGABE FINDE("Hallo", "xyz")')
        assert int(r[0]) == -1


# ─── BEGINNT_MIT / ENDET_MIT ──────────────────────────────────────────────

class TestStartEnd:
    def test_beginnt_mit_wahr(self):
        r = ausfuehren('AUSGABE BEGINNT_MIT("Hallo Welt", "Hallo")')
        assert r[0] == "True"

    def test_beginnt_mit_falsch(self):
        r = ausfuehren('AUSGABE BEGINNT_MIT("Hallo Welt", "Welt")')
        assert r[0] == "False"

    def test_endet_mit_wahr(self):
        r = ausfuehren('AUSGABE ENDET_MIT("Hallo Welt", "Welt")')
        assert r[0] == "True"

    def test_endet_mit_falsch(self):
        r = ausfuehren('AUSGABE ENDET_MIT("Hallo Welt", "Hallo")')
        assert r[0] == "False"


# ─── VERBINDE ──────────────────────────────────────────────────────────────

class TestVerbinde:
    def test_verbinde_mit_trenner(self):
        r = ausfuehren('AUSGABE VERBINDE(["a", "b", "c"], ", ")')
        assert r[0] == "a, b, c"

    def test_verbinde_ohne_trenner(self):
        r = ausfuehren('AUSGABE VERBINDE(["x", "y", "z"])')
        assert r[0] == "xyz"


# ─── Transpiler ────────────────────────────────────────────────────────────

class TestTranspiler:
    def test_python_grossbuchstaben(self):
        code = transpiliere('AUSGABE GROSSBUCHSTABEN("hallo")')
        assert ".upper()" in code

    def test_python_ersetze(self):
        code = transpiliere('AUSGABE ERSETZE("ab", "a", "x")')
        assert ".replace(" in code

    def test_js_grossbuchstaben(self):
        code = transpiliere('AUSGABE GROSSBUCHSTABEN("hallo")', backend="javascript")
        assert ".toUpperCase()" in code

    def test_js_enthaelt(self):
        code = transpiliere('AUSGABE ENTHAELT("hallo", "all")', backend="javascript")
        assert ".includes(" in code

    def test_java_grossbuchstaben(self):
        code = transpiliere('AUSGABE GROSSBUCHSTABEN("hallo")', backend="java")
        assert ".toUpperCase()" in code

    def test_csharp_grossbuchstaben(self):
        code = transpiliere('AUSGABE GROSSBUCHSTABEN("hallo")', backend="csharp")
        assert ".ToUpper()" in code

    def test_alle_backends_kompilieren(self):
        """Alle Backends transpilieren Text-Code ohne Fehler."""
        zuse_code = 'x = GROSSBUCHSTABEN("hallo")\nAUSGABE x'
        for backend in ['python', 'javascript', 'java', 'csharp']:
            code = transpiliere(zuse_code, backend=backend)
            assert len(code) > 0, f"Backend {backend} hat leeren Code erzeugt"


# ─── Python-Ausführbar ────────────────────────────────────────────────────

class TestPythonAusfuehrbar:
    def test_transpilierter_code_laeuft(self):
        import subprocess
        code = transpiliere('AUSGABE GROSSBUCHSTABEN("hallo")')
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert 'HALLO' in result.stdout

    def test_ersetze_laeuft(self):
        import subprocess
        code = transpiliere('AUSGABE ERSETZE("Hallo Welt", "Welt", "Zuse")')
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert 'Hallo Zuse' in result.stdout
