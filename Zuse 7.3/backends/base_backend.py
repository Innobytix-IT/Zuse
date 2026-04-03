# FILE: backends/base_backend.py
# Abstrakte Basisklasse für alle Zuse-Transpiler-Backends
# Jedes Backend erbt von dieser Klasse und implementiert die Methoden.
# Nutzt das Visitor-Pattern für AST-Traversierung.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from visitor import NodeVisitor

class TranspilerError(Exception):
    pass

class BaseBackend(NodeVisitor):
    """
    Abstrakte Basisklasse. Jedes Backend (Python, JS, Java, C#)
    erbt von hier und überschreibt die generierten Methoden.
    Nutzt NodeVisitor für dispatch-basierte AST-Traversierung.
    """
    LANGUAGE_NAME = "Abstract"
    FILE_EXTENSION = ".txt"

    def __init__(self):
        self._indent_level = 0
        self._lines = []

    # ─── Öffentliche Hauptmethode ────────────────────────────────────────────

    def generate(self, ast):
        """Nimmt den AST entgegen und gibt fertigen Quellcode zurück."""
        self._indent_level = 0
        self._lines = []
        self._emit_header()
        self._gen_block(ast['body'])
        self._emit_footer()
        return "\n".join(self._lines)

    # ─── Interne Hilfsmethoden ───────────────────────────────────────────────

    def _indent(self):
        return "    " * self._indent_level

    def _emit(self, line=""):
        self._lines.append(self._indent() + line)

    def _emit_raw(self, line):
        self._lines.append(line)

    def _gen_block(self, stmts):
        for stmt in stmts:
            self._gen_stmt(stmt)

    # ─── Statement-Dispatcher (Visitor-Pattern) ─────────────────────────────

    def _gen_stmt(self, node):
        if node is None:
            return
        self.visit(node)

    def generic_visit(self, node):
        """Fallback: Ausdrucks-Statements (z.B. Funktionsaufrufe als Anweisung)."""
        expr_code = self._gen_expr(node)
        if expr_code:
            self._emit(expr_code)

    # Visitor-Methoden für Anweisungen delegieren an _gen_*-Methoden.
    # Backends überschreiben weiterhin die _gen_*-Methoden.
    def visit_ZUWEISUNG(self, node):            self._gen_assignment(node)
    def visit_MEHRFACH_ZUWEISUNG(self, node):   self._gen_multi_assignment(node)
    def visit_AUSGABE_ANWEISUNG(self, node):    self._gen_print(node)
    def visit_ERGEBNIS_ANWEISUNG(self, node):   self._gen_return(node)
    def visit_WENN_ANWEISUNG(self, node):       self._gen_if(node)
    def visit_SCHLEIFE_SOLANGE(self, node):     self._gen_while(node)
    def visit_SCHLEIFE_FÜR(self, node):         self._gen_for(node)
    def visit_FUNKTIONS_DEFINITION(self, node): self._gen_function(node)
    def visit_KLASSEN_DEFINITION(self, node):   self._gen_class(node)
    def visit_IMPORT_ANWEISUNG(self, node):     self._gen_import(node)
    def visit_GLOBAL_ANWEISUNG(self, node):     self._gen_global(node)
    def visit_VERSUCHE_ANWEISUNG(self, node):   self._gen_try(node)
    def visit_ABBRUCH_ANWEISUNG(self, node):    self._gen_break(node)
    def visit_WEITER_ANWEISUNG(self, node):     self._gen_continue(node)
    def visit_WAEHLE_ANWEISUNG(self, node):     self._gen_switch(node)

    # ─── Ausdruck-Generator (Visitor-Pattern) ────────────────────────────────

    def _gen_expr(self, node):
        """Dispatcht Ausdrücke zum passenden expr_TYPE-Handler."""
        t = node.get('type')
        handler = getattr(self, f'expr_{t}', None)
        if handler:
            return handler(node)
        return f"/* UNBEKANNT: {t} */"

    def expr_ZAHL_LITERAL(self, node):
        v = node['wert']
        return str(int(float(v))) if '.' not in v else str(float(v))

    def expr_STRING_LITERAL(self, node):
        return self._gen_string(node['wert'])

    def expr_VARIABLE(self, node):
        return self._gen_variable_name(node['name'])

    def expr_BINÄRER_AUSDRUCK(self, node):
        return self._gen_binary(node)

    def expr_UNAER_MINUS(self, node):
        return f"-{self._gen_expr(node['wert'])}"

    def expr_UNAER_NICHT(self, node):
        return self._gen_not(node)

    def expr_LISTEN_LITERAL(self, node):
        items = ", ".join(self._gen_expr(e) for e in node['elemente'])
        return self._gen_list_literal(items)

    def expr_DICT_LITERAL(self, node):
        pairs = [(self._gen_expr(k), self._gen_expr(v)) for k, v in node['paare']]
        return self._gen_dict_literal(pairs)

    def expr_INDEX_ZUGRIFF(self, node):
        return f"{self._gen_expr(node['objekt'])}[{self._gen_expr(node['index'])}]"

    def expr_SLICING(self, node):
        obj = self._gen_expr(node['objekt'])
        start = self._gen_expr(node['start']) if node['start'] else ""
        ende = self._gen_expr(node['ende']) if node['ende'] else ""
        return self._gen_slice(obj, start, ende)

    def expr_ATTRIBUT_ZUGRIFF(self, node):
        return f"{self._gen_expr(node['objekt'])}.{node['attribut']}"

    def expr_FUNKTIONS_AUFRUF(self, node):
        return self._gen_func_call(node)

    def expr_METHODEN_AUFRUF(self, node):
        return self._gen_method_call(node)

    def expr_EINGABE_AUFRUF(self, node):
        return self._gen_input(node)

    def expr_LAMBDA_ERSTELLUNG(self, node):
        return self._gen_lambda(node)

    def expr_ELTERN_ZUGRIFF(self, node):
        return self._gen_super()

    def _gen_binary(self, node):
        l = self._gen_expr(node['links'])
        r = self._gen_expr(node['rechts'])
        op = node['operator']
        return self._gen_binary_op(l, r, op)

    def _gen_func_call(self, node):
        name = self._map_builtin(node['name'])
        args = [self._gen_expr(a) for a in node['args']]
        kwargs = [f"{k}={self._gen_expr(v)}" for k, v in node['kwargs']]
        all_args = ", ".join(args + kwargs)
        return f"{name}({all_args})"

    def _gen_method_call(self, node):
        obj = self._gen_expr(node['objekt'])
        args = [self._gen_expr(a) for a in node['args']]
        kwargs = [f"{k}={self._gen_expr(v)}" for k, v in node['kwargs']]
        all_args = ", ".join(args + kwargs)
        return f"{obj}.{node['methode']}({all_args})"

    # ─── Methoden, die Backends ÜBERSCHREIBEN ───────────────────────────────
    # (Default-Implementierungen für Python-ähnliche Syntax)

    def _emit_header(self): pass
    def _emit_footer(self): pass

    def _gen_string(self, raw):       return raw  # raw = '"..."'
    def _gen_variable_name(self, n):  return n
    def _gen_list_literal(self, items): return f"[{items}]"
    def _gen_dict_literal(self, pairs):
        s = ", ".join(f"{k}: {v}" for k, v in pairs)
        return "{" + s + "}"
    def _gen_slice(self, obj, start, end): return f"{obj}[{start}:{end}]"
    def _gen_super(self): return "super()"
    def _gen_input(self, node):
        prompt = self._gen_expr(node['prompt'])
        return f"input({prompt})"
    def _gen_lambda(self, node):
        params = ", ".join(node['params'])
        body = self._gen_expr(node['body'])
        return f"lambda {params}: {body}"

    def _gen_not(self, node):
        val = self._gen_expr(node['wert'])
        return f"not {val}"

    def _gen_binary_op(self, l, r, op):
        py_ops = {'^': '**', 'und': 'and', 'oder': 'or'}
        return f"({l} {py_ops.get(op, op)} {r})"

    def _map_builtin(self, name):
        return name

    def _gen_multi_assignment(self, node):
        targets = ", ".join(self._gen_expr(z) for z in node['ziele'])
        values = ", ".join(self._gen_expr(w) for w in node['werte'])
        self._emit(f"{targets} = {values}")

    def _gen_assignment(self, node):
        target = self._gen_expr(node['ziel'])
        value = self._gen_expr(node['wert'])
        self._emit(f"{target} = {value}")

    def _gen_print(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"print({val})")

    def _gen_return(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"return {val}")

    def _gen_if(self, node):
        for i, (cond_node, block) in enumerate(node['faelle']):
            kw = "if" if i == 0 else "elif"
            cond = self._gen_expr(cond_node)
            self._emit(f"{kw} {cond}:")
            self._indent_level += 1
            self._gen_block(block)
            self._indent_level -= 1
        if node.get('sonst_koerper'):
            self._emit("else:")
            self._indent_level += 1
            self._gen_block(node['sonst_koerper'])
            self._indent_level -= 1

    def _gen_while(self, node):
        cond = self._gen_expr(node['bedingung'])
        self._emit(f"while {cond}:")
        self._indent_level += 1
        self._gen_block(node['koerper'])
        self._indent_level -= 1

    def _gen_for(self, node):
        var = node['variable']
        lst = self._gen_expr(node['liste'])
        self._emit(f"for {var} in {lst}:")
        self._indent_level += 1
        self._gen_block(node['koerper'])
        self._indent_level -= 1

    def _gen_function(self, node):
        params = ", ".join(node['parameter'])
        self._emit(f"def {node['name']}({params}):")
        self._indent_level += 1
        if not node['body']:
            self._emit("pass")
        else:
            self._gen_block(node['body'])
        self._indent_level -= 1
        self._emit()

    def _gen_class(self, node):
        parent = f"({node['elternklasse']})" if node['elternklasse'] else ""
        self._emit(f"class {node['name']}{parent}:")
        self._indent_level += 1
        if not node['methoden']:
            self._emit("pass")
        for m in node['methoden']:
            self._gen_method(m)
        self._indent_level -= 1
        self._emit()

    def _gen_method(self, m):
        params = ["self"] + m['parameter']
        self._emit(f"def {m['name']}({', '.join(params)}):")
        self._indent_level += 1
        if not m['body']:
            self._emit("pass")
        else:
            self._gen_block(m['body'])
        self._indent_level -= 1
        self._emit()

    def _gen_import(self, node):
        m = node['modul']
        a = node['alias']
        if m == a:
            self._emit(f"import {m}")
        else:
            self._emit(f"import {m} as {a}")

    def _gen_break(self, node):
        self._emit("break")

    def _gen_continue(self, node):
        self._emit("continue")

    def _gen_global(self, node):
        self._emit(f"global {node['name']}")

    def _gen_try(self, node):
        fehler_var = node.get('fehler_var', '_e')
        self._emit("try:")
        self._indent_level += 1
        self._gen_block(node['versuche_block'])
        self._indent_level -= 1
        self._emit(f"except Exception as {fehler_var or '_e'}:")
        self._indent_level += 1
        self._gen_block(node['fange_block'])
        self._indent_level -= 1

    def _gen_switch(self, node):
        """WÄHLE → Python: if/elif/else Kette (Python hat kein switch vor 3.10)."""
        ausdruck = self._gen_expr(node['ausdruck'])
        _tmp = f"_switch_val"
        self._emit(f"{_tmp} = {ausdruck}")
        first = True
        for fall in node['faelle']:
            wert = self._gen_expr(fall['wert'])
            keyword = "if" if first else "elif"
            self._emit(f"{keyword} {_tmp} == {wert}:")
            self._indent_level += 1
            self._gen_block(fall['block'])
            self._indent_level -= 1
            first = False
        if node.get('sonst_block'):
            self._emit("else:")
            self._indent_level += 1
            self._gen_block(node['sonst_block'])
            self._indent_level -= 1
