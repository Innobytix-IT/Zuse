# FILE: tests/test_ir.py
# Tests für die Intermediate Representation (Phase 3.3)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ast
from ir import (
    ASTtoIR, IRProgram, IRAssign, IRMultiAssign, IRPrint, IRReturn,
    IRIf, IRWhile, IRFor, IRFunction, IRClass, IRMethod, IRImport,
    IRGlobal, IRTry, IRBreak, IRContinue,
    IRNumber, IRString, IRVariable, IRBinaryOp, IRUnaryMinus, IRUnaryNot,
    IRList, IRDict, IRIndex, IRSlice, IRAttribute,
    IRFuncCall, IRMethodCall, IRInput, IRLambda, IRSuper,
)


def to_ir(code, sprache="deutsch"):
    ast = zuse_ast(code, sprache)
    return ASTtoIR().convert(ast)


# ─── Grundlagen ──────────────────────────────────────────────────────────────

class TestIRGrundlagen:
    def test_programm_wrapper(self):
        ir = to_ir("AUSGABE 1")
        assert isinstance(ir, IRProgram)
        assert len(ir.body) == 1

    def test_leeres_programm(self):
        ir = to_ir("")
        assert isinstance(ir, IRProgram)
        assert len(ir.body) == 0


# ─── Anweisungen ─────────────────────────────────────────────────────────────

class TestIRAnweisungen:
    def test_zuweisung(self):
        ir = to_ir("x = 42")
        stmt = ir.body[0]
        assert isinstance(stmt, IRAssign)
        assert isinstance(stmt.target, IRVariable)
        assert stmt.target.name == 'x'
        assert isinstance(stmt.value, IRNumber)
        assert stmt.value.value == '42'

    def test_mehrfach_zuweisung(self):
        ir = to_ir("a, b = 1, 2")
        stmt = ir.body[0]
        assert isinstance(stmt, IRMultiAssign)
        assert len(stmt.targets) == 2
        assert len(stmt.values) == 2
        assert stmt.targets[0].name == 'a'
        assert stmt.targets[1].name == 'b'

    def test_ausgabe(self):
        ir = to_ir('AUSGABE "hallo"')
        stmt = ir.body[0]
        assert isinstance(stmt, IRPrint)
        assert isinstance(stmt.value, IRString)

    def test_ergebnis(self):
        ir = to_ir("DEFINIERE foo()\nERGEBNIS IST 42\nENDE FUNKTION")
        func = ir.body[0]
        assert isinstance(func, IRFunction)
        ret = func.body[0]
        assert isinstance(ret, IRReturn)
        assert isinstance(ret.value, IRNumber)

    def test_import(self):
        ir = to_ir("BENUTZE mathe ALS m")
        stmt = ir.body[0]
        assert isinstance(stmt, IRImport)
        assert stmt.module == 'mathe'
        assert stmt.alias == 'm'

    def test_global(self):
        ir = to_ir("GLOBAL x")
        stmt = ir.body[0]
        assert isinstance(stmt, IRGlobal)
        assert stmt.name == 'x'

    def test_break(self):
        ir = to_ir("SCHLEIFE SOLANGE wahr MACHE\nABBRUCH\nENDE SCHLEIFE")
        loop = ir.body[0]
        assert isinstance(loop.body[0], IRBreak)

    def test_continue(self):
        ir = to_ir("SCHLEIFE SOLANGE wahr MACHE\nWEITER\nENDE SCHLEIFE")
        loop = ir.body[0]
        assert isinstance(loop.body[0], IRContinue)


# ─── Kontrollstrukturen ─────────────────────────────────────────────────────

class TestIRKontrollstrukturen:
    def test_wenn(self):
        ir = to_ir("WENN wahr DANN\nAUSGABE 1\nENDE WENN")
        stmt = ir.body[0]
        assert isinstance(stmt, IRIf)
        assert len(stmt.cases) == 1
        cond, block = stmt.cases[0]
        assert isinstance(cond, IRVariable)
        assert cond.name == 'wahr'
        assert len(block) == 1
        assert stmt.else_body is None

    def test_wenn_sonst(self):
        ir = to_ir("WENN wahr DANN\nAUSGABE 1\nSONST\nAUSGABE 2\nENDE WENN")
        stmt = ir.body[0]
        assert isinstance(stmt, IRIf)
        assert stmt.else_body is not None
        assert len(stmt.else_body) == 1

    def test_while_schleife(self):
        ir = to_ir("SCHLEIFE SOLANGE wahr MACHE\nAUSGABE 1\nENDE SCHLEIFE")
        stmt = ir.body[0]
        assert isinstance(stmt, IRWhile)
        assert isinstance(stmt.condition, IRVariable)
        assert len(stmt.body) == 1

    def test_for_schleife(self):
        ir = to_ir("SCHLEIFE FÜR i IN BEREICH(5) MACHE\nAUSGABE i\nENDE SCHLEIFE")
        stmt = ir.body[0]
        assert isinstance(stmt, IRFor)
        assert stmt.variable == 'i'
        assert isinstance(stmt.iterable, IRFuncCall)
        assert len(stmt.body) == 1

    def test_try_catch(self):
        ir = to_ir("VERSUCHE\nAUSGABE 1\nFANGE\nAUSGABE 0\nENDE VERSUCHE")
        stmt = ir.body[0]
        assert isinstance(stmt, IRTry)
        assert len(stmt.try_body) == 1
        assert len(stmt.catch_body) == 1


# ─── Funktionen und Klassen ─────────────────────────────────────────────────

class TestIRFunktionenKlassen:
    def test_funktion(self):
        ir = to_ir("DEFINIERE addiere(a, b)\nERGEBNIS IST a + b\nENDE FUNKTION")
        func = ir.body[0]
        assert isinstance(func, IRFunction)
        assert func.name == 'addiere'
        assert func.params == ['a', 'b']
        assert len(func.body) == 1

    def test_funktion_mit_default(self):
        ir = to_ir("DEFINIERE gruss(name, laut=falsch)\nAUSGABE name\nENDE FUNKTION")
        func = ir.body[0]
        assert isinstance(func, IRFunction)
        assert 'laut' in func.defaults
        assert isinstance(func.defaults['laut'], IRVariable)

    def test_klasse(self):
        ir = to_ir("KLASSE Hund:\nDEFINIERE bellen()\nAUSGABE 1\nENDE FUNKTION\nENDE KLASSE")
        cls = ir.body[0]
        assert isinstance(cls, IRClass)
        assert cls.name == 'Hund'
        assert cls.parent is None
        assert len(cls.methods) == 1
        assert isinstance(cls.methods[0], IRMethod)
        assert cls.methods[0].name == 'bellen'

    def test_klasse_mit_vererbung(self):
        code = "KLASSE Tier:\nDEFINIERE sag()\nAUSGABE 1\nENDE FUNKTION\nENDE KLASSE\n"
        code += "KLASSE Hund(Tier):\nDEFINIERE bellen()\nAUSGABE 2\nENDE FUNKTION\nENDE KLASSE"
        ir = to_ir(code)
        hund = ir.body[1]
        assert isinstance(hund, IRClass)
        assert hund.parent == 'Tier'


# ─── Ausdrücke ───────────────────────────────────────────────────────────────

class TestIRAusdruecke:
    def test_zahl(self):
        ir = to_ir("AUSGABE 42")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '42'

    def test_float(self):
        ir = to_ir("AUSGABE 3.14")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '3.14'

    def test_string(self):
        ir = to_ir('AUSGABE "hallo"')
        val = ir.body[0].value
        assert isinstance(val, IRString)

    def test_variable(self):
        ir = to_ir("x = 1\nAUSGABE x")
        val = ir.body[1].value
        assert isinstance(val, IRVariable)
        assert val.name == 'x'

    def test_binaer(self):
        ir = to_ir("AUSGABE 1 + 2")
        val = ir.body[0].value
        assert isinstance(val, IRBinaryOp)
        assert val.op == '+'
        assert isinstance(val.left, IRNumber)
        assert isinstance(val.right, IRNumber)

    def test_unaer_minus(self):
        ir = to_ir("AUSGABE -5")
        val = ir.body[0].value
        assert isinstance(val, IRUnaryMinus)
        assert isinstance(val.operand, IRNumber)

    def test_unaer_nicht(self):
        ir = to_ir("AUSGABE NICHT wahr")
        val = ir.body[0].value
        assert isinstance(val, IRUnaryNot)

    def test_liste(self):
        ir = to_ir("AUSGABE [1, 2, 3]")
        val = ir.body[0].value
        assert isinstance(val, IRList)
        assert len(val.elements) == 3

    def test_dict(self):
        ir = to_ir('AUSGABE {"a": 1}')
        val = ir.body[0].value
        assert isinstance(val, IRDict)
        assert len(val.pairs) == 1

    def test_index(self):
        ir = to_ir("x = [1, 2]\nAUSGABE x[0]")
        val = ir.body[1].value
        assert isinstance(val, IRIndex)

    def test_attribut(self):
        ir = to_ir("x = 1\nAUSGABE x.wert")
        val = ir.body[1].value
        assert isinstance(val, IRAttribute)
        assert val.attr == 'wert'

    def test_funktionsaufruf(self):
        ir = to_ir("AUSGABE BEREICH(5)")
        val = ir.body[0].value
        assert isinstance(val, IRFuncCall)
        assert val.name == 'BEREICH'
        assert len(val.args) == 1

    def test_methodenaufruf(self):
        ir = to_ir('x = [1]\nx.hinzufuegen(2)')
        stmt = ir.body[1]
        assert isinstance(stmt, IRMethodCall)
        assert stmt.method == 'hinzufuegen'

    def test_lambda(self):
        ir = to_ir("f = AKTION x: x + 1")
        assign = ir.body[0]
        lam = assign.value
        assert isinstance(lam, IRLambda)
        assert lam.params == ['x']


# ─── Mehrsprachig ───────────────────────────────────────────────────────────

class TestIRMehrsprachig:
    def test_english_produces_same_ir(self):
        ir_de = to_ir("x = 42\nAUSGABE x", sprache="deutsch")
        ir_en = to_ir("x = 42\nPRINT x", sprache="english")
        # Beide sollten die gleiche IR-Struktur erzeugen
        assert len(ir_de.body) == len(ir_en.body)
        assert isinstance(ir_de.body[0], IRAssign)
        assert isinstance(ir_en.body[0], IRAssign)
        assert isinstance(ir_de.body[1], IRPrint)
        assert isinstance(ir_en.body[1], IRPrint)

    def test_french_for_loop(self):
        ir = to_ir("BOUCLE POUR i DANS PORTEE(3) FAIRE\nAFFICHER i\nFIN BOUCLE", sprache="francais")
        stmt = ir.body[0]
        assert isinstance(stmt, IRFor)
        assert stmt.variable == 'i'

    def test_spanish_if(self):
        ir = to_ir("SI verdadero ENTONCES\nIMPRIMIR 1\nFIN SI", sprache="espaniol")
        stmt = ir.body[0]
        assert isinstance(stmt, IRIf)


# ─── Roundtrip: Alle Zuse-Konstrukte konvertierbar ──────────────────────────

class TestIRKomplett:
    def test_komplexes_programm(self):
        code = """x = 10
y = 20
a, b = 1, 2
DEFINIERE addiere(a, b)
    ERGEBNIS IST a + b
ENDE FUNKTION
summe = addiere(x, y)
AUSGABE summe
KLASSE Tier:
    DEFINIERE ERSTELLE(name)
        MEIN.name = name
    ENDE FUNKTION
ENDE KLASSE
SCHLEIFE FÜR i IN BEREICH(5) MACHE
    WENN i == 3 DANN
        ABBRUCH
    ENDE WENN
    AUSGABE i
ENDE SCHLEIFE
VERSUCHE
    AUSGABE 1
FANGE
    AUSGABE 0
ENDE VERSUCHE"""
        ir = to_ir(code)
        assert isinstance(ir, IRProgram)
        # Zähle die Statements: x=, y=, a,b=, DEFINIERE, summe=, AUSGABE, KLASSE, SCHLEIFE, VERSUCHE
        assert len(ir.body) == 9
        assert isinstance(ir.body[0], IRAssign)
        assert isinstance(ir.body[1], IRAssign)
        assert isinstance(ir.body[2], IRMultiAssign)
        assert isinstance(ir.body[3], IRFunction)
        assert isinstance(ir.body[4], IRAssign)
        assert isinstance(ir.body[5], IRPrint)
        assert isinstance(ir.body[6], IRClass)
        assert isinstance(ir.body[7], IRFor)
        assert isinstance(ir.body[8], IRTry)
