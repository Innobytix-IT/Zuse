# FILE: tests/test_liste.py
# Tests für die Listen-Bibliothek (Phase 4.3)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren
from transpiler import transpile


def ausfuehren(code):
    return zuse_ausfuehren(code)


def transpiliere(code, backend="python"):
    return transpile(code, source_lang="deutsch", target_backend=backend, include_stdlib=False)["code"]


# ─── SORTIEREN ─────────────────────────────────────────────────────────────

class TestSortieren:
    def test_sortieren_zahlen(self):
        r = ausfuehren("AUSGABE SORTIEREN([3, 1, 4, 1, 5])")
        assert r[0] == "[1, 1, 3, 4, 5]"

    def test_sortieren_strings(self):
        r = ausfuehren('AUSGABE SORTIEREN(["c", "a", "b"])')
        assert r[0] == "['a', 'b', 'c']"

    def test_sortieren_original_unveraendert(self):
        r = ausfuehren("x = [3, 1, 2]\ny = SORTIEREN(x)\nAUSGABE x")
        assert r[0] == "[3, 1, 2]"


# ─── FILTERN ──────────────────────────────────────────────────────────────

class TestFiltern:
    def test_filtern_gerade(self):
        r = ausfuehren("AUSGABE FILTERN([1, 2, 3, 4, 5, 6], AKTION x: x % 2 == 0)")
        assert r[0] == "[2, 4, 6]"

    def test_filtern_leer(self):
        r = ausfuehren("AUSGABE FILTERN([1, 3, 5], AKTION x: x > 10)")
        assert r[0] == "[]"


# ─── UMWANDELN ─────────────────────────────────────────────────────────────

class TestUmwandeln:
    def test_umwandeln_verdoppeln(self):
        r = ausfuehren("AUSGABE UMWANDELN([1, 2, 3], AKTION x: x * 2)")
        assert r[0] == "[2, 4, 6]"

    def test_umwandeln_string(self):
        r = ausfuehren('AUSGABE UMWANDELN([1, 2, 3], AKTION x: str(x))')
        assert r[0] == "['1', '2', '3']"


# ─── UMKEHREN ─────────────────────────────────────────────────────────────

class TestUmkehren:
    def test_umkehren(self):
        r = ausfuehren("AUSGABE UMKEHREN([1, 2, 3])")
        assert r[0] == "[3, 2, 1]"

    def test_umkehren_original_unveraendert(self):
        r = ausfuehren("x = [1, 2, 3]\ny = UMKEHREN(x)\nAUSGABE x")
        assert r[0] == "[1, 2, 3]"


# ─── FLACH ─────────────────────────────────────────────────────────────────

class TestFlach:
    def test_flach_verschachtelt(self):
        r = ausfuehren("AUSGABE FLACH([[1, 2], [3, 4], [5]])")
        assert r[0] == "[1, 2, 3, 4, 5]"

    def test_flach_gemischt(self):
        r = ausfuehren("AUSGABE FLACH([[1, 2], 3, [4, 5]])")
        assert r[0] == "[1, 2, 3, 4, 5]"


# ─── EINDEUTIG ─────────────────────────────────────────────────────────────

class TestEindeutig:
    def test_eindeutig(self):
        r = ausfuehren("AUSGABE EINDEUTIG([1, 2, 2, 3, 1, 3])")
        assert r[0] == "[1, 2, 3]"

    def test_eindeutig_strings(self):
        r = ausfuehren('AUSGABE EINDEUTIG(["a", "b", "a", "c"])')
        assert r[0] == "['a', 'b', 'c']"


# ─── AUFZAEHLEN ────────────────────────────────────────────────────────────

class TestAufzaehlen:
    def test_aufzaehlen(self):
        r = ausfuehren('AUSGABE AUFZAEHLEN(["a", "b", "c"])')
        assert "(0, 'a')" in r[0]
        assert "(1, 'b')" in r[0]
        assert "(2, 'c')" in r[0]


# ─── KOMBINIEREN ──────────────────────────────────────────────────────────

class TestKombinieren:
    def test_kombinieren(self):
        r = ausfuehren('AUSGABE KOMBINIEREN([1, 2, 3], ["a", "b", "c"])')
        assert "(1, 'a')" in r[0]
        assert "(2, 'b')" in r[0]


# ─── ANHAENGEN ─────────────────────────────────────────────────────────────

class TestAnhaengen:
    def test_anhaengen(self):
        r = ausfuehren("AUSGABE ANHAENGEN([1, 2], 3)")
        assert r[0] == "[1, 2, 3]"

    def test_anhaengen_mehrere(self):
        r = ausfuehren("AUSGABE ANHAENGEN([1], 2, 3, 4)")
        assert r[0] == "[1, 2, 3, 4]"


# ─── BEREICH_LISTE ────────────────────────────────────────────────────────

class TestBereichListe:
    def test_bereich_liste(self):
        r = ausfuehren("AUSGABE BEREICH_LISTE(5)")
        assert r[0] == "[0, 1, 2, 3, 4]"


# ─── Transpiler ────────────────────────────────────────────────────────────

class TestTranspiler:
    def test_python_sortieren(self):
        code = transpiliere("AUSGABE SORTIEREN([3, 1, 2])")
        assert "sorted(" in code

    def test_python_filtern(self):
        code = transpiliere("AUSGABE FILTERN([1, 2], AKTION x: x > 1)")
        assert "filter(" in code

    def test_python_umwandeln(self):
        code = transpiliere("AUSGABE UMWANDELN([1, 2], AKTION x: x * 2)")
        assert "map(" in code

    def test_js_sortieren(self):
        code = transpiliere("AUSGABE SORTIEREN([3, 1, 2])", backend="javascript")
        assert ".sort()" in code

    def test_js_filtern(self):
        code = transpiliere("AUSGABE FILTERN([1, 2], AKTION x: x > 1)", backend="javascript")
        assert ".filter(" in code

    def test_js_umwandeln(self):
        code = transpiliere("AUSGABE UMWANDELN([1, 2], AKTION x: x * 2)", backend="javascript")
        assert ".map(" in code

    def test_csharp_sortieren(self):
        code = transpiliere("AUSGABE SORTIEREN([3, 1, 2])", backend="csharp")
        assert "OrderBy" in code

    def test_java_sortieren(self):
        code = transpiliere("AUSGABE SORTIEREN([3, 1, 2])", backend="java")
        assert "sorted" in code

    def test_alle_backends_kompilieren(self):
        """Alle Backends transpilieren Listen-Code ohne Fehler."""
        zuse_code = "AUSGABE SORTIEREN([3, 1, 2])"
        for backend in ['python', 'javascript', 'java', 'csharp']:
            code = transpiliere(zuse_code, backend=backend)
            assert len(code) > 0, f"Backend {backend} hat leeren Code erzeugt"


# ─── Python-Ausführbar ────────────────────────────────────────────────────

class TestPythonAusfuehrbar:
    def test_sortieren_laeuft(self):
        import subprocess
        code = transpiliere("AUSGABE SORTIEREN([3, 1, 2])")
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert '[1, 2, 3]' in result.stdout

    def test_umkehren_laeuft(self):
        import subprocess
        code = transpiliere("AUSGABE UMKEHREN([1, 2, 3])")
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert '[3, 2, 1]' in result.stdout
