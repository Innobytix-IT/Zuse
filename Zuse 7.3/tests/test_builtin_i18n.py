# FILE: tests/test_builtin_i18n.py — Tests für mehrsprachige Builtins (ROADMAP 7.2 S1)
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ausfuehren


# ─── Grundlagen: Builtins in jeder Sprache ──────────────────────────

class TestBuiltinsDeutsch:
    def test_bereich(self):
        assert zuse_ausfuehren('AUSGABE BEREICH(5)', 'deutsch') == ['[0, 1, 2, 3, 4]']

    def test_laenge(self):
        assert zuse_ausfuehren('AUSGABE LAENGE("Hallo")', 'deutsch') == ['5']

    def test_sortieren(self):
        assert zuse_ausfuehren('AUSGABE SORTIEREN([3,1,2])', 'deutsch') == ['[1, 2, 3]']

    def test_wurzel(self):
        assert zuse_ausfuehren('AUSGABE WURZEL(16)', 'deutsch') == ['4.0']

    def test_grossbuchstaben(self):
        assert zuse_ausfuehren('AUSGABE GROSSBUCHSTABEN("hallo")', 'deutsch') == ['HALLO']

    def test_verbinde(self):
        assert zuse_ausfuehren('AUSGABE VERBINDE(["a","b","c"], "-")', 'deutsch') == ['a-b-c']


class TestBuiltinsEnglish:
    def test_range(self):
        assert zuse_ausfuehren('PRINT RANGE(5)', 'english') == ['[0, 1, 2, 3, 4]']

    def test_length(self):
        assert zuse_ausfuehren('PRINT LENGTH("Hello")', 'english') == ['5']

    def test_sort(self):
        assert zuse_ausfuehren('PRINT SORT([3,1,2])', 'english') == ['[1, 2, 3]']

    def test_sqrt(self):
        assert zuse_ausfuehren('PRINT SQRT(16)', 'english') == ['4.0']

    def test_uppercase(self):
        assert zuse_ausfuehren('PRINT UPPERCASE("hello")', 'english') == ['HELLO']

    def test_join(self):
        assert zuse_ausfuehren('PRINT JOIN(["a","b","c"], "-")', 'english') == ['a-b-c']

    def test_contains(self):
        assert zuse_ausfuehren('PRINT CONTAINS("Hello World", "World")', 'english') == ['True']

    def test_replace(self):
        assert zuse_ausfuehren('PRINT REPLACE("Hello", "l", "r")', 'english') == ['Herro']

    def test_min_max(self):
        code = 'PRINT MIN(3, 1, 2)\nPRINT MAX(3, 1, 2)'
        assert zuse_ausfuehren(code, 'english') == ['1', '3']

    def test_abs(self):
        assert zuse_ausfuehren('PRINT ABS(-42)', 'english') == ['42']

    def test_round(self):
        result = zuse_ausfuehren('PRINT ROUND(3.7)', 'english')
        assert float(result[0]) == 4.0

    def test_floor_ceil(self):
        code = 'PRINT FLOOR(3.7)\nPRINT CEIL(3.2)'
        assert zuse_ausfuehren(code, 'english') == ['3', '4']

    def test_power(self):
        assert zuse_ausfuehren('PRINT POWER(2, 10)', 'english') == ['1024']

    def test_sum(self):
        assert zuse_ausfuehren('PRINT SUM([1,2,3,4,5])', 'english') == ['15']

    def test_map(self):
        code = '''DEFINE double(x)
    RETURN x * 2
END FUNCTION
PRINT MAP([1,2,3], double)'''
        assert zuse_ausfuehren(code, 'english') == ['[2, 4, 6]']

    def test_filter(self):
        code = '''DEFINE is_even(x)
    RETURN x % 2 == 0
END FUNCTION
PRINT FILTER([1,2,3,4,5], is_even)'''
        assert zuse_ausfuehren(code, 'english') == ['[2, 4]']

    def test_reverse(self):
        assert zuse_ausfuehren('PRINT REVERSE([1,2,3])', 'english') == ['[3, 2, 1]']

    def test_unique(self):
        assert zuse_ausfuehren('PRINT UNIQUE([1,2,2,3,3])', 'english') == ['[1, 2, 3]']

    def test_split(self):
        assert zuse_ausfuehren('PRINT SPLIT("a-b-c", "-")', 'english') == ["['a', 'b', 'c']"]

    def test_trim(self):
        assert zuse_ausfuehren('PRINT TRIM("  hello  ")', 'english') == ['hello']

    def test_starts_ends_with(self):
        code = 'PRINT STARTS_WITH("Hello", "He")\nPRINT ENDS_WITH("Hello", "lo")'
        assert zuse_ausfuehren(code, 'english') == ['True', 'True']

    def test_find(self):
        assert zuse_ausfuehren('PRINT FIND("Hello", "ll")', 'english') == ['2']

    def test_range_list(self):
        assert zuse_ausfuehren('PRINT RANGE_LIST(5)', 'english') == ['[0, 1, 2, 3, 4]']

    def test_enumerate(self):
        assert zuse_ausfuehren('PRINT ENUMERATE(["a","b"])', 'english') == ['[(0, \'a\'), (1, \'b\')]']


class TestBuiltinsEspaniol:
    def test_rango(self):
        assert zuse_ausfuehren('IMPRIMIR RANGO(5)', 'espaniol') == ['[0, 1, 2, 3, 4]']

    def test_longitud(self):
        assert zuse_ausfuehren('IMPRIMIR LONGITUD("Hola")', 'espaniol') == ['4']

    def test_ordenar(self):
        assert zuse_ausfuehren('IMPRIMIR ORDENAR([3,1,2])', 'espaniol') == ['[1, 2, 3]']

    def test_raiz(self):
        assert zuse_ausfuehren('IMPRIMIR RAIZ(25)', 'espaniol') == ['5.0']

    def test_mayusculas(self):
        assert zuse_ausfuehren('IMPRIMIR MAYUSCULAS("hola")', 'espaniol') == ['HOLA']


class TestBuiltinsFrancais:
    def test_plage(self):
        assert zuse_ausfuehren('IMPRIMER PLAGE(5)', 'francais') == ['[0, 1, 2, 3, 4]']

    def test_longueur(self):
        assert zuse_ausfuehren('IMPRIMER LONGUEUR("Bonjour")', 'francais') == ['7']

    def test_trier(self):
        assert zuse_ausfuehren('IMPRIMER TRIER([3,1,2])', 'francais') == ['[1, 2, 3]']

    def test_racine(self):
        assert zuse_ausfuehren('IMPRIMER RACINE(9)', 'francais') == ['3.0']

    def test_majuscules(self):
        assert zuse_ausfuehren('IMPRIMER MAJUSCULES("bonjour")', 'francais') == ['BONJOUR']


class TestBuiltinsItaliano:
    def test_intervallo(self):
        assert zuse_ausfuehren('STAMPA INTERVALLO(5)', 'italiano') == ['[0, 1, 2, 3, 4]']

    def test_lunghezza(self):
        assert zuse_ausfuehren('STAMPA LUNGHEZZA("Ciao")', 'italiano') == ['4']

    def test_ordinare(self):
        assert zuse_ausfuehren('STAMPA ORDINARE([3,1,2])', 'italiano') == ['[1, 2, 3]']

    def test_radice(self):
        assert zuse_ausfuehren('STAMPA RADICE(4)', 'italiano') == ['2.0']

    def test_maiuscolo(self):
        assert zuse_ausfuehren('STAMPA MAIUSCOLO("ciao")', 'italiano') == ['CIAO']


class TestBuiltinsPortugues:
    def test_intervalo(self):
        assert zuse_ausfuehren('IMPRIMIR INTERVALO(5)', 'portugues') == ['[0, 1, 2, 3, 4]']

    def test_comprimento(self):
        assert zuse_ausfuehren('IMPRIMIR COMPRIMENTO("Ola")', 'portugues') == ['3']

    def test_ordenar(self):
        assert zuse_ausfuehren('IMPRIMIR ORDENAR([3,1,2])', 'portugues') == ['[1, 2, 3]']

    def test_raiz(self):
        assert zuse_ausfuehren('IMPRIMIR RAIZ(49)', 'portugues') == ['7.0']

    def test_maiusculas(self):
        assert zuse_ausfuehren('IMPRIMIR MAIUSCULAS("ola")', 'portugues') == ['OLA']


# ─── Methoden mehrsprachig ──────────────────────────────────────────

class TestMethodenEnglish:
    def test_list_add(self):
        code = '''x = [1, 2, 3]
x.add(4)
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['[1, 2, 3, 4]']

    def test_list_remove(self):
        code = '''x = [1, 2, 3]
x.remove(2)
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['[1, 3]']

    def test_string_upper(self):
        code = '''x = "hello"
PRINT x.upper()'''
        assert zuse_ausfuehren(code, 'english') == ['HELLO']

    def test_string_lower(self):
        code = '''x = "HELLO"
PRINT x.lower()'''
        assert zuse_ausfuehren(code, 'english') == ['hello']

    def test_string_replace(self):
        code = '''x = "Hello World"
PRINT x.replace("World", "Zuse")'''
        assert zuse_ausfuehren(code, 'english') == ['Hello Zuse']

    def test_string_split(self):
        code = '''x = "a-b-c"
PRINT x.split("-")'''
        assert zuse_ausfuehren(code, 'english') == ["['a', 'b', 'c']"]

    def test_string_trim(self):
        code = '''x = "  hello  "
PRINT x.trim()'''
        assert zuse_ausfuehren(code, 'english') == ['hello']

    def test_string_starts_with(self):
        code = '''x = "Hello"
PRINT x.starts_with("He")'''
        assert zuse_ausfuehren(code, 'english') == ['True']

    def test_string_contains(self):
        code = '''x = "Hello World"
PRINT x.contains("World")'''
        assert zuse_ausfuehren(code, 'english') == ['True']

    def test_list_sort(self):
        code = '''x = [3, 1, 2]
x.sort()
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['[1, 2, 3]']

    def test_list_reverse(self):
        code = '''x = [1, 2, 3]
x.reverse()
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['[3, 2, 1]']

    def test_list_clear(self):
        code = '''x = [1, 2, 3]
x.clear()
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['[]']

    def test_list_count(self):
        code = '''x = [1, 2, 2, 3]
PRINT x.count(2)'''
        assert zuse_ausfuehren(code, 'english') == ['2']

    def test_list_copy(self):
        code = '''x = [1, 2, 3]
y = x.copy()
x.add(4)
PRINT y'''
        assert zuse_ausfuehren(code, 'english') == ['[1, 2, 3]']


class TestMethodenEspaniol:
    def test_list_agregar(self):
        code = '''x = [1, 2]
x.agregar(3)
IMPRIMIR x'''
        assert zuse_ausfuehren(code, 'espaniol') == ['[1, 2, 3]']

    def test_string_mayus(self):
        code = '''x = "hola"
IMPRIMIR x.mayus()'''
        assert zuse_ausfuehren(code, 'espaniol') == ['HOLA']


# ─── Rückwärtskompatibilität: Deutsche Builtins funktionieren immer ─

class TestRueckwaertskompatibilitaet:
    def test_deutsche_builtins_in_english(self):
        """Deutsche Builtins müssen auch in englischem Modus funktionieren."""
        assert zuse_ausfuehren('PRINT BEREICH(3)', 'english') == ['[0, 1, 2]']
        assert zuse_ausfuehren('PRINT LAENGE("Hi")', 'english') == ['2']
        assert zuse_ausfuehren('PRINT SORTIEREN([3,1,2])', 'english') == ['[1, 2, 3]']

    def test_deutsche_methoden_in_english(self):
        """Deutsche Methoden müssen auch in englischem Modus funktionieren."""
        code = '''x = [1, 2]
x.hinzufuegen(3)
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['[1, 2, 3]']


# ─── Komplexe Programme in verschiedenen Sprachen ───────────────────

class TestKomplexeProgramme:
    def test_fibonacci_deutsch(self):
        code = '''DEFINIERE fib(n)
    WENN n <= 1 DANN
        ERGEBNIS IST n
    ENDE WENN
    ERGEBNIS IST fib(n - 1) + fib(n - 2)
ENDE FUNKTION

AUSGABE VERBINDE(UMWANDELN(BEREICH(8), fib), ", ")'''
        assert zuse_ausfuehren(code, 'deutsch') == ['0, 1, 1, 2, 3, 5, 8, 13']

    def test_fibonacci_english(self):
        code = '''DEFINE fib(n)
    IF n <= 1 THEN
        RETURN n
    END IF
    RETURN fib(n - 1) + fib(n - 2)
END FUNCTION

PRINT JOIN(MAP(RANGE(8), fib), ", ")'''
        assert zuse_ausfuehren(code, 'english') == ['0, 1, 1, 2, 3, 5, 8, 13']

    def test_fibonacci_espaniol(self):
        code = '''DEFINIR fib(n)
    SI n <= 1 ENTONCES
        RETORNO n
    FIN SI
    RETORNO fib(n - 1) + fib(n - 2)
FIN FUNCION

IMPRIMIR UNIR(MAPEAR(RANGO(8), fib), ", ")'''
        assert zuse_ausfuehren(code, 'espaniol') == ['0, 1, 1, 2, 3, 5, 8, 13']

    def test_fibonacci_francais(self):
        code = '''DEFINIR fib(n)
    SI n <= 1 ALORS
        RETOURNER n
    FIN SI
    RETOURNER fib(n - 1) + fib(n - 2)
FIN FONCTION

IMPRIMER JOINDRE(TRANSFORMER(PLAGE(8), fib), ", ")'''
        assert zuse_ausfuehren(code, 'francais') == ['0, 1, 1, 2, 3, 5, 8, 13']

    def test_fibonacci_italiano(self):
        code = '''DEFINIRE fib(n)
    SE n <= 1 ALLORA
        RITORNA n
    FINE SE
    RITORNA fib(n - 1) + fib(n - 2)
FINE FUNZIONE

STAMPA UNIRE(MAPPARE(INTERVALLO(8), fib), ", ")'''
        assert zuse_ausfuehren(code, 'italiano') == ['0, 1, 1, 2, 3, 5, 8, 13']

    def test_fibonacci_portugues(self):
        code = '''DEFINIR fib(n)
    SE n <= 1 ENTAO
        RETORNO n
    FIM SE
    RETORNO fib(n - 1) + fib(n - 2)
FIM FUNCAO

IMPRIMIR JUNTAR(MAPEAR(INTERVALO(8), fib), ", ")'''
        assert zuse_ausfuehren(code, 'portugues') == ['0, 1, 1, 2, 3, 5, 8, 13']


# ─── Mathe-Builtins in English ──────────────────────────────────────

class TestMatheEnglish:
    def test_sin_cos_tan(self):
        code = '''PRINT ROUND(SIN(0), 2)
PRINT ROUND(COS(0), 2)
PRINT ROUND(TAN(0), 2)'''
        result = zuse_ausfuehren(code, 'english')
        assert float(result[0]) == 0.0
        assert float(result[1]) == 1.0
        assert float(result[2]) == 0.0

    def test_log(self):
        code = 'PRINT ROUND(LOG(E), 2)'
        assert zuse_ausfuehren(code, 'english') == ['1.0']

    def test_random_range(self):
        code = '''x = RANDOM_RANGE(1, 1)
PRINT x'''
        assert zuse_ausfuehren(code, 'english') == ['1']
