# FILE: tests/test_spielfeld.py
# Tests für die Spielfeld-Bibliothek (Phase 4.5)
# Hinweis: GUI-Tests sind begrenzt, da kein Display nötig sein soll.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from conftest import zuse_ausfuehren
from transpiler import transpile


def transpiliere(code, backend="python"):
    return transpile(code, source_lang="deutsch", target_backend=backend, include_stdlib=False)["code"]


# ─── Modul-Import ─────────────────────────────────────────────────────────

class TestModul:
    def test_import_spielfeld(self):
        """spielfeld.py lässt sich importieren."""
        from spielfeld import Spielfeld, Sprite, TextSprite
        assert Spielfeld is not None
        assert Sprite is not None
        assert TextSprite is not None

    def test_spielfeld_hat_methoden(self):
        """Spielfeld-Klasse hat die erwarteten Methoden."""
        from spielfeld import Spielfeld
        erwartete = [
            'neuer_sprite', 'neuer_text', 'bei_taste', 'taste_gedrueckt',
            'nach_zeit', 'aktualisiere', 'starte', 'schliessen',
            'setze_titel', 'loesche_alles',
            'zeichne_rechteck', 'zeichne_kreis', 'zeichne_linie',
        ]
        for m in erwartete:
            assert hasattr(Spielfeld, m), f"Methode '{m}' fehlt in Spielfeld"

    def test_sprite_hat_methoden(self):
        """Sprite-Klasse hat die erwarteten Methoden."""
        from spielfeld import Sprite
        erwartete = [
            'bewege', 'setze_position', 'kollidiert_mit', 'am_rand',
            'verstecke', 'zeige', 'aendere_farbe', 'entferne',
        ]
        for m in erwartete:
            assert hasattr(Sprite, m), f"Methode '{m}' fehlt in Sprite"

    def test_text_sprite_hat_methoden(self):
        """TextSprite-Klasse hat die erwarteten Methoden."""
        from spielfeld import TextSprite
        erwartete = ['setze_text', 'setze_position', 'entferne']
        for m in erwartete:
            assert hasattr(TextSprite, m), f"Methode '{m}' fehlt in TextSprite"


# ─── Kollisionslogik (ohne GUI) ───────────────────────────────────────────

class _FakeSprite:
    """Fake-Sprite für Kollisionstests ohne tkinter."""
    def __init__(self, x, y, breite, hoehe):
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe


class TestKollision:
    def _kollidiert(self, a, b):
        """AABB-Kollision wie in Sprite.kollidiert_mit."""
        return (a.x < b.x + b.breite and
                a.x + a.breite > b.x and
                a.y < b.y + b.hoehe and
                a.y + a.hoehe > b.y)

    def test_kollision_ueberlappung(self):
        a = _FakeSprite(0, 0, 50, 50)
        b = _FakeSprite(25, 25, 50, 50)
        assert self._kollidiert(a, b)

    def test_keine_kollision(self):
        a = _FakeSprite(0, 0, 50, 50)
        b = _FakeSprite(100, 100, 50, 50)
        assert not self._kollidiert(a, b)

    def test_kollision_rand(self):
        """Sprites die sich exakt berühren kollidieren nicht (open boundary)."""
        a = _FakeSprite(0, 0, 50, 50)
        b = _FakeSprite(50, 0, 50, 50)
        assert not self._kollidiert(a, b)

    def test_kollision_enthalten(self):
        """Ein Sprite komplett im anderen."""
        a = _FakeSprite(0, 0, 100, 100)
        b = _FakeSprite(25, 25, 10, 10)
        assert self._kollidiert(a, b)


# ─── Am-Rand-Logik ────────────────────────────────────────────────────────

class TestAmRand:
    def _am_rand(self, sprite_x, sprite_y, sprite_b, sprite_h, feld_b=600, feld_h=400):
        return (sprite_x <= 0 or sprite_y <= 0 or
                sprite_x + sprite_b >= feld_b or
                sprite_y + sprite_h >= feld_h)

    def test_am_linken_rand(self):
        assert self._am_rand(0, 50, 20, 20)

    def test_am_rechten_rand(self):
        assert self._am_rand(590, 50, 20, 20)

    def test_in_der_mitte(self):
        assert not self._am_rand(100, 100, 20, 20)

    def test_am_oberen_rand(self):
        assert self._am_rand(50, 0, 20, 20)

    def test_am_unteren_rand(self):
        assert self._am_rand(50, 390, 20, 20)


# ─── Interpreter: Spielfeld ist verfügbar ─────────────────────────────────

class TestInterpreter:
    def test_spielfeld_existiert(self):
        """Spielfeld ist als Builtin verfügbar."""
        r = zuse_ausfuehren('AUSGABE typ(Spielfeld)')
        assert r[0] == "type"

    def test_spielfeld_aufrufbar(self):
        """Spielfeld-Klasse ist aufrufbar (Typ-Check)."""
        r = zuse_ausfuehren('AUSGABE typ(Spielfeld) == "type"')
        assert r[0] == "True"


# ─── Transpiler ────────────────────────────────────────────────────────────

class TestTranspiler:
    def test_python_spielfeld(self):
        code = transpiliere('feld = Spielfeld("Test", 800, 600)')
        assert "Spielfeld" in code

    def test_js_spielfeld(self):
        code = transpiliere('feld = Spielfeld("Test", 800, 600)', backend="javascript")
        assert "Spielfeld" in code

    def test_java_spielfeld(self):
        code = transpiliere('feld = Spielfeld("Test", 800, 600)', backend="java")
        assert "Spielfeld" in code

    def test_csharp_spielfeld(self):
        code = transpiliere('feld = Spielfeld("Test", 800, 600)', backend="csharp")
        assert "Spielfeld" in code

    def test_alle_backends_kompilieren(self):
        """Alle Backends transpilieren Spielfeld-Code ohne Fehler."""
        zuse_code = 'feld = Spielfeld("Mein Spiel", 800, 600)'
        for backend in ['python', 'javascript', 'java', 'csharp']:
            code = transpiliere(zuse_code, backend=backend)
            assert len(code) > 0, f"Backend {backend} hat leeren Code erzeugt"
