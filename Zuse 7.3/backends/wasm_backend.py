# FILE: backends/wasm_backend.py
# Zuse → WebAssembly Text Format (WAT) Transpiler
# Generiert .wat Dateien die mit wat2wasm kompiliert werden können.
# Numerische Operationen werden nativ in WASM abgebildet.
# Strings und AUSGABE nutzen importierte Host-Funktionen.

from backends.base_backend import BaseBackend, TranspilerError


class WasmBackend(BaseBackend):
    LANGUAGE_NAME = "WebAssembly (WAT)"
    FILE_EXTENSION = ".wat"

    def __init__(self):
        super().__init__()
        self._locals = {}          # Variable -> Index
        self._local_counter = 0
        self._func_defs = []
        self._top_level_stmts = []
        self._string_table = []    # String-Literale für Data-Section
        self._string_offsets = {}  # String -> Offset
        self._data_offset = 0

    def generate(self, ast):
        self._indent_level = 0
        self._lines = []
        self._locals = {}
        self._local_counter = 0
        self._func_defs = []
        self._top_level_stmts = []
        self._string_table = []
        self._string_offsets = {}
        self._data_offset = 1024  # Strings starten bei Offset 1024

        # Trenne Funktionen von Top-Level-Statements
        for node in ast['body']:
            t = node.get('type')
            if t == 'FUNKTIONS_DEFINITION':
                self._func_defs.append(node)
            else:
                self._top_level_stmts.append(node)

        # Ersten Pass: Strings sammeln
        self._collect_strings(ast['body'])

        # WAT generieren
        self._emit_raw(";; Generiert von Zuse Transpiler")
        self._emit_raw(";; WebAssembly Text Format (WAT)")
        self._emit_raw(";; Kompilieren: wat2wasm programm.wat -o programm.wasm")
        self._emit_raw("")
        self._emit_raw("(module")
        self._indent_level += 1

        # Imports: Host-Funktionen fuer I/O
        self._emit(';; Importierte Host-Funktionen')
        self._emit('(import "env" "print_i32" (func $print_i32 (param i32)))')
        self._emit('(import "env" "print_f64" (func $print_f64 (param f64)))')
        self._emit('(import "env" "print_str" (func $print_str (param i32) (param i32)))')
        self._emit("")

        # Memory
        self._emit(';; Linearer Speicher (1 Page = 64KB)')
        self._emit('(memory (export "memory") 1)')
        self._emit("")

        # Data-Section fuer Strings
        if self._string_table:
            self._emit(';; String-Daten')
            for text, offset in self._string_table:
                escaped = text.replace('\\', '\\\\').replace('"', '\\"')
                self._emit(f'(data (i32.const {offset}) "{escaped}")')
            self._emit("")

        # Mathe-Hilfsfunktionen
        self._emit_math_helpers()

        # Benutzer-Funktionen
        for func in self._func_defs:
            self._gen_function(func)

        # Hauptprogramm (_start)
        self._locals = {}
        self._local_counter = 0
        self._emit('(func $main (export "_start")')
        self._indent_level += 1

        # Lokale Variablen vorab deklarieren
        local_decls = self._pre_scan_locals(self._top_level_stmts)
        for name in local_decls:
            idx = self._get_or_create_local(name)
        if self._locals:
            decls = " ".join(f"(local ${name} f64)" for name in self._locals)
            self._emit(decls)

        for stmt in self._top_level_stmts:
            self._gen_stmt(stmt)

        self._indent_level -= 1
        self._emit(")")
        self._emit("")

        self._indent_level -= 1
        self._emit_raw(")")

        return "\n".join(self._lines)

    # ─── String-Sammlung ──────────────────────────────────────────────────

    def _collect_strings(self, nodes):
        """Sammelt alle String-Literale für die Data-Section."""
        for node in nodes:
            self._collect_strings_node(node)

    def _collect_strings_node(self, node):
        if node is None or not isinstance(node, dict):
            return
        if node.get('type') == 'STRING_LITERAL':
            text = node['wert'].strip('"')
            if text not in self._string_offsets:
                self._string_offsets[text] = self._data_offset
                self._string_table.append((text, self._data_offset))
                self._data_offset += len(text.encode('utf-8'))
        for key, val in node.items():
            if isinstance(val, dict):
                self._collect_strings_node(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        self._collect_strings_node(item)
                    elif isinstance(item, (list, tuple)):
                        for sub in item:
                            if isinstance(sub, dict):
                                self._collect_strings_node(sub)

    # ─── Lokale Variablen ────────────────────────────────────────────────

    def _get_or_create_local(self, name):
        if name not in self._locals:
            self._locals[name] = self._local_counter
            self._local_counter += 1
        return self._locals[name]

    def _pre_scan_locals(self, stmts):
        """Scannt voraus welche Variablen benötigt werden."""
        names = set()
        for stmt in stmts:
            if stmt.get('type') == 'ZUWEISUNG':
                ziel = stmt['ziel']
                if ziel.get('type') == 'VARIABLE':
                    names.add(ziel['name'])
        return sorted(names)

    # ─── Mathe-Helfer ────────────────────────────────────────────────────

    def _emit_math_helpers(self):
        self._emit(';; Mathe-Hilfsfunktionen')
        self._emit('(func $abs_f64 (param $x f64) (result f64)')
        self._indent_level += 1
        self._emit('(f64.abs (local.get $x))')
        self._indent_level -= 1
        self._emit(')')
        self._emit('(func $min_f64 (param $a f64) (param $b f64) (result f64)')
        self._indent_level += 1
        self._emit('(f64.min (local.get $a) (local.get $b))')
        self._indent_level -= 1
        self._emit(')')
        self._emit('(func $max_f64 (param $a f64) (param $b f64) (result f64)')
        self._indent_level += 1
        self._emit('(f64.max (local.get $a) (local.get $b))')
        self._indent_level -= 1
        self._emit(')')
        self._emit("")

    # ─── Ausdruecke ──────────────────────────────────────────────────────

    def _gen_expr(self, node):
        if node is None:
            return "f64.const 0"
        t = node.get('type')
        if t == 'ZAHL_LITERAL':
            return f"f64.const {node['wert']}"
        if t == 'STRING_LITERAL':
            text = node['wert'].strip('"')
            offset = self._string_offsets.get(text, 0)
            length = len(text.encode('utf-8'))
            return f"i32.const {offset} ;; str \"{text[:20]}\" len={length}"
        if t == 'VARIABLE':
            name = node['name']
            if name == 'PI':
                return "f64.const 3.141592653589793"
            if name == 'E':
                return "f64.const 2.718281828459045"
            if name == 'wahr':
                return "f64.const 1"
            if name == 'falsch':
                return "f64.const 0"
            self._get_or_create_local(name)
            return f"local.get ${name}"
        if t == 'BINÄRER_AUSDRUCK':
            return self._gen_binary(node)
        if t == 'UNAER_MINUS':
            return f"f64.neg ({self._gen_expr(node['wert'])})"
        if t == 'FUNKTIONS_AUFRUF':
            return self._gen_func_call_expr(node)
        # Fallback
        raise TranspilerError(f"WASM-Backend: Ausdruckstyp '{t}' wird nicht unterstützt")

    def _gen_binary(self, node):
        l = self._gen_expr(node['links'])
        r = self._gen_expr(node['rechts'])
        op = node['operator']
        ops = {
            '+': 'f64.add', '-': 'f64.sub',
            '*': 'f64.mul', '/': 'f64.div',
            '%': None,  # kein direkter WASM-Op
            '==': 'f64.eq', '!=': 'f64.ne',
            '<': 'f64.lt', '>': 'f64.gt',
            '<=': 'f64.le', '>=': 'f64.ge',
        }
        wasm_op = ops.get(op)
        if wasm_op:
            return f"({wasm_op} ({l}) ({r}))"
        if op == '^':
            # Potenz: kein nativer WASM-Op, als Schleife nicht praktikabel
            return f"({l}) ;; pow nicht nativ in WASM"
        if op == '%':
            # Modulo über Truncation
            return f"(f64.sub ({l}) (f64.mul (f64.trunc (f64.div ({l}) ({r}))) ({r})))"
        return f"({l}) ;; operator {op}"

    def _gen_func_call_expr(self, node):
        name = node['name']
        args = node['args']

        wasm_math = {
            'WURZEL': 'f64.sqrt', 'ABSOLUT': 'f64.abs',
            'BODEN': 'f64.floor', 'DECKE': 'f64.ceil',
        }
        if name in wasm_math and len(args) == 1:
            return f"({wasm_math[name]} ({self._gen_expr(args[0])}))"
        if name == 'MINIMUM' and len(args) == 2:
            return f"(call $min_f64 ({self._gen_expr(args[0])}) ({self._gen_expr(args[1])}))"
        if name == 'MAXIMUM' and len(args) == 2:
            return f"(call $max_f64 ({self._gen_expr(args[0])}) ({self._gen_expr(args[1])}))"
        if name in self._locals or any(f['name'] == name for f in self._func_defs):
            call_args = " ".join(f"({self._gen_expr(a)})" for a in args)
            return f"(call ${name} {call_args})"

        # Fallback: erste Arg zurückgeben
        if args:
            return self._gen_expr(args[0])
        return "f64.const 0"

    # ─── Statements ──────────────────────────────────────────────────────

    def _gen_stmt(self, node):
        if node is None:
            return
        t = node.get('type')
        if t == 'ZUWEISUNG':
            self._gen_assignment(node)
        elif t == 'AUSGABE_ANWEISUNG':
            self._gen_print(node)
        elif t == 'WENN_ANWEISUNG':
            self._gen_if(node)
        elif t == 'SCHLEIFE_SOLANGE':
            self._gen_while(node)
        elif t == 'SCHLEIFE_FÜR':
            self._gen_for(node)
        elif t == 'ERGEBNIS_ANWEISUNG':
            self._gen_return(node)
        elif t == 'ABBRUCH_ANWEISUNG':
            self._emit("br $loop_exit")
        elif t == 'WEITER_ANWEISUNG':
            self._emit("br $loop_continue")
        elif t == 'WAEHLE_ANWEISUNG':
            self._gen_switch(node)
        elif t == 'VERSUCHE_ANWEISUNG':
            self._gen_try(node)
        else:
            raise TranspilerError(f"WASM-Backend: Anweisungstyp '{t}' wird nicht unterstützt")

    def _gen_assignment(self, node):
        ziel = node['ziel']
        if ziel.get('type') == 'VARIABLE':
            name = ziel['name']
            self._get_or_create_local(name)
            expr = self._gen_expr(node['wert'])
            self._emit(f"({expr})")
            self._emit(f"local.set ${name}")

    def _gen_print(self, node):
        wert = node['wert']
        if wert.get('type') == 'STRING_LITERAL':
            text = wert['wert'].strip('"')
            offset = self._string_offsets.get(text, 0)
            length = len(text.encode('utf-8'))
            self._emit(f"(call $print_str (i32.const {offset}) (i32.const {length}))")
        elif wert.get('type') == 'ZAHL_LITERAL':
            self._emit(f"(call $print_f64 (f64.const {wert['wert']}))")
        else:
            expr = self._gen_expr(wert)
            self._emit(f"(call $print_f64 ({expr}))")

    def _gen_if(self, node):
        for i, (cond, block) in enumerate(node['faelle']):
            cond_expr = self._gen_expr(cond)
            # Bool-Konvertierung: f64 -> i32
            self._emit(f"(if (i32.trunc_f64_s ({cond_expr}))")
            self._indent_level += 1
            self._emit("(then")
            self._indent_level += 1
            for stmt in block:
                self._gen_stmt(stmt)
            self._indent_level -= 1
            self._emit(")")
        # Sonst-Block
        if node.get('sonst_koerper'):
            self._emit("(else")
            self._indent_level += 1
            for stmt in node['sonst_koerper']:
                self._gen_stmt(stmt)
            self._indent_level -= 1
            self._emit(")")
        # Alle if-Klammern schliessen
        for _ in node['faelle']:
            self._indent_level -= 1
            self._emit(")")

    def _gen_while(self, node):
        self._emit("(block $loop_exit")
        self._indent_level += 1
        self._emit("(loop $loop_continue")
        self._indent_level += 1
        # Bedingung prüfen, bei false -> exit
        cond_expr = self._gen_expr(node['bedingung'])
        self._emit(f"(br_if $loop_exit (i32.eqz (i32.trunc_f64_s ({cond_expr}))))")
        for stmt in node['koerper']:
            self._gen_stmt(stmt)
        self._emit("(br $loop_continue)")
        self._indent_level -= 1
        self._emit(")")
        self._indent_level -= 1
        self._emit(")")

    def _gen_for(self, node):
        # FUR i IN BEREICH(n) → Zähler-Schleife
        var = node['variable']
        self._get_or_create_local(var)
        self._get_or_create_local("__for_end")

        liste = node['liste']
        # Versuche BEREICH zu erkennen
        if (liste.get('type') == 'FUNKTIONS_AUFRUF' and
                liste['name'] in ('BEREICH', 'range') and liste['args']):
            args = liste['args']
            if len(args) == 1:
                self._emit(f"(f64.const 0)")
                self._emit(f"local.set ${var}")
                self._emit(f"({self._gen_expr(args[0])})")
                self._emit(f"local.set $__for_end")
            elif len(args) >= 2:
                self._emit(f"({self._gen_expr(args[0])})")
                self._emit(f"local.set ${var}")
                self._emit(f"({self._gen_expr(args[1])})")
                self._emit(f"local.set $__for_end")
        else:
            raise TranspilerError("WASM-Backend: Listen-Iteration wird noch nicht unterstützt, nur BEREICH()")

        self._emit("(block $loop_exit")
        self._indent_level += 1
        self._emit("(loop $loop_continue")
        self._indent_level += 1
        self._emit(f"(br_if $loop_exit (i32.trunc_f64_s (f64.ge (local.get ${var}) (local.get $__for_end))))")
        for stmt in node['koerper']:
            self._gen_stmt(stmt)
        # Inkrement
        self._emit(f"(f64.add (local.get ${var}) (f64.const 1))")
        self._emit(f"local.set ${var}")
        self._emit("(br $loop_continue)")
        self._indent_level -= 1
        self._emit(")")
        self._indent_level -= 1
        self._emit(")")

    def _gen_function(self, node):
        old_locals = self._locals.copy()
        old_counter = self._local_counter
        self._locals = {}
        self._local_counter = 0

        params = " ".join(f"(param ${p} f64)" for p in node['parameter'])
        self._emit(f'(func ${node["name"]} {params} (result f64)')
        self._indent_level += 1

        # Parameter als lokale Variablen registrieren
        for p in node['parameter']:
            self._get_or_create_local(p)

        # Lokale Variablen vordeklarieren
        local_names = self._pre_scan_locals(node['body'])
        for name in local_names:
            if name not in self._locals:
                self._get_or_create_local(name)
        extra_locals = [n for n in self._locals if n not in node['parameter']]
        if extra_locals:
            decls = " ".join(f"(local ${n} f64)" for n in extra_locals)
            self._emit(decls)

        for stmt in node['body']:
            self._gen_stmt(stmt)

        # Default-Return
        self._emit("f64.const 0")
        self._indent_level -= 1
        self._emit(")")
        self._emit("")

        self._locals = old_locals
        self._local_counter = old_counter

    def _gen_return(self, node):
        expr = self._gen_expr(node['wert'])
        self._emit(f"({expr})")
        self._emit("return")

    def _gen_switch(self, node):
        """WÄHLE/SWITCH → Kaskadierte if/else in WASM."""
        ausdruck = node['ausdruck']
        faelle = node['faelle']
        sonst_block = node.get('sonst_block')

        # Wert in temp-Variable speichern
        self._get_or_create_local("__switch_val")
        expr_code = self._gen_expr(ausdruck)
        self._emit(f"({expr_code})")
        self._emit("local.set $__switch_val")

        for i, fall in enumerate(faelle):
            fall_expr = self._gen_expr(fall['wert'])
            self._emit(f"(if (i32.trunc_f64_s (f64.eq (local.get $__switch_val) ({fall_expr})))")
            self._indent_level += 1
            self._emit("(then")
            self._indent_level += 1
            for stmt in fall['block']:
                self._gen_stmt(stmt)
            self._indent_level -= 1
            self._emit(")")

            if i < len(faelle) - 1 or sonst_block:
                self._emit("(else")
                self._indent_level += 1

        if sonst_block:
            for stmt in sonst_block:
                self._gen_stmt(stmt)

        # Alle else/if-Klammern schließen
        if sonst_block:
            self._indent_level -= 1
            self._emit(")")
        for i in range(len(faelle)):
            if i < len(faelle) - 1 or sonst_block:
                self._indent_level -= 1
                self._emit(")")
            self._indent_level -= 1
            self._emit(")")

    def _gen_try(self, node):
        """VERSUCHE/FANGE → In WASM gibt es kein Try/Catch.
        Wir generieren den Versuche-Block direkt und den Fange-Block als Kommentar.
        WASM hat kein natives Exception-Handling (ohne Exception-Handling Proposal)."""
        self._emit(";; VERSUCHE (WASM hat kein natives Exception-Handling)")
        self._emit(";; Der Try-Block wird direkt ausgefuehrt:")
        for stmt in node['versuche_block']:
            self._gen_stmt(stmt)
        self._emit(";; FANGE-Block (nur bei Host-Runtime Exception-Support):")
        fehler_var = node.get('fehler_var')
        if fehler_var:
            self._emit(f";; Fehler-Variable: {fehler_var}")
        self._emit(";; (Fange-Block wird uebersprungen in reinem WASM)")
        for stmt in node['fange_block']:
            self._emit(f";; {stmt.get('type', 'stmt')}")

    # ─── Nicht genutzte abstrakte Methoden ───────────────────────────────

    def _gen_string(self, raw):
        return raw

    def _gen_variable_name(self, name):
        return name
