# FILE: tests/test_lexer.py — Lexer-Tests für alle Sprachen
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from tests.conftest import zuse_tokens


# ─── 1. Basis-Tokenisierung ───────────────────────────────────

class TestLexerBasis:
    """Grundlegende Token-Erkennung."""

    def test_leerer_code(self, deutsch_lexer):
        tokens = deutsch_lexer.tokenize("")
        assert tokens[-1]["type"] == "EOF"

    def test_zahl_integer(self):
        tokens = zuse_tokens("42")
        zahlen = [t for t in tokens if t["type"] == "ZAHL"]
        assert len(zahlen) == 1
        assert zahlen[0]["value"] == "42"

    def test_zahl_float(self):
        tokens = zuse_tokens("3.14")
        zahlen = [t for t in tokens if t["type"] == "ZAHL"]
        assert len(zahlen) == 1
        assert zahlen[0]["value"] == "3.14"

    def test_string(self):
        tokens = zuse_tokens('"Hallo Welt"')
        strings = [t for t in tokens if t["type"] == "STRING"]
        assert len(strings) == 1
        assert strings[0]["value"] == '"Hallo Welt"'

    def test_name_einfach(self):
        tokens = zuse_tokens("meinName")
        namen = [t for t in tokens if t["type"] == "NAME"]
        assert len(namen) == 1
        assert namen[0]["value"] == "meinName"

    def test_name_mit_umlauten(self):
        tokens = zuse_tokens("größe")
        namen = [t for t in tokens if t["type"] == "NAME"]
        assert len(namen) == 1
        assert namen[0]["value"] == "größe"

    def test_operatoren(self):
        tokens = zuse_tokens("+ - * / = == != < > <= >=")
        ops = [t for t in tokens if t["type"] == "OPERATOR"]
        werte = [t["value"] for t in ops]
        assert "+" in werte
        assert "==" in werte
        assert "!=" in werte
        assert "<=" in werte
        assert ">=" in werte

    def test_klammern(self):
        tokens = zuse_tokens("(x)[y]{z}")
        typen = [t["type"] for t in tokens if t["type"] not in ("EOF",)]
        assert "KLAMMER_AUF" in typen
        assert "KLAMMER_ZU" in typen
        assert "KLAMMER_AUF_ECKIG" in typen
        assert "KLAMMER_ZU_ECKIG" in typen
        assert "GESCHWEIFT_AUF" in typen
        assert "GESCHWEIFT_ZU" in typen

    def test_kommentar_wird_erkannt(self):
        tokens = zuse_tokens("# Dies ist ein Kommentar\n42")
        typen = [t["type"] for t in tokens]
        # Kommentare werden als Token erzeugt aber vom Parser gefiltert
        assert "KOMMENTAR" in typen

    def test_zeilennummern(self):
        tokens = zuse_tokens("a\nb\nc")
        namen = [t for t in tokens if t["type"] == "NAME"]
        assert namen[0]["line"] == 1
        assert namen[1]["line"] == 2
        assert namen[2]["line"] == 3

    def test_unbekanntes_zeichen_fehler(self, deutsch_lexer):
        with pytest.raises(RuntimeError, match="Unbekanntes Zeichen"):
            deutsch_lexer.tokenize("§")


# ─── 2. Keyword-Erkennung (Deutsch) ───────────────────────────

class TestLexerKeywordsDeutsch:
    """Deutsche Keywords werden korrekt als kanonische Schlüssel erkannt."""

    ERWARTETE_KEYWORDS = {
        "WENN": "KW_WENN",
        "DANN": "KW_DANN",
        "SONST": "KW_SONST",
        "DEFINIERE": "KW_DEFINIERE",
        "SCHLEIFE": "KW_SCHLEIFE",
        "AUSGABE": "KW_AUSGABE",
        "KLASSE": "KW_KLASSE",
        "VERSUCHE": "KW_VERSUCHE",
        "FANGE": "KW_FANGE",
        "GLOBAL": "KW_GLOBAL",
    }

    @pytest.mark.parametrize("keyword,kanonisch", ERWARTETE_KEYWORDS.items())
    def test_keyword(self, keyword, kanonisch):
        tokens = zuse_tokens(keyword)
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == kanonisch

    def test_mehrteiliges_keyword_ende_wenn(self):
        tokens = zuse_tokens("ENDE WENN")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "KW_ENDE_WENN"

    def test_mehrteiliges_keyword_ende_schleife(self):
        tokens = zuse_tokens("ENDE SCHLEIFE")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "KW_ENDE_SCHLEIFE"

    def test_mehrteiliges_keyword_ende_funktion(self):
        tokens = zuse_tokens("ENDE FUNKTION")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "KW_ENDE_FUNKTION"

    def test_mehrteiliges_keyword_ergebnis_ist(self):
        tokens = zuse_tokens("ERGEBNIS IST")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "KW_ERGEBNIS"

    def test_boolean_wahr(self):
        tokens = zuse_tokens("wahr")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "CONST_WAHR"

    def test_boolean_falsch(self):
        tokens = zuse_tokens("falsch")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "CONST_FALSCH"

    def test_mein_keyword(self):
        tokens = zuse_tokens("MEIN")
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) == 1
        assert kw_tokens[0]["value"] == "KW_SELBST"

    def test_eingabe_text(self):
        tokens = zuse_tokens('EINGABE_TEXT("Name?")')
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert any(t["value"] == "FUNC_EINGABE_TEXT" for t in kw_tokens)

    def test_eingabe_zahl(self):
        tokens = zuse_tokens('EINGABE_ZAHL("Alter?")')
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert any(t["value"] == "FUNC_EINGABE_ZAHL" for t in kw_tokens)


# ─── 3. Mehrsprachigkeit ──────────────────────────────────────

class TestLexerMehrsprachig:
    """Keywords werden in allen Sprachen korrekt erkannt."""

    # Mapping: Sprache → lokales IF-Keyword
    IF_KEYWORDS = {
        "deutsch": "WENN",
        "english": "IF",
        "espaniol": "SI",
        "francais": "SI",
        "italiano": "SE",
        "portugues": "SE",
    }

    @pytest.mark.parametrize("sprache,keyword", IF_KEYWORDS.items())
    def test_wenn_keyword_in_sprache(self, sprache, keyword):
        tokens = zuse_tokens(keyword, sprache=sprache)
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) >= 1
        assert kw_tokens[0]["value"] == "KW_WENN"

    PRINT_KEYWORDS = {
        "deutsch": "AUSGABE",
        "english": "PRINT",
        "espaniol": "IMPRIMIR",
        "francais": "IMPRIMER",
        "italiano": "STAMPA",
        "portugues": "IMPRIMIR",
    }

    @pytest.mark.parametrize("sprache,keyword", PRINT_KEYWORDS.items())
    def test_ausgabe_keyword_in_sprache(self, sprache, keyword):
        tokens = zuse_tokens(keyword, sprache=sprache)
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) >= 1
        assert kw_tokens[0]["value"] == "KW_AUSGABE"

    DEFINE_KEYWORDS = {
        "deutsch": "DEFINIERE",
        "english": "DEFINE",
        "espaniol": "DEFINIR",
        "francais": "DEFINIR",
        "italiano": "DEFINIRE",
        "portugues": "DEFINIR",
    }

    @pytest.mark.parametrize("sprache,keyword", DEFINE_KEYWORDS.items())
    def test_definiere_keyword_in_sprache(self, sprache, keyword):
        tokens = zuse_tokens(keyword, sprache=sprache)
        kw_tokens = [t for t in tokens if t["type"] == "KEYWORD"]
        assert len(kw_tokens) >= 1
        assert kw_tokens[0]["value"] == "KW_DEFINIERE"


# ─── 4. Komplexe Token-Sequenzen ──────────────────────────────

class TestLexerKomplexeSequenzen:
    """Vollständige Code-Zeilen korrekt tokenisieren."""

    def test_variable_zuweisung(self):
        tokens = zuse_tokens('name = "Manuel"')
        typen = [t["type"] for t in tokens if t["type"] not in ("EOF",)]
        assert typen == ["NAME", "OPERATOR", "STRING"]

    def test_wenn_dann_zeile(self):
        tokens = zuse_tokens("WENN x > 5 DANN")
        typen = [t["type"] for t in tokens if t["type"] not in ("EOF",)]
        assert typen == ["KEYWORD", "NAME", "OPERATOR", "ZAHL", "KEYWORD"]

    def test_schleife_fuer_zeile(self):
        tokens = zuse_tokens("SCHLEIFE FÜR i IN liste MACHE")
        typen = [t["type"] for t in tokens if t["type"] not in ("EOF",)]
        assert typen == ["KEYWORD", "KEYWORD", "NAME", "KEYWORD", "NAME", "KEYWORD"]

    def test_methoden_aufruf(self):
        tokens = zuse_tokens('pablo.farbe("rot")')
        typen = [t["type"] for t in tokens if t["type"] not in ("EOF",)]
        assert typen == ["NAME", "PUNKT", "NAME", "KLAMMER_AUF", "STRING", "KLAMMER_ZU"]

    def test_liste_literal(self):
        tokens = zuse_tokens("[1, 2, 3]")
        typen = [t["type"] for t in tokens if t["type"] not in ("EOF",)]
        assert typen == [
            "KLAMMER_AUF_ECKIG", "ZAHL", "KOMMA", "ZAHL", "KOMMA", "ZAHL", "KLAMMER_ZU_ECKIG"
        ]

    def test_potenz_operator(self):
        tokens = zuse_tokens("2^3")
        ops = [t for t in tokens if t["type"] == "OPERATOR"]
        assert any(t["value"] == "^" for t in ops)

    def test_modulo_operator(self):
        tokens = zuse_tokens("10 % 3")
        ops = [t for t in tokens if t["type"] == "OPERATOR"]
        assert any(t["value"] == "%" for t in ops)
