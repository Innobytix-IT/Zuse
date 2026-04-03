# FILE: backends/csharp_backend.py
# Zuse → C# 10+ Transpiler
# Nutzt 'dynamic' für dynamische Typen - perfekte Brücke für Zuse.

from backends.base_backend import BaseBackend

class CSharpBackend(BaseBackend):
    LANGUAGE_NAME = "C# 10+"
    FILE_EXTENSION = ".cs"

    def __init__(self):
        super().__init__()
        self._class_defs = []
        self._func_defs = []
        self._top_level_stmts = []
        self._declared_vars = set()  # Trackt bereits deklarierte Variablen

    def generate(self, ast):
        self._indent_level = 0
        self._lines = []
        self._class_defs = []
        self._func_defs = []
        self._top_level_stmts = []

        # Trenne Typen von Top-Level-Statements
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
        self._emit_raw("// C# 10+ - Kompilieren mit: dotnet run oder csc ZuseProgramm.cs")
        self._emit_raw("")
        self._emit_raw("using System;")
        self._emit_raw("using System.Collections.Generic;")
        self._emit_raw("using System.Linq;")
        self._emit_raw("")
        self._emit_raw("namespace ZuseProgramm")
        self._emit_raw("{")
        self._indent_level += 1

        # Klassen-Definitionen
        for cls in self._class_defs:
            self._gen_class(cls)

        # Haupt-Programm-Klasse
        self._emit("class Program")
        self._emit("{")
        self._indent_level += 1

        # Funktionen als statische Methoden
        for func in self._func_defs:
            self._gen_function(func)

        # main()
        self._emit("static void Main(string[] args)")
        self._emit("{")
        self._indent_level += 1
        for stmt in self._top_level_stmts:
            self._gen_stmt(stmt)
        self._indent_level -= 1
        self._emit("}")

        self._indent_level -= 1
        self._emit("}")  # class Program

        self._indent_level -= 1
        self._emit_raw("}")  # namespace

        return "\n".join(self._lines)

    def _gen_string(self, raw):
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
        return f"!((bool){val})"

    def _gen_binary_op(self, l, r, op):
        cs_ops = {
            '^':    f"Math.Pow((double){l}, (double){r})",
            '==':   f"Equals({l}, {r})",
            '!=':   f"!Equals({l}, {r})",
            'und':  f"((bool){l} && (bool){r})",
            'oder': f"((bool){l} || (bool){r})",
        }
        if op in cs_ops:
            return cs_ops[op]
        return f"({l} {op} {r})"

    def _gen_list_literal(self, items):
        return f"new List<dynamic> {{ {items} }}"

    def _gen_dict_literal(self, pairs):
        entries = ", ".join(f"{{ {k}, {v} }}" for k, v in pairs)
        return f"new Dictionary<dynamic, dynamic> {{ {entries} }}"

    def _gen_slice(self, obj, start, end):
        if start and end:
            return f"((List<dynamic>){obj}).GetRange({start}, {end} - {start})"
        elif start:
            return f"((List<dynamic>){obj}).Skip({start}).ToList()"
        elif end:
            return f"((List<dynamic>){obj}).Take({end}).ToList()"
        return f"new List<dynamic>((List<dynamic>){obj})"

    def _gen_input(self, node):
        prompt = self._gen_expr(node['prompt'])
        if node['modus'] == 'zahl':
            return f"(Console.Write({prompt}), double.Parse(Console.ReadLine()))"
        return f"(Console.Write({prompt}), Console.ReadLine())"

    def _gen_lambda(self, node):
        params = ", ".join(f"dynamic {p}" for p in node['params'])
        body = self._gen_expr(node['body'])
        return f"(({params}) => {body})"

    def _gen_super(self):
        return "base"

    def _map_builtin(self, name):
        builtins = {
            'str':   'Convert.ToString',
            'int':   'Convert.ToInt64',
            'float': 'Convert.ToDouble',
            'len':   None,  # special
            'typ':   None,  # special
            'liste': 'new List<dynamic>',
            'dict':  'new Dictionary<dynamic, dynamic>',
        }
        return builtins.get(name, name)

    _CS_MATH_MAP = {
        'WURZEL': 'Math.Sqrt', 'SINUS': 'Math.Sin', 'COSINUS': 'Math.Cos',
        'TANGENS': 'Math.Tan', 'ABSOLUT': 'Math.Abs',
        'BODEN': 'Math.Floor', 'DECKE': 'Math.Ceiling',
        'POTENZ': 'Math.Pow', 'LOGARITHMUS': 'Math.Log',
        'MINIMUM': 'Math.Min', 'MAXIMUM': 'Math.Max',
    }

    def _gen_func_call(self, node):
        name = node['name']
        args = [self._gen_expr(a) for a in node['args']]

        # Mathe-Funktionen
        if name in self._CS_MATH_MAP:
            cast_args = ", ".join(f"(double){a}" for a in args)
            return f"{self._CS_MATH_MAP[name]}({cast_args})"
        if name == 'RUNDEN':
            if len(args) == 1:
                return f"Math.Round((double){args[0]})"
            return f"Math.Round((double){args[0]}, (int){args[1]})"
        if name == 'SUMME' and len(args) == 1:
            return f"((IEnumerable<dynamic>){args[0]}).Sum(x => (double)x)"
        if name == 'ZUFALL':
            return "new Random().NextDouble()"
        if name == 'ZUFALL_BEREICH' and len(args) == 2:
            return f"new Random().Next((int){args[0]}, (int){args[1]} + 1)"

        if name == 'len' and len(args) == 1:
            a = args[0]
            return f"((dynamic){a} is string ? ((string)(dynamic){a}).Length : ((ICollection<dynamic>)(dynamic){a}).Count)"
        if name == 'str':
            return f"Convert.ToString({args[0]})" if args else '""'
        if name == 'int':
            return f"Convert.ToInt64({args[0]})"
        if name == 'float':
            return f"Convert.ToDouble({args[0]})"
        if name == 'typ':
            return f"{args[0]}.GetType().Name"
        if name == 'liste':
            return "new List<dynamic>()"
        if name == 'dict':
            return "new Dictionary<dynamic, dynamic>()"

        if name == 'BEREICH':
            if len(args) == 1:
                return f"Enumerable.Range(0, (int){args[0]}).Cast<dynamic>().ToList()"
            if len(args) == 2:
                return f"Enumerable.Range((int){args[0]}, (int)({args[1]} - {args[0]})).Cast<dynamic>().ToList()"
            if len(args) == 3:
                return f"Enumerable.Range(0, ((int){args[1]} - (int){args[0]} + (int){args[2]} - 1) / (int){args[2]}).Select(i => (dynamic)((int){args[0]} + i * (int){args[2]})).ToList()"

        # Text-Funktionen (4.2)
        if name == 'GROSSBUCHSTABEN' and len(args) == 1:
            return f"Convert.ToString({args[0]}).ToUpper()"
        if name == 'KLEINBUCHSTABEN' and len(args) == 1:
            return f"Convert.ToString({args[0]}).ToLower()"
        if name == 'ERSETZE' and len(args) == 3:
            return f"Convert.ToString({args[0]}).Replace(Convert.ToString({args[1]}), Convert.ToString({args[2]}))"
        if name == 'TEILE':
            if len(args) == 1:
                return f"Convert.ToString({args[0]}).Split((string[])null, StringSplitOptions.RemoveEmptyEntries).Cast<dynamic>().ToList()"
            return f"Convert.ToString({args[0]}).Split(new string[] {{ Convert.ToString({args[1]}) }}, StringSplitOptions.None).Cast<dynamic>().ToList()"
        if name == 'TRIMME' and len(args) == 1:
            return f"Convert.ToString({args[0]}).Trim()"
        if name == 'ENTHAELT' and len(args) == 2:
            return f"Convert.ToString({args[0]}).Contains(Convert.ToString({args[1]}))"
        if name == 'LAENGE' and len(args) == 1:
            return f"(({args[0]} is string) ? ((string){args[0]}).Length : ((ICollection<dynamic>){args[0]}).Count)"
        if name == 'FINDE' and len(args) == 2:
            return f"Convert.ToString({args[0]}).IndexOf(Convert.ToString({args[1]}))"
        if name == 'BEGINNT_MIT' and len(args) == 2:
            return f"Convert.ToString({args[0]}).StartsWith(Convert.ToString({args[1]}))"
        if name == 'ENDET_MIT' and len(args) == 2:
            return f"Convert.ToString({args[0]}).EndsWith(Convert.ToString({args[1]}))"
        if name == 'VERBINDE' and len(args) >= 1:
            trenner = args[1] if len(args) > 1 else '""'
            return f"string.Join({trenner}, ((IEnumerable<dynamic>){args[0]}).Select(e => Convert.ToString(e)))"

        # Listen-Funktionen (4.3)
        if name == 'SORTIEREN' and len(args) >= 1:
            return f"((IEnumerable<dynamic>){args[0]}).OrderBy(x => x).ToList()"
        if name == 'FILTERN' and len(args) == 2:
            return f"((IEnumerable<dynamic>){args[0]}).Where((Func<dynamic, bool>){args[1]}).ToList()"
        if name == 'UMWANDELN' and len(args) == 2:
            return f"((IEnumerable<dynamic>){args[0]}).Select((Func<dynamic, dynamic>){args[1]}).ToList()"
        if name == 'UMKEHREN' and len(args) == 1:
            return f"((IEnumerable<dynamic>){args[0]}).Reverse().ToList()"
        if name == 'FLACH' and len(args) == 1:
            return f"((IEnumerable<dynamic>){args[0]}).SelectMany(e => e is IEnumerable<dynamic> ? (IEnumerable<dynamic>)e : new List<dynamic>{{e}}).ToList()"
        if name == 'EINDEUTIG' and len(args) == 1:
            return f"((IEnumerable<dynamic>){args[0]}).Distinct().ToList()"
        if name == 'AUFZAEHLEN' and len(args) == 1:
            return f"((IEnumerable<dynamic>){args[0]}).Select((v, i) => (dynamic)new List<dynamic>{{i, v}}).ToList()"
        if name == 'ANHAENGEN' and len(args) >= 2:
            extra = ", ".join(args[1:])
            return f"((IEnumerable<dynamic>){args[0]}).Concat(new List<dynamic>{{{extra}}}).ToList()"
        if name == 'BEREICH_LISTE' and len(args) == 1:
            return f"Enumerable.Range(0, (int){args[0]}).Cast<dynamic>().ToList()"

        # Datei-Funktionen (4.4)
        if name == 'LESE_DATEI' and len(args) >= 1:
            return f"System.IO.File.ReadAllText(Convert.ToString({args[0]}))"
        if name == 'SCHREIBE_DATEI' and len(args) >= 2:
            return f"System.IO.File.WriteAllText(Convert.ToString({args[0]}), Convert.ToString({args[1]}))"
        if name == 'ERGAENZE_DATEI' and len(args) >= 2:
            return f"System.IO.File.AppendAllText(Convert.ToString({args[0]}), Convert.ToString({args[1]}))"
        if name == 'EXISTIERT' and len(args) == 1:
            return f"System.IO.File.Exists(Convert.ToString({args[0]}))"
        if name == 'LESE_ZEILEN' and len(args) >= 1:
            return f"System.IO.File.ReadAllLines(Convert.ToString({args[0]})).Cast<dynamic>().ToList()"
        if name == 'LOESCHE_DATEI' and len(args) == 1:
            return f"System.IO.File.Delete(Convert.ToString({args[0]}))"

        all_args = ", ".join(args + [f"/* {k}= */{self._gen_expr(v)}" for k, v in node['kwargs']])
        return f"{name}({all_args})"

    # ─── Statement-Generatoren ────────────────────────────────────────────────

    def _gen_multi_assignment(self, node):
        # C# tuple deconstruction: var (a, b) = (1, 2);
        targets = ", ".join(self._gen_expr(z) for z in node['ziele'])
        values = ", ".join(self._gen_expr(w) for w in node['werte'])
        self._emit(f"var ({targets}) = ({values});")

    def _gen_assignment(self, node):
        target = self._gen_expr(node['ziel'])
        value = self._gen_expr(node['wert'])
        if node['ziel']['type'] == 'VARIABLE':
            if target in self._declared_vars:
                self._emit(f"{target} = {value};")
            else:
                self._declared_vars.add(target)
                self._emit(f"dynamic {target} = {value};")
        else:
            self._emit(f"{target} = {value};")

    def _gen_print(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"Console.WriteLine({val});")

    def _gen_return(self, node):
        val = self._gen_expr(node['wert'])
        self._emit(f"return {val};")

    def _gen_if(self, node):
        for i, (cond_node, block) in enumerate(node['faelle']):
            kw = "if" if i == 0 else "else if"
            cond = self._gen_expr(cond_node)
            self._emit(f"{kw} ({cond})")
            self._emit("{")
            self._indent_level += 1
            self._gen_block(block)
            self._indent_level -= 1
            self._emit("}")
        if node.get('sonst_koerper'):
            self._emit("else")
            self._emit("{")
            self._indent_level += 1
            self._gen_block(node['sonst_koerper'])
            self._indent_level -= 1
            self._emit("}")

    def _gen_while(self, node):
        cond = self._gen_expr(node['bedingung'])
        self._emit(f"while ({cond})")
        self._emit("{")
        self._indent_level += 1
        self._gen_block(node['koerper'])
        self._indent_level -= 1
        self._emit("}")

    def _gen_for(self, node):
        var = node['variable']
        lst = self._gen_expr(node['liste'])
        self._emit(f"foreach (dynamic {var} in {lst})")
        self._emit("{")
        self._indent_level += 1
        self._gen_block(node['koerper'])
        self._indent_level -= 1
        self._emit("}")

    def _gen_function(self, node):
        params = ", ".join(f"dynamic {p}" for p in node['parameter'])
        self._emit(f"static dynamic {node['name']}({params})")
        self._emit("{")
        self._indent_level += 1
        if not node['body']:
            self._emit("return null;")
        else:
            has_return = (node['body'] and
                          node['body'][-1].get('type') == 'ERGEBNIS_ANWEISUNG')
            self._gen_block(node['body'])
            if not has_return:
                self._emit("return null;")
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_class(self, node):
        parent = f" : {node['elternklasse']}" if node['elternklasse'] else ""
        self._emit(f"class {node['name']}{parent}")
        self._emit("{")
        self._indent_level += 1
        for m in node['methoden']:
            self._gen_method(m, class_name=node['name'])
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_method(self, m, class_name=None):
        method_name = m['name']
        is_ctor = method_name in ['ERSTELLE', 'NEW', 'CREAR', 'CRIAR', 'CREER', 'CREARE']
        params = ", ".join(f"dynamic {p}" for p in m['parameter'])
        if is_ctor and class_name:
            self._emit(f"public {class_name}({params})")
        elif is_ctor:
            self._emit(f"public _Klasse_({params})")
        else:
            self._emit(f"public dynamic {method_name}({params})")
        self._emit("{")
        self._indent_level += 1
        self._gen_block(m['body'])
        if not is_ctor:
            has_return = (m['body'] and
                          m['body'][-1].get('type') == 'ERGEBNIS_ANWEISUNG')
            if not has_return:
                self._emit("return null;")
        self._indent_level -= 1
        self._emit("}")
        self._emit()

    def _gen_import(self, node):
        self._emit(f"// using {node['modul']}; // Als NuGet-Paket hinzufügen falls nötig")

    def _gen_global(self, node):
        self._emit(f"// static dynamic {node['name']}; // Als statisches Feld deklarieren")

    def _gen_break(self, node):
        self._emit("break;")

    def _gen_continue(self, node):
        self._emit("continue;")

    def _gen_try(self, node):
        fehler_var = node.get('fehler_var', '_e')
        self._emit("try")
        self._emit("{")
        self._indent_level += 1
        self._gen_block(node['versuche_block'])
        self._indent_level -= 1
        self._emit("}")
        self._emit(f"catch (Exception {fehler_var or '_e'})")
        self._emit("{")
        self._indent_level += 1
        self._gen_block(node['fange_block'])
        self._indent_level -= 1
        self._emit("}")

    def _gen_switch(self, node):
        ausdruck = self._gen_expr(node['ausdruck'])
        self._emit(f"switch ({ausdruck})")
        self._emit("{")
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
