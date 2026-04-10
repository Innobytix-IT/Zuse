# FILE: backends/python_backend.py
# Zuse → Python 3 Transpiler
# Das einfachste Backend - Zuse ist Python sehr ähnlich.

from backends.base_backend import BaseBackend
from builtin_i18n import (
    resolve_maler_method, resolve_color,
    resolve_fenster_method, is_fenster_class,
    MALER_KLASSEN, FENSTER_KLASSEN,
)

class PythonBackend(BaseBackend):
    LANGUAGE_NAME = "Python 3"
    FILE_EXTENSION = ".py"

    def __init__(self):
        super().__init__()
        self._maler_vars = set()   # Variablennamen die Maler-Instanzen halten
        self._fenster_vars = set() # Variablennamen die Fenster-Instanzen halten

    def generate(self, ast):
        self._maler_vars = set()
        self._fenster_vars = set()
        return super().generate(ast)

    def _gen_assignment(self, node):
        """Überschreibt base: trackt Maler/Fenster-Instanzen für korrekte Methoden-Übersetzung."""
        wert = node['wert']
        ziel = node['ziel']
        if wert.get('type') == 'FUNKTIONS_AUFRUF':
            if wert['name'] in MALER_KLASSEN and ziel.get('type') == 'NAME':
                self._maler_vars.add(ziel.get('name', ''))
            elif wert['name'] in FENSTER_KLASSEN and ziel.get('type') == 'NAME':
                self._fenster_vars.add(ziel.get('name', ''))
        super()._gen_assignment(node)

    def _emit_header(self):
        self._emit_raw("# Generiert von Zuse Transpiler")
        self._emit_raw("# Python 3 - Direkt ausführbar")
        self._emit_raw("import math, random, os, turtle")
        self._emit_raw("")
        # _ZuseMaler Wrapper: übersetzt alle Maler/Painter-Methoden zu turtle
        self._emit_raw("class _ZuseMaler:")
        self._emit_raw("    def __init__(self):")
        self._emit_raw("        self._s = turtle.Screen()")
        self._emit_raw("        self._s.title('Zuse')")
        self._emit_raw("        self._t = turtle.Turtle()")
        self._emit_raw("        self._t.speed(3)")
        self._emit_raw("    def forward(self, n):    self._t.forward(n)")
        self._emit_raw("    def backward(self, n):   self._t.backward(n)")
        self._emit_raw("    def left(self, n):       self._t.left(n)")
        self._emit_raw("    def right(self, n):      self._t.right(n)")
        self._emit_raw("    def penup(self):         self._t.penup()")
        self._emit_raw("    def pendown(self):       self._t.pendown()")
        self._emit_raw("    def color(self, c):      self._t.color(c)")
        self._emit_raw("    def pensize(self, d):    self._t.pensize(d)")
        self._emit_raw("    def circle(self, r):     self._t.circle(r)")
        self._emit_raw("    def done(self):          turtle.done()")
        self._emit_raw("")

    def _map_builtin(self, name):
        # Alle Maler/Painter-Klassen → _ZuseMaler
        if name in MALER_KLASSEN:
            return '_ZuseMaler'
        # Fenster/Window-Klassen → _ZuseFenster
        if name in FENSTER_KLASSEN:
            return '_ZuseFenster'
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

    def _gen_method_call(self, node):
        """Überschreibt base: löst mehrsprachige Maler/Painter und Fenster/Window-Methoden auf."""
        obj_node = node['objekt']
        obj = self._gen_expr(obj_node)
        methode = node['methode']
        args = [self._gen_expr(a) for a in node['args']]
        kwargs = [f"{k}={self._gen_expr(v)}" for k, v in node['kwargs']]

        # Maler/Painter Methoden — nur wenn Objekt als Maler bekannt oder 'self' in Maler-Kontext
        obj_name = obj_node.get('name', '') if obj_node.get('type') == 'NAME' else ''
        is_maler = obj_name in self._maler_vars or obj_name == 'self'
        is_fenster = obj_name in self._fenster_vars or obj_name == 'self'

        turtle_method = resolve_maler_method(methode) if is_maler else None
        if turtle_method:
            if turtle_method == 'color' and args:
                raw = args[0].strip('"').strip("'")
                args = [f'"{resolve_color(raw)}"']
            if turtle_method == 'done':
                return f"turtle.done()"
            all_args = ", ".join(args + kwargs)
            return f"{obj}.{turtle_method}({all_args})"

        # Fenster/Window Methoden — nur wenn Objekt als Fenster bekannt
        window_method = resolve_fenster_method(methode) if is_fenster else None
        if window_method:
            all_args = ", ".join(args + kwargs)
            return f"{obj}.{window_method}({all_args})"

        # Fallback: unverändert ausgeben
        all_args = ", ".join(args + kwargs)
        return f"{obj}.{methode}({all_args})"
