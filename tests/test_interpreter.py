# FILE: tests/test_interpreter.py — Interpreter-Tests: Ausführung aller Konstrukte
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from tests.conftest import zuse_ausfuehren


# ─── 1. Ausgabe ───────────────────────────────────────────────

class TestAusgabe:

    def test_string_ausgabe(self):
        out = zuse_ausfuehren('AUSGABE "Hallo Welt"')
        assert out == ["Hallo Welt"]

    def test_zahl_ausgabe(self):
        out = zuse_ausfuehren("AUSGABE 42")
        assert out == ["42"]

    def test_float_ausgabe(self):
        out = zuse_ausfuehren("AUSGABE 3.14")
        assert out == ["3.14"]

    def test_mehrere_ausgaben(self):
        out = zuse_ausfuehren('AUSGABE "A"\nAUSGABE "B"\nAUSGABE "C"')
        assert out == ["A", "B", "C"]


# ─── 2. Variablen ─────────────────────────────────────────────

class TestVariablen:

    def test_string_variable(self):
        out = zuse_ausfuehren('name = "Manuel"\nAUSGABE name')
        assert out == ["Manuel"]

    def test_zahl_variable(self):
        out = zuse_ausfuehren("x = 42\nAUSGABE x")
        assert out == ["42"]

    def test_variable_ueberschreiben(self):
        out = zuse_ausfuehren("x = 1\nx = 2\nAUSGABE x")
        assert out == ["2"]

    def test_undefinierte_variable_fehler(self):
        out = zuse_ausfuehren("AUSGABE unbekannt")
        assert any("nicht definiert" in s for s in out)


# ─── 3. Arithmetik ────────────────────────────────────────────

class TestArithmetik:

    def test_addition(self):
        out = zuse_ausfuehren("AUSGABE 3 + 4")
        assert out == ["7"]

    def test_subtraktion(self):
        out = zuse_ausfuehren("AUSGABE 10 - 3")
        assert out == ["7"]

    def test_multiplikation(self):
        out = zuse_ausfuehren("AUSGABE 6 * 7")
        assert out == ["42"]

    def test_division(self):
        out = zuse_ausfuehren("AUSGABE 10 / 4")
        assert out == ["2.5"]

    def test_potenz(self):
        out = zuse_ausfuehren("AUSGABE 2 ^ 3")
        assert out == ["8"]

    def test_modulo(self):
        out = zuse_ausfuehren("AUSGABE 10 % 3")
        assert out == ["1"]

    def test_unaeres_minus(self):
        out = zuse_ausfuehren("AUSGABE -5")
        assert out == ["-5"]

    def test_praezedenz(self):
        out = zuse_ausfuehren("AUSGABE 2 + 3 * 4")
        assert out == ["14"]

    def test_klammern(self):
        out = zuse_ausfuehren("AUSGABE (2 + 3) * 4")
        assert out == ["20"]

    def test_string_konkatenation(self):
        out = zuse_ausfuehren('AUSGABE "Hallo" + " " + "Welt"')
        assert out == ["Hallo Welt"]

    def test_string_zahl_konkatenation(self):
        out = zuse_ausfuehren('AUSGABE "Alter: " + str(42)')
        assert out == ["Alter: 42"]


# ─── 4. Vergleiche & Booleans ─────────────────────────────────

class TestVergleiche:

    def test_gleich_wahr(self):
        out = zuse_ausfuehren("AUSGABE 5 == 5")
        assert out == ["True"]

    def test_gleich_falsch(self):
        out = zuse_ausfuehren("AUSGABE 5 == 3")
        assert out == ["False"]

    def test_ungleich(self):
        out = zuse_ausfuehren("AUSGABE 5 != 3")
        assert out == ["True"]

    def test_groesser(self):
        out = zuse_ausfuehren("AUSGABE 10 > 5")
        assert out == ["True"]

    def test_kleiner(self):
        out = zuse_ausfuehren("AUSGABE 3 < 10")
        assert out == ["True"]

    def test_boolean_wahr(self):
        out = zuse_ausfuehren("x = wahr\nAUSGABE x")
        assert out == ["True"]

    def test_boolean_falsch(self):
        out = zuse_ausfuehren("x = falsch\nAUSGABE x")
        assert out == ["False"]


# ─── 5. WENN/DANN/SONST ───────────────────────────────────────

class TestBedingungen:

    def test_wenn_wahr(self):
        code = """x = 10
WENN x > 5 DANN
    AUSGABE "ja"
ENDE WENN"""
        out = zuse_ausfuehren(code)
        assert out == ["ja"]

    def test_wenn_falsch(self):
        code = """x = 3
WENN x > 5 DANN
    AUSGABE "ja"
ENDE WENN"""
        out = zuse_ausfuehren(code)
        assert out == []

    def test_wenn_sonst(self):
        code = """x = 3
WENN x > 5 DANN
    AUSGABE "groß"
SONST
    AUSGABE "klein"
ENDE WENN"""
        out = zuse_ausfuehren(code)
        assert out == ["klein"]

    def test_wenn_sonst_wenn(self):
        code = """x = 7
WENN x > 10 DANN
    AUSGABE "groß"
SONST WENN x > 5 DANN
    AUSGABE "mittel"
SONST
    AUSGABE "klein"
ENDE WENN"""
        out = zuse_ausfuehren(code)
        assert out == ["mittel"]

    def test_verschachtelte_wenn(self):
        code = """x = 10
y = 20
WENN x > 5 DANN
    WENN y > 15 DANN
        AUSGABE "beide"
    ENDE WENN
ENDE WENN"""
        out = zuse_ausfuehren(code)
        assert out == ["beide"]


# ─── 6. Schleifen ─────────────────────────────────────────────

class TestSchleifen:

    def test_fuer_schleife(self):
        code = """SCHLEIFE FÜR i IN [1, 2, 3] MACHE
    AUSGABE i
ENDE SCHLEIFE"""
        out = zuse_ausfuehren(code)
        assert out == ["1", "2", "3"]

    def test_solange_schleife(self):
        code = """x = 0
SCHLEIFE SOLANGE x < 3 MACHE
    x = x + 1
ENDE SCHLEIFE
AUSGABE x"""
        out = zuse_ausfuehren(code)
        assert out == ["3"]

    def test_verschachtelte_schleifen(self):
        code = """SCHLEIFE FÜR i IN [1, 2] MACHE
    SCHLEIFE FÜR j IN [10, 20] MACHE
        AUSGABE i * j
    ENDE SCHLEIFE
ENDE SCHLEIFE"""
        out = zuse_ausfuehren(code)
        assert out == ["10", "20", "20", "40"]

    def test_leere_liste_schleife(self):
        code = """SCHLEIFE FÜR i IN [] MACHE
    AUSGABE "nie"
ENDE SCHLEIFE
AUSGABE "fertig" """
        out = zuse_ausfuehren(code)
        assert out == ["fertig"]


# ─── 7. Funktionen ────────────────────────────────────────────

class TestFunktionen:

    def test_einfache_funktion(self):
        code = """DEFINIERE hallo():
    AUSGABE "Hallo!"
ENDE FUNKTION
hallo()"""
        out = zuse_ausfuehren(code)
        assert out == ["Hallo!"]

    def test_funktion_mit_parameter(self):
        code = """DEFINIERE gruss(name):
    AUSGABE "Hallo " + name
ENDE FUNKTION
gruss("Manuel")"""
        out = zuse_ausfuehren(code)
        assert out == ["Hallo Manuel"]

    def test_funktion_mit_rueckgabe(self):
        code = """DEFINIERE doppelt(x):
    ERGEBNIS IST x * 2
ENDE FUNKTION
AUSGABE doppelt(21)"""
        out = zuse_ausfuehren(code)
        assert out == ["42"]

    def test_rekursion(self):
        code = """DEFINIERE fakultaet(n):
    WENN n <= 1 DANN
        ERGEBNIS IST 1
    ENDE WENN
    ERGEBNIS IST n * fakultaet(n - 1)
ENDE FUNKTION
AUSGABE fakultaet(5)"""
        out = zuse_ausfuehren(code)
        assert out == ["120"]

    def test_globale_variable(self):
        code = """zaehler = 0
DEFINIERE erhoehe():
    GLOBAL zaehler
    zaehler = zaehler + 1
ENDE FUNKTION
erhoehe()
erhoehe()
erhoehe()
AUSGABE zaehler"""
        out = zuse_ausfuehren(code)
        assert out == ["3"]

    def test_lambda(self):
        code = """verdopple = AKTION x: x * 2
AUSGABE verdopple(5)"""
        out = zuse_ausfuehren(code)
        assert out == ["10"]


# ─── 8. Listen & Dicts ────────────────────────────────────────

class TestDatenstrukturen:

    def test_liste_erstellen(self):
        out = zuse_ausfuehren("x = [1, 2, 3]\nAUSGABE len(x)")
        assert out == ["3"]

    def test_liste_index(self):
        out = zuse_ausfuehren("x = [10, 20, 30]\nAUSGABE x[1]")
        assert out == ["20"]

    def test_liste_index_zuweisung(self):
        out = zuse_ausfuehren("x = [1, 2, 3]\nx[0] = 99\nAUSGABE x[0]")
        assert out == ["99"]

    def test_liste_slicing(self):
        out = zuse_ausfuehren("x = [1, 2, 3, 4, 5]\nAUSGABE x[1:3]")
        assert out == ["[2, 3]"]

    def test_dict_erstellen(self):
        out = zuse_ausfuehren('d = {"name": "Zuse"}\nAUSGABE d["name"]')
        assert out == ["Zuse"]

    def test_dict_zuweisung(self):
        out = zuse_ausfuehren('d = {}\nd["key"] = "value"\nAUSGABE d["key"]')
        assert out == ["value"]

    def test_leere_liste(self):
        out = zuse_ausfuehren("x = liste()\nAUSGABE len(x)")
        assert out == ["0"]

    def test_leeres_dict(self):
        out = zuse_ausfuehren("d = dict()\nAUSGABE typ(d)")
        assert out == ["dict"]


# ─── 9. Eingebaute Funktionen ─────────────────────────────────

class TestBuiltins:

    def test_str(self):
        out = zuse_ausfuehren("AUSGABE str(42)")
        assert out == ["42"]

    def test_int(self):
        out = zuse_ausfuehren('AUSGABE int("10")')
        assert out == ["10"]

    def test_float(self):
        out = zuse_ausfuehren('AUSGABE float("3.5")')
        assert out == ["3.5"]

    def test_len_string(self):
        out = zuse_ausfuehren('AUSGABE len("Hallo")')
        assert out == ["5"]

    def test_len_liste(self):
        out = zuse_ausfuehren("AUSGABE len([1, 2, 3])")
        assert out == ["3"]

    def test_typ(self):
        out = zuse_ausfuehren("AUSGABE typ(42)")
        assert out == ["int"]


# ─── 10. Klassen & OOP ────────────────────────────────────────

class TestKlassen:

    def test_klasse_erstellen(self):
        code = """KLASSE Hund:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION
    DEFINIERE bellen():
        AUSGABE MEIN.name + " sagt Wuff!"
    ENDE FUNKTION
ENDE KLASSE
rex = Hund.ERSTELLE("Rex")
rex.bellen()"""
        out = zuse_ausfuehren(code)
        assert out == ["Rex sagt Wuff!"]

    def test_klasse_attribut_lesen(self):
        code = """KLASSE Auto:
    DEFINIERE ERSTELLE(marke):
        MEIN.marke = marke
    ENDE FUNKTION
ENDE KLASSE
a = Auto.ERSTELLE("BMW")
AUSGABE a.marke"""
        out = zuse_ausfuehren(code)
        assert out == ["BMW"]

    def test_vererbung(self):
        code = """KLASSE Tier:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION
    DEFINIERE ruf():
        AUSGABE MEIN.name + " macht Geräusch"
    ENDE FUNKTION
ENDE KLASSE
KLASSE Hund(Tier):
    DEFINIERE ruf():
        AUSGABE MEIN.name + " sagt Wuff"
    ENDE FUNKTION
ENDE KLASSE
h = Hund.ERSTELLE("Rex")
h.ruf()"""
        out = zuse_ausfuehren(code)
        assert out == ["Rex sagt Wuff"]

    def test_vererbung_konstruktor(self):
        code = """KLASSE Basis:
    DEFINIERE ERSTELLE(x):
        MEIN.x = x
    ENDE FUNKTION
ENDE KLASSE
KLASSE Kind(Basis):
    DEFINIERE zeige():
        AUSGABE MEIN.x
    ENDE FUNKTION
ENDE KLASSE
k = Kind.ERSTELLE(42)
k.zeige()"""
        out = zuse_ausfuehren(code)
        assert out == ["42"]


# ─── 11. Fehlerbehandlung ─────────────────────────────────────

class TestFehlerbehandlung:

    def test_versuche_fange(self):
        code = """VERSUCHE
    x = 10 / 0
FANGE
    AUSGABE "Fehler gefangen"
ENDE VERSUCHE"""
        out = zuse_ausfuehren(code)
        assert out == ["Fehler gefangen"]

    def test_versuche_ohne_fehler(self):
        code = """VERSUCHE
    AUSGABE "OK"
FANGE
    AUSGABE "Fehler"
ENDE VERSUCHE"""
        out = zuse_ausfuehren(code)
        assert out == ["OK"]


# ─── 12. Imports ──────────────────────────────────────────────

class TestImports:

    def test_import_math(self):
        code = """BENUTZE math ALS m
AUSGABE m.pi > 3"""
        out = zuse_ausfuehren(code)
        assert out == ["True"]

    def test_import_zuse_lib_ignoriert(self):
        """BENUTZE deutsch sollte keinen Fehler werfen."""
        out = zuse_ausfuehren("BENUTZE deutsch")
        assert not any("Fehler" in s for s in out)

    def test_safe_mode_blockiert(self):
        """Im Lernmodus sind gefährliche Module gesperrt."""
        out = zuse_ausfuehren("BENUTZE os", safe_mode=True)
        assert any("Sicherheits-Sperre" in s or "nicht erlaubt" in s for s in out)


# ─── 13. Eingabe ──────────────────────────────────────────────

class TestEingabe:

    def test_eingabe_text(self):
        out = zuse_ausfuehren('name = EINGABE_TEXT("Name?")\nAUSGABE name', eingaben=["Manuel"])
        assert out == ["Manuel"]

    def test_eingabe_zahl(self):
        out = zuse_ausfuehren('alter = EINGABE_ZAHL("Alter?")\nAUSGABE alter', eingaben=["25"])
        assert out == ["25"]

    def test_eingabe_zahl_float(self):
        out = zuse_ausfuehren('x = EINGABE_ZAHL("Zahl?")\nAUSGABE x', eingaben=["3.5"])
        assert out == ["3.5"]
