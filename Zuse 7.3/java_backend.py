# FILE: backends/java_backend.py
# Zuse → Java 11+ Transpiler
# Da Zuse dynamisch typisiert ist, nutzen wir Object + Cast-Helpers.

from backends.base_backend import BaseBackend
from builtin_i18n import resolve_maler_method, resolve_color, resolve_fenster_method, MALER_KLASSEN, FENSTER_KLASSEN

class JavaBackend(BaseBackend):
    LANGUAGE_NAME = "Java 11+"
    FILE_EXTENSION = ".java"

    def __init__(self):
        super().__init__()
        self._class_name = "ZuseProgramm"
        self._in_class = False
        self._top_level_stmts = []
        self._class_defs = []
        self._func_defs = []
        self._collecting = True  # True = top-level, sammle alles für main()
        self._declared_vars = set()  # Trackt bereits deklarierte Variablen

    def generate(self, ast):
        """Sonderlogik: Java braucht eine Wrapper-Klasse mit main()."""
        self._indent_level = 0
        self._lines = []
        self._top_level_stmts = []
        self._class_defs = []
        self._func_defs = []

        # Trenne Klassen/Funktionen von Top-Level-Statements
        for node in ast['body']:
            t = node.get('type')
            if t == 'KLASSEN_DEFINITION':
                self._class_defs.append(node)
            elif t == 'FUNKTIONS_DEFINITION':
                self._func_defs.append(node)
            else:
                self._top_level_stmts.append(node)

        # Header
        self._emit_raw("// Generiert von Zuse Transpiler")
        self._emit_raw("// Java 11+ - Kompilieren mit: javac ZuseProgramm.java")
        self._emit_raw("// Ausführen mit: java ZuseProgramm")
        self._emit_raw("")
        self._emit_raw("import java.util.*;")
        self._emit_raw("import java.util.Scanner;")
        self._emit_raw("")

        # Haupt-Klasse
        self._emit_raw(f"public class {self._class_name} {{")
        self._indent_level += 1

        # _ZuseMaler Stub (Turtle-Grafik)
        self._emit("// _ZuseMaler: Turtle-Grafik Stub")
        self._emit("// Für echte Grafik: Java Swing/JavaFX oder externe Bibliothek verwenden")
        self._emit("static class _ZuseMaler {")
        self._indent_level += 1
        self._emit("public void forward(double n)  { System.out.println(\"→ forward(\" + n + \")\"); }")
        self._emit("public void backward(double n) { System.out.println(\"← backward(\" + n + \")\"); }")
        self._emit("public void left(double n)     { System.out.println(\"↺ left(\" + n + \")\"); }")
        self._emit("public void right(double n)    { System.out.println(\"↻ right(\" + n + \")\"); }")
        self._emit("public void penup()            { System.out.println(\"penup\"); }")
        self._emit("public void pendown()          { System.out.println(\"pendown\"); }")
        self._emit("public void color(String c)    { System.out.println(\"color: \" + c); }")
        self._emit("public void pensize(double d)  { System.out.println(\"pensize: \" + d); }")
        self._emit("public void circle(double r)   { System.out.println(\"circle: \" + r); }")
        self._emit("public void done()             { System.out.println(\"[Fertig]\"); }")
        self._indent_level -= 1
        self._emit("}")
        self._emit()
        # _ZuseFenster Stub
        self._emit("// _ZuseFenster: Fenster/Window Stub")
        self._emit("static class _ZuseFenster {")
        self._indent_level += 1
        self._emit("public _ZuseFenster() {}")
        self._emit("public _ZuseFenster(String title, int w, int h) { System.out.println(\"[Fenster] \" + title); }")
        self._emit("public Object new_canvas(String color) { System.out.println(\"[Canvas] \" + color); return null; }")
        self._emit("public void press_key(String key, Object action) { System.out.println(\"[Key] \" + key); }")
        self._emit("public void after_time(int ms, Object fn) { System.out.println(\"[Timer] \" + ms + \"ms\"); }")
        self._emit("public void set_title(String t) { System.out.println(\"[Titel] \" + t); }")
        self._emit("public void close() { System.out.println(\"[Fenster geschlossen]\"); }")
        self._emit("public void run() { System.out.println(\"[Mainloop]\"); }")
        self._indent_level -= 1
        self._emit("}")
        self._emit()

        # Scanner für Eingaben
        self._emit("private static final Scanner _scanner = new Scanner(System.in);")
        self._emit()

        # Statische Hilfsmethoden
        self._gen_java_helpers()

        # Klassen-Definitionen als innere statische Klassen
        for cls in self._class_defs:
            self._gen_class(cls)

        # Funktions-Definitionen als statische Methoden
        for func in self._func_defs:
            self._gen_function(func)

        # main()-Methode mit allen Top-Level-Statements
        self._emit("public static void main(String[] args) {")
        self._indent_level += 1
        for stmt in self._top_level_stmts:
            self._gen_stmt(stmt)
        self._indent_level -= 1
        self._emit("}")

        self._indent_level -= 1
        self._emit_raw("}")

        return "\n".join(self._lines)

    def _gen_java_helpers(self):
        """Erzeugt Hilfsmethoden für dynamische Typen."""
        helpers = [
            "// Zuse Typ-Helfer",
            "static Object _add(Object a, Object b) {",
            "    if (a instanceof String || b instanceof String) return String.valueOf(a) + String.valueOf(b);",
            "    if (a instanceof Double || b instanceof Double) return ((Number)a).doubleValue() + ((Number)b).doubleValue();",
            "    return ((Number)a).longValue() + ((Number)b).longValue();",
            "}",
            "static Object _sub(Object a, Object b) { return ((Number)a).doubleValue() - ((Number)b).doubleValue(); }",
            "static Object _mul(Object a, Object b) { return ((Number)a).doubleValue() * ((Number)b).doubleValue(); }",
            "static Object _div(Object a, Object b) { return ((Number)a).doubleValue() / ((Number)b).doubleValue(); }",
            "static Object _pow(Object a, Object b) { return Math.pow(((Number)a).doubleValue(), ((Number)b).doubleValue()); }",
            "static Object _mod(Object a, Object b) { return ((Number)a).doubleValue() % ((Number)b).doubleValue(); }",
            "static boolean _truthy(Object v) { if (v == null) return false; if (v instanceof Boolean) return (Boolean)v; if (v instanceof Number) return ((Number)v).doubleValue() != 0; return !v.equals(\"\"); }",
            "@SuppressWarnings(\"unchecked\")",
            "static int _cmp(Object a, Object b) {",
            "    if (a instanceof Number && b instanceof Number) return Double.compare(((Number)a).doubleValue(), ((Number)b).doubleValue());",
            "    if (a instanceof String && b instanceof String) return ((String)a).compareTo((String)b);",
            "    if (a instanceof Comparable) return ((Comparable)a).compareTo(b);",
            "    throw new RuntimeException(\"Vergleich nicht möglich: \" + a.getClass().getSimpleName() + \" und \" + b.getClass().getSimpleName());",
            "}",
            "",
        ]
        for h in helpers:
            self._emit(h)

    def _gen_string(self, raw):
        return raw  # Java nutzt auch doppelte Anführungszeichen

    def _gen_variable_name(self, name):
        if name == 'SELBST':  return 'this'
        if name == 'wahr':    return 'true'
        if name == 'falsch':  return 'false'
        if name == 'PI':      return 'Math.PI'
        if name == 'E':       return 'Math.E'
        return name

    def _gen_not(self, node):
        val = self._gen_expr(node['wert'])
        return f"!_truthy({val})"

    def _gen_binary_op(self, l, r, op):
        java_ops = {
            '+':  f"_add({l}, {r})",
            '-':  f"_sub({l}, {r})",
            '*':  f"_mul({l}, {r})",
            '/':  f"_div({l}, {r})",
            '^':  f"_pow({l}, {r})",
            '%':  f"_mod({l}, {r})",
            '==': f"Objects.equals({l}, {r})",
            '!=': f"!Objects.equals({l}, {r})",
            '>':  f"(_cmp({l}, {r}) > 0)",
            '<':  f"(_cmp({l}, {r}) < 0)",
            '>=': f"(_cmp({l}, {r}) >= 0)",
            '<=': f"(_cmp({l}, {r}) <= 0)",
            'und': f"(_truthy({l}) && _truthy({r}))",
            'oder': f"(_truthy({l}) || _truthy({r}))",
        }
        return java_ops.get(op, f"({l} {op} {r})")

    def _gen_list_literal(self, items):
        return f"new ArrayList<>(Arrays.asList({items}))"

    def _gen_dict_literal(self, pairs):
        # Java Map via putAll
        entries = ", ".join(f"Map.entry({k}, {v})" for k, v in pairs)
        return f"new HashMap<>(Map.ofEntries({entries}))"

    def _gen_slice(self, obj, start, end):
        if start and end:
            return f"((List){obj}).subList({start}, {end})"
        elif start:
            return f"((List){obj}).subList({start}, ((List){obj}).size())"
        elif end:
            return f"((List){obj}).subList(0, {end})"
        return f"new ArrayList<>((List){obj})"

    def _gen_input(self, node):
        prompt = self._gen_expr(node['prompt'])
        if node['modus'] == 'zahl':
            return f"(System.out.print({prompt}), Double.parseDouble(_scanner.nextLine().trim()))"
        return f"(System.out.print({prompt}), _scanner.nextLine())"

    def _gen_lambda(self, node):
        params = ", ".join(f"Object {p}" for p in node['params'])
        body = self._gen_expr(node['body'])
        return f"(({params}) -> {body})"

    def _gen_super(self):
        return "super"

    def _map_builtin(self, name):
        if name in MALER_KLASSEN:
            return 'new _ZuseMaler()'
        if name in FENSTER_KLASSEN:
            return 'new _ZuseFenster()'
        builtins = {
            'str':   'String.valueOf',
            'int':   '(int)(double)(Double)',
            'float': 'Double.parseDouble',
            'len':   None,
            'typ':   None,
        }
        return builtins.get(name, name)

    def _gen_method_call(self, node):
        """Löst mehrsprachige Maler/Painter und Fenster/Window-Methoden für Java auf."""
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
                return "new java.util.Scanner(System.in).nextLine(); // done"
            all_args = ", ".join(args + kwargs)
            return f"{obj}.{turtle_method}({all_args})"

        window_method = resolve_fenster_method(methode)
        if window_method:
            all_args = ", ".join(args + kwargs)
            return f"{obj}.{window_method}({all_args})"

        all_args = ", ".join(args + kwargs)
        return f"{obj}.{methode}({all_args})"

    _JAVA_MATH_MAP = {
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

        # Mathe-Funktionen
        if name in self._JAVA_MATH_MAP:
            return f"{self._JAVA_MATH_MAP[name]}(((Number){args[0]}).doubleValue(){', ((Number)' + args[1] + ').doubleValue()' if len(args) > 1 else ''})"
        if name == 'RUNDEN':
            if len(args) == 1:
                return f"Math.round(((Number){args[0]}).doubleValue())"
            return f"(Math.round(((Number){args[0]}).doubleValue() * Math.pow(10, ((Number){args[1]}).intValue())) / Math.pow(10, ((Number){args[1]}).intValue()))"
        if name == 'SUMME' and len(args) == 1:
            return f"((List){args[0]}).stream().mapToDouble(o -> ((Number)o).doubleValue()).sum()"
        if name == 'ZUFALL_BEREICH' and len(args) == 2:
            return f"(new java.util.Random().nextInt(((Number){args[1]}).intValue() - ((Number){args[0]}).intValue() + 1) + ((Number){args[0]}).intValue())"

        if name == 'len' and len(args) == 1:
            a = args[0]
            return f"(({a} instanceof String) ? ((String){a}).length() : ((List){a}).size())"
        if name == 'str':
            return f"String.valueOf({args[0]})" if args else '""'
        if name == 'int':
            return f"(long)(((Number)({args[0]})).doubleValue())"
        if name == 'float':
            return f"((Number)({args[0]})).doubleValue()"
        if name == 'typ':
            return f"{args[0]}.getClass().getSimpleName()"
        if name == 'liste':
            return "new ArrayList<>()"
        if name == 'dict':
            return "new HashMap<>()"
        if name == 'BEREICH' or name == 'range':
            if len(args) == 1:
                return f"java.util.stream.IntStream.range(0, ((Number){args[0]}).intValue()).boxed().collect(java.util.stream.Collectors.toList())"
            if len(args) == 2:
                return f"java.util.stream.IntStream.range(((Number){args[0]}).intValue(), ((Number){args[1]}).intValue()).boxed().collect(java.util.stream.Collectors.toList())"
            if len(args) == 3:
                return f"java.util.stream.IntStream.iterate(((Number){args[0]}).intValue(), i -> i < ((Number){args[1]}).intValue(), i -> i + ((Number){args[2]}).intValue()).boxed().collect(java.util.stream.Collectors.toList())"

        # Text-Funktionen (4.2)
        if name == 'GROSSBUCHSTABEN' and len(args) == 1:
            return f"String.valueOf({args[0]}).toUpperCase()"
        if name == 'KLEINBUCHSTABEN' and len(args) == 1:
            return f"String.valueOf({args[0]}).toLowerCase()"
        if name == 'ERSETZE' and len(args) == 3:
            return f"String.valueOf({args[0]}).replace(String.valueOf({args[1]}), String.valueOf({args[2]}))"
        if name == 'TEILE':
            if len(args) == 1:
                return f"new ArrayList<>(Arrays.asList(String.valueOf({args[0]}).trim().split(\"\\\\s+\")))"
            return f"new ArrayList<>(Arrays.asList(String.valueOf({args[0]}).split(String.valueOf({args[1]}))))"
        if name == 'TRIMME' and len(args) == 1:
            return f"String.valueOf({args[0]}).trim()"
        if name == 'ENTHAELT' and len(args) == 2:
            return f"String.valueOf({args[0]}).contains(String.valueOf({args[1]}))"
        if name == 'LAENGE' and len(args) == 1:
            return f"(({args[0]} instanceof String) ? ((String){args[0]}).length() : ((List){args[0]}).size())"
        if name == 'FINDE' and len(args) == 2:
            return f"String.valueOf({args[0]}).indexOf(String.valueOf({args[1]}))"
        if name == 'BEGINNT_MIT' and len(args) == 2:
            return f"String.valueOf({args[0]}).startsWith(String.valueOf({args[1]}))"
        if name == 'ENDET_MIT' and len(args) == 2:
            return f"String.valueOf({args[0]}).endsWith(String.valueOf({args[1]}))"
        if name == 'VERBINDE' and len(args) >= 1:
            trenner = args[1] if len(args) > 1 else '""'
            return f"String.join({trenner}, (Iterable<? extends CharSequence>){args[0]})"

        # Listen-Funktionen (4.3)
        if name == 'SORTIEREN' and len(args) >= 1:
            return f"((List)((List){args[0]}).stream().sorted().collect(java.util.stream.Collectors.toList()))"
        if name == 'FILTERN' and len(args) == 2:
            return f"((List)((List){args[0]}).stream().filter(e -> _truthy({args[1]})).collect(java.util.stream.Collectors.toList()))"
        if name == 'UMWANDELN' and len(args) == 2:
            return f"((List)((List){args[0]}).stream().map(e -> e).collect(java.util.stream.Collectors.toList()))"
        if name == 'UMKEHREN' and len(args) == 1:
            return f"{{ List _r = new ArrayList<>((List){args[0]}); Collections.reverse(_r); _r; }}"
        if name == 'FLACH' and len(args) == 1:
            return f"((List)((List){args[0]}).stream().flatMap(e -> e instanceof List ? ((List)e).stream() : java.util.stream.Stream.of(e)).collect(java.util.stream.Collectors.toList()))"
        if name == 'EINDEUTIG' and len(args) == 1:
            return f"new ArrayList<>(new LinkedHashSet<>((List){args[0]}))"
        if name == 'AUFZAEHLEN' and len(args) == 1:
            return f"java.util.stream.IntStream.range(0, ((List){args[0]}).size()).mapToObj(i -> Arrays.asList(i, ((List){args[0]}).get(i))).collect(java.util.stream.Collectors.toList())"
        if name == 'ANHAENGEN' and len(args) >= 2:
            extra = ", ".join(args[1:])
            return f"{{ List _l = new ArrayList<>((List){args[0]}); _l.addAll(Arrays.asList({extra})); _l; }}"
        if name == 'BEREICH_LISTE' and len(args) == 1:
            return f"java.util.stream.IntStream.range(0, ((Number){args[0]}).intValue()).boxed().collect(java.util.stream.Collectors.toList())"

        # Datei-Funktionen (4.4)
        if name == 'LESE_DATEI' and len(args) >= 1:
            return f"java.nio.file.Files.readString(java.nio.file.Path.of(String.valueOf({args[0]})))"
        if name == 'SCHREIBE_DATEI' and len(args) >= 2:
            return f"java.nio.file.Files.writeString(java.nio.file.Path.of(String.valueOf({args[0]})), String.valueOf({args[1]}))"
        if name == 'ERGAENZE_DATEI' and len(args) >= 2:
            return f"java.nio.file.Files.writeString(java.nio.file.Path.of(String.valueOf({args[0]})), String.valueOf({args[1]}), java.nio.file.StandardOpenOption.APPEND)"
        if name == 'EXISTIERT' and len(args) == 1:
            return f"java.nio.file.Files.exists(java.nio.file.Path.of(String.valueOf({args[0]})))"
        if name == 'LESE_ZEILEN' and len(args) >= 1:
            return f"java.nio.file.Files.readAllLines(java.nio.file.Path.of(String.valueOf({args[0]})))"
        if name == 'LOESCHE_DATEI' and len(args) == 1:
            return f"java.nio.file.Files.delete(java.nio.file.Path.of(String.valueOf({args[0]})))"

        all_args = ", ".join(args + [f"/* {k}= */{self._gen_expr(v)}" for k, v in node['kwargs']])
        if name in MALER_KLASSEN:
            return f"new _ZuseMaler()"
        if name in FENSTER_KLASSEN:
            return f"new _ZuseFenster({all_args})"
        return f"{name}({all_args})"

    # ─── Statement-Generatoren ────────────────────────────────────────────────

    def _gen_multi_assignment(self, node):
        # Java has no destructuring — use temp array + individual assignments
        values = ", ".join(self._gen_expr(w) for w in node['werte'])
        self._emit(f"Object[] _tmp = new Object[]{{{values}}};")
        for i, z in enumerate(node['ziele']):
            target = self._gen_expr(z)
            self._emit(f"{target} = _tmp[{i}];")

    def generic_visit(self, node):
        """Java braucht Semikolon nach jedem Ausdruck-Statement."""
        expr_code = self._gen_expr(node)
        if expr_code:
            # Kein doppeltes Semikolon (done() gibt bereits '; // done' zurück)
            if expr_code.rstrip().endswith(';') or '// done' in expr_code:
                self._emit(expr_code)
            else:
                self._emit(expr_code + ';')

    def _gen_assignment(self, node):
        target = self._gen_expr(node['ziel'])
        value = self._gen_expr(node['wert'])
        if node['ziel']['type'] == 'VARIABLE':
            if target in self._declared_vars:
                self._emit(f"{target} = {value};")
            else:
                self._declared_vars.add(target)
                # Spezifischen Typ verwenden statt Object, damit Methoden aufrufbar sind
                if value == 'new _ZuseMaler()':
                    java_type = '_ZuseMaler'
                elif value.startswith('new _ZuseFenster('):
                    java_type = '_ZuseFenster'
                else:
                    java_type = 'Object'
                self._emit(f"{java_type} {target} = {value};")
        else:
            self._emit(f"{target} = {value};")

    def _gen_print(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"System.out.println({val});")

    def _gen_return(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"return {val};")

    def _gen_if(self, node):
        for i, (cond_node, block) in enumerate(node['faelle']):
            kw = "if" if i == 0 else "} else if"
            cond = self._gen_expr(cond_node)
            self._emit(f"{kw} (_truthy({cond})) {{")
            self._indent_level += 1
            self._gen_block(block)
            self._indent_level -= 1
        if node.get('sonst_koerper'):
            self._emit("} else {")
            self._indent_level += 1
            self._gen_block(node['sonst_koerper'])
            self._indent_level -= 1
        self._emit("}")

    def _gen_while(self, node):
        cond = self._gen_expr(node['bedingung'])
        self._emit(f"while (_truthy({cond})) {{")
        self._indent_level += 1
        self._gen_block(node['koerper'])
        self._indent_level -= 1
        self._emit("}")

    def _gen_for(self, node):
        var = node['variable']
        lst = self._gen_expr(node['liste'])
        self._emit(f"for (Object {var} : (Iterable<?>){lst}) {{")
        self._indent_level += 1
        self._gen_block(node['koerper'])
        self._indent_level -= 1
        self._emit("}")

    def _gen_function(self, node):
        params = ", ".join(f"Object {p}" for p in node['parameter'])
        self._emit(f"static Object {node['name']}({params}) {{")
        self._indent_level += 1
        if not node['body']:
            self._emit("return null;")
        else:
            # Prüfe ob letztes Statement bereits ein Return ist
            has_return = (node['body'] and
                          node['body'][-1].get('type') == 'ERGEBNIS_ANWEISUNG')
            self._gen_block(node['body'])
            if not has_return:
                self._emit("return null;")
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_class(self, node):
        parent = f" extends {node['elternklasse']}" if node['elternklasse'] else ""
        self._emit(f"static class {node['name']}{parent} {{")
        self._indent_level += 1
        for m in node['methoden']:
            self._gen_method(m, node['name'])
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_method(self, m, class_name=None):
        method_name = m['name']
        is_constructor = method_name in ['ERSTELLE', 'NEW', 'CREAR', 'CRIAR', 'CREER', 'CREARE']
        # Parameter ohne SELBST/MEIN/SELF/THIS
        raw_params = [p for p in m['parameter'] if p not in ['SELBST', 'MEIN', 'self', 'this', 'SELF', 'THIS']]
        params = ", ".join(f"Object {p}" for p in raw_params)
        if is_constructor and class_name:
            self._emit(f"public {class_name}({params}) {{")
            self._indent_level += 1
            self._gen_block(m['body'])
            self._indent_level -= 1
            self._emit("}")
        else:
            self._emit(f"Object {method_name}({params}) {{")
            self._indent_level += 1
            self._gen_block(m['body'])
            has_return = (m['body'] and
                          m['body'][-1].get('type') == 'ERGEBNIS_ANWEISUNG')
            if not has_return:
                self._emit("return null;")
            self._indent_level -= 1
            self._emit("}")
        self._emit()

    def _gen_import(self, node):
        self._emit(f"// import {node['modul']}; // Manuell als Java-Abhängigkeit hinzufügen")

    def _gen_global(self, node):
        self._emit(f"// global {node['name']} → Als statisches Feld in der Klasse deklarieren")

    def _gen_break(self, node):
        self._emit("break;")

    def _gen_continue(self, node):
        self._emit("continue;")

    def _gen_try(self, node):
        fehler_var = node.get('fehler_var', '_e')
        self._emit("try {")
        self._indent_level += 1
        self._gen_block(node['versuche_block'])
        self._indent_level -= 1
        self._emit(f"}} catch (Exception {fehler_var or '_e'}) {{")
        self._indent_level += 1
        self._gen_block(node['fange_block'])
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
