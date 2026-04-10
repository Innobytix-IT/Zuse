# FILE: tests/test_fehlermeldungen.py
# Tests fuer verstaendliche Fehlermeldungen und Tipps (B5.2)
# Erweitert fuer mehrsprachige Fehlermeldungen (i18n)

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tests.conftest import zuse_ausfuehren
from error_hints import get_hint, format_error_with_hint
from error_i18n import set_language, t


# ─── Fehlermeldungs-Inhalt ────────────────────────────────────────────────

class TestFehlerInhalt:
    """Prueft, dass Fehler verstaendliche Meldungen enthalten."""

    def test_fehlendes_dann(self):
        with pytest.raises(RuntimeError, match="Erwartet.*KEYWORD"):
            zuse_ausfuehren("WENN wahr\n    AUSGABE 1\nENDE WENN")

    def test_fehlendes_ende_funktion(self):
        with pytest.raises(RuntimeError):
            zuse_ausfuehren("DEFINIERE f():\n    AUSGABE 1")

    def test_fehlendes_mache(self):
        with pytest.raises(RuntimeError, match="Erwartet.*KEYWORD"):
            zuse_ausfuehren("SOLANGE wahr\n    AUSGABE 1\nENDE SCHLEIFE")

    def test_lexer_fehler(self):
        with pytest.raises(RuntimeError, match="Lexer"):
            zuse_ausfuehren("!!! ungueltig")

    def test_klasse_nur_definitionen(self):
        with pytest.raises(RuntimeError, match="DEFINE|DEFINIERE"):
            zuse_ausfuehren("KLASSE Foo:\n    x = 5\nENDE KLASSE")


# ─── Fehler-Tipps (Deutsch) ──────────────────────────────────────────────

class TestHints:
    """Prueft, dass error_hints passende Tipps zurueckgibt."""

    def setup_method(self):
        set_language("deutsch")

    def test_hint_dann(self):
        hint = get_hint("Syntaxfehler Zeile 5: Erwartet 'KW_DANN'")
        assert hint is not None
        assert "DANN" in hint

    def test_hint_mache(self):
        hint = get_hint("Syntaxfehler Zeile 3: Erwartet 'KW_MACHE'")
        assert hint is not None
        assert "MACHE" in hint

    def test_hint_ende_wenn(self):
        hint = get_hint("Erwartet 'KW_ENDE_WENN'")
        assert hint is not None
        assert "ENDE WENN" in hint

    def test_hint_ende_funktion(self):
        hint = get_hint("Erwartet 'KW_ENDE_FUNKTION'")
        assert hint is not None
        assert "ENDE FUNKTION" in hint

    def test_hint_ende_schleife(self):
        hint = get_hint("Erwartet 'KW_ENDE_SCHLEIFE'")
        assert hint is not None
        assert "ENDE SCHLEIFE" in hint

    def test_hint_ende_klasse(self):
        hint = get_hint("Erwartet 'KW_ENDE_KLASSE'")
        assert hint is not None
        assert "ENDE KLASSE" in hint

    def test_hint_variable(self):
        hint = get_hint("Zeile 5: Variable 'x' nicht definiert.")
        assert hint is not None
        assert "Variable" in hint or "variable" in hint

    def test_hint_division(self):
        hint = get_hint("Division durch Null")
        assert hint is not None

    def test_hint_typen(self):
        hint = get_hint("Unverträgliche Typen in Rechenoperation")
        assert hint is not None
        assert "str()" in hint

    def test_hint_iterierbar(self):
        hint = get_hint("Objekt ist nicht iterierbar")
        assert hint is not None
        assert "BEREICH" in hint

    def test_hint_rekursion(self):
        hint = get_hint("Maximale Rekursionstiefe erreicht")
        assert hint is not None
        assert "Abbruchbedingung" in hint

    def test_hint_modul(self):
        hint = get_hint("Modul 'xyz' nicht gefunden")
        assert hint is not None
        assert "zpkg" in hint

    def test_hint_sicherheit(self):
        hint = get_hint("Sicherheits-Sperre: Modul 'os' ist im Lernmodus nicht erlaubt.")
        assert hint is not None
        assert "Lernmodus" in hint or "Profi" in hint

    def test_hint_mehrfach_zuweisung(self):
        hint = get_hint("Mehrfach-Zuweisung: 3 Ziele aber 2 Werte.")
        assert hint is not None
        assert "=" in hint

    def test_hint_unerwartetes_token(self):
        hint = get_hint("Unerwartetes Token: AUSGABE Zeile 7")
        assert hint is not None
        assert "Zuse" in hint or "Rechtschreibung" in hint

    def test_hint_schleife(self):
        hint = get_hint("Erwartet FÜR oder SOLANGE")
        assert hint is not None
        assert "SCHLEIFE" in hint or "FÜR" in hint

    def test_hint_klasse(self):
        hint = get_hint("'Foo' ist keine Klasse.")
        assert hint is not None
        assert "KLASSE" in hint

    def test_hint_attribut(self):
        hint = get_hint("Kann Attribut 'name' nicht setzen")
        assert hint is not None
        assert "Attribut" in hint

    def test_hint_unbekannt_gibt_none(self):
        hint = get_hint("Ein komplett unbekannter Fehler xyz123")
        assert hint is None

    def test_format_mit_hint(self):
        result = format_error_with_hint("Division durch Null")
        assert "Division durch Null" in result
        assert "Tipp:" in result

    def test_format_ohne_hint(self):
        result = format_error_with_hint("xyz unbekannt")
        assert result == "xyz unbekannt"

    # ─── Schluessel-basierte Hints ────────────────────────────────────────

    def test_hint_per_key(self):
        hint = get_hint("ERR_VAR_NOT_DEFINED")
        assert hint is not None
        assert "Variable" in hint

    def test_hint_per_key_mit_kontext(self):
        hint = get_hint("ERR_SYNTAX_EXPECTED_TYPE", context="KW_DANN")
        assert hint is not None
        assert "DANN" in hint

    def test_format_mit_key(self):
        result = format_error_with_hint(
            "Zeile 5: Division durch Null ist nicht erlaubt.",
            error_key="ERR_DIVISION_BY_ZERO")
        assert "Tipp:" in result


# ─── Mehrsprachige Fehlermeldungen ────────────────────────────────────────

class TestI18nErrors:
    """Prueft, dass Fehlermeldungen in allen 6 Sprachen funktionieren."""

    def test_deutsch_default(self):
        set_language("deutsch")
        msg = t("ERR_VAR_NOT_DEFINED", line=5, name="x")
        assert "Variable" in msg
        assert "'x'" in msg
        assert "Zeile 5" in msg

    def test_english(self):
        set_language("english")
        msg = t("ERR_VAR_NOT_DEFINED", line=5, name="x")
        assert "Variable" in msg
        assert "'x'" in msg
        assert "Line 5" in msg

    def test_espaniol(self):
        set_language("espaniol")
        msg = t("ERR_DIVISION_BY_ZERO", line=3)
        assert "cero" in msg
        assert "Linea 3" in msg

    def test_francais(self):
        set_language("francais")
        msg = t("ERR_DIVISION_BY_ZERO", line=3)
        assert "zero" in msg
        assert "Ligne 3" in msg

    def test_italiano(self):
        set_language("italiano")
        msg = t("ERR_VAR_NOT_DEFINED", line=1, name="y")
        assert "Riga 1" in msg
        assert "'y'" in msg

    def test_portugues(self):
        set_language("portugues")
        msg = t("ERR_VAR_NOT_DEFINED", line=1, name="y")
        assert "Linha 1" in msg
        assert "'y'" in msg

    def test_fallback_to_deutsch(self):
        """Unbekannte Sprache -> Deutsch als Fallback."""
        set_language("klingonisch")
        # Bleibt bei vorheriger Sprache
        msg = t("ERR_DIVISION_BY_ZERO", line=1)
        assert msg  # Sollte irgendetwas zurueckgeben

    def test_unknown_key_returns_key(self):
        set_language("deutsch")
        msg = t("ERR_DOES_NOT_EXIST")
        assert msg == "ERR_DOES_NOT_EXIST"


# ─── Mehrsprachige Hints ─────────────────────────────────────────────────

class TestI18nHints:
    """Prueft, dass Hints in verschiedenen Sprachen funktionieren."""

    def test_hint_english(self):
        set_language("english")
        hint = get_hint("ERR_VAR_NOT_DEFINED")
        assert hint is not None
        assert "Tip:" in hint
        assert "variable" in hint.lower()

    def test_hint_espaniol(self):
        set_language("espaniol")
        hint = get_hint("ERR_DIVISION_BY_ZERO")
        assert hint is not None
        assert "Consejo:" in hint

    def test_hint_francais(self):
        set_language("francais")
        hint = get_hint("ERR_NOT_ITERABLE")
        assert hint is not None
        assert "Conseil:" in hint

    def test_hint_italiano(self):
        set_language("italiano")
        hint = get_hint("ERR_MAX_RECURSION")
        assert hint is not None
        assert "Suggerimento:" in hint

    def test_hint_portugues(self):
        set_language("portugues")
        hint = get_hint("ERR_VAR_NOT_DEFINED")
        assert hint is not None
        assert "Dica:" in hint

    def test_syntax_hint_english(self):
        set_language("english")
        hint = get_hint("ERR_SYNTAX_EXPECTED_TYPE", context="KW_DANN")
        assert hint is not None
        assert "THEN" in hint

    def test_format_english(self):
        set_language("english")
        result = format_error_with_hint(
            "Line 5: Division by zero is not allowed.",
            error_key="ERR_DIVISION_BY_ZERO")
        assert "Tip:" in result

    def teardown_method(self):
        """Reset to default language."""
        set_language("deutsch")
