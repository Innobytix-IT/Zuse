# FILE: ir.py
# Intermediate Representation (IR) für Zuse.
# Normalisiert den deutsch-sprachigen AST in eine sprachunabhängige Zwischenform.
# Backends können wahlweise direkt auf dem AST oder auf der IR arbeiten.

from visitor import NodeVisitor


class IRNode:
    """Basisklasse für alle IR-Knoten."""
    __slots__ = ('line',)

    def __init__(self, line=0):
        self.line = line

    def __repr__(self):
        attrs = {k: getattr(self, k) for k in self.__slots__}
        return f"{self.__class__.__name__}({attrs})"


# ─── Programm ───────────────────────────────────────────────────────────────

class IRProgram(IRNode):
    __slots__ = ('line', 'body')
    def __init__(self, body, line=0):
        super().__init__(line)
        self.body = body


# ─── Anweisungen ─────────────────────────────────────────────────────────────

class IRAssign(IRNode):
    __slots__ = ('line', 'target', 'value')
    def __init__(self, target, value, line=0):
        super().__init__(line)
        self.target = target
        self.value = value


class IRMultiAssign(IRNode):
    __slots__ = ('line', 'targets', 'values')
    def __init__(self, targets, values, line=0):
        super().__init__(line)
        self.targets = targets
        self.values = values


class IRPrint(IRNode):
    __slots__ = ('line', 'value')
    def __init__(self, value, line=0):
        super().__init__(line)
        self.value = value


class IRReturn(IRNode):
    __slots__ = ('line', 'value')
    def __init__(self, value, line=0):
        super().__init__(line)
        self.value = value


class IRIf(IRNode):
    __slots__ = ('line', 'cases', 'else_body')
    def __init__(self, cases, else_body=None, line=0):
        super().__init__(line)
        self.cases = cases          # [(condition_expr, [stmts]), ...]
        self.else_body = else_body  # [stmts] or None


class IRWhile(IRNode):
    __slots__ = ('line', 'condition', 'body')
    def __init__(self, condition, body, line=0):
        super().__init__(line)
        self.condition = condition
        self.body = body


class IRFor(IRNode):
    __slots__ = ('line', 'variable', 'iterable', 'body')
    def __init__(self, variable, iterable, body, line=0):
        super().__init__(line)
        self.variable = variable
        self.iterable = iterable
        self.body = body


class IRFunction(IRNode):
    __slots__ = ('line', 'name', 'params', 'defaults', 'body')
    def __init__(self, name, params, body, defaults=None, line=0):
        super().__init__(line)
        self.name = name
        self.params = params
        self.defaults = defaults or {}
        self.body = body


class IRClass(IRNode):
    __slots__ = ('line', 'name', 'parent', 'methods')
    def __init__(self, name, parent, methods, line=0):
        super().__init__(line)
        self.name = name
        self.parent = parent        # str or None
        self.methods = methods       # [IRMethod]


class IRMethod(IRNode):
    __slots__ = ('line', 'name', 'params', 'body')
    def __init__(self, name, params, body, line=0):
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body


class IRImport(IRNode):
    __slots__ = ('line', 'module', 'alias')
    def __init__(self, module, alias, line=0):
        super().__init__(line)
        self.module = module
        self.alias = alias


class IRGlobal(IRNode):
    __slots__ = ('line', 'name')
    def __init__(self, name, line=0):
        super().__init__(line)
        self.name = name


class IRTry(IRNode):
    __slots__ = ('line', 'try_body', 'catch_body')
    def __init__(self, try_body, catch_body, line=0):
        super().__init__(line)
        self.try_body = try_body
        self.catch_body = catch_body


class IRBreak(IRNode):
    __slots__ = ('line',)


class IRContinue(IRNode):
    __slots__ = ('line',)


# ─── Ausdrücke ───────────────────────────────────────────────────────────────

class IRNumber(IRNode):
    __slots__ = ('line', 'value')
    def __init__(self, value, line=0):
        super().__init__(line)
        self.value = value  # str: "42" or "3.14"


class IRString(IRNode):
    __slots__ = ('line', 'value')
    def __init__(self, value, line=0):
        super().__init__(line)
        self.value = value  # raw string with quotes


class IRVariable(IRNode):
    __slots__ = ('line', 'name')
    def __init__(self, name, line=0):
        super().__init__(line)
        self.name = name


class IRBinaryOp(IRNode):
    __slots__ = ('line', 'left', 'right', 'op')
    def __init__(self, left, op, right, line=0):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class IRUnaryMinus(IRNode):
    __slots__ = ('line', 'operand')
    def __init__(self, operand, line=0):
        super().__init__(line)
        self.operand = operand


class IRUnaryNot(IRNode):
    __slots__ = ('line', 'operand')
    def __init__(self, operand, line=0):
        super().__init__(line)
        self.operand = operand


class IRList(IRNode):
    __slots__ = ('line', 'elements')
    def __init__(self, elements, line=0):
        super().__init__(line)
        self.elements = elements


class IRDict(IRNode):
    __slots__ = ('line', 'pairs')
    def __init__(self, pairs, line=0):
        super().__init__(line)
        self.pairs = pairs  # [(key_expr, val_expr), ...]


class IRIndex(IRNode):
    __slots__ = ('line', 'obj', 'index')
    def __init__(self, obj, index, line=0):
        super().__init__(line)
        self.obj = obj
        self.index = index


class IRSlice(IRNode):
    __slots__ = ('line', 'obj', 'start', 'end')
    def __init__(self, obj, start=None, end=None, line=0):
        super().__init__(line)
        self.obj = obj
        self.start = start
        self.end = end


class IRAttribute(IRNode):
    __slots__ = ('line', 'obj', 'attr')
    def __init__(self, obj, attr, line=0):
        super().__init__(line)
        self.obj = obj
        self.attr = attr


class IRFuncCall(IRNode):
    __slots__ = ('line', 'name', 'args', 'kwargs')
    def __init__(self, name, args, kwargs=None, line=0):
        super().__init__(line)
        self.name = name
        self.args = args
        self.kwargs = kwargs or []  # [(key, val_expr), ...]


class IRMethodCall(IRNode):
    __slots__ = ('line', 'obj', 'method', 'args', 'kwargs')
    def __init__(self, obj, method, args, kwargs=None, line=0):
        super().__init__(line)
        self.obj = obj
        self.method = method
        self.args = args
        self.kwargs = kwargs or []


class IRInput(IRNode):
    __slots__ = ('line', 'mode', 'prompt')
    def __init__(self, mode, prompt, line=0):
        super().__init__(line)
        self.mode = mode    # 'text' or 'zahl'
        self.prompt = prompt


class IRLambda(IRNode):
    __slots__ = ('line', 'params', 'body')
    def __init__(self, params, body, line=0):
        super().__init__(line)
        self.params = params
        self.body = body


class IRSuper(IRNode):
    __slots__ = ('line',)


# ─── AST → IR Konverter ─────────────────────────────────────────────────────

class ASTtoIR(NodeVisitor):
    """Konvertiert den deutsch-sprachigen Zuse-AST in die sprachunabhängige IR."""

    def convert(self, ast):
        """Hauptmethode: AST → IRProgram."""
        body = [self.visit(stmt) for stmt in ast['body']]
        return IRProgram(body)

    def generic_visit(self, node):
        """Fallback: Ausdruck konvertieren."""
        return self._convert_expr(node)

    def _convert_expr(self, node):
        """Dispatcht Ausdrücke zum passenden _expr_TYPE-Handler."""
        if node is None:
            return None
        t = node.get('type')
        handler = getattr(self, f'_expr_{t}', None)
        if handler:
            return handler(node)
        raise ValueError(f"Unbekannter Ausdruck-Typ: {t}")

    def _convert_block(self, stmts):
        return [self.visit(s) for s in stmts]

    # ─── Anweisungen ─────────────────────────────────────────────────────

    def visit_ZUWEISUNG(self, node):
        return IRAssign(
            target=self._convert_expr(node['ziel']),
            value=self._convert_expr(node['wert']),
            line=node.get('line', 0)
        )

    def visit_MEHRFACH_ZUWEISUNG(self, node):
        return IRMultiAssign(
            targets=[self._convert_expr(z) for z in node['ziele']],
            values=[self._convert_expr(w) for w in node['werte']],
            line=node.get('line', 0)
        )

    def visit_AUSGABE_ANWEISUNG(self, node):
        return IRPrint(
            value=self._convert_expr(node['wert']),
            line=node.get('line', 0)
        )

    def visit_ERGEBNIS_ANWEISUNG(self, node):
        return IRReturn(
            value=self._convert_expr(node['wert']),
            line=node.get('line', 0)
        )

    def visit_WENN_ANWEISUNG(self, node):
        cases = []
        for cond, block in node['faelle']:
            cases.append((self._convert_expr(cond), self._convert_block(block)))
        else_body = self._convert_block(node['sonst_koerper']) if node.get('sonst_koerper') else None
        return IRIf(cases=cases, else_body=else_body, line=node.get('line', 0))

    def visit_SCHLEIFE_SOLANGE(self, node):
        return IRWhile(
            condition=self._convert_expr(node['bedingung']),
            body=self._convert_block(node['koerper']),
            line=node.get('line', 0)
        )

    def visit_SCHLEIFE_FÜR(self, node):
        return IRFor(
            variable=node['variable'],
            iterable=self._convert_expr(node['liste']),
            body=self._convert_block(node['koerper']),
            line=node.get('line', 0)
        )

    def visit_FUNKTIONS_DEFINITION(self, node):
        defaults = {}
        for k, v in node.get('defaults', {}).items():
            defaults[k] = self._convert_expr(v)
        return IRFunction(
            name=node['name'],
            params=node['parameter'],
            body=self._convert_block(node['body']),
            defaults=defaults,
            line=node.get('line', 0)
        )

    def visit_KLASSEN_DEFINITION(self, node):
        methods = []
        for m in node['methoden']:
            methods.append(IRMethod(
                name=m['name'],
                params=m['parameter'],
                body=self._convert_block(m['body']),
                line=m.get('line', 0)
            ))
        return IRClass(
            name=node['name'],
            parent=node.get('elternklasse'),
            methods=methods,
            line=node.get('line', 0)
        )

    def visit_IMPORT_ANWEISUNG(self, node):
        return IRImport(
            module=node['modul'],
            alias=node['alias'],
            line=node.get('line', 0)
        )

    def visit_GLOBAL_ANWEISUNG(self, node):
        return IRGlobal(name=node['name'], line=node.get('line', 0))

    def visit_VERSUCHE_ANWEISUNG(self, node):
        return IRTry(
            try_body=self._convert_block(node['versuche_block']),
            catch_body=self._convert_block(node['fange_block']),
            line=node.get('line', 0)
        )

    def visit_ABBRUCH_ANWEISUNG(self, node):
        return IRBreak(line=node.get('line', 0))

    def visit_WEITER_ANWEISUNG(self, node):
        return IRContinue(line=node.get('line', 0))

    # ─── Ausdrücke ───────────────────────────────────────────────────────

    def _expr_ZAHL_LITERAL(self, node):
        return IRNumber(value=node['wert'])

    def _expr_STRING_LITERAL(self, node):
        return IRString(value=node['wert'])

    def _expr_VARIABLE(self, node):
        return IRVariable(name=node['name'])

    def _expr_BINÄRER_AUSDRUCK(self, node):
        return IRBinaryOp(
            left=self._convert_expr(node['links']),
            op=node['operator'],
            right=self._convert_expr(node['rechts'])
        )

    def _expr_UNAER_MINUS(self, node):
        return IRUnaryMinus(operand=self._convert_expr(node['wert']))

    def _expr_UNAER_NICHT(self, node):
        return IRUnaryNot(operand=self._convert_expr(node['wert']))

    def _expr_LISTEN_LITERAL(self, node):
        return IRList(elements=[self._convert_expr(e) for e in node['elemente']])

    def _expr_DICT_LITERAL(self, node):
        return IRDict(pairs=[(self._convert_expr(k), self._convert_expr(v)) for k, v in node['paare']])

    def _expr_INDEX_ZUGRIFF(self, node):
        return IRIndex(
            obj=self._convert_expr(node['objekt']),
            index=self._convert_expr(node['index'])
        )

    def _expr_SLICING(self, node):
        return IRSlice(
            obj=self._convert_expr(node['objekt']),
            start=self._convert_expr(node['start']) if node['start'] else None,
            end=self._convert_expr(node['ende']) if node['ende'] else None
        )

    def _expr_ATTRIBUT_ZUGRIFF(self, node):
        return IRAttribute(
            obj=self._convert_expr(node['objekt']),
            attr=node['attribut']
        )

    def _expr_FUNKTIONS_AUFRUF(self, node):
        return IRFuncCall(
            name=node['name'],
            args=[self._convert_expr(a) for a in node['args']],
            kwargs=[(k, self._convert_expr(v)) for k, v in node['kwargs']]
        )

    def _expr_METHODEN_AUFRUF(self, node):
        return IRMethodCall(
            obj=self._convert_expr(node['objekt']),
            method=node['methode'],
            args=[self._convert_expr(a) for a in node['args']],
            kwargs=[(k, self._convert_expr(v)) for k, v in node['kwargs']]
        )

    def _expr_EINGABE_AUFRUF(self, node):
        return IRInput(
            mode=node['modus'],
            prompt=self._convert_expr(node['prompt'])
        )

    def _expr_LAMBDA_ERSTELLUNG(self, node):
        return IRLambda(
            params=node['params'],
            body=self._convert_expr(node['body'])
        )

    def _expr_ELTERN_ZUGRIFF(self, node):
        return IRSuper()
