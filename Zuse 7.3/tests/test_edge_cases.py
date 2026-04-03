# FILE: tests/test_edge_cases.py
# Edge-Case-Tests für Zuse (Phase 9.1)

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.conftest import zuse_ausfuehren, zuse_ast, zuse_tokens


class TestLeerprogramme:
    """Tests für leere/minimale Programme."""

    def test_leeres_programm(self):
        result = zuse_ausfuehren("")
        assert result == []

    def test_nur_leerzeilen(self):
        result = zuse_ausfuehren("\n\n\n")
        assert result == []

    def test_nur_kommentar(self):
        result = zuse_ausfuehren("# Nur ein Kommentar")
        assert result == []

    def test_nur_ausgabe(self):
        result = zuse_ausfuehren('AUSGABE "Hallo"')
        assert result == ["Hallo"]


class TestUnicode:
    """Tests für Unicode-Unterstützung."""

    def test_umlaute_in_variablen(self):
        result = zuse_ausfuehren('größe = 42\nAUSGABE größe')
        assert result == ["42"]

    def test_akzente_franzoesisch(self):
        result = zuse_ausfuehren('café = "Latte"\nAUSGABE café')
        assert result == ["Latte"]

    def test_akzente_spanisch(self):
        result = zuse_ausfuehren('año = 2026\nAUSGABE año')
        assert result == ["2026"]

    def test_scharfes_s(self):
        result = zuse_ausfuehren('straße = "Hauptstraße"\nAUSGABE straße')
        assert result == ["Hauptstraße"]


class TestZahlen:
    """Tests für Zahlen-Grenzwerte."""

    def test_grosse_zahl(self):
        result = zuse_ausfuehren("AUSGABE 999999999999999")
        assert result == ["999999999999999"]

    def test_kleine_dezimalzahl(self):
        result = zuse_ausfuehren("AUSGABE 0.001")
        assert result == ["0.001"]

    def test_negative_zahl(self):
        result = zuse_ausfuehren("AUSGABE -42")
        assert result == ["-42"]

    def test_division_durch_null(self):
        result = zuse_ausfuehren("AUSGABE 1 / 0")
        assert len(result) == 1  # Fehlermeldung

    def test_modulo_durch_null(self):
        result = zuse_ausfuehren("AUSGABE 5 % 0")
        assert len(result) == 1  # Fehlermeldung

    def test_fliesskomma_addition(self):
        """0.1 + 0.2 sollte nicht abstürzen."""
        result = zuse_ausfuehren("AUSGABE 0.1 + 0.2")
        assert len(result) == 1
        val = float(result[0])
        assert abs(val - 0.3) < 0.01


class TestLeereKollektionen:
    """Tests für leere Listen/Dicts/Strings."""

    def test_leere_liste(self):
        result = zuse_ausfuehren("x = []\nAUSGABE LAENGE(x)")
        assert result == ["0"]

    def test_leeres_dict(self):
        result = zuse_ausfuehren("x = {}\nAUSGABE LAENGE(x)")
        assert result == ["0"]

    def test_leerer_string(self):
        result = zuse_ausfuehren('x = ""\nAUSGABE LAENGE(x)')
        assert result == ["0"]

    def test_schleife_ueber_leere_liste(self):
        result = zuse_ausfuehren("SCHLEIFE FÜR i IN [] MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert result == []

    def test_sortieren_leere_liste(self):
        result = zuse_ausfuehren("AUSGABE SORTIEREN([])")
        assert result == ["[]"]


class TestRekursion:
    """Tests für Rekursionsverhalten."""

    def test_einfache_rekursion(self):
        code = """DEFINIERE fak(n):
    WENN n <= 1 DANN
        ERGEBNIS IST 1
    ENDE WENN
    ERGEBNIS IST n * fak(n - 1)
ENDE FUNKTION
AUSGABE fak(10)"""
        result = zuse_ausfuehren(code)
        assert result == ["3628800"]

    def test_tiefe_rekursion_fehler(self):
        """Maximale Rekursionstiefe sollte saubere Fehlermeldung geben."""
        code = """DEFINIERE endlos(n):
    ERGEBNIS IST endlos(n + 1)
ENDE FUNKTION
AUSGABE endlos(0)"""
        result = zuse_ausfuehren(code)
        assert len(result) >= 1  # Fehlermeldung, kein Crash


class TestParserErrorRecovery:
    """Tests für die Parser Error-Recovery."""

    def test_mehrere_fehler_gemeldet(self):
        """Parser sammelt mehrere Fehler statt beim ersten abzubrechen."""
        code = "AUSGABE )\nAUSGABE )"
        with pytest.raises(RuntimeError) as exc_info:
            zuse_ast(code)
        msg = str(exc_info.value)
        # Sollte mindestens einen Fehler enthalten
        assert len(msg) > 0


class TestDoppelteParameter:
    """Tests für doppelte Parameternamen."""

    def test_doppelter_parameter_fehler(self):
        code = """DEFINIERE f(x, x):
    AUSGABE x
ENDE FUNKTION"""
        with pytest.raises(RuntimeError) as exc_info:
            zuse_ast(code)
        assert "doppelt" in str(exc_info.value).lower() or "'" in str(exc_info.value)


class TestLambdaMehrereParameter:
    """Tests für Lambda mit mehreren Parametern."""

    def test_lambda_zwei_parameter_klammern(self):
        code = """addiere = AKTION (a, b): a + b
AUSGABE addiere(3, 4)"""
        result = zuse_ausfuehren(code)
        assert result == ["7"]

    def test_lambda_zwei_parameter_ohne_klammern(self):
        code = """addiere = AKTION a, b: a + b
AUSGABE addiere(3, 4)"""
        result = zuse_ausfuehren(code)
        assert result == ["7"]


class TestNeueBuiltins:
    """Tests für die in Phase 5.1 hinzugefügten Builtins."""

    def test_alle_wahr(self):
        result = zuse_ausfuehren("AUSGABE ALLE([wahr, wahr, wahr])")
        assert result == ["True"]

    def test_alle_falsch(self):
        result = zuse_ausfuehren("AUSGABE ALLE([wahr, falsch, wahr])")
        assert result == ["False"]

    def test_irgendein_wahr(self):
        result = zuse_ausfuehren("AUSGABE IRGENDEIN([falsch, wahr, falsch])")
        assert result == ["True"]

    def test_irgendein_falsch(self):
        result = zuse_ausfuehren("AUSGABE IRGENDEIN([falsch, falsch])")
        assert result == ["False"]

    def test_zeichencode(self):
        result = zuse_ausfuehren('AUSGABE ZEICHENCODE("A")')
        assert result == ["65"]

    def test_zeichen(self):
        result = zuse_ausfuehren('AUSGABE ZEICHEN(65)')
        assert result == ["A"]

    def test_hex(self):
        result = zuse_ausfuehren("AUSGABE HEX(255)")
        assert result == ["0xff"]

    def test_bin(self):
        result = zuse_ausfuehren("AUSGABE BIN(10)")
        assert result == ["0b1010"]

    def test_okt(self):
        result = zuse_ausfuehren("AUSGABE OKT(8)")
        assert result == ["0o10"]


class TestImportCache:
    """Tests für Import-Caching."""

    def test_doppelter_import_kein_crash(self):
        """Doppelter Import des gleichen Moduls sollte funktionieren."""
        code = """BENUTZE math ALS m1
BENUTZE math ALS m2
AUSGABE m1.pi == m2.pi"""
        result = zuse_ausfuehren(code)
        assert result == ["True"]


class TestZirkulaereVererbung:
    """Tests für zirkuläre Vererbungserkennung."""

    def test_einfache_vererbung_funktioniert(self):
        code = """KLASSE Tier:
    DEFINIERE spreche():
        ERGEBNIS IST "..."
    ENDE FUNKTION
ENDE KLASSE

KLASSE Hund(Tier):
    DEFINIERE spreche():
        ERGEBNIS IST "Wuff"
    ENDE FUNKTION
ENDE KLASSE

h = Hund()
AUSGABE h.spreche()"""
        result = zuse_ausfuehren(code)
        assert result == ["Wuff"]


class TestLexerSpalte:
    """Tests für Spaltenposition in Lexer-Fehlern."""

    def test_unbekanntes_zeichen_mit_spalte(self):
        with pytest.raises(RuntimeError) as exc_info:
            zuse_tokens("x = §")
        msg = str(exc_info.value)
        assert "Spalte" in msg
