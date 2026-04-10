# FILE: tests/test_transpiler.py — Transpiler-Tests für alle 4 Backends
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from transpiler import transpile

# ─── Helper ────────────────────────────────────────────────────

ALLE_BACKENDS = ["python", "javascript", "java", "csharp"]

def transpiliere(code, backend="python", sprache="deutsch"):
    """Transpiliert Zuse-Code und gibt den generierten Code zurück."""
    result = transpile(code, source_lang=sprache, target_backend=backend, include_stdlib=False)
    return result["code"]

def python_code(code, sprache="deutsch"):
    return transpiliere(code, "python", sprache)

def js_code(code, sprache="deutsch"):
    return transpiliere(code, "javascript", sprache)

def java_code(code, sprache="deutsch"):
    return transpiliere(code, "java", sprache)

def csharp_code(code, sprache="deutsch"):
    return transpiliere(code, "csharp", sprache)


# ─── 1. Grundlegende Transpiler-Funktion ───────────────────────

class TestTranspilerBasis:

    def test_ergebnis_hat_code(self):
        result = transpile('AUSGABE "Hallo"', target_backend="python", include_stdlib=False)
        assert "code" in result
        assert len(result["code"]) > 0

    def test_ergebnis_hat_backend(self):
        result = transpile('AUSGABE "Hallo"', target_backend="python", include_stdlib=False)
        assert result["backend"] == "Python 3"

    def test_ergebnis_hat_extension(self):
        result = transpile('AUSGABE "Hallo"', target_backend="python", include_stdlib=False)
        assert result["extension"] == ".py"

    def test_ergebnis_hat_warnings_liste(self):
        result = transpile('AUSGABE "Hallo"', target_backend="python", include_stdlib=False)
        assert isinstance(result["warnings"], list)

    def test_unbekanntes_backend_fehler(self):
        with pytest.raises(ValueError, match="Unbekanntes Backend"):
            transpile('AUSGABE "Hallo"', target_backend="ruby", include_stdlib=False)

    @pytest.mark.parametrize("backend,ext", [
        ("python", ".py"),
        ("javascript", ".js"),
        ("java", ".java"),
        ("csharp", ".cs"),
    ])
    def test_dateiendungen(self, backend, ext):
        result = transpile('AUSGABE "Hallo"', target_backend=backend, include_stdlib=False)
        assert result["extension"] == ext

    @pytest.mark.parametrize("backend", ALLE_BACKENDS)
    def test_leerer_code(self, backend):
        """Leerer Code erzeugt trotzdem validen Output (Header etc.)."""
        result = transpile("", target_backend=backend, include_stdlib=False)
        assert isinstance(result["code"], str)


# ─── 2. Python-Backend ────────────────────────────────────────

class TestPythonBackend:

    def test_ausgabe(self):
        code = python_code('AUSGABE "Hallo Welt"')
        assert 'print("Hallo Welt")' in code

    def test_variable(self):
        code = python_code('name = "Manuel"')
        assert 'name = "Manuel"' in code

    def test_zahl(self):
        code = python_code("x = 42")
        assert "x = 42" in code

    def test_wenn_dann(self):
        code = python_code("WENN x > 5 DANN\n    AUSGABE x\nENDE WENN")
        assert "if (x > 5):" in code

    def test_sonst(self):
        code = python_code("WENN x > 5 DANN\n    AUSGABE x\nSONST\n    AUSGABE 0\nENDE WENN")
        assert "else:" in code

    def test_schleife_fuer(self):
        code = python_code("SCHLEIFE FÜR i IN [1, 2, 3] MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert "for i in [1, 2, 3]:" in code

    def test_schleife_solange(self):
        code = python_code("SCHLEIFE SOLANGE x < 10 MACHE\n    x = x + 1\nENDE SCHLEIFE")
        assert "while (x < 10):" in code

    def test_funktion(self):
        code = python_code("DEFINIERE hallo(name):\n    AUSGABE name\nENDE FUNKTION")
        assert "def hallo(name):" in code

    def test_ergebnis_ist_return(self):
        code = python_code("DEFINIERE doppelt(x):\n    ERGEBNIS IST x * 2\nENDE FUNKTION")
        assert "return (x * 2)" in code

    def test_klasse(self):
        code = python_code("KLASSE Hund:\n    DEFINIERE ERSTELLE(name):\n        MEIN.name = name\n    ENDE FUNKTION\nENDE KLASSE")
        assert "class Hund:" in code
        assert "def __init__(self, name):" in code
        assert "self.name = name" in code

    def test_vererbung(self):
        code = python_code("KLASSE Dackel(Hund):\n    DEFINIERE bellen():\n        AUSGABE MEIN.name\n    ENDE FUNKTION\nENDE KLASSE")
        assert "class Dackel(Hund):" in code

    def test_potenz(self):
        code = python_code("AUSGABE 2 ^ 3")
        assert "**" in code

    def test_boolean_wahr(self):
        code = python_code("x = wahr")
        assert "True" in code

    def test_boolean_falsch(self):
        code = python_code("x = falsch")
        assert "False" in code

    def test_selbst_wird_self(self):
        code = python_code("KLASSE A:\n    DEFINIERE test():\n        MEIN.x = 1\n    ENDE FUNKTION\nENDE KLASSE")
        assert "self.x = 1" in code

    def test_versuche_fange(self):
        code = python_code("VERSUCHE\n    x = 1\nFANGE\n    AUSGABE 0\nENDE VERSUCHE")
        assert "try:" in code
        assert "except Exception as _e:" in code

    def test_import(self):
        code = python_code("BENUTZE math ALS m")
        assert "import math as m" in code

    def test_lambda(self):
        code = python_code("f = AKTION x: x * 2")
        assert "lambda x: (x * 2)" in code

    def test_liste(self):
        code = python_code("x = [1, 2, 3]")
        assert "[1, 2, 3]" in code

    def test_dict(self):
        code = python_code('d = {"a": 1}')
        assert '"a": 1' in code

    def test_index_zugriff(self):
        code = python_code("AUSGABE x[0]")
        assert "x[0]" in code

    def test_slicing(self):
        code = python_code("AUSGABE x[1:3]")
        assert "x[1:3]" in code

    def test_global(self):
        code = python_code("DEFINIERE test():\n    GLOBAL zaehler\n    zaehler = 1\nENDE FUNKTION")
        assert "global zaehler" in code

    def test_eingabe_text(self):
        code = python_code('name = EINGABE_TEXT("Name?")')
        assert "input(" in code

    def test_eingabe_zahl(self):
        code = python_code('alter = EINGABE_ZAHL("Alter?")')
        assert "float(input(" in code

    def test_methoden_aufruf(self):
        code = python_code("pablo.gehe(100)")
        assert "pablo.gehe(100)" in code

    def test_header(self):
        code = python_code("")
        assert "Generiert von Zuse Transpiler" in code


# ─── 3. JavaScript-Backend ────────────────────────────────────

class TestJavaScriptBackend:

    def test_ausgabe(self):
        code = js_code('AUSGABE "Hallo"')
        assert 'console.log("Hallo");' in code

    def test_variable_let(self):
        code = js_code('name = "Manuel"')
        assert 'let name = "Manuel";' in code

    def test_use_strict(self):
        code = js_code("")
        assert '"use strict";' in code

    def test_wenn_curly_braces(self):
        code = js_code("WENN x > 5 DANN\n    AUSGABE x\nENDE WENN")
        assert "if (" in code
        assert "{" in code
        assert "}" in code

    def test_sonst(self):
        code = js_code("WENN x > 5 DANN\n    AUSGABE x\nSONST\n    AUSGABE 0\nENDE WENN")
        assert "} else {" in code

    def test_schleife_fuer_of(self):
        code = js_code("SCHLEIFE FÜR i IN liste MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert "for (const i of liste)" in code

    def test_funktion(self):
        code = js_code("DEFINIERE hallo(name):\n    AUSGABE name\nENDE FUNKTION")
        assert "function hallo(name) {" in code

    def test_klasse_constructor(self):
        code = js_code("KLASSE Hund:\n    DEFINIERE ERSTELLE(name):\n        MEIN.name = name\n    ENDE FUNKTION\nENDE KLASSE")
        assert "class Hund" in code
        assert "constructor(name)" in code
        assert "this.name = name" in code

    def test_vererbung_extends(self):
        code = js_code("KLASSE Dackel(Hund):\n    DEFINIERE bellen():\n        AUSGABE MEIN.name\n    ENDE FUNKTION\nENDE KLASSE")
        assert "extends Hund" in code

    def test_potenz_math_pow(self):
        code = js_code("AUSGABE 2 ^ 3")
        assert "Math.pow(2, 3)" in code

    def test_gleichheit_strict(self):
        code = js_code("AUSGABE x == 5")
        assert "===" in code

    def test_ungleichheit_strict(self):
        code = js_code("AUSGABE x != 5")
        assert "!==" in code

    def test_boolean_true(self):
        code = js_code("x = wahr")
        assert "true" in code

    def test_boolean_false(self):
        code = js_code("x = falsch")
        assert "false" in code

    def test_self_wird_this(self):
        code = js_code("KLASSE A:\n    DEFINIERE test():\n        MEIN.x = 1\n    ENDE FUNKTION\nENDE KLASSE")
        assert "this.x = 1" in code

    def test_len_wird_length(self):
        code = js_code("AUSGABE len(x)")
        assert ".length" in code

    def test_lambda_arrow(self):
        code = js_code("f = AKTION x: x * 2")
        assert "=>" in code

    def test_slice_methode(self):
        code = js_code("AUSGABE x[1:3]")
        assert ".slice(1, 3)" in code

    def test_try_catch(self):
        code = js_code("VERSUCHE\n    x = 1\nFANGE\n    AUSGABE 0\nENDE VERSUCHE")
        assert "try {" in code
        assert "} catch (_e) {" in code

    def test_eingabe_prompt(self):
        code = js_code('name = EINGABE_TEXT("Name?")')
        assert "prompt(" in code

    def test_eingabe_zahl_parseFloat(self):
        code = js_code('x = EINGABE_ZAHL("Zahl?")')
        assert "parseFloat(prompt(" in code

    def test_return_mit_semikolon(self):
        code = js_code("DEFINIERE doppelt(x):\n    ERGEBNIS IST x * 2\nENDE FUNKTION")
        assert "return (x * 2);" in code


# ─── 4. Java-Backend ──────────────────────────────────────────

class TestJavaBackend:

    def test_wrapper_klasse(self):
        code = java_code('AUSGABE "Hallo"')
        assert "public class ZuseProgramm" in code

    def test_main_methode(self):
        code = java_code('AUSGABE "Hallo"')
        assert "public static void main(String[] args)" in code

    def test_ausgabe_println(self):
        code = java_code('AUSGABE "Hallo"')
        assert 'System.out.println("Hallo")' in code

    def test_import_java_util(self):
        code = java_code("")
        assert "import java.util.*;" in code

    def test_variable_object(self):
        code = java_code("x = 42")
        assert "Object x = 42;" in code

    def test_liste_arraylist(self):
        code = java_code("x = [1, 2, 3]")
        assert "ArrayList" in code

    def test_dict_hashmap(self):
        code = java_code('d = {"a": 1}')
        assert "HashMap" in code

    def test_addition_helper(self):
        code = java_code("AUSGABE x + y")
        assert "_add(x, y)" in code

    def test_subtraktion_helper(self):
        code = java_code("AUSGABE x - y")
        assert "_sub(x, y)" in code

    def test_multiplikation_helper(self):
        code = java_code("AUSGABE x * y")
        assert "_mul(x, y)" in code

    def test_division_helper(self):
        code = java_code("AUSGABE x / y")
        assert "_div(x, y)" in code

    def test_potenz_helper(self):
        code = java_code("AUSGABE x ^ y")
        assert "_pow(x, y)" in code

    def test_modulo_helper(self):
        code = java_code("AUSGABE x % y")
        assert "_mod(x, y)" in code

    def test_gleichheit_objects_equals(self):
        code = java_code("AUSGABE x == y")
        assert "Objects.equals(x, y)" in code

    def test_boolean_true(self):
        code = java_code("x = wahr")
        assert "true" in code

    def test_boolean_false(self):
        code = java_code("x = falsch")
        assert "false" in code

    def test_funktion_static(self):
        code = java_code("DEFINIERE hallo(name):\n    AUSGABE name\nENDE FUNKTION")
        assert "static Object hallo(Object name)" in code

    def test_klasse_static_inner(self):
        code = java_code("KLASSE Hund:\n    DEFINIERE bellen():\n        AUSGABE 1\n    ENDE FUNKTION\nENDE KLASSE")
        assert "static class Hund" in code

    def test_fuer_schleife_iterable(self):
        code = java_code("SCHLEIFE FÜR i IN liste MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert "for (Object i : (Iterable<?>)liste)" in code

    def test_if_truthy(self):
        code = java_code("WENN x > 5 DANN\n    AUSGABE x\nENDE WENN")
        assert "_truthy(" in code

    def test_try_catch_exception(self):
        code = java_code("VERSUCHE\n    x = 1\nFANGE\n    AUSGABE 0\nENDE VERSUCHE")
        assert "try {" in code
        assert "} catch (Exception _e) {" in code

    def test_scanner_fuer_eingabe(self):
        code = java_code("")
        assert "Scanner" in code

    def test_typ_helper_methoden(self):
        """Java braucht Hilfsmethoden für dynamische Typen."""
        code = java_code("")
        assert "static Object _add(Object a, Object b)" in code
        assert "_truthy" in code

    def test_self_wird_this(self):
        code = java_code("KLASSE A:\n    DEFINIERE test():\n        MEIN.x = 1\n    ENDE FUNKTION\nENDE KLASSE")
        assert "this.x = 1" in code


# ─── 5. C#-Backend ────────────────────────────────────────────

class TestCSharpBackend:

    def test_namespace(self):
        code = csharp_code("")
        assert "namespace ZuseProgramm" in code

    def test_using_system(self):
        code = csharp_code("")
        assert "using System;" in code

    def test_class_program(self):
        code = csharp_code("")
        assert "class Program" in code

    def test_main_methode(self):
        code = csharp_code("")
        assert "static void Main(string[] args)" in code

    def test_ausgabe_writeline(self):
        code = csharp_code('AUSGABE "Hallo"')
        assert 'Console.WriteLine("Hallo")' in code

    def test_variable_dynamic(self):
        code = csharp_code("x = 42")
        assert "dynamic x = 42;" in code

    def test_liste_generic(self):
        code = csharp_code("x = [1, 2, 3]")
        assert "List<dynamic>" in code

    def test_dict_generic(self):
        code = csharp_code('d = {"a": 1}')
        assert "Dictionary<dynamic, dynamic>" in code

    def test_potenz_math_pow(self):
        code = csharp_code("AUSGABE 2 ^ 3")
        assert "Math.Pow(" in code

    def test_gleichheit_equals(self):
        code = csharp_code("AUSGABE x == y")
        assert "Equals(x, y)" in code

    def test_boolean_true(self):
        code = csharp_code("x = wahr")
        assert "true" in code

    def test_boolean_false(self):
        code = csharp_code("x = falsch")
        assert "false" in code

    def test_self_wird_this(self):
        code = csharp_code("KLASSE A:\n    DEFINIERE test():\n        MEIN.x = 1\n    ENDE FUNKTION\nENDE KLASSE")
        assert "this.x = 1" in code

    def test_super_wird_base(self):
        code = csharp_code("KLASSE Kind(Basis):\n    DEFINIERE test():\n        ELTERN.test()\n    ENDE FUNKTION\nENDE KLASSE")
        assert "base" in code

    def test_vererbung_doppelpunkt(self):
        code = csharp_code("KLASSE Dackel(Hund):\n    DEFINIERE bellen():\n        AUSGABE 1\n    ENDE FUNKTION\nENDE KLASSE")
        assert ": Hund" in code

    def test_konstruktor_klassenname(self):
        code = csharp_code("KLASSE Hund:\n    DEFINIERE ERSTELLE(name):\n        MEIN.name = name\n    ENDE FUNKTION\nENDE KLASSE")
        assert "public Hund(dynamic name)" in code

    def test_funktion_static_dynamic(self):
        code = csharp_code("DEFINIERE hallo(name):\n    AUSGABE name\nENDE FUNKTION")
        assert "static dynamic hallo(dynamic name)" in code

    def test_foreach(self):
        code = csharp_code("SCHLEIFE FÜR i IN liste MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert "foreach (dynamic i in liste)" in code

    def test_while(self):
        code = csharp_code("SCHLEIFE SOLANGE x < 10 MACHE\n    x = x + 1\nENDE SCHLEIFE")
        assert "while ((x < 10))" in code

    def test_try_catch(self):
        code = csharp_code("VERSUCHE\n    x = 1\nFANGE\n    AUSGABE 0\nENDE VERSUCHE")
        assert "try" in code
        assert "catch (Exception _e)" in code

    def test_lambda_syntax(self):
        code = csharp_code("f = AKTION x: x * 2")
        assert "=>" in code

    def test_slice_getrange(self):
        code = csharp_code("AUSGABE x[1:3]")
        assert "GetRange(" in code


# ─── 6. Cross-Backend: Gleicher Zuse-Code, alle Backends ──────

class TestCrossBackend:
    """Sicherstellen, dass jedes Backend für denselben Input kompiliert."""

    TESTPROGRAMME = [
        ('AUSGABE "Hallo Welt"', "Ausgabe"),
        ("x = 42", "Variable"),
        ("WENN x > 5 DANN\n    AUSGABE x\nENDE WENN", "Bedingung"),
        ("SCHLEIFE FÜR i IN [1, 2, 3] MACHE\n    AUSGABE i\nENDE SCHLEIFE", "For-Schleife"),
        ("SCHLEIFE SOLANGE x < 10 MACHE\n    x = x + 1\nENDE SCHLEIFE", "While-Schleife"),
        ("DEFINIERE hallo():\n    AUSGABE 1\nENDE FUNKTION", "Funktion"),
        ("KLASSE Hund:\n    DEFINIERE ERSTELLE(name):\n        MEIN.name = name\n    ENDE FUNKTION\nENDE KLASSE", "Klasse"),
        ("VERSUCHE\n    x = 1\nFANGE\n    AUSGABE 0\nENDE VERSUCHE", "Try-Catch"),
        ("f = AKTION x: x * 2", "Lambda"),
        ("x = [1, 2, 3]", "Liste"),
    ]

    @pytest.mark.parametrize("backend", ALLE_BACKENDS)
    @pytest.mark.parametrize("code,name", TESTPROGRAMME, ids=[t[1] for t in TESTPROGRAMME])
    def test_transpiliert_ohne_fehler(self, code, name, backend):
        """Jedes Backend muss für jedes Testprogramm Code erzeugen können."""
        result = transpile(code, target_backend=backend, include_stdlib=False)
        assert isinstance(result["code"], str)
        assert len(result["code"]) > 0


# ─── 7. Python-Backend: Ausführbarkeitstests ──────────────────

class TestPythonAusfuehrbar:
    """Der generierte Python-Code muss tatsächlich ausführbar sein."""

    def _exec_python(self, zuse_code):
        """Transpiliert und führt den Python-Code aus, gibt Ausgaben zurück."""
        py_code = python_code(zuse_code)
        ausgaben = []
        # Eigenes print einsetzen zum Capturen
        exec_globals = {"print": lambda *a, **kw: ausgaben.append(" ".join(str(x) for x in a))}
        exec(py_code, exec_globals)
        return ausgaben

    def test_hallo_welt(self):
        out = self._exec_python('AUSGABE "Hallo Welt"')
        assert out == ["Hallo Welt"]

    def test_rechnung(self):
        out = self._exec_python("AUSGABE 2 + 3")
        assert out == ["5"]

    def test_variable_und_ausgabe(self):
        out = self._exec_python('name = "Zuse"\nAUSGABE name')
        assert out == ["Zuse"]

    def test_wenn_dann(self):
        out = self._exec_python("x = 10\nWENN x > 5 DANN\n    AUSGABE x\nENDE WENN")
        assert out == ["10"]

    def test_schleife(self):
        out = self._exec_python("SCHLEIFE FÜR i IN [1, 2, 3] MACHE\n    AUSGABE i\nENDE SCHLEIFE")
        assert out == ["1", "2", "3"]

    def test_funktion(self):
        out = self._exec_python("DEFINIERE doppelt(x):\n    return (x * 2)\nENDE FUNKTION\nAUSGABE doppelt(21)")
        # Note: The transpiler generates "return (x * 2)" which works
        assert out == ["42"]

    def test_potenz(self):
        out = self._exec_python("AUSGABE 2 ^ 3")
        assert out == ["8"]

    def test_boolean(self):
        out = self._exec_python("x = wahr\nAUSGABE x")
        assert out == ["True"]

    def test_liste_zugriff(self):
        out = self._exec_python("x = [10, 20, 30]\nAUSGABE x[1]")
        assert out == ["20"]
