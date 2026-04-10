# FILE: tests/test_keyword_aliase.py — Tests für Keyword-Aliase (ROADMAP 7.2 S2)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren


# ─── S2.1: ZEIGE als Alias für AUSGABE ──────────────────────────────

class TestZeige:
    def test_zeige_deutsch(self):
        assert zuse_ausfuehren('ZEIGE "Hallo Welt"', 'deutsch') == ['Hallo Welt']

    def test_ausgabe_bleibt_gueltig(self):
        assert zuse_ausfuehren('AUSGABE "Hallo Welt"', 'deutsch') == ['Hallo Welt']

    def test_zeige_mit_ausdruck(self):
        assert zuse_ausfuehren('ZEIGE 2 + 3', 'deutsch') == ['5']

    def test_zeige_mit_variable(self):
        code = '''x = 42
ZEIGE x'''
        assert zuse_ausfuehren(code, 'deutsch') == ['42']

    def test_show_english(self):
        assert zuse_ausfuehren('SHOW "Hello World"', 'english') == ['Hello World']

    def test_print_bleibt_gueltig_english(self):
        assert zuse_ausfuehren('PRINT "Hello World"', 'english') == ['Hello World']

    def test_mostrar_espaniol(self):
        assert zuse_ausfuehren('MOSTRAR "Hola Mundo"', 'espaniol') == ['Hola Mundo']

    def test_afficher_francais(self):
        assert zuse_ausfuehren('AFFICHER "Bonjour"', 'francais') == ['Bonjour']

    def test_mostra_italiano(self):
        assert zuse_ausfuehren('MOSTRA "Ciao Mondo"', 'italiano') == ['Ciao Mondo']

    def test_mostrar_portugues(self):
        assert zuse_ausfuehren('MOSTRAR "Ola Mundo"', 'portugues') == ['Ola Mundo']


# ─── S2.2: LADE als Alias für BENUTZE ───────────────────────────────

class TestLade:
    def test_lade_modul_deutsch(self):
        code = '''LADE mathe
ZEIGE WURZEL(16)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['4.0']

    def test_benutze_bleibt_gueltig(self):
        code = '''BENUTZE mathe
AUSGABE WURZEL(16)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['4.0']

    def test_load_english(self):
        code = '''LOAD math
SHOW SQRT(16)'''
        assert zuse_ausfuehren(code, 'english') == ['4.0']

    def test_import_bleibt_gueltig_english(self):
        code = '''IMPORT math
PRINT SQRT(16)'''
        assert zuse_ausfuehren(code, 'english') == ['4.0']

    def test_cargar_espaniol(self):
        code = '''CARGAR mate
MOSTRAR RAIZ(16)'''
        assert zuse_ausfuehren(code, 'espaniol') == ['4.0']

    def test_charger_francais(self):
        code = '''CHARGER maths
AFFICHER RACINE(16)'''
        assert zuse_ausfuehren(code, 'francais') == ['4.0']

    def test_carica_italiano(self):
        code = '''CARICA mate
MOSTRA RADICE(16)'''
        assert zuse_ausfuehren(code, 'italiano') == ['4.0']

    def test_carregar_portugues(self):
        code = '''CARREGAR mate
MOSTRAR RAIZ(16)'''
        assert zuse_ausfuehren(code, 'portugues') == ['4.0']


# ─── S2.3: ERGEBNIS als Kurzform für ERGEBNIS IST ───────────────────

class TestErgebnisKurz:
    def test_ergebnis_kurz_deutsch(self):
        code = '''DEFINIERE verdopple(x)
    ERGEBNIS x * 2
ENDE FUNKTION
ZEIGE verdopple(21)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['42']

    def test_ergebnis_ist_bleibt_gueltig(self):
        code = '''DEFINIERE verdopple(x)
    ERGEBNIS IST x * 2
ENDE FUNKTION
AUSGABE verdopple(21)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['42']

    def test_result_english(self):
        code = '''DEFINE double(x)
    RESULT x * 2
END FUNCTION
SHOW double(21)'''
        assert zuse_ausfuehren(code, 'english') == ['42']

    def test_return_bleibt_gueltig_english(self):
        code = '''DEFINE double(x)
    RETURN x * 2
END FUNCTION
PRINT double(21)'''
        assert zuse_ausfuehren(code, 'english') == ['42']

    def test_resultado_espaniol(self):
        code = '''DEFINIR doble(x)
    RESULTADO x * 2
FIN FUNCION
MOSTRAR doble(21)'''
        assert zuse_ausfuehren(code, 'espaniol') == ['42']

    def test_resultat_francais(self):
        code = '''DEFINIR double(x)
    RESULTAT x * 2
FIN FONCTION
AFFICHER double(21)'''
        assert zuse_ausfuehren(code, 'francais') == ['42']

    def test_risultato_italiano(self):
        code = '''DEFINIRE doppio(x)
    RISULTATO x * 2
FINE FUNZIONE
MOSTRA doppio(21)'''
        assert zuse_ausfuehren(code, 'italiano') == ['42']

    def test_resultado_portugues(self):
        code = '''DEFINIR dobro(x)
    RESULTADO x * 2
FIM FUNCAO
MOSTRAR dobro(21)'''
        assert zuse_ausfuehren(code, 'portugues') == ['42']


# ─── S2.4: OBER als Alias für ELTERN ────────────────────────────────

class TestOber:
    def test_ober_deutsch(self):
        code = '''KLASSE Tier
    DEFINIERE ERSTELLE(name)
        MEIN.name = name
    ENDE FUNKTION
    DEFINIERE sprechen()
        ERGEBNIS "..."
    ENDE FUNKTION
ENDE KLASSE

KLASSE Hund(Tier)
    DEFINIERE sprechen()
        ERGEBNIS "Wuff! Ich bin " + MEIN.name
    ENDE FUNKTION
    DEFINIERE vorstellen()
        ERGEBNIS OBER.sprechen() + " aber auch: " + MEIN.sprechen()
    ENDE FUNKTION
ENDE KLASSE

h = Hund("Rex")
ZEIGE h.sprechen()'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Wuff! Ich bin Rex']

    def test_eltern_bleibt_gueltig(self):
        code = '''KLASSE Tier
    DEFINIERE ERSTELLE(name)
        MEIN.name = name
    ENDE FUNKTION
ENDE KLASSE

KLASSE Hund(Tier)
    DEFINIERE ERSTELLE(name, rasse)
        ELTERN.ERSTELLE(name)
        MEIN.rasse = rasse
    ENDE FUNKTION
ENDE KLASSE

h = Hund("Rex", "Schäferhund")
ZEIGE h.name'''
        assert zuse_ausfuehren(code, 'deutsch') == ['Rex']

    def test_parent_english(self):
        code = '''CLASS Animal
    DEFINE NEW(name)
        SELF.name = name
    END FUNCTION
END CLASS

CLASS Dog(Animal)
    DEFINE NEW(name, breed)
        PARENT.NEW(name)
        SELF.breed = breed
    END FUNCTION
END CLASS

d = Dog("Rex", "Shepherd")
SHOW d.name'''
        assert zuse_ausfuehren(code, 'english') == ['Rex']

    def test_super_bleibt_gueltig_english(self):
        code = '''CLASS Animal
    DEFINE NEW(name)
        SELF.name = name
    END FUNCTION
END CLASS

CLASS Dog(Animal)
    DEFINE NEW(name)
        SUPER.NEW(name)
    END FUNCTION
END CLASS

d = Dog("Rex")
PRINT d.name'''
        assert zuse_ausfuehren(code, 'english') == ['Rex']


# ─── Gemischter Test: Alle Aliase zusammen ──────────────────────────

class TestAlleAliaseZusammen:
    def test_komplettes_programm_mit_aliase_deutsch(self):
        code = '''LADE mathe

DEFINIERE berechne_kreis(radius)
    ERGEBNIS PI * POTENZ(radius, 2)
ENDE FUNKTION

ergebnis = RUNDEN(berechne_kreis(5), 2)
ZEIGE ergebnis'''
        assert zuse_ausfuehren(code, 'deutsch') == ['78.54']

    def test_komplettes_programm_mit_aliase_english(self):
        code = '''LOAD math

DEFINE calc_circle(radius)
    RESULT PI * POWER(radius, 2)
END FUNCTION

result = ROUND(calc_circle(5), 2)
SHOW result'''
        assert zuse_ausfuehren(code, 'english') == ['78.54']

    def test_altes_und_neues_gemischt_deutsch(self):
        """Alte und neue Keywords können im selben Programm gemischt werden."""
        code = '''BENUTZE mathe
DEFINIERE f(x)
    ERGEBNIS IST x * 2
ENDE FUNKTION
ZEIGE f(21)'''
        assert zuse_ausfuehren(code, 'deutsch') == ['42']
