# FILE: tests/test_typ_pruefung.py — Tests für Typ-Prüfung & Konvertierung (ROADMAP 7.2 S5)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren


# ─── IST_ZAHL / IS_NUMBER ───────────────────────────────────────────

class TestIstZahl:
    def test_ganzzahl(self):
        assert zuse_ausfuehren('ZEIGE IST_ZAHL(42)', 'deutsch') == ['True']

    def test_kommazahl(self):
        assert zuse_ausfuehren('ZEIGE IST_ZAHL(3.14)', 'deutsch') == ['True']

    def test_text_ist_keine_zahl(self):
        assert zuse_ausfuehren('ZEIGE IST_ZAHL("hello")', 'deutsch') == ['False']

    def test_liste_ist_keine_zahl(self):
        assert zuse_ausfuehren('ZEIGE IST_ZAHL([1, 2])', 'deutsch') == ['False']

    def test_bool_ist_keine_zahl(self):
        assert zuse_ausfuehren('ZEIGE IST_ZAHL(wahr)', 'deutsch') == ['False']

    def test_is_number_english(self):
        assert zuse_ausfuehren('SHOW IS_NUMBER(42)', 'english') == ['True']
        assert zuse_ausfuehren('SHOW IS_NUMBER("hi")', 'english') == ['False']


# ─── IST_TEXT / IS_TEXT ──────────────────────────────────────────────

class TestIstText:
    def test_string(self):
        assert zuse_ausfuehren('ZEIGE IST_TEXT("hallo")', 'deutsch') == ['True']

    def test_zahl_ist_kein_text(self):
        assert zuse_ausfuehren('ZEIGE IST_TEXT(42)', 'deutsch') == ['False']

    def test_is_text_english(self):
        assert zuse_ausfuehren('SHOW IS_TEXT("hello")', 'english') == ['True']


# ─── IST_LISTE / IS_LIST ────────────────────────────────────────────

class TestIstListe:
    def test_liste(self):
        assert zuse_ausfuehren('ZEIGE IST_LISTE([1, 2, 3])', 'deutsch') == ['True']

    def test_text_ist_keine_liste(self):
        assert zuse_ausfuehren('ZEIGE IST_LISTE("abc")', 'deutsch') == ['False']

    def test_is_list_english(self):
        assert zuse_ausfuehren('SHOW IS_LIST([1])', 'english') == ['True']


# ─── IST_DICT / IS_DICT ─────────────────────────────────────────────

class TestIstDict:
    def test_dict(self):
        assert zuse_ausfuehren('ZEIGE IST_DICT({"a": 1})', 'deutsch') == ['True']

    def test_liste_ist_kein_dict(self):
        assert zuse_ausfuehren('ZEIGE IST_DICT([1, 2])', 'deutsch') == ['False']

    def test_is_dict_english(self):
        assert zuse_ausfuehren('SHOW IS_DICT({"a": 1})', 'english') == ['True']


# ─── IST_BOOL / IS_BOOL ─────────────────────────────────────────────

class TestIstBool:
    def test_wahr(self):
        assert zuse_ausfuehren('ZEIGE IST_BOOL(wahr)', 'deutsch') == ['True']

    def test_falsch(self):
        assert zuse_ausfuehren('ZEIGE IST_BOOL(falsch)', 'deutsch') == ['True']

    def test_zahl_ist_kein_bool(self):
        assert zuse_ausfuehren('ZEIGE IST_BOOL(1)', 'deutsch') == ['False']

    def test_is_bool_english(self):
        assert zuse_ausfuehren('SHOW IS_BOOL(true)', 'english') == ['True']


# ─── IST_NICHTS / IS_NONE ───────────────────────────────────────────

class TestIstNichts:
    def test_nichts(self):
        assert zuse_ausfuehren('ZEIGE IST_NICHTS(NICHTS)', 'deutsch') == ['True']

    def test_zahl_ist_nicht_nichts(self):
        assert zuse_ausfuehren('ZEIGE IST_NICHTS(42)', 'deutsch') == ['False']

    def test_is_none_english(self):
        assert zuse_ausfuehren('SHOW IS_NONE(NOTHING)', 'english') == ['True']
        assert zuse_ausfuehren('SHOW IS_NONE(42)', 'english') == ['False']


# ─── NICHTS / NOTHING Keyword ────────────────────────────────────────

class TestNichtsKeyword:
    def test_nichts_zuweisung(self):
        code = '''x = NICHTS
ZEIGE IST_NICHTS(x)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['True']

    def test_nichts_vergleich(self):
        code = '''x = NICHTS
WENN x == NICHTS DANN
    ZEIGE "ist nichts"
ENDE WENN'''
        assert zuse_ausfuehren(code, 'deutsch') == ['ist nichts']

    def test_nothing_english(self):
        code = '''x = NOTHING
SHOW IS_NONE(x)'''
        assert zuse_ausfuehren(code, 'english') == ['True']

    def test_nada_espaniol(self):
        code = '''x = NADA
IMPRIMIR ES_NADA(x)'''
        assert zuse_ausfuehren(code, 'espaniol') == ['True']

    def test_rien_francais(self):
        code = '''x = RIEN
IMPRIMER EST_RIEN(x)'''
        assert zuse_ausfuehren(code, 'francais') == ['True']

    def test_niente_italiano(self):
        code = '''x = NIENTE
STAMPA E_NIENTE(x)'''
        assert zuse_ausfuehren(code, 'italiano') == ['True']

    def test_nada_portugues(self):
        code = '''x = NADA
IMPRIMIR E_NADA(x)'''
        assert zuse_ausfuehren(code, 'portugues') == ['True']


# ─── ALS_ZAHL / TO_NUMBER ───────────────────────────────────────────

class TestAlsZahl:
    def test_text_zu_ganzzahl(self):
        assert zuse_ausfuehren('ZEIGE ALS_ZAHL("42")', 'deutsch') == ['42']

    def test_text_zu_kommazahl(self):
        assert zuse_ausfuehren('ZEIGE ALS_ZAHL("3.14")', 'deutsch') == ['3.14']

    def test_to_number_english(self):
        assert zuse_ausfuehren('SHOW TO_NUMBER("42")', 'english') == ['42']
        assert zuse_ausfuehren('SHOW TO_NUMBER("3.14")', 'english') == ['3.14']


# ─── ALS_TEXT / TO_TEXT ──────────────────────────────────────────────

class TestAlsText:
    def test_zahl_zu_text(self):
        assert zuse_ausfuehren('ZEIGE ALS_TEXT(42)', 'deutsch') == ['42']

    def test_liste_zu_text(self):
        assert zuse_ausfuehren('ZEIGE ALS_TEXT([1, 2])', 'deutsch') == ['[1, 2]']

    def test_to_text_english(self):
        assert zuse_ausfuehren('SHOW TO_TEXT(42)', 'english') == ['42']


# ─── Praxisbeispiel: Sichere Eingabeverarbeitung ────────────────────

class TestPraxisTypPruefung:
    def test_typ_basierte_verarbeitung(self):
        code = '''DEFINIERE beschreibe(x)
    WÄHLE IST_ZAHL(x)
        FALL wahr DANN
            ERGEBNIS "Zahl: " + ALS_TEXT(x)
    ENDE WÄHLE
    WÄHLE IST_TEXT(x)
        FALL wahr DANN
            ERGEBNIS "Text: " + x
    ENDE WÄHLE
    ERGEBNIS "Unbekannt"
ENDE FUNKTION

ZEIGE beschreibe(42)
ZEIGE beschreibe("hallo")'''
        result = zuse_ausfuehren(code, 'deutsch')
        assert result == ['Zahl: 42', 'Text: hallo']

    def test_type_check_english(self):
        code = '''DEFINE describe(x)
    IF IS_NUMBER(x) THEN
        RESULT "Number: " + TO_TEXT(x)
    END IF
    IF IS_TEXT(x) THEN
        RESULT "Text: " + x
    END IF
    RESULT "Unknown"
END FUNCTION

SHOW describe(42)
SHOW describe("hello")'''
        result = zuse_ausfuehren(code, 'english')
        assert result == ['Number: 42', 'Text: hello']
