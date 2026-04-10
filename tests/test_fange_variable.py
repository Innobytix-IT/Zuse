# FILE: tests/test_fange_variable.py — Tests für FANGE mit Fehlervariable (ROADMAP 7.2 S3)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren


# ─── FANGE ohne Variable (Rückwärtskompatibilität) ──────────────────

class TestFangeOhneVariable:
    def test_fange_ohne_variable_deutsch(self):
        code = '''VERSUCHE
    x = 10 / 0
FANGE
    ZEIGE "Fehler aufgefangen"
ENDE VERSUCHE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Fehler aufgefangen']

    def test_catch_ohne_variable_english(self):
        code = '''TRY
    x = 10 / 0
CATCH
    SHOW "Error caught"
END TRY'''
        assert zuse_ausfuehren(code, 'english') == ['Error caught']

    def test_fange_kein_fehler(self):
        """Wenn kein Fehler auftritt, wird der FANGE-Block übersprungen."""
        code = '''VERSUCHE
    x = 42
    ZEIGE x
FANGE
    ZEIGE "Fehler"
ENDE VERSUCHE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['42']


# ─── FANGE mit Variable (neues Feature) ─────────────────────────────

class TestFangeMitVariable:
    def test_division_durch_null_deutsch(self):
        code = '''VERSUCHE
    x = 10 / 0
FANGE fehler
    ZEIGE fehler
ENDE VERSUCHE'''
        result = zuse_ausfuehren(code, 'deutsch')
        assert len(result) == 1
        assert 'division' in result[0].lower() or '0' in result[0] or 'null' in result[0].lower() or 'zero' in result[0].lower()

    def test_catch_with_variable_english(self):
        code = '''TRY
    x = 10 / 0
CATCH error
    SHOW error
END TRY'''
        result = zuse_ausfuehren(code, 'english')
        assert len(result) == 1
        assert 'division' in result[0].lower() or '0' in result[0] or 'zero' in result[0].lower()

    def test_capturar_con_variable_espaniol(self):
        code = '''INTENTAR
    x = 10 / 0
CAPTURAR error
    IMPRIMIR error
FIN INTENTAR'''
        result = zuse_ausfuehren(code, 'espaniol')
        assert len(result) == 1

    def test_attraper_avec_variable_francais(self):
        code = '''ESSAYER
    x = 10 / 0
ATTRAPER erreur
    IMPRIMER erreur
FIN ESSAYER'''
        result = zuse_ausfuehren(code, 'francais')
        assert len(result) == 1

    def test_cattura_con_variabile_italiano(self):
        code = '''PROVA
    x = 10 / 0
CATTURA errore
    STAMPA errore
FINE PROVA'''
        result = zuse_ausfuehren(code, 'italiano')
        assert len(result) == 1

    def test_pegar_com_variavel_portugues(self):
        code = '''TENTAR
    x = 10 / 0
PEGAR erro
    IMPRIMIR erro
FIM TENTAR'''
        result = zuse_ausfuehren(code, 'portugues')
        assert len(result) == 1


# ─── Variable enthält Fehlermeldung ─────────────────────────────────

class TestFehlerVariableInhalt:
    def test_variable_ist_string(self):
        code = '''VERSUCHE
    x = 10 / 0
FANGE fehler
    ZEIGE typ(fehler)
ENDE VERSUCHE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['str']

    def test_variable_in_bedingung(self):
        """Fehlervariable kann in Bedingungen verwendet werden."""
        code = '''VERSUCHE
    x = 10 / 0
FANGE fehler
    WENN LAENGE(fehler) > 0 DANN
        ZEIGE "Fehler hat Text"
    ENDE WENN
ENDE VERSUCHE'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Fehler hat Text']

    def test_variable_in_string_verkettung(self):
        code = '''VERSUCHE
    x = 10 / 0
FANGE fehler
    ZEIGE "Problem: " + fehler
ENDE VERSUCHE'''
        result = zuse_ausfuehren(code, 'deutsch')
        assert len(result) == 1
        assert result[0].startswith('Problem: ')

    def test_kein_fehler_variable_nicht_definiert(self):
        """Wenn kein Fehler: FANGE-Block wird nicht ausgeführt, Variable existiert nicht."""
        code = '''VERSUCHE
    x = 42
FANGE fehler
    ZEIGE fehler
ENDE VERSUCHE
ZEIGE x'''
        assert zuse_ausfuehren(code, 'deutsch') == ['42']


# ─── Verschachtelte VERSUCHE ────────────────────────────────────────

class TestVerschachtelteVersuche:
    def test_verschachtelt_mit_variablen(self):
        code = '''VERSUCHE
    VERSUCHE
        x = 10 / 0
    FANGE inner
        ZEIGE "Inner: " + inner
    ENDE VERSUCHE
FANGE outer
    ZEIGE "Outer: " + outer
ENDE VERSUCHE'''
        result = zuse_ausfuehren(code, 'deutsch')
        assert len(result) == 1
        assert result[0].startswith('Inner: ')


# ─── Praxisbeispiel: Robuste Eingabevalidierung ─────────────────────

class TestPraxisBeispiel:
    def test_robuste_berechnung(self):
        """Fehler auffangen und Meldung anzeigen."""
        code = '''DEFINIERE sicher_teilen(a, b)
    ergebnis_wert = 0
    VERSUCHE
        ergebnis_wert = a / b
    FANGE fehler
        ergebnis_wert = "Fehler: " + fehler
    ENDE VERSUCHE
    ERGEBNIS ergebnis_wert
ENDE FUNKTION

ZEIGE sicher_teilen(10, 2)
ZEIGE sicher_teilen(10, 0)'''
        result = zuse_ausfuehren(code, 'deutsch')
        assert result[0] == '5.0'
        assert result[1].startswith('Fehler: ')

    def test_robust_division_english(self):
        code = '''DEFINE safe_divide(a, b)
    result_val = 0
    TRY
        result_val = a / b
    CATCH error
        result_val = "Error: " + error
    END TRY
    RESULT result_val
END FUNCTION

SHOW safe_divide(10, 2)
SHOW safe_divide(10, 0)'''
        result = zuse_ausfuehren(code, 'english')
        assert result[0] == '5.0'
        assert result[1].startswith('Error: ')
