# FILE: tests/conftest.py — Zentrale Test-Konfiguration für Zuse
import sys
import os
import json
import pytest

# Zuse-Quellverzeichnis zum Python-Pfad hinzufügen
ZUSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ZUSE_DIR not in sys.path:
    sys.path.insert(0, ZUSE_DIR)

from language_loader import lade_sprache
from lexer import Lexer, tokenize
from parser import Parser
from interpreter import Interpreter, Environment, ZuseFunction, ZuseClassWrapper, ZuseInstance

# ─── Sprach-Fixtures ───────────────────────────────────────────

SPRACHEN = ["deutsch", "english", "espaniol", "francais", "italiano", "portugues"]

@pytest.fixture
def deutsch_config():
    """Lädt die deutsche Sprachkonfiguration."""
    return lade_sprache("deutsch")

@pytest.fixture
def english_config():
    """Lädt die englische Sprachkonfiguration."""
    return lade_sprache("english")

@pytest.fixture(params=SPRACHEN)
def alle_sprachen_config(request):
    """Parametrisierte Fixture: läuft für JEDE Sprache einmal."""
    sprache = request.param
    config = lade_sprache(sprache)
    return {"sprache": sprache, "config": config}


# ─── Hilfs-Fixtures ───────────────────────────────────────────

@pytest.fixture
def deutsch_lexer(deutsch_config):
    """Fertiger Lexer mit deutscher Konfiguration."""
    return Lexer(deutsch_config)

@pytest.fixture
def make_lexer():
    """Factory-Fixture: Lexer für beliebige Sprache erstellen."""
    def _make(sprache="deutsch"):
        config = lade_sprache(sprache)
        return Lexer(config)
    return _make

@pytest.fixture
def make_interpreter():
    """Factory-Fixture: Interpreter mit Ausgabe-Capture erstellen."""
    def _make(safe_mode=False):
        ausgaben = []
        eingaben = []

        def capture_output(text):
            ausgaben.append(str(text))

        def fake_input(prompt, modus):
            if eingaben:
                return eingaben.pop(0)
            return "0" if modus == "zahl" else "test"

        interp = Interpreter(
            output_callback=capture_output,
            input_callback=fake_input,
            safe_mode=safe_mode
        )
        return interp, ausgaben, eingaben
    return _make


# ─── Komplett-Pipeline Helpers ─────────────────────────────────

def zuse_ausfuehren(code, sprache="deutsch", safe_mode=False, eingaben=None):
    """
    Führt Zuse-Code komplett aus (Lexer → Parser → Interpreter)
    und gibt die gesammelten Ausgaben als Liste zurück.

    Args:
        code: Zuse-Quellcode als String
        sprache: Sprachcode (default: "deutsch")
        safe_mode: Lernmodus aktivieren
        eingaben: Liste von vordefinierten Eingaben

    Returns:
        Liste von Ausgabe-Strings
    """
    from error_i18n import set_language
    set_language(sprache)
    config = lade_sprache(sprache)
    tokens = tokenize(code, config)
    parser = Parser(tokens)
    ast = parser.parse()

    ausgaben = []
    eingabe_liste = list(eingaben) if eingaben else []

    def capture(text):
        ausgaben.append(str(text))

    def fake_input(prompt, modus):
        if eingabe_liste:
            return eingabe_liste.pop(0)
        return "0" if modus == "zahl" else "test"

    interp = Interpreter(
        output_callback=capture,
        input_callback=fake_input,
        safe_mode=safe_mode,
        sprache=sprache
    )
    interp.interpretiere(ast)
    return ausgaben


def zuse_tokens(code, sprache="deutsch"):
    """Tokenisiert Zuse-Code und gibt die Token-Liste zurück."""
    config = lade_sprache(sprache)
    return tokenize(code, config)


def zuse_ast(code, sprache="deutsch"):
    """Parsed Zuse-Code und gibt den AST zurück."""
    config = lade_sprache(sprache)
    tokens = tokenize(code, config)
    parser = Parser(tokens)
    return parser.parse()


@pytest.fixture
def ausfuehren():
    """Fixture-Variante von zuse_ausfuehren."""
    return zuse_ausfuehren


@pytest.fixture
def parse():
    """Fixture-Variante von zuse_ast."""
    return zuse_ast
