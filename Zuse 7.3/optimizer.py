# FILE: optimizer.py
# Optimierungen auf der IR-Ebene.
# - Konstanten-Faltung (Constant Folding): 1 + 2 → 3
# - Dead-Code-Elimination: Code nach return/break entfernen
# - Boolean-Vereinfachung: NICHT NICHT x → x

from ir import (
    IRProgram, IRAssign, IRMultiAssign, IRPrint, IRReturn,
    IRIf, IRWhile, IRFor, IRFunction, IRClass, IRMethod,
    IRImport, IRGlobal, IRTry, IRBreak, IRContinue,
    IRNumber, IRString, IRVariable, IRBinaryOp, IRUnaryMinus, IRUnaryNot,
    IRList, IRDict, IRIndex, IRSlice, IRAttribute,
    IRFuncCall, IRMethodCall, IRInput, IRLambda, IRSuper,
)

# Operatoren für Konstanten-Faltung
_FOLD_OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else None,
    '%': lambda a, b: a % b if b != 0 else None,
    '^': lambda a, b: a ** b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
}


def _parse_number(val_str):
    """Parst einen Zahlen-String zu int oder float."""
    if '.' in val_str:
        return float(val_str)
    return int(val_str)


def _number_to_ir(val):
    """Konvertiert eine Python-Zahl zurück zu IRNumber."""
    if isinstance(val, bool):
        return IRVariable(name='wahr' if val else 'falsch')
    if isinstance(val, float):
        if val == int(val) and not ('.' in str(val)):
            return IRNumber(value=str(int(val)))
        return IRNumber(value=str(val))
    return IRNumber(value=str(val))


def _is_terminator(stmt):
    """Prüft ob ein Statement den Kontrollfluss beendet."""
    return isinstance(stmt, (IRReturn, IRBreak, IRContinue))


class Optimizer:
    """Optimiert die IR durch verschiedene Transformationen."""

    def __init__(self):
        self.stats = {
            'constants_folded': 0,
            'dead_code_removed': 0,
            'booleans_simplified': 0,
        }

    def optimize(self, ir_program):
        """Hauptmethode: Optimiert ein IRProgram."""
        self.stats = {'constants_folded': 0, 'dead_code_removed': 0, 'booleans_simplified': 0}
        optimized_body = self._opt_block(ir_program.body)
        return IRProgram(optimized_body, ir_program.line)

    # ─── Block-Optimierung ───────────────────────────────────────────────

    def _opt_block(self, stmts):
        """Optimiert einen Block und entfernt Dead Code."""
        result = []
        for stmt in stmts:
            opt_stmt = self._opt_stmt(stmt)
            if opt_stmt is not None:
                result.append(opt_stmt)
                if _is_terminator(opt_stmt):
                    # Alles nach return/break/continue ist Dead Code
                    removed = len(stmts) - len(result)
                    if removed > 0:
                        self.stats['dead_code_removed'] += removed
                    break
        return result

    # ─── Statement-Optimierung ───────────────────────────────────────────

    def _opt_stmt(self, stmt):
        if isinstance(stmt, IRAssign):
            return IRAssign(self._opt_expr(stmt.target), self._opt_expr(stmt.value), stmt.line)

        if isinstance(stmt, IRMultiAssign):
            return IRMultiAssign(
                [self._opt_expr(t) for t in stmt.targets],
                [self._opt_expr(v) for v in stmt.values],
                stmt.line
            )

        if isinstance(stmt, IRPrint):
            return IRPrint(self._opt_expr(stmt.value), stmt.line)

        if isinstance(stmt, IRReturn):
            return IRReturn(self._opt_expr(stmt.value), stmt.line)

        if isinstance(stmt, IRIf):
            return self._opt_if(stmt)

        if isinstance(stmt, IRWhile):
            cond = self._opt_expr(stmt.condition)
            # while falsch → entfernen
            if isinstance(cond, IRVariable) and cond.name == 'falsch':
                self.stats['dead_code_removed'] += 1
                return None
            return IRWhile(cond, self._opt_block(stmt.body), stmt.line)

        if isinstance(stmt, IRFor):
            return IRFor(stmt.variable, self._opt_expr(stmt.iterable),
                         self._opt_block(stmt.body), stmt.line)

        if isinstance(stmt, IRFunction):
            defaults = {k: self._opt_expr(v) for k, v in stmt.defaults.items()}
            return IRFunction(stmt.name, stmt.params, self._opt_block(stmt.body),
                              defaults, stmt.line)

        if isinstance(stmt, IRClass):
            methods = []
            for m in stmt.methods:
                methods.append(IRMethod(m.name, m.params, self._opt_block(m.body), m.line))
            return IRClass(stmt.name, stmt.parent, methods, stmt.line)

        if isinstance(stmt, IRTry):
            return IRTry(self._opt_block(stmt.try_body),
                         self._opt_block(stmt.catch_body), stmt.line)

        if isinstance(stmt, (IRBreak, IRContinue, IRImport, IRGlobal)):
            return stmt

        # Ausdrucks-Statements (Funktionsaufrufe etc.)
        if isinstance(stmt, (IRFuncCall, IRMethodCall)):
            return self._opt_expr(stmt)

        return stmt

    def _opt_if(self, stmt):
        """Optimiert if-Anweisungen: eliminiert Branches mit konstanter Bedingung."""
        cases = []
        for cond, block in stmt.cases:
            opt_cond = self._opt_expr(cond)
            opt_block = self._opt_block(block)

            # Konstante Bedingung: wahr → immer ausführen, Rest ignorieren
            if isinstance(opt_cond, IRVariable) and opt_cond.name == 'wahr':
                self.stats['dead_code_removed'] += 1
                # Dieser Branch wird immer genommen
                if not cases:
                    # Erster Branch ist immer wahr → kein if nötig, aber wir
                    # geben trotzdem IRIf zurück für Konsistenz
                    return IRIf([(opt_cond, opt_block)], None, stmt.line)
                cases.append((opt_cond, opt_block))
                break

            # Konstante Bedingung: falsch → Branch überspringen
            if isinstance(opt_cond, IRVariable) and opt_cond.name == 'falsch':
                self.stats['dead_code_removed'] += 1
                continue

            cases.append((opt_cond, opt_block))

        else_body = self._opt_block(stmt.else_body) if stmt.else_body else None

        # Wenn keine Cases übrig: else-Body oder nichts
        if not cases:
            if else_body:
                # Alle Bedingungen waren falsch → nur else ausführen
                return IRIf([(IRVariable('wahr'), else_body)], None, stmt.line)
            return None

        return IRIf(cases, else_body, stmt.line)

    # ─── Ausdruck-Optimierung ────────────────────────────────────────────

    def _opt_expr(self, expr):
        if expr is None:
            return None

        if isinstance(expr, (IRNumber, IRString, IRVariable, IRSuper)):
            return expr

        if isinstance(expr, IRBinaryOp):
            return self._opt_binary(expr)

        if isinstance(expr, IRUnaryMinus):
            operand = self._opt_expr(expr.operand)
            # -ZAHL → direkte Negation
            if isinstance(operand, IRNumber):
                val = _parse_number(operand.value)
                self.stats['constants_folded'] += 1
                return _number_to_ir(-val)
            return IRUnaryMinus(operand, expr.line)

        if isinstance(expr, IRUnaryNot):
            return self._opt_not(expr)

        if isinstance(expr, IRList):
            return IRList([self._opt_expr(e) for e in expr.elements], expr.line)

        if isinstance(expr, IRDict):
            return IRDict([(self._opt_expr(k), self._opt_expr(v)) for k, v in expr.pairs], expr.line)

        if isinstance(expr, IRIndex):
            return IRIndex(self._opt_expr(expr.obj), self._opt_expr(expr.index), expr.line)

        if isinstance(expr, IRSlice):
            return IRSlice(self._opt_expr(expr.obj),
                           self._opt_expr(expr.start), self._opt_expr(expr.end), expr.line)

        if isinstance(expr, IRAttribute):
            return IRAttribute(self._opt_expr(expr.obj), expr.attr, expr.line)

        if isinstance(expr, IRFuncCall):
            return IRFuncCall(expr.name,
                              [self._opt_expr(a) for a in expr.args],
                              [(k, self._opt_expr(v)) for k, v in expr.kwargs],
                              expr.line)

        if isinstance(expr, IRMethodCall):
            return IRMethodCall(self._opt_expr(expr.obj), expr.method,
                                [self._opt_expr(a) for a in expr.args],
                                [(k, self._opt_expr(v)) for k, v in expr.kwargs],
                                expr.line)

        if isinstance(expr, IRInput):
            return IRInput(expr.mode, self._opt_expr(expr.prompt), expr.line)

        if isinstance(expr, IRLambda):
            return IRLambda(expr.params, self._opt_expr(expr.body), expr.line)

        return expr

    def _opt_binary(self, expr):
        """Optimiert binäre Operationen: Konstanten-Faltung + String-Konkatenation."""
        left = self._opt_expr(expr.left)
        right = self._opt_expr(expr.right)
        op = expr.op

        # Konstanten-Faltung: Zahl OP Zahl
        if isinstance(left, IRNumber) and isinstance(right, IRNumber) and op in _FOLD_OPS:
            l_val = _parse_number(left.value)
            r_val = _parse_number(right.value)
            try:
                result = _FOLD_OPS[op](l_val, r_val)
                if result is not None:
                    self.stats['constants_folded'] += 1
                    return _number_to_ir(result)
            except (ArithmeticError, OverflowError):
                pass

        # String-Konkatenation: "a" + "b" → "ab"
        if op == '+' and isinstance(left, IRString) and isinstance(right, IRString):
            l_str = left.value[1:-1]   # Anführungszeichen entfernen
            r_str = right.value[1:-1]
            self.stats['constants_folded'] += 1
            return IRString(f'"{l_str}{r_str}"')

        # Identitäts-Optimierungen
        if op == '+' and isinstance(right, IRNumber) and _parse_number(right.value) == 0:
            self.stats['constants_folded'] += 1
            return left
        if op == '+' and isinstance(left, IRNumber) and _parse_number(left.value) == 0:
            self.stats['constants_folded'] += 1
            return right
        if op == '*' and isinstance(right, IRNumber) and _parse_number(right.value) == 1:
            self.stats['constants_folded'] += 1
            return left
        if op == '*' and isinstance(left, IRNumber) and _parse_number(left.value) == 1:
            self.stats['constants_folded'] += 1
            return right
        if op == '*' and ((isinstance(left, IRNumber) and _parse_number(left.value) == 0) or
                          (isinstance(right, IRNumber) and _parse_number(right.value) == 0)):
            self.stats['constants_folded'] += 1
            return IRNumber('0')

        return IRBinaryOp(left, op, right, expr.line)

    def _opt_not(self, expr):
        """Optimiert NOT-Ausdrücke."""
        operand = self._opt_expr(expr.operand)

        # NICHT NICHT x → x
        if isinstance(operand, IRUnaryNot):
            self.stats['booleans_simplified'] += 1
            return operand.operand

        # NICHT wahr → falsch, NICHT falsch → wahr
        if isinstance(operand, IRVariable):
            if operand.name == 'wahr':
                self.stats['booleans_simplified'] += 1
                return IRVariable('falsch')
            if operand.name == 'falsch':
                self.stats['booleans_simplified'] += 1
                return IRVariable('wahr')

        return IRUnaryNot(operand, expr.line)
