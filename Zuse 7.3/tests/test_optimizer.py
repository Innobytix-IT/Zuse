# FILE: tests/test_optimizer.py
# Tests für den IR-Optimizer (Phase 3.4)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conftest import zuse_ast
from ir import (
    ASTtoIR, IRProgram, IRAssign, IRPrint, IRReturn, IRIf, IRWhile,
    IRNumber, IRString, IRVariable, IRBinaryOp, IRUnaryMinus, IRUnaryNot,
    IRBreak, IRContinue, IRFunction,
)
from optimizer import Optimizer


def optimiere(code, sprache="deutsch"):
    """Hilfsfunktion: Zuse-Code → optimierte IR."""
    ast = zuse_ast(code, sprache)
    ir = ASTtoIR().convert(ast)
    opt = Optimizer()
    result = opt.optimize(ir)
    return result, opt.stats


# ─── Konstanten-Faltung ─────────────────────────────────────────────────────

class TestKonstantenFaltung:
    def test_addition(self):
        ir, stats = optimiere("AUSGABE 1 + 2")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '3'
        assert stats['constants_folded'] >= 1

    def test_subtraktion(self):
        ir, stats = optimiere("AUSGABE 10 - 3")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '7'

    def test_multiplikation(self):
        ir, stats = optimiere("AUSGABE 4 * 5")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '20'

    def test_division(self):
        ir, stats = optimiere("AUSGABE 10 / 4")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert float(val.value) == 2.5

    def test_potenz(self):
        ir, stats = optimiere("AUSGABE 2 ^ 3")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '8'

    def test_modulo(self):
        ir, stats = optimiere("AUSGABE 10 % 3")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '1'

    def test_vergleich_gleich(self):
        ir, stats = optimiere("AUSGABE 1 == 1")
        val = ir.body[0].value
        assert isinstance(val, IRVariable)
        assert val.name == 'wahr'

    def test_vergleich_ungleich(self):
        ir, stats = optimiere("AUSGABE 1 != 2")
        val = ir.body[0].value
        assert isinstance(val, IRVariable)
        assert val.name == 'wahr'

    def test_vergleich_falsch(self):
        ir, stats = optimiere("AUSGABE 1 > 2")
        val = ir.body[0].value
        assert isinstance(val, IRVariable)
        assert val.name == 'falsch'

    def test_verschachtelt(self):
        ir, stats = optimiere("AUSGABE 2 + 3 * 4")
        # 3*4=12, dann 2+12=14
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '14'

    def test_string_konkatenation(self):
        ir, stats = optimiere('AUSGABE "hallo" + " welt"')
        val = ir.body[0].value
        assert isinstance(val, IRString)
        assert val.value == '"hallo welt"'

    def test_unaer_minus(self):
        ir, stats = optimiere("AUSGABE -5")
        val = ir.body[0].value
        assert isinstance(val, IRNumber)
        assert val.value == '-5'

    def test_division_durch_null_bleibt(self):
        ir, stats = optimiere("AUSGABE 1 / 0")
        val = ir.body[0].value
        # Division durch 0 wird nicht gefaltet
        assert isinstance(val, IRBinaryOp)

    def test_variable_bleibt(self):
        ir, stats = optimiere("x = 5\nAUSGABE x + 1")
        val = ir.body[1].value
        # x + 1 kann nicht gefaltet werden
        assert isinstance(val, IRBinaryOp)


# ─── Identitäts-Optimierungen ───────────────────────────────────────────────

class TestIdentitaet:
    def test_plus_null_rechts(self):
        ir, stats = optimiere("x = 5\nAUSGABE x + 0")
        val = ir.body[1].value
        assert isinstance(val, IRVariable)
        assert val.name == 'x'

    def test_plus_null_links(self):
        ir, stats = optimiere("x = 5\nAUSGABE 0 + x")
        val = ir.body[1].value
        assert isinstance(val, IRVariable)
        assert val.name == 'x'

    def test_mal_eins_rechts(self):
        ir, stats = optimiere("x = 5\nAUSGABE x * 1")
        val = ir.body[1].value
        assert isinstance(val, IRVariable)
        assert val.name == 'x'

    def test_mal_null(self):
        ir, stats = optimiere("x = 5\nAUSGABE x * 0")
        val = ir.body[1].value
        assert isinstance(val, IRNumber)
        assert val.value == '0'


# ─── Boolean-Vereinfachung ──────────────────────────────────────────────────

class TestBooleanVereinfachung:
    def test_nicht_wahr(self):
        ir, stats = optimiere("AUSGABE NICHT wahr")
        val = ir.body[0].value
        assert isinstance(val, IRVariable)
        assert val.name == 'falsch'

    def test_nicht_falsch(self):
        ir, stats = optimiere("AUSGABE NICHT falsch")
        val = ir.body[0].value
        assert isinstance(val, IRVariable)
        assert val.name == 'wahr'

    def test_doppelte_negation(self):
        ir, stats = optimiere("AUSGABE NICHT NICHT wahr")
        val = ir.body[0].value
        assert isinstance(val, IRVariable)
        assert val.name == 'wahr'
        assert stats['booleans_simplified'] >= 1


# ─── Dead-Code-Elimination ──────────────────────────────────────────────────

class TestDeadCode:
    def test_code_nach_return(self):
        code = "DEFINIERE foo()\nERGEBNIS IST 1\nAUSGABE 2\nENDE FUNKTION"
        ir, stats = optimiere(code)
        func = ir.body[0]
        assert isinstance(func, IRFunction)
        assert len(func.body) == 1  # Nur ERGEBNIS, AUSGABE entfernt
        assert isinstance(func.body[0], IRReturn)
        assert stats['dead_code_removed'] >= 1

    def test_code_nach_break(self):
        code = "SCHLEIFE SOLANGE wahr MACHE\nABBRUCH\nAUSGABE 1\nENDE SCHLEIFE"
        ir, stats = optimiere(code)
        loop = ir.body[0]
        assert len(loop.body) == 1  # Nur ABBRUCH
        assert isinstance(loop.body[0], IRBreak)

    def test_code_nach_continue(self):
        code = "SCHLEIFE SOLANGE wahr MACHE\nWEITER\nAUSGABE 1\nENDE SCHLEIFE"
        ir, stats = optimiere(code)
        loop = ir.body[0]
        assert len(loop.body) == 1
        assert isinstance(loop.body[0], IRContinue)

    def test_code_vor_return_bleibt(self):
        code = "DEFINIERE foo()\nAUSGABE 1\nERGEBNIS IST 2\nENDE FUNKTION"
        ir, stats = optimiere(code)
        func = ir.body[0]
        assert len(func.body) == 2  # AUSGABE + ERGEBNIS

    def test_while_falsch_eliminiert(self):
        code = "SCHLEIFE SOLANGE falsch MACHE\nAUSGABE 1\nENDE SCHLEIFE\nAUSGABE 2"
        ir, stats = optimiere(code)
        # Die while-Schleife sollte eliminiert sein
        assert len(ir.body) == 1
        assert isinstance(ir.body[0], IRPrint)


# ─── Statistiken ─────────────────────────────────────────────────────────────

class TestStatistiken:
    def test_stats_werden_gezaehlt(self):
        code = "AUSGABE 1 + 2\nAUSGABE NICHT wahr"
        ir, stats = optimiere(code)
        assert stats['constants_folded'] >= 1
        assert stats['booleans_simplified'] >= 1

    def test_keine_optimierung_noetig(self):
        code = "x = 5\nAUSGABE x"
        ir, stats = optimiere(code)
        assert stats['constants_folded'] == 0
        assert stats['dead_code_removed'] == 0
        assert stats['booleans_simplified'] == 0


# ─── Kein Seiteneffekt ──────────────────────────────────────────────────────

class TestKeineSeiteneffekte:
    def test_original_ir_unveraendert(self):
        """Optimizer darf die Original-IR nicht verändern."""
        ast = zuse_ast("AUSGABE 1 + 2")
        ir = ASTtoIR().convert(ast)
        original_val = ir.body[0].value
        assert isinstance(original_val, IRBinaryOp)  # Vor Optimierung

        opt = Optimizer()
        opt_ir = opt.optimize(ir)

        # Original unverändert
        assert isinstance(ir.body[0].value, IRBinaryOp)
        # Optimierte Version gefaltet
        assert isinstance(opt_ir.body[0].value, IRNumber)
