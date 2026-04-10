# FILE: backends/javascript_backend.py
# Zuse → JavaScript (ES6+) Transpiler

from backends.base_backend import BaseBackend
from builtin_i18n import resolve_maler_method, resolve_color, resolve_fenster_method, MALER_KLASSEN, FENSTER_KLASSEN

class JavaScriptBackend(BaseBackend):
    LANGUAGE_NAME = "JavaScript (ES6+)"
    FILE_EXTENSION = ".js"

    def __init__(self):
        super().__init__()
        self._declared_vars = [set()]  # Stack für Scope-Tracking

    def _emit_header(self):
        self._emit_raw("// Generiert von Zuse Transpiler")
        self._emit_raw("// JavaScript ES6+ - Läuft in Node.js oder im Browser")
        self._emit_raw('"use strict";')
        self._emit_raw("")

    def _push_scope(self):
        self._declared_vars.append(set())

    def _pop_scope(self):
        self._declared_vars.pop()

    def _declare(self, name):
        self._declared_vars[-1].add(name)

    def _is_declared(self, name):
        for scope in reversed(self._declared_vars):
            if name in scope:
                return True
        return False

    def _gen_string(self, raw):
        # Zuse nutzt "...", JS auch → direkt übernehmen
        return raw

    def _gen_variable_name(self, name):
        if name == 'SELBST':  return 'this'
        if name == 'wahr':    return 'true'
        if name == 'falsch':  return 'false'
        if name == 'PI':      return 'Math.PI'
        if name == 'E':       return 'Math.E'
        return name

    def _gen_not(self, node):
        val = self._gen_expr(node['wert'])
        return f"!{val}"

    def _gen_binary_op(self, l, r, op):
        op_map = {
            '^':    f"Math.pow({l}, {r})",
            '==':   f"({l} === {r})",
            '!=':   f"({l} !== {r})",
            'und':  f"({l} && {r})",
            'oder': f"({l} || {r})",
        }
        if op in op_map:
            result = op_map[op]
            return result
        return f"({l} {op} {r})"

    def _gen_list_literal(self, items):
        return f"[{items}]"

    def _gen_dict_literal(self, pairs):
        s = ", ".join(f"{k}: {v}" for k, v in pairs)
        return "{" + s + "}"

    def _gen_slice(self, obj, start, end):
        # JS: array.slice(start, end)
        if start and end:
            return f"{obj}.slice({start}, {end})"
        elif start:
            return f"{obj}.slice({start})"
        elif end:
            return f"{obj}.slice(0, {end})"
        return f"{obj}.slice()"

    def _gen_input(self, node):
        prompt = self._gen_expr(node['prompt'])
        if node['modus'] == 'zahl':
            return f"parseFloat(prompt({prompt}))"
        return f"prompt({prompt})"

    def _gen_lambda(self, node):
        params = ", ".join(node['params'])
        body = self._gen_expr(node['body'])
        return f"({params}) => {body}"

    def _gen_super(self):
        return "super"

    def _map_builtin(self, name):
        if name in MALER_KLASSEN:
            return '_ZuseMaler'
        if name in FENSTER_KLASSEN:
            return '_ZuseFenster'
        builtins = {
            'str':   'String',
            'int':   'parseInt',
            'float': 'parseFloat',
            'len':   None,
            'typ':   'typeof',
            'liste': 'Array',
            'print': 'console.log',
        }
        return builtins.get(name, name)

    def _gen_method_call(self, node):
        """Löst mehrsprachige Maler/Painter und Fenster/Window-Methoden für JavaScript auf."""
        obj = self._gen_expr(node['objekt'])
        methode = node['methode']
        args = [self._gen_expr(a) for a in node['args']]
        kwargs = [f"/* {k}= */{self._gen_expr(v)}" for k, v in node['kwargs']]

        turtle_method = resolve_maler_method(methode)
        if turtle_method:
            if turtle_method == 'color' and args:
                raw = args[0].strip('"').strip("'")
                args = [f'"{resolve_color(raw)}"']
            if turtle_method == 'done':
                return "/* done() - Fenster offen lassen */"
            all_args = ", ".join(args + kwargs)
            return f"{obj}.{turtle_method}({all_args})"

        window_method = resolve_fenster_method(methode)
        if window_method:
            all_args = ", ".join(args + kwargs)
            return f"{obj}.{window_method}({all_args})"

        all_args = ", ".join(args + kwargs)
        return f"{obj}.{methode}({all_args})"

    _JS_MATH_MAP = {
        'WURZEL': 'Math.sqrt', 'SINUS': 'Math.sin', 'COSINUS': 'Math.cos',
        'TANGENS': 'Math.tan', 'ABSOLUT': 'Math.abs',
        'BODEN': 'Math.floor', 'DECKE': 'Math.ceil',
        'POTENZ': 'Math.pow', 'LOGARITHMUS': 'Math.log',
        'MINIMUM': 'Math.min', 'MAXIMUM': 'Math.max',
        'ZUFALL': 'Math.random',
    }

    def _gen_func_call(self, node):
        name = node['name']
        args = [self._gen_expr(a) for a in node['args']]
        kwargs = node['kwargs']

        # Mathe-Funktionen
        if name in self._JS_MATH_MAP:
            return f"{self._JS_MATH_MAP[name]}({', '.join(args)})"
        if name == 'RUNDEN':
            if len(args) == 1:
                return f"Math.round({args[0]})"
            return f"parseFloat(({args[0]}).toFixed({args[1]}))"
        if name == 'SUMME' and len(args) == 1:
            return f"{args[0]}.reduce((a, b) => a + b, 0)"
        if name == 'ZUFALL_BEREICH' and len(args) == 2:
            return f"(Math.floor(Math.random() * ({args[1]} - {args[0]} + 1)) + {args[0]})"

        # Spezialbehandlung für BEREICH() → Array.from
        if name == 'BEREICH':
            if len(args) == 1:
                return f"Array.from({{length: {args[0]}}}, (_, i) => i)"
            if len(args) == 2:
                return f"Array.from({{length: {args[1]} - {args[0]}}}, (_, i) => i + {args[0]})"
            if len(args) == 3:
                return f"Array.from({{length: Math.ceil(({args[1]} - {args[0]}) / {args[2]})}}, (_, i) => {args[0]} + i * {args[2]})"

        # Text-Funktionen (4.2)
        if name == 'GROSSBUCHSTABEN' and len(args) == 1:
            return f"String({args[0]}).toUpperCase()"
        if name == 'KLEINBUCHSTABEN' and len(args) == 1:
            return f"String({args[0]}).toLowerCase()"
        if name == 'ERSETZE' and len(args) == 3:
            return f"String({args[0]}).split({args[1]}).join({args[2]})"
        if name == 'TEILE':
            if len(args) == 1:
                return f"String({args[0]}).split(/\\s+/)"
            return f"String({args[0]}).split({args[1]})"
        if name == 'TRIMME' and len(args) == 1:
            return f"String({args[0]}).trim()"
        if name == 'ENTHAELT' and len(args) == 2:
            return f"String({args[0]}).includes(String({args[1]}))"
        if name == 'LAENGE' and len(args) == 1:
            return f"{args[0]}.length"
        if name == 'FINDE' and len(args) == 2:
            return f"String({args[0]}).indexOf(String({args[1]}))"
        if name == 'BEGINNT_MIT' and len(args) == 2:
            return f"String({args[0]}).startsWith(String({args[1]}))"
        if name == 'ENDET_MIT' and len(args) == 2:
            return f"String({args[0]}).endsWith(String({args[1]}))"
        if name == 'VERBINDE' and len(args) >= 1:
            trenner = args[1] if len(args) > 1 else '""'
            return f"{args[0]}.join({trenner})"

        # Listen-Funktionen (4.3)
        if name == 'SORTIEREN':
            if len(args) == 1:
                return f"[...{args[0]}].sort()"
            return f"[...{args[0]}].sort({args[1]})"
        if name == 'FILTERN' and len(args) == 2:
            return f"{args[0]}.filter({args[1]})"
        if name == 'UMWANDELN' and len(args) == 2:
            return f"{args[0]}.map({args[1]})"
        if name == 'UMKEHREN' and len(args) == 1:
            return f"[...{args[0]}].reverse()"
        if name == 'FLACH' and len(args) == 1:
            return f"{args[0]}.flat()"
        if name == 'EINDEUTIG' and len(args) == 1:
            return f"[...new Set({args[0]})]"
        if name == 'AUFZAEHLEN' and len(args) == 1:
            return f"{args[0]}.map((v, i) => [i, v])"
        if name == 'KOMBINIEREN':
            return f"{args[0]}.map((v, i) => [{', '.join(f'{a}[i]' for a in args)}])"
        if name == 'ANHAENGEN' and len(args) >= 2:
            return f"[...{args[0]}, {', '.join(args[1:])}]"
        if name == 'BEREICH_LISTE' and len(args) == 1:
            return f"Array.from({{length: parseInt({args[0]})}}, (_, i) => i)"

        # Spezialbehandlung für len() → .length
        if name == 'len' and len(args) == 1:
            return f"{args[0]}.length"

        # Datei-Funktionen (4.4) — Node.js fs
        if name == 'LESE_DATEI' and len(args) >= 1:
            kodierung = args[1] if len(args) > 1 else '"utf-8"'
            return f"require('fs').readFileSync({args[0]}, {kodierung})"
        if name == 'SCHREIBE_DATEI' and len(args) >= 2:
            kodierung = args[2] if len(args) > 2 else '"utf-8"'
            return f"require('fs').writeFileSync({args[0]}, String({args[1]}), {kodierung})"
        if name == 'ERGAENZE_DATEI' and len(args) >= 2:
            return f"require('fs').appendFileSync({args[0]}, String({args[1]}))"
        if name == 'EXISTIERT' and len(args) == 1:
            return f"require('fs').existsSync({args[0]})"
        if name == 'LESE_ZEILEN' and len(args) >= 1:
            kodierung = args[1] if len(args) > 1 else '"utf-8"'
            return f"require('fs').readFileSync({args[0]}, {kodierung}).split('\\n')"
        if name == 'LOESCHE_DATEI' and len(args) == 1:
            return f"require('fs').unlinkSync({args[0]})"

        mapped = self._map_builtin(name)
        all_args = ", ".join(args + [f"/* {k}= */{self._gen_expr(v)}" for k, v in kwargs])
        return f"{mapped}({all_args})"

    # ─── Statement-Generatoren ────────────────────────────────────────────────

    def _gen_multi_assignment(self, node):
        # JS destructuring: let [a, b] = [1, 2];
        targets = ", ".join(self._gen_expr(z) for z in node['ziele'])
        values = ", ".join(self._gen_expr(w) for w in node['werte'])
        # Track all variables as declared
        for z in node['ziele']:
            if z['type'] == 'VARIABLE' and not self._is_declared(z['name']):
                self._declare(z['name'])
        self._emit(f"let [{targets}] = [{values}];")

    def _gen_assignment(self, node):
        target = self._gen_expr(node['ziel'])
        value = self._gen_expr(node['wert'])
        # Erste Zuweisung → let, danach einfache Zuweisung
        if node['ziel']['type'] == 'VARIABLE':
            var_name = node['ziel']['name']
            if not self._is_declared(var_name):
                self._declare(var_name)
                self._emit(f"let {target} = {value};")
                return
        self._emit(f"{target} = {value};")

    def _gen_print(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"console.log({val});")

    def _gen_return(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"return {val};")

    def _gen_if(self, node):
        for i, (cond_node, block) in enumerate(node['faelle']):
            kw = "if" if i == 0 else "} else if"
            cond = self._gen_expr(cond_node)
            self._emit(f"{kw} ({cond}) {{")
            self._indent_level += 1
            self._push_scope()
            self._gen_block(block)
            self._pop_scope()
            self._indent_level -= 1
        if node.get('sonst_koerper'):
            self._emit("} else {")
            self._indent_level += 1
            self._push_scope()
            self._gen_block(node['sonst_koerper'])
            self._pop_scope()
            self._indent_level -= 1
        self._emit("}")

    def _gen_while(self, node):
        cond = self._gen_expr(node['bedingung'])
        self._emit(f"while ({cond}) {{")
        self._indent_level += 1
        self._push_scope()
        self._gen_block(node['koerper'])
        self._pop_scope()
        self._indent_level -= 1
        self._emit("}")

    def _gen_for(self, node):
        var = node['variable']
        lst = self._gen_expr(node['liste'])
        self._emit(f"for (const {var} of {lst}) {{")
        self._indent_level += 1
        self._push_scope()
        self._declare(var)
        self._gen_block(node['koerper'])
        self._pop_scope()
        self._indent_level -= 1
        self._emit("}")

    def _gen_function(self, node):
        params = ", ".join(node['parameter'])
        self._emit(f"function {node['name']}({params}) {{")
        self._indent_level += 1
        self._push_scope()
        for p in node['parameter']:
            self._declare(p)
        self._gen_block(node['body'])
        self._pop_scope()
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_class(self, node):
        parent = f" extends {node['elternklasse']}" if node['elternklasse'] else ""
        self._emit(f"class {node['name']}{parent} {{")
        self._indent_level += 1
        for m in node['methoden']:
            self._gen_method(m)
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_method(self, m):
        method_name = m['name']
        if method_name in ['ERSTELLE', 'NEW', 'CREAR', 'CRIAR', 'CREER', 'CREARE']:
            method_name = 'constructor'
        params = ", ".join(m['parameter'])
        self._emit(f"{method_name}({params}) {{")
        self._indent_level += 1
        self._push_scope()
        for p in m['parameter']:
            self._declare(p)
        self._gen_block(m['body'])
        self._pop_scope()
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_import(self, node):
        m = node['modul']
        a = node['alias']
        if a != m:
            self._emit(f"const {a} = require('{m}');  // alias: {m} → {a}")
        else:
            self._emit(f"const {m} = require('{m}');")

    def _gen_global(self, node):
        # In JS: Variable ohne let/const deklarieren → globaler Scope
        self._emit(f"var {node['name']};")

    def _gen_break(self, node):
        self._emit("break;")

    def _gen_continue(self, node):
        self._emit("continue;")

    def _gen_try(self, node):
        fehler_var = node.get('fehler_var', '_e')
        self._emit("try {")
        self._indent_level += 1
        self._push_scope()
        self._gen_block(node['versuche_block'])
        self._pop_scope()
        self._indent_level -= 1
        self._emit(f"}} catch ({fehler_var or '_e'}) {{")
        self._indent_level += 1
        self._push_scope()
        self._gen_block(node['fange_block'])
        self._pop_scope()
        self._indent_level -= 1
        self._emit("}")

    def _gen_switch(self, node):
        ausdruck = self._gen_expr(node['ausdruck'])
        self._emit(f"switch ({ausdruck}) {{")
        self._indent_level += 1
        for fall in node['faelle']:
            wert = self._gen_expr(fall['wert'])
            self._emit(f"case {wert}:")
            self._indent_level += 1
            self._gen_block(fall['block'])
            self._emit("break;")
            self._indent_level -= 1
        if node.get('sonst_block'):
            self._emit("default:")
            self._indent_level += 1
            self._gen_block(node['sonst_block'])
            self._indent_level -= 1
        self._indent_level -= 1
        self._emit("}")
