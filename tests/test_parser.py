# FILE: tests/test_parser.py — Parser-Tests: AST-Struktur für alle Konstrukte
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from tests.conftest import zuse_ast


# ─── 1. Programm-Struktur ─────────────────────────────────────

class TestParserBasis:
    """Grundlegende AST-Struktur."""

    def test_leeres_programm(self):
        ast = zuse_ast("")
        assert ast["type"] == "PROGRAMM"
        assert ast["body"] == []

    def test_programm_hat_body(self):
        ast = zuse_ast('AUSGABE "Hallo"')
        assert ast["type"] == "PROGRAMM"
        assert len(ast["body"]) == 1


# ─── 2. Ausgabe ───────────────────────────────────────────────

class TestParserAusgabe:

    def test_ausgabe_string(self):
        ast = zuse_ast('AUSGABE "Hallo Welt"')
        stmt = ast["body"][0]
        assert stmt["type"] == "AUSGABE_ANWEISUNG"
        assert stmt["wert"]["type"] == "STRING_LITERAL"
        assert stmt["wert"]["wert"] == '"Hallo Welt"'

    def test_ausgabe_zahl(self):
        ast = zuse_ast("AUSGABE 42")
        stmt = ast["body"][0]
        assert stmt["wert"]["type"] == "ZAHL_LITERAL"
        assert stmt["wert"]["wert"] == "42"

    def test_ausgabe_ausdruck(self):
        ast = zuse_ast("AUSGABE 1 + 2")
        stmt = ast["body"][0]
        assert stmt["wert"]["type"] == "BINÄRER_AUSDRUCK"
        assert stmt["wert"]["operator"] == "+"


# ─── 3. Variablen & Zuweisungen ───────────────────────────────

class TestParserZuweisung:

    def test_einfache_zuweisung(self):
        ast = zuse_ast('name = "Manuel"')
        stmt = ast["body"][0]
        assert stmt["type"] == "ZUWEISUNG"
        assert stmt["ziel"]["type"] == "VARIABLE"
        assert stmt["ziel"]["name"] == "name"
        assert stmt["wert"]["type"] == "STRING_LITERAL"

    def test_zahl_zuweisung(self):
        ast = zuse_ast("alter = 35")
        stmt = ast["body"][0]
        assert stmt["wert"]["type"] == "ZAHL_LITERAL"

    def test_ausdruck_zuweisung(self):
        ast = zuse_ast("x = 1 + 2 * 3")
        stmt = ast["body"][0]
        # Operator-Präzedenz: 1 + (2 * 3)
        wert = stmt["wert"]
        assert wert["type"] == "BINÄRER_AUSDRUCK"
        assert wert["operator"] == "+"
        assert wert["rechts"]["type"] == "BINÄRER_AUSDRUCK"
        assert wert["rechts"]["operator"] == "*"

    def test_attribut_zuweisung(self):
        ast = zuse_ast("MEIN.name = x")
        stmt = ast["body"][0]
        assert stmt["type"] == "ZUWEISUNG"
        assert stmt["ziel"]["type"] == "ATTRIBUT_ZUGRIFF"
        assert stmt["ziel"]["attribut"] == "name"

    def test_index_zuweisung(self):
        ast = zuse_ast("liste[0] = 42")
        stmt = ast["body"][0]
        assert stmt["type"] == "ZUWEISUNG"
        assert stmt["ziel"]["type"] == "INDEX_ZUGRIFF"


# ─── 4. Ausdrücke & Operatoren ────────────────────────────────

class TestParserAusdruecke:

    def test_addition(self):
        ast = zuse_ast("AUSGABE 1 + 2")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "+"

    def test_subtraktion(self):
        ast = zuse_ast("AUSGABE 5 - 3")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "-"

    def test_multiplikation(self):
        ast = zuse_ast("AUSGABE 4 * 4")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "*"

    def test_division(self):
        ast = zuse_ast("AUSGABE 10 / 2")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "/"

    def test_potenz(self):
        ast = zuse_ast("AUSGABE 2 ^ 3")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "^"

    def test_modulo(self):
        ast = zuse_ast("AUSGABE 10 % 3")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "%"

    def test_vergleich_gleich(self):
        ast = zuse_ast("AUSGABE x == 5")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "=="

    def test_vergleich_ungleich(self):
        ast = zuse_ast("AUSGABE x != 5")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "!="

    def test_vergleich_kleiner(self):
        ast = zuse_ast("AUSGABE x < 5")
        expr = ast["body"][0]["wert"]
        assert expr["operator"] == "<"

    def test_unaeres_minus(self):
        ast = zuse_ast("AUSGABE -5")
        expr = ast["body"][0]["wert"]
        assert expr["type"] == "UNAER_MINUS"

    def test_praezedenz_punkt_vor_strich(self):
        ast = zuse_ast("AUSGABE 2 + 3 * 4")
        expr = ast["body"][0]["wert"]
        # Sollte (2 + (3 * 4)) sein
        assert expr["operator"] == "+"
        assert expr["links"]["type"] == "ZAHL_LITERAL"
        assert expr["rechts"]["operator"] == "*"

    def test_klammer_aendert_praezedenz(self):
        ast = zuse_ast("AUSGABE (2 + 3) * 4")
        expr = ast["body"][0]["wert"]
        # Sollte ((2 + 3) * 4) sein
        assert expr["operator"] == "*"
        assert expr["links"]["operator"] == "+"


# ─── 5. Listen & Dicts ────────────────────────────────────────

class TestParserDatenstrukturen:

    def test_leere_liste(self):
        ast = zuse_ast("x = []")
        wert = ast["body"][0]["wert"]
        assert wert["type"] == "LISTEN_LITERAL"
        assert wert["elemente"] == []

    def test_liste_mit_elementen(self):
        ast = zuse_ast("x = [1, 2, 3]")
        wert = ast["body"][0]["wert"]
        assert wert["type"] == "LISTEN_LITERAL"
        assert len(wert["elemente"]) == 3

    def test_leeres_dict(self):
        ast = zuse_ast("x = {}")
        wert = ast["body"][0]["wert"]
        assert wert["type"] == "DICT_LITERAL"
        assert wert["paare"] == []

    def test_dict_mit_paaren(self):
        ast = zuse_ast('x = {"a": 1, "b": 2}')
        wert = ast["body"][0]["wert"]
        assert wert["type"] == "DICT_LITERAL"
        assert len(wert["paare"]) == 2

    def test_index_zugriff(self):
        ast = zuse_ast("AUSGABE liste[0]")
        expr = ast["body"][0]["wert"]
        assert expr["type"] == "INDEX_ZUGRIFF"

    def test_slicing(self):
        ast = zuse_ast("AUSGABE liste[1:3]")
        expr = ast["body"][0]["wert"]
        assert expr["type"] == "SLICING"


# ─── 6. Kontrollstrukturen ────────────────────────────────────

class TestParserKontrollstrukturen:

    def test_wenn_dann(self):
        code = """WENN x > 5 DANN
    AUSGABE "ja"
ENDE WENN"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert stmt["type"] == "WENN_ANWEISUNG"
        assert len(stmt["faelle"]) == 1
        assert stmt["sonst_koerper"] is None

    def test_wenn_sonst(self):
        code = """WENN x > 5 DANN
    AUSGABE "ja"
SONST
    AUSGABE "nein"
ENDE WENN"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert len(stmt["faelle"]) == 1
        assert stmt["sonst_koerper"] is not None
        assert len(stmt["sonst_koerper"]) == 1

    def test_wenn_sonst_wenn(self):
        code = """WENN x > 10 DANN
    AUSGABE "groß"
SONST WENN x > 5 DANN
    AUSGABE "mittel"
SONST
    AUSGABE "klein"
ENDE WENN"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert len(stmt["faelle"]) == 2  # WENN + SONST WENN
        assert stmt["sonst_koerper"] is not None

    def test_schleife_solange(self):
        code = """SCHLEIFE SOLANGE x < 10 MACHE
    x = x + 1
ENDE SCHLEIFE"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert stmt["type"] == "SCHLEIFE_SOLANGE"
        assert stmt["bedingung"] is not None
        assert len(stmt["koerper"]) == 1

    def test_schleife_fuer(self):
        code = """SCHLEIFE FÜR i IN [1, 2, 3] MACHE
    AUSGABE i
ENDE SCHLEIFE"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert stmt["type"] == "SCHLEIFE_FÜR"
        assert stmt["variable"] == "i"
        assert stmt["liste"]["type"] == "LISTEN_LITERAL"
        assert len(stmt["koerper"]) == 1

    def test_schleife_ohne_schleife_keyword(self):
        """FÜR ... MACHE ohne vorangestelltes SCHLEIFE funktioniert auch."""
        code = """FÜR i IN [1, 2] MACHE
    AUSGABE i
ENDE SCHLEIFE"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert stmt["type"] == "SCHLEIFE_FÜR"


# ─── 7. Funktionen ────────────────────────────────────────────

class TestParserFunktionen:

    def test_funktion_ohne_parameter(self):
        code = """DEFINIERE hallo():
    AUSGABE "Hallo"
ENDE FUNKTION"""
        ast = zuse_ast(code)
        func = ast["body"][0]
        assert func["type"] == "FUNKTIONS_DEFINITION"
        assert func["name"] == "hallo"
        assert func["parameter"] == []
        assert len(func["body"]) == 1

    def test_funktion_mit_parametern(self):
        code = """DEFINIERE addiere(a, b):
    ERGEBNIS IST a + b
ENDE FUNKTION"""
        ast = zuse_ast(code)
        func = ast["body"][0]
        assert func["parameter"] == ["a", "b"]
        assert func["body"][0]["type"] == "ERGEBNIS_ANWEISUNG"

    def test_funktions_aufruf(self):
        ast = zuse_ast("hallo()")
        stmt = ast["body"][0]
        assert stmt["type"] == "FUNKTIONS_AUFRUF"
        assert stmt["name"] == "hallo"
        assert stmt["args"] == []

    def test_funktions_aufruf_mit_args(self):
        ast = zuse_ast('gruss("Manuel", 35)')
        stmt = ast["body"][0]
        assert stmt["type"] == "FUNKTIONS_AUFRUF"
        assert len(stmt["args"]) == 2

    def test_funktions_aufruf_mit_kwargs(self):
        ast = zuse_ast("test(x=1, y=2)")
        stmt = ast["body"][0]
        assert len(stmt["kwargs"]) == 2
        assert stmt["kwargs"][0][0] == "x"
        assert stmt["kwargs"][1][0] == "y"

    def test_lambda(self):
        ast = zuse_ast("cmd = AKTION x: x + 1")
        stmt = ast["body"][0]
        lam = stmt["wert"]
        assert lam["type"] == "LAMBDA_ERSTELLUNG"
        assert lam["params"] == ["x"]

    def test_ergebnis_anweisung(self):
        code = """DEFINIERE doppelt(x):
    ERGEBNIS IST x * 2
ENDE FUNKTION"""
        ast = zuse_ast(code)
        ret = ast["body"][0]["body"][0]
        assert ret["type"] == "ERGEBNIS_ANWEISUNG"

    def test_global_anweisung(self):
        code = """DEFINIERE test():
    GLOBAL zaehler
    zaehler = zaehler + 1
ENDE FUNKTION"""
        ast = zuse_ast(code)
        body = ast["body"][0]["body"]
        assert body[0]["type"] == "GLOBAL_ANWEISUNG"
        assert body[0]["name"] == "zaehler"


# ─── 8. Klassen ───────────────────────────────────────────────

class TestParserKlassen:

    def test_einfache_klasse(self):
        code = """KLASSE Hund:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION
ENDE KLASSE"""
        ast = zuse_ast(code)
        klass = ast["body"][0]
        assert klass["type"] == "KLASSEN_DEFINITION"
        assert klass["name"] == "Hund"
        assert klass["elternklasse"] is None
        assert len(klass["methoden"]) == 1

    def test_klasse_mit_vererbung(self):
        code = """KLASSE Dackel(Hund):
    DEFINIERE bellen():
        AUSGABE "Wuff!"
    ENDE FUNKTION
ENDE KLASSE"""
        ast = zuse_ast(code)
        klass = ast["body"][0]
        assert klass["elternklasse"] == "Hund"

    def test_klasse_mehrere_methoden(self):
        code = """KLASSE Tier:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION
    DEFINIERE ruf():
        AUSGABE MEIN.name
    ENDE FUNKTION
ENDE KLASSE"""
        ast = zuse_ast(code)
        klass = ast["body"][0]
        assert len(klass["methoden"]) == 2


# ─── 9. Fehlerbehandlung ──────────────────────────────────────

class TestParserVersuche:

    def test_versuche_fange(self):
        code = """VERSUCHE
    x = 10 / 0
FANGE
    AUSGABE "Fehler!"
ENDE VERSUCHE"""
        ast = zuse_ast(code)
        stmt = ast["body"][0]
        assert stmt["type"] == "VERSUCHE_ANWEISUNG"
        assert len(stmt["versuche_block"]) == 1
        assert len(stmt["fange_block"]) == 1


# ─── 10. Imports ──────────────────────────────────────────────

class TestParserImport:

    def test_einfacher_import(self):
        ast = zuse_ast("BENUTZE math")
        stmt = ast["body"][0]
        assert stmt["type"] == "IMPORT_ANWEISUNG"
        assert stmt["modul"] == "math"
        assert stmt["alias"] == "math"

    def test_import_mit_alias(self):
        ast = zuse_ast("BENUTZE math ALS m")
        stmt = ast["body"][0]
        assert stmt["modul"] == "math"
        assert stmt["alias"] == "m"


# ─── 11. Methoden & Attribute ─────────────────────────────────

class TestParserObjektzugriff:

    def test_attribut_zugriff(self):
        ast = zuse_ast("AUSGABE obj.name")
        expr = ast["body"][0]["wert"]
        assert expr["type"] == "ATTRIBUT_ZUGRIFF"
        assert expr["attribut"] == "name"

    def test_methoden_aufruf(self):
        ast = zuse_ast('pablo.gehe(100)')
        stmt = ast["body"][0]
        assert stmt["type"] == "METHODEN_AUFRUF"
        assert stmt["methode"] == "gehe"
        assert len(stmt["args"]) == 1

    def test_ketten_aufruf(self):
        """obj.a.b wird korrekt als verschachtelt geparst."""
        ast = zuse_ast("AUSGABE obj.a.b")
        expr = ast["body"][0]["wert"]
        assert expr["type"] == "ATTRIBUT_ZUGRIFF"
        assert expr["attribut"] == "b"
        assert expr["objekt"]["type"] == "ATTRIBUT_ZUGRIFF"
        assert expr["objekt"]["attribut"] == "a"

    def test_eingabe_text(self):
        ast = zuse_ast('name = EINGABE_TEXT("Name?")')
        wert = ast["body"][0]["wert"]
        assert wert["type"] == "EINGABE_AUFRUF"
        assert wert["modus"] == "text"

    def test_eingabe_zahl(self):
        ast = zuse_ast('alter = EINGABE_ZAHL("Alter?")')
        wert = ast["body"][0]["wert"]
        assert wert["type"] == "EINGABE_AUFRUF"
        assert wert["modus"] == "zahl"
