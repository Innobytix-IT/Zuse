# FILE: tests/test_waehle.py — Tests für WÄHLE-Anweisung (ROADMAP 7.2 S4)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren


# ─── Grundlagen: WÄHLE in Deutsch ───────────────────────────────────

class TestWaehleDeutsch:
    def test_einfaches_waehle(self):
        code = '''note = 1
WÄHLE note
    FALL 1 DANN
        ZEIGE "Sehr gut"
    FALL 2 DANN
        ZEIGE "Gut"
    FALL 3 DANN
        ZEIGE "Befriedigend"
    SONST
        ZEIGE "Unbekannt"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Sehr gut']

    def test_waehle_zweiter_fall(self):
        code = '''x = 2
WÄHLE x
    FALL 1 DANN
        ZEIGE "eins"
    FALL 2 DANN
        ZEIGE "zwei"
    FALL 3 DANN
        ZEIGE "drei"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['zwei']

    def test_waehle_sonst(self):
        code = '''x = 99
WÄHLE x
    FALL 1 DANN
        ZEIGE "eins"
    FALL 2 DANN
        ZEIGE "zwei"
    SONST
        ZEIGE "anderes"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['anderes']

    def test_waehle_kein_treffer_kein_sonst(self):
        """Kein FALL passt und kein SONST → keine Ausgabe."""
        code = '''x = 99
WÄHLE x
    FALL 1 DANN
        ZEIGE "eins"
    FALL 2 DANN
        ZEIGE "zwei"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == []

    def test_waehle_mit_strings(self):
        code = '''farbe = "rot"
WÄHLE farbe
    FALL "rot" DANN
        ZEIGE "Stopp"
    FALL "gelb" DANN
        ZEIGE "Achtung"
    FALL "grün" DANN
        ZEIGE "Fahren"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Stopp']

    def test_waehle_mit_ausdruck(self):
        """WÄHLE kann einen berechneten Ausdruck vergleichen."""
        code = '''a = 3
b = 2
WÄHLE a + b
    FALL 5 DANN
        ZEIGE "fünf"
    FALL 6 DANN
        ZEIGE "sechs"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['fünf']

    def test_waehle_mit_mehreren_anweisungen_pro_fall(self):
        code = '''x = 2
WÄHLE x
    FALL 1 DANN
        ZEIGE "a"
        ZEIGE "b"
    FALL 2 DANN
        ZEIGE "c"
        ZEIGE "d"
ENDE WÄHLE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['c', 'd']

    def test_waehle_in_funktion(self):
        code = '''DEFINIERE bewerte(note)
    WÄHLE note
        FALL 1 DANN
            ERGEBNIS "Sehr gut"
        FALL 2 DANN
            ERGEBNIS "Gut"
        SONST
            ERGEBNIS "Unbekannt"
    ENDE WÄHLE
ENDE FUNKTION

ZEIGE bewerte(1)
ZEIGE bewerte(2)
ZEIGE bewerte(5)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Sehr gut', 'Gut', 'Unbekannt']


# ─── SWITCH/CASE in English ─────────────────────────────────────────

class TestSwitchEnglish:
    def test_switch_basic(self):
        code = '''grade = 1
SWITCH grade
    CASE 1 THEN
        SHOW "Excellent"
    CASE 2 THEN
        SHOW "Good"
    ELSE
        SHOW "Unknown"
END SWITCH'''
        assert zuse_ausfuehren(code, 'english') == ['Excellent']

    def test_switch_default(self):
        code = '''x = 99
SWITCH x
    CASE 1 THEN
        SHOW "one"
    ELSE
        SHOW "other"
END SWITCH'''
        assert zuse_ausfuehren(code, 'english') == ['other']

    def test_switch_string(self):
        code = '''day = "monday"
SWITCH day
    CASE "monday" THEN
        SHOW "Start of week"
    CASE "friday" THEN
        SHOW "Almost weekend"
    ELSE
        SHOW "Regular day"
END SWITCH'''
        assert zuse_ausfuehren(code, 'english') == ['Start of week']

    def test_switch_in_function(self):
        code = '''DEFINE describe(n)
    SWITCH n
        CASE 1 THEN
            RESULT "one"
        CASE 2 THEN
            RESULT "two"
        ELSE
            RESULT "many"
    END SWITCH
END FUNCTION

SHOW describe(1)
SHOW describe(2)
SHOW describe(100)'''
        assert zuse_ausfuehren(code, 'english') == ['one', 'two', 'many']


# ─── Alle Sprachen ──────────────────────────────────────────────────

class TestWaehleAllesSprachen:
    def test_elegir_espaniol(self):
        code = '''x = 1
ELEGIR x
    CASO 1 ENTONCES
        IMPRIMIR "uno"
    CASO 2 ENTONCES
        IMPRIMIR "dos"
FIN ELEGIR'''
        assert zuse_ausfuehren(code, 'espaniol') == ['uno']

    def test_choisir_francais(self):
        code = '''x = 2
CHOISIR x
    CAS 1 ALORS
        IMPRIMER "un"
    CAS 2 ALORS
        IMPRIMER "deux"
FIN CHOISIR'''
        assert zuse_ausfuehren(code, 'francais') == ['deux']

    def test_scegli_italiano(self):
        code = '''x = 1
SCEGLI x
    CASO 1 ALLORA
        STAMPA "uno"
    CASO 2 ALLORA
        STAMPA "due"
FINE SCEGLI'''
        assert zuse_ausfuehren(code, 'italiano') == ['uno']

    def test_escolher_portugues(self):
        code = '''x = 2
ESCOLHER x
    CASO 1 ENTAO
        IMPRIMIR "um"
    CASO 2 ENTAO
        IMPRIMIR "dois"
FIM ESCOLHER'''
        assert zuse_ausfuehren(code, 'portugues') == ['dois']


# ─── Transpiler-Tests ───────────────────────────────────────────────

class TestWaehleTranspiler:
    def test_transpile_python(self):
        from transpiler import transpile
        code = '''WÄHLE x
    FALL 1 DANN
        AUSGABE "eins"
    FALL 2 DANN
        AUSGABE "zwei"
    SONST
        AUSGABE "anderes"
ENDE WÄHLE'''
        result = transpile(code, 'python')['code']
        assert '_switch_val' in result
        assert 'if _switch_val == 1' in result
        assert 'elif _switch_val == 2' in result
        assert 'else:' in result

    def test_transpile_javascript(self):
        from transpiler import transpile
        code = '''WÄHLE x
    FALL 1 DANN
        AUSGABE "eins"
    FALL 2 DANN
        AUSGABE "zwei"
    SONST
        AUSGABE "anderes"
ENDE WÄHLE'''
        result = transpile(code, 'deutsch', 'javascript')['code']
        assert 'switch' in result
        assert 'case 1:' in result
        assert 'case 2:' in result
        assert 'default:' in result
        assert 'break;' in result

    def test_transpile_java(self):
        from transpiler import transpile
        code = '''WÄHLE x
    FALL 1 DANN
        AUSGABE "eins"
    SONST
        AUSGABE "anderes"
ENDE WÄHLE'''
        result = transpile(code, 'deutsch', 'java')['code']
        assert 'switch' in result
        assert 'case 1:' in result
        assert 'default:' in result

    def test_transpile_csharp(self):
        from transpiler import transpile
        code = '''WÄHLE x
    FALL 1 DANN
        AUSGABE "eins"
    SONST
        AUSGABE "anderes"
ENDE WÄHLE'''
        result = transpile(code, 'deutsch', 'csharp')['code']
        assert 'switch' in result
        assert 'case 1:' in result
        assert 'default:' in result
