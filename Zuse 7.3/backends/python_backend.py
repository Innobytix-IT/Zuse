# FILE: backends/python_backend.py
# Zuse → Python 3 Transpiler
# Das einfachste Backend - Zuse ist Python sehr ähnlich.

from backends.base_backend import BaseBackend

class PythonBackend(BaseBackend):
    LANGUAGE_NAME = "Python 3"
    FILE_EXTENSION = ".py"

    def _emit_header(self):
        self._emit_raw("# Generiert von Zuse Transpiler")
        self._emit_raw("# Python 3 - Direkt ausführbar")
        self._emit_raw("import math, random, os")
        self._emit_raw("")

    def _gen_string(self, raw):
        # raw kommt als '"..."' aus dem Lexer
        return raw

    def _gen_binary_op(self, l, r, op):
        op_map = {'^': '**', 'und': 'and', 'oder': 'or', 'nicht': 'not'}
        return f"({l} {op_map.get(op, op)} {r})"

    def _map_builtin(self, name):
        builtins = {
            'str': 'str', 'int': 'int', 'float': 'float',
            'len': 'len', 'typ': 'type',
            'liste': 'list', 'dict': 'dict',
            'BEREICH': 'range',
            'WURZEL': 'math.sqrt', 'SINUS': 'math.sin', 'COSINUS': 'math.cos',
            'TANGENS': 'math.tan', 'RUNDEN': 'round', 'ABSOLUT': 'abs',
            'POTENZ': 'pow', 'LOGARITHMUS': 'math.log',
            'MINIMUM': 'min', 'MAXIMUM': 'max', 'SUMME': 'sum',
            'BODEN': 'math.floor', 'DECKE': 'math.ceil',
            'ZUFALL': 'random.random', 'ZUFALL_BEREICH': 'random.randint',
            'Maler': 'Maler',
        }
        return builtins.get(name, name)

    _PY_TEXT_METHOD_MAP = {
        'GROSSBUCHSTABEN': 'upper', 'KLEINBUCHSTABEN': 'lower',
        'TRIMME': 'strip',
    }

    def _gen_func_call(self, node):
        name = node['name']
        args = [self._gen_expr(a) for a in node['args']]

        # Text-Funktionen (4.2)
        if name in self._PY_TEXT_METHOD_MAP:
            return f"str({args[0]}).{self._PY_TEXT_METHOD_MAP[name]}()"
        if name == 'ERSETZE' and len(args) == 3:
            return f"str({args[0]}).replace({args[1]}, {args[2]})"
        if name == 'TEILE':
            if len(args) == 1:
                return f"str({args[0]}).split()"
            return f"str({args[0]}).split({args[1]})"
        if name == 'ENTHAELT' and len(args) == 2:
            return f"({args[1]} in str({args[0]}))"
        if name == 'LAENGE' and len(args) == 1:
            return f"len({args[0]})"
        if name == 'FINDE' and len(args) == 2:
            return f"str({args[0]}).find({args[1]})"
        if name == 'BEGINNT_MIT' and len(args) == 2:
            return f"str({args[0]}).startswith({args[1]})"
        if name == 'ENDET_MIT' and len(args) == 2:
            return f"str({args[0]}).endswith({args[1]})"
        if name == 'VERBINDE' and len(args) >= 1:
            trenner = args[1] if len(args) > 1 else '""'
            return f"{trenner}.join(str(e) for e in {args[0]})"

        # Listen-Funktionen (4.3)
        if name == 'SORTIEREN':
            if len(args) == 1:
                return f"sorted({args[0]})"
            return f"sorted({args[0]}, key={args[1]})"
        if name == 'FILTERN' and len(args) == 2:
            return f"list(filter({args[1]}, {args[0]}))"
        if name == 'UMWANDELN' and len(args) == 2:
            return f"list(map({args[1]}, {args[0]}))"
        if name == 'UMKEHREN' and len(args) == 1:
            return f"list(reversed({args[0]}))"
        if name == 'FLACH' and len(args) == 1:
            return f"[e for sub in {args[0]} for e in (sub if isinstance(sub, list) else [sub])]"
        if name == 'EINDEUTIG' and len(args) == 1:
            return f"list(dict.fromkeys({args[0]}))"
        if name == 'AUFZAEHLEN' and len(args) == 1:
            return f"list(enumerate({args[0]}))"
        if name == 'KOMBINIEREN':
            return f"list(zip({', '.join(args)}))"
        if name == 'ANHAENGEN' and len(args) >= 2:
            return f"{args[0]} + [{', '.join(args[1:])}]"
        if name == 'BEREICH_LISTE' and len(args) == 1:
            return f"list(range(int({args[0]})))"

        # Datei-Funktionen (4.4)
        if name == 'LESE_DATEI' and len(args) >= 1:
            kodierung = args[1] if len(args) > 1 else '"utf-8"'
            return f"open({args[0]}, 'r', encoding={kodierung}).read()"
        if name == 'SCHREIBE_DATEI' and len(args) >= 2:
            kodierung = args[2] if len(args) > 2 else '"utf-8"'
            return f"open({args[0]}, 'w', encoding={kodierung}).write(str({args[1]}))"
        if name == 'ERGAENZE_DATEI' and len(args) >= 2:
            kodierung = args[2] if len(args) > 2 else '"utf-8"'
            return f"open({args[0]}, 'a', encoding={kodierung}).write(str({args[1]}))"
        if name == 'EXISTIERT' and len(args) == 1:
            return f"os.path.exists({args[0]})"
        if name == 'LESE_ZEILEN' and len(args) >= 1:
            kodierung = args[1] if len(args) > 1 else '"utf-8"'
            return f"open({args[0]}, 'r', encoding={kodierung}).read().splitlines()"
        if name == 'LOESCHE_DATEI' and len(args) == 1:
            return f"os.remove({args[0]})"

        # Fallback: base class logic
        mapped = self._map_builtin(name)
        kwargs = [f"{k}={self._gen_expr(v)}" for k, v in node['kwargs']]
        all_args = ", ".join(args + kwargs)
        return f"{mapped}({all_args})"

    def _gen_variable_name(self, name):
        if name == 'SELBST': return 'self'
        if name == 'wahr':   return 'True'
        if name == 'falsch': return 'False'
        if name == 'PI':     return 'math.pi'
        if name == 'E':      return 'math.e'
        return name

    def _gen_input(self, node):
        prompt = self._gen_expr(node['prompt'])
        if node['modus'] == 'zahl':
            return f"float(input({prompt}))"
        return f"input({prompt})"

    def _gen_lambda(self, node):
        params = ", ".join(node['params'])
        body = self._gen_expr(node['body'])
        return f"lambda {params}: {body}"

    # Methode: SELBST → self, ERSTELLE → __init__
    def _gen_method(self, m):
        method_name = m['name']
        if method_name in ['ERSTELLE', 'NEW', 'CREAR', 'CRIAR', 'CREER', 'CREARE']:
            method_name = '__init__'
        params = ["self"] + m['parameter']
        self._emit(f"def {method_name}({', '.join(params)}):")
        self._indent_level += 1
        if not m['body']:
            self._emit("pass")
        else:
            self._gen_block(m['body'])
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

    def _gen_super(self):
        return "super()"
