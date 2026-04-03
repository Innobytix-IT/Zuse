# FILE: semantic_analyzer.py
# Semantische Analyse für Zuse-AST.
# Läuft zwischen Parser und Interpreter/Transpiler.
# Erkennt Fehler wie undefinierte Variablen, break außerhalb von Schleifen, etc.

from visitor import NodeVisitor


class SemanticWarning:
    """Eine Warnung (kein Abbruch, aber Hinweis auf mögliches Problem)."""
    def __init__(self, zeile, nachricht):
        self.zeile = zeile
        self.nachricht = nachricht

    def __str__(self):
        return f"Warnung Zeile {self.zeile}: {self.nachricht}"


class SemanticError:
    """Ein semantischer Fehler (Programm wird wahrscheinlich abstürzen)."""
    def __init__(self, zeile, nachricht):
        self.zeile = zeile
        self.nachricht = nachricht

    def __str__(self):
        return f"Fehler Zeile {self.zeile}: {self.nachricht}"


class Scope:
    """Verwaltet Variablen-Sichtbarkeit in verschachtelten Scopes."""
    def __init__(self, parent=None, name="global"):
        self.parent = parent
        self.name = name
        self.variables = set()

    def define(self, name):
        self.variables.add(name)

    def is_defined(self, name):
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.is_defined(name)
        return False


# Eingebaute Funktionen und Variablen, die immer verfügbar sind
# Synchronisiert mit interpreter.py std_funcs (Stand: v7.3)
BUILTINS = {
    # Basis-Typen und Konvertierung
    'str', 'int', 'float', 'len', 'typ', 'liste', 'dict', 'eval',
    'BEREICH', 'FORMAT', 'wahr', 'falsch', 'SELBST',
    # Typ-Prüfung & Konvertierung
    'IST_ZAHL', 'IST_TEXT', 'IST_LISTE', 'IST_DICT', 'IST_BOOL', 'IST_NICHTS',
    'ALS_ZAHL', 'ALS_TEXT',
    'ALLE', 'IRGENDEIN', 'ZEICHENCODE', 'ZEICHEN', 'HEX', 'BIN', 'OKT',
    # Mathe-Bibliothek
    'PI', 'E', 'WURZEL', 'SINUS', 'COSINUS', 'TANGENS',
    'RUNDEN', 'ABSOLUT', 'POTENZ', 'LOGARITHMUS',
    'MINIMUM', 'MAXIMUM', 'SUMME', 'BODEN', 'DECKE',
    'ZUFALL', 'ZUFALL_BEREICH',
    # Text-Bibliothek
    'GROSSBUCHSTABEN', 'KLEINBUCHSTABEN', 'ERSETZE', 'TEILE',
    'TRIMME', 'ENTHAELT', 'LAENGE', 'FINDE',
    'BEGINNT_MIT', 'ENDET_MIT', 'VERBINDE',
    # Listen-Bibliothek
    'SORTIEREN', 'FILTERN', 'UMWANDELN', 'UMKEHREN',
    'FLACH', 'EINDEUTIG', 'AUFZAEHLEN', 'KOMBINIEREN',
    'ANHAENGEN', 'BEREICH_LISTE',
    # Datei-Bibliothek
    'LESE_DATEI', 'SCHREIBE_DATEI', 'ERGAENZE_DATEI',
    'EXISTIERT', 'LESE_ZEILEN', 'LOESCHE_DATEI',
    # Spielfeld-Bibliothek
    'Spielfeld',
}


class SemanticAnalyzer(NodeVisitor):
    """
    Analysiert den AST auf semantische Fehler und Warnungen.

    Prüft:
    - Undefinierte Variablen (Warnung)
    - ABBRUCH/WEITER außerhalb von Schleifen (Fehler)
    - ERGEBNIS außerhalb von Funktionen (Fehler)
    - Funktionsname-Shadowing von Builtins (Warnung)
    """

    def __init__(self):
        self.errors = []
        self.warnings = []
        self._scope = Scope(name="global")
        self._in_loop = 0       # Verschachtelungstiefe von Schleifen
        self._in_function = 0   # Verschachtelungstiefe von Funktionen

        # Builtins im globalen Scope definieren
        for name in BUILTINS:
            self._scope.define(name)

    def analyze(self, ast):
        """Hauptmethode: Analysiert den AST und gibt (errors, warnings) zurück."""
        self.errors = []
        self.warnings = []
        self._scope = Scope(name="global")
        self._in_loop = 0
        self._in_function = 0
        for name in BUILTINS:
            self._scope.define(name)

        for stmt in ast.get('body', []):
            self._analyze_stmt(stmt)

        return self.errors, self.warnings

    def _analyze_stmt(self, node):
        if node is None:
            return
        self.visit(node)

    def _analyze_expr(self, node):
        """Analysiert einen Ausdruck rekursiv."""
        if node is None:
            return
        t = node.get('type')
        handler = getattr(self, f'expr_{t}', None)
        if handler:
            handler(node)

    def _line(self, node):
        return node.get('line', '?')

    # ─── Hilfsmethoden ───────────────────────────────────────────────────────

    def _push_scope(self, name="block"):
        self._scope = Scope(parent=self._scope, name=name)

    def _pop_scope(self):
        if self._scope.parent:
            self._scope = self._scope.parent

    def _define_var(self, name, zeile=None):
        # Warnung bei Shadowing einer Variable aus äußerem Scope
        if self._scope.parent and self._scope.parent.is_defined(name) and name not in BUILTINS:
            if zeile is not None:
                self.warnings.append(SemanticWarning(
                    zeile, f"Variable '{name}' verdeckt gleichnamige Variable aus äußerem Scope."
                ))
        self._scope.define(name)

    def _check_var(self, name, zeile):
        if not self._scope.is_defined(name):
            self.warnings.append(SemanticWarning(
                zeile, f"Variable '{name}' wird verwendet, bevor sie definiert wurde."
            ))

    def _analyze_block(self, stmts):
        found_return = False
        for stmt in stmts:
            if found_return:
                self.warnings.append(SemanticWarning(
                    self._line(stmt), "Unerreichbarer Code nach ERGEBNIS."
                ))
                break
            self._analyze_stmt(stmt)
            if stmt.get('type') == 'ERGEBNIS_ANWEISUNG':
                found_return = True

    # ─── Visitor: Anweisungen ────────────────────────────────────────────────

    def generic_visit(self, node):
        """Fallback: Ausdruck als Statement analysieren."""
        self._analyze_expr(node)

    def visit_ZUWEISUNG(self, node):
        # Wert zuerst analysieren (rechte Seite)
        self._analyze_expr(node['wert'])
        # Ziel definieren
        ziel = node['ziel']
        if ziel['type'] == 'VARIABLE':
            self._define_var(ziel['name'])
        else:
            self._analyze_expr(ziel)

    def visit_MEHRFACH_ZUWEISUNG(self, node):
        for w in node['werte']:
            self._analyze_expr(w)
        for z in node['ziele']:
            if z['type'] == 'VARIABLE':
                self._define_var(z['name'])
            else:
                self._analyze_expr(z)

    def visit_AUSGABE_ANWEISUNG(self, node):
        self._analyze_expr(node['wert'])

    def visit_ERGEBNIS_ANWEISUNG(self, node):
        if self._in_function == 0:
            self.errors.append(SemanticError(
                self._line(node), "ERGEBNIS kann nur innerhalb einer Funktion verwendet werden."
            ))
        self._analyze_expr(node['wert'])

    def visit_FUNKTIONS_DEFINITION(self, node):
        name = node['name']
        if name in BUILTINS:
            self.warnings.append(SemanticWarning(
                self._line(node), f"Funktion '{name}' überschattet eine eingebaute Funktion."
            ))
        self._define_var(name)

        self._push_scope(f"funktion:{name}")
        self._in_function += 1
        for p in node['parameter']:
            self._define_var(p)
        # Default-Werte analysieren
        for default_expr in node.get('defaults', {}).values():
            self._analyze_expr(default_expr)
        self._analyze_block(node['body'])
        self._in_function -= 1
        self._pop_scope()

    def visit_KLASSEN_DEFINITION(self, node):
        self._define_var(node['name'])
        if node.get('elternklasse'):
            self._check_var(node['elternklasse'], self._line(node))

        self._push_scope(f"klasse:{node['name']}")
        for m in node['methoden']:
            self._push_scope(f"methode:{m['name']}")
            self._in_function += 1
            self._define_var('SELBST')
            for p in m['parameter']:
                self._define_var(p)
            self._analyze_block(m['body'])
            self._in_function -= 1
            self._pop_scope()
        self._pop_scope()

    def visit_WENN_ANWEISUNG(self, node):
        for cond, block in node['faelle']:
            self._analyze_expr(cond)
            self._analyze_block(block)
        if node.get('sonst_koerper'):
            self._analyze_block(node['sonst_koerper'])

    def visit_SCHLEIFE_SOLANGE(self, node):
        self._analyze_expr(node['bedingung'])
        self._in_loop += 1
        self._analyze_block(node['koerper'])
        self._in_loop -= 1

    def visit_SCHLEIFE_FÜR(self, node):
        self._analyze_expr(node['liste'])
        self._define_var(node['variable'])
        self._in_loop += 1
        self._analyze_block(node['koerper'])
        self._in_loop -= 1

    def visit_ABBRUCH_ANWEISUNG(self, node):
        if self._in_loop == 0:
            self.errors.append(SemanticError(
                self._line(node), "ABBRUCH kann nur innerhalb einer Schleife verwendet werden."
            ))

    def visit_WEITER_ANWEISUNG(self, node):
        if self._in_loop == 0:
            self.errors.append(SemanticError(
                self._line(node), "WEITER kann nur innerhalb einer Schleife verwendet werden."
            ))

    def visit_VERSUCHE_ANWEISUNG(self, node):
        self._analyze_block(node['versuche_block'])
        fehler_var = node.get('fehler_var')
        if fehler_var:
            self._define_var(fehler_var)
        self._analyze_block(node['fange_block'])

    def visit_WAEHLE_ANWEISUNG(self, node):
        self._analyze_expr(node['ausdruck'])
        for fall in node['faelle']:
            self._analyze_expr(fall['wert'])
            self._analyze_block(fall['block'])
        if node.get('sonst_block'):
            self._analyze_block(node['sonst_block'])

    def visit_IMPORT_ANWEISUNG(self, node):
        self._define_var(node['alias'])

    def visit_GLOBAL_ANWEISUNG(self, node):
        self._define_var(node['name'])

    # ─── Visitor: Ausdrücke ──────────────────────────────────────────────────

    def expr_VARIABLE(self, node):
        self._check_var(node['name'], self._line(node))

    def expr_ZAHL_LITERAL(self, node):
        pass

    def expr_STRING_LITERAL(self, node):
        pass

    def expr_LISTEN_LITERAL(self, node):
        for e in node['elemente']:
            self._analyze_expr(e)

    def expr_DICT_LITERAL(self, node):
        for k, v in node['paare']:
            self._analyze_expr(k)
            self._analyze_expr(v)

    def expr_BINÄRER_AUSDRUCK(self, node):
        self._analyze_expr(node['links'])
        self._analyze_expr(node['rechts'])

    def expr_UNAER_MINUS(self, node):
        self._analyze_expr(node['wert'])

    def expr_UNAER_NICHT(self, node):
        self._analyze_expr(node['wert'])

    def expr_INDEX_ZUGRIFF(self, node):
        self._analyze_expr(node['objekt'])
        self._analyze_expr(node['index'])

    def expr_SLICING(self, node):
        self._analyze_expr(node['objekt'])
        if node['start']:
            self._analyze_expr(node['start'])
        if node['ende']:
            self._analyze_expr(node['ende'])

    def expr_ATTRIBUT_ZUGRIFF(self, node):
        self._analyze_expr(node['objekt'])

    def expr_FUNKTIONS_AUFRUF(self, node):
        self._check_var(node['name'], node.get('line', '?'))
        for a in node['args']:
            self._analyze_expr(a)
        for _, v in node['kwargs']:
            self._analyze_expr(v)

    def expr_METHODEN_AUFRUF(self, node):
        self._analyze_expr(node['objekt'])
        for a in node['args']:
            self._analyze_expr(a)
        for _, v in node['kwargs']:
            self._analyze_expr(v)

    def expr_EINGABE_AUFRUF(self, node):
        self._analyze_expr(node['prompt'])

    def expr_LAMBDA_ERSTELLUNG(self, node):
        self._push_scope("lambda")
        for p in node['params']:
            self._define_var(p)
        self._analyze_expr(node['body'])
        self._pop_scope()

    def expr_ELTERN_ZUGRIFF(self, node):
        pass
