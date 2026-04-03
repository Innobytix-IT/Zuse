# FILE: tests/test_beispiele.py
# Automatisierte Tests für alle Beispielprogramme (B5.1)

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tests.conftest import zuse_ausfuehren


BEISPIELE_DIR = os.path.join(os.path.dirname(__file__), "..", "beispiele")


def _lade_beispiel(name):
    pfad = os.path.join(BEISPIELE_DIR, name)
    with open(pfad, "r", encoding="utf-8") as f:
        return f.read()


# ─── Nicht-interaktive Beispiele ──────────────────────────────────────────

class TestGrundlagen:
    def test_01_hallo_welt(self):
        r = zuse_ausfuehren(_lade_beispiel("01_hallo_welt.zuse"))
        assert "Hallo Welt!" in r
        assert "Willkommen bei Zuse!" in r
        assert len(r) == 3

    def test_02_variablen(self):
        r = zuse_ausfuehren(_lade_beispiel("02_variablen.zuse"))
        assert "Sprache: Zuse" in r
        assert "Version: 7" in r
        assert "Punkte: 15" in r


class TestKontrollfluss:
    def test_05_fizzbuzz(self):
        r = zuse_ausfuehren(_lade_beispiel("05_fizzbuzz.zuse"))
        assert len(r) == 50
        assert r[0] == "1"
        assert r[2] == "Fizz"
        assert r[4] == "Buzz"
        assert r[14] == "FizzBuzz"

    def test_06_primzahlen(self):
        r = zuse_ausfuehren(_lade_beispiel("06_primzahlen.zuse"))
        assert "2" in r[1]  # Primzahlen-Liste enthält 2
        assert "Anzahl: 15" in r


class TestFunktionen:
    def test_07_fibonacci(self):
        r = zuse_ausfuehren(_lade_beispiel("07_fibonacci.zuse"))
        assert any("fib(0) = 0" in line for line in r)
        assert any("fib(1) = 1" in line for line in r)
        assert any("fib(10) = 55" in line for line in r)

    def test_08_fakultaet(self):
        r = zuse_ausfuehren(_lade_beispiel("08_fakultaet.zuse"))
        assert any("0! = 1" in line for line in r)
        assert any("5! = 120" in line for line in r)
        assert any("10! = 3628800" in line for line in r)


class TestListen:
    def test_09_sortieren(self):
        r = zuse_ausfuehren(_lade_beispiel("09_sortieren.zuse"))
        assert any("11" in line and "12" in line and "22" in line for line in r)

    def test_10_suchen(self):
        r = zuse_ausfuehren(_lade_beispiel("10_suchen.zuse"))
        assert any("33" in line and "gefunden" in line for line in r)

    def test_11_statistik(self):
        r = zuse_ausfuehren(_lade_beispiel("11_statistik.zuse"))
        assert any("Durchschnitt" in line for line in r)
        assert any("Bestanden" in line for line in r)


class TestOOP:
    def test_12_tierwelt(self):
        r = zuse_ausfuehren(_lade_beispiel("12_tierwelt.zuse"))
        assert any("Rex ist ein Hund" in line for line in r)
        assert any("Minka" in line for line in r)
        assert any("Wuff" in line for line in r)
        assert any("Sitz" in line for line in r)

    def test_13_bankkonto(self):
        r = zuse_ausfuehren(_lade_beispiel("13_bankkonto.zuse"))
        assert any("200" in line and "eingezahlt" in line for line in r)
        assert any("Nicht genug Guthaben" in line for line in r)

    def test_14_inventar(self):
        r = zuse_ausfuehren(_lade_beispiel("14_inventar.zuse"))
        assert any("Schwert eingepackt" in line for line in r)
        assert any("Zu schwer" in line for line in r)
        assert any("Gesamtwert" in line for line in r)


# ─── Interaktive Beispiele (mit vordefinierten Eingaben) ─────────────────

class TestInteraktiv:
    def test_03_rechner(self):
        r = zuse_ausfuehren(_lade_beispiel("03_rechner.zuse"), eingaben=[10, 3])
        assert any("13" in line for line in r)  # 10 + 3
        assert any("7" in line for line in r)   # 10 - 3
        assert any("30" in line for line in r)  # 10 * 3

    def test_04_zahlenraten_parse(self):
        """Nur Parse-Check — braucht Zufallszahl und interaktive Eingabe."""
        from language_loader import lade_sprache
        from lexer import tokenize
        from parser import Parser
        code = _lade_beispiel("04_zahlenraten.zuse")
        config = lade_sprache("deutsch")
        tokens = tokenize(code, config)
        ast = Parser(tokens).parse()
        assert ast["type"] == "PROGRAMM"

    def test_15_quiz(self):
        r = zuse_ausfuehren(_lade_beispiel("15_quiz.zuse"), eingaben=[2, 2, 2, 2, 2])
        assert any("5 von 5" in line for line in r)
        assert any("Ausgezeichnet" in line for line in r)
