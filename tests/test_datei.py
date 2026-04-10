# FILE: tests/test_datei.py
# Tests für die Datei-Bibliothek (Phase 4.4)

import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren
from transpiler import transpile


def ausfuehren(code):
    return zuse_ausfuehren(code)


def transpiliere(code, backend="python"):
    return transpile(code, source_lang="deutsch", target_backend=backend, include_stdlib=False)["code"]


def _pfad():
    """Erstellt einen temporären Dateipfad mit Forward-Slashes für Zuse."""
    fd, pfad = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    return pfad.replace('\\', '/')


# ─── SCHREIBE_DATEI + LESE_DATEI ──────────────────────────────────────────

class TestSchreibenLesen:
    def test_schreibe_und_lese(self):
        pfad = _pfad()
        try:
            ausfuehren(f'SCHREIBE_DATEI("{pfad}", "Hallo Zuse")')
            r = ausfuehren(f'AUSGABE LESE_DATEI("{pfad}")')
            assert r[0] == "Hallo Zuse"
        finally:
            os.unlink(pfad)

    def test_ueberschreiben(self):
        pfad = _pfad()
        try:
            ausfuehren(f'SCHREIBE_DATEI("{pfad}", "Erste Zeile")')
            ausfuehren(f'SCHREIBE_DATEI("{pfad}", "Zweite Zeile")')
            r = ausfuehren(f'AUSGABE LESE_DATEI("{pfad}")')
            assert r[0] == "Zweite Zeile"
        finally:
            os.unlink(pfad)


# ─── ERGAENZE_DATEI ───────────────────────────────────────────────────────

class TestErgaenzen:
    def test_ergaenze(self):
        pfad = _pfad()
        try:
            ausfuehren(f'SCHREIBE_DATEI("{pfad}", "Hallo")')
            ausfuehren(f'ERGAENZE_DATEI("{pfad}", " Welt")')
            r = ausfuehren(f'AUSGABE LESE_DATEI("{pfad}")')
            assert r[0] == "Hallo Welt"
        finally:
            os.unlink(pfad)


# ─── EXISTIERT ─────────────────────────────────────────────────────────────

class TestExistiert:
    def test_existiert_wahr(self):
        pfad = _pfad()
        try:
            r = ausfuehren(f'AUSGABE EXISTIERT("{pfad}")')
            assert r[0] == "True"
        finally:
            os.unlink(pfad)

    def test_existiert_falsch(self):
        r = ausfuehren('AUSGABE EXISTIERT("/nicht/vorhanden/xyz123.txt")')
        assert r[0] == "False"


# ─── LESE_ZEILEN ──────────────────────────────────────────────────────────

class TestLeseZeilen:
    def test_lese_zeilen(self):
        pfad = _pfad()
        try:
            # Datei direkt mit Python schreiben (um \n korrekt zu haben)
            with open(pfad, 'w', encoding='utf-8') as f:
                f.write("eins\nzwei\ndrei")
            r = ausfuehren(f'AUSGABE LESE_ZEILEN("{pfad}")')
            assert "eins" in r[0]
            assert "zwei" in r[0]
            assert "drei" in r[0]
        finally:
            os.unlink(pfad)


# ─── LOESCHE_DATEI ────────────────────────────────────────────────────────

class TestLoeschen:
    def test_loesche_datei(self):
        pfad = _pfad()
        ausfuehren(f'LOESCHE_DATEI("{pfad}")')
        assert not os.path.exists(pfad)


# ─── Kombination ──────────────────────────────────────────────────────────

class TestKombination:
    def test_schreibe_lese_zeilen_zaehle(self):
        pfad = _pfad()
        try:
            with open(pfad, 'w', encoding='utf-8') as f:
                f.write("a\nb\nc\nd\ne")
            r = ausfuehren(f'zeilen = LESE_ZEILEN("{pfad}")\nAUSGABE LAENGE(zeilen)')
            assert int(r[0]) == 5
        finally:
            os.unlink(pfad)


# ─── Transpiler ────────────────────────────────────────────────────────────

class TestTranspiler:
    def test_python_lese_datei(self):
        code = transpiliere('AUSGABE LESE_DATEI("test.txt")')
        assert "open(" in code
        assert ".read()" in code

    def test_python_schreibe_datei(self):
        code = transpiliere('SCHREIBE_DATEI("test.txt", "inhalt")')
        assert "open(" in code
        assert ".write(" in code

    def test_python_existiert(self):
        code = transpiliere('AUSGABE EXISTIERT("test.txt")')
        assert "os.path.exists" in code

    def test_js_lese_datei(self):
        code = transpiliere('AUSGABE LESE_DATEI("test.txt")', backend="javascript")
        assert "readFileSync" in code

    def test_js_existiert(self):
        code = transpiliere('AUSGABE EXISTIERT("test.txt")', backend="javascript")
        assert "existsSync" in code

    def test_java_lese_datei(self):
        code = transpiliere('AUSGABE LESE_DATEI("test.txt")', backend="java")
        assert "readString" in code or "Files" in code

    def test_csharp_lese_datei(self):
        code = transpiliere('AUSGABE LESE_DATEI("test.txt")', backend="csharp")
        assert "ReadAllText" in code

    def test_alle_backends_kompilieren(self):
        """Alle Backends transpilieren Datei-Code ohne Fehler."""
        zuse_code = 'AUSGABE EXISTIERT("test.txt")'
        for backend in ['python', 'javascript', 'java', 'csharp']:
            code = transpiliere(zuse_code, backend=backend)
            assert len(code) > 0, f"Backend {backend} hat leeren Code erzeugt"


# ─── Python-Ausführbar ────────────────────────────────────────────────────

class TestPythonAusfuehrbar:
    def test_existiert_laeuft(self):
        import subprocess
        code = transpiliere('AUSGABE EXISTIERT("nichtda.txt")')
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0
        assert 'False' in result.stdout
