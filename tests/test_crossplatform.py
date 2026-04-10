# FILE: tests/test_crossplatform.py
# Cross-Platform-Kompatibilitätstests (B5.3)
# Prüft, dass keine plattformspezifischen Annahmen im Code stecken.

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tests.conftest import zuse_ausfuehren


class TestPfade:
    """Prüft, dass Pfade plattformunabhängig gehandhabt werden."""

    def test_sprachen_ordner_existiert(self):
        sprachen = os.path.join(os.path.dirname(__file__), "..", "sprachen")
        assert os.path.isdir(sprachen)

    def test_alle_sprach_jsons(self):
        sprachen = os.path.join(os.path.dirname(__file__), "..", "sprachen")
        erwartet = {"deutsch", "english", "espaniol", "francais", "italiano", "portugues"}
        vorhanden = {f.replace(".json", "") for f in os.listdir(sprachen) if f.endswith(".json")}
        assert erwartet.issubset(vorhanden)

    def test_beispiele_ordner(self):
        beispiele = os.path.join(os.path.dirname(__file__), "..", "beispiele")
        assert os.path.isdir(beispiele)

    def test_docs_ordner(self):
        docs = os.path.join(os.path.dirname(__file__), "..", "docs")
        assert os.path.isdir(docs)


class TestImports:
    """Prüft, dass alle Module importiert werden können."""

    def test_lexer(self):
        from lexer import Lexer, tokenize

    def test_parser(self):
        from parser import Parser

    def test_interpreter(self):
        from interpreter import Interpreter

    def test_language_loader(self):
        from language_loader import lade_sprache

    def test_semantic_analyzer(self):
        from semantic_analyzer import SemanticAnalyzer

    def test_debugger(self):
        from debugger import ZuseDebugger

    def test_error_hints(self):
        from error_hints import get_hint, format_error_with_hint

    def test_transpiler(self):
        from transpiler import transpile, BACKENDS

    def test_backends(self):
        from backends.python_backend import PythonBackend
        from backends.javascript_backend import JavaScriptBackend
        from backends.java_backend import JavaBackend
        from backends.csharp_backend import CSharpBackend
        from backends.wasm_backend import WasmBackend

    def test_zpkg(self):
        import zpkg_core


class TestUnicode:
    """Prüft, dass Unicode (Umlaute, Sonderzeichen) korrekt verarbeitet wird."""

    def test_umlaute_in_strings(self):
        r = zuse_ausfuehren('AUSGABE "Hallo Wörld! Ä Ö Ü ß"')
        assert "Ä" in r[0]
        assert "ß" in r[0]

    def test_utf8_variablen(self):
        r = zuse_ausfuehren('name = "München"\nAUSGABE name')
        assert "München" in r[0]

    def test_schleife_mit_umlaut(self):
        r = zuse_ausfuehren('SCHLEIFE FÜR i IN BEREICH(3) MACHE\n    AUSGABE i\nENDE SCHLEIFE')
        assert r == ["0", "1", "2"]


class TestMehrsprachigkeit:
    """Prüft, dass alle 6 Sprachen das gleiche Ergebnis liefern."""

    PROG = {
        "deutsch":   'AUSGABE 2 + 3',
        "english":   'PRINT 2 + 3',
        "espaniol":  'IMPRIMIR 2 + 3',
        "francais":  'IMPRIMER 2 + 3',
        "italiano":  'STAMPA 2 + 3',
        "portugues": 'IMPRIMIR 2 + 3',
    }

    @pytest.mark.parametrize("sprache", list(PROG.keys()))
    def test_ausgabe_in_sprache(self, sprache):
        r = zuse_ausfuehren(self.PROG[sprache], sprache=sprache)
        assert r == ["5"]


class TestDateiOperationen:
    """Prüft Dateioperationen mit plattformunabhängigen Pfaden."""

    def test_schreibe_und_lese(self, tmp_path):
        pfad = str(tmp_path / "test.txt").replace("\\", "/")
        code = f'SCHREIBE_DATEI("{pfad}", "Hallo")\nAUSGABE LESE_DATEI("{pfad}")'
        r = zuse_ausfuehren(code)
        assert r == ["Hallo"]

    def test_existiert(self, tmp_path):
        pfad = str(tmp_path / "nichtda.txt").replace("\\", "/")
        code = f'AUSGABE EXISTIERT("{pfad}")'
        r = zuse_ausfuehren(code)
        assert r[0] == "False"
