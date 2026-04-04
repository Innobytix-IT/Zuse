# FILE: interpreter.py (Version ZUSE 7.0 VISITOR PATTERN + SYMBOL TABLE)
import os
import time
import math
import random
import datetime
import threading
import tkinter
import importlib
from visitor import NodeVisitor
from symbol_table import SymbolTable
from spielfeld import Spielfeld
from error_i18n import t
from builtin_i18n import get_builtin_aliases, get_methoden_map, get_module_aliases

# Standard-Module
ALLOWED_MODULES = {
    'mathe': math,
    'zufall': random,
    'zeit': time,
    'datum': datetime,
    'tkinter': tkinter
}

# Unsere eigenen Sprach-Bibliotheken (diese sind sicher!)
ZUSE_LIBS = {'deutsch', 'english', 'espanol', 'francais', 'italiano', 'portugues', 'hindi', 'zhongwen'}

# Whitelist für Lernmodus
SAFE_MODULES_WHITELIST = {
    'math', 'random', 'time', 'datetime', 'tkinter', 'turtle' 
}

# Deutsche Methoden-Aliase fuer Listen und Strings (Fallback)
_METHODEN_MAP = {
    # Listen
    'hinzufuegen': 'append',
    'einfuegen': 'insert',
    'entfernen': 'remove',
    'sortieren': 'sort',
    'umkehren': 'reverse',
    'laenge': '__len__',
    'index': 'index',
    'zaehle': 'count',
    'leeren': 'clear',
    'kopie': 'copy',
    # Strings
    'gross': 'upper',
    'klein': 'lower',
    'ersetze': 'replace',
    'teile': 'split',
    'trimme': 'strip',
    'beginnt_mit': 'startswith',
    'endet_mit': 'endswith',
    'enthaelt': '__contains__',
    'finde': 'find',
}

# Modul-Mapping (Fallback, wird durch Sprache erweitert)
_BASE_MODULES = {
    'mathe': math,
    'zufall': random,
    'zeit': time,
    'datum': datetime,
    'tkinter': tkinter
}

class ZuseError(Exception):
    pass

class _ZuseBreak(Exception):
    """Signal fuer ABBRUCH/break in Schleifen."""
    pass

class _ZuseContinue(Exception):
    """Signal fuer WEITER/continue in Schleifen."""
    pass

# Rückwärtskompatibilität: Environment ist jetzt ein Alias für SymbolTable
Environment = SymbolTable

class ZuseFunction:
    def __init__(self, name, parameter, body, definition_env, owner_class=None, defaults=None):
        self.name = name
        self.parameter = parameter
        self.body = body
        self.definition_env = definition_env
        self.is_lambda = isinstance(body, dict)
        self.owner_class = owner_class
        self.bound_instance = None
        self.defaults = defaults or {}

class ZuseClassWrapper:
    def __init__(self, ast_node, env):
        self.ast = ast_node
        self.env = env 

class ZuseInstance:
    def __init__(self, class_wrapper, interpreter_ref):
        self._class_wrapper = class_wrapper
        self._class_name = class_wrapper.ast['name']
        self._attributes = {}
        self._interpreter = interpreter_ref

    _MISSING = object()  # Sentinel für "Attribut existiert nicht"

    def get_attr(self, name):
        return self._attributes.get(name, ZuseInstance._MISSING)

    def set_attr(self, name, val):
        self._attributes[name] = val

    def find_method(self, method_name, start_class_wrapper=None):
        curr_wrapper = start_class_wrapper or self._class_wrapper
        visited = set()
        while curr_wrapper:
            class_id = id(curr_wrapper)
            if class_id in visited:
                raise ZuseError(t("ERR_RUNTIME_ERROR", error=f"Zirkuläre Vererbung erkannt bei Klasse '{curr_wrapper.ast['name']}'"))
            visited.add(class_id)
            ast = curr_wrapper.ast
            for m in ast['methoden']:
                if m['name'] == method_name:
                    return m, curr_wrapper.env, curr_wrapper
            parent_name = ast.get('elternklasse')
            if parent_name:
                try:
                    parent_wrapper = curr_wrapper.env.get(parent_name)
                except ZuseError:
                    return None, None, None  # Elternklasse nicht im Scope
                if not isinstance(parent_wrapper, ZuseClassWrapper):
                    raise ZuseError(t("ERR_NOT_A_CLASS", name=parent_name))
                curr_wrapper = parent_wrapper
            else: curr_wrapper = None
        return None, None, None


class ZuseModul:
    """Wrapper für ein importiertes Zuse-Paket (.zuse Datei)."""
    def __init__(self, name, env):
        self.name = name
        self._env = env

    def __getattr__(self, attr):
        try:
            return self._env.get(attr)
        except Exception:
            raise AttributeError(t("ERR_MODULE_NO_ATTR", name=self.name, attr=attr))

    def __repr__(self):
        return f"<ZuseModul '{self.name}'>"


def _lese_datei(pfad, kodierung="utf-8"):
    with open(str(pfad), 'r', encoding=str(kodierung)) as f:
        return f.read()

def _schreibe_datei(pfad, inhalt, kodierung="utf-8", modus='w'):
    with open(str(pfad), modus, encoding=str(kodierung)) as f:
        f.write(str(inhalt))


class Interpreter(NodeVisitor):
    def __init__(self, output_callback=print, input_callback=input, safe_mode=False, sprache='deutsch'):
        self.global_env = SymbolTable(scope_type='global', scope_name='global')
        self.safe_mode = safe_mode
        self.sprache = sprache
        self.working_dir = os.getcwd()
        self._debugger = None  # Optional: ZuseDebugger für Breakpoints
        self._import_cache = {}  # Cache für importierte Zuse-Module
        self.global_env.define("__UMGEBUNG__", "STANDALONE", symbol_type='builtin')

        # Mehrsprachige Methoden-Map und Modul-Map laden
        self._methoden_map = get_methoden_map(sprache)
        self._module_aliases = get_module_aliases(sprache)
        # ALLOWED_MODULES mit Sprach-Aliase erweitern
        self._allowed_modules = dict(ALLOWED_MODULES)
        for alias_name, de_name in self._module_aliases.items():
            if de_name in _BASE_MODULES:
                self._allowed_modules[alias_name] = _BASE_MODULES[de_name]

        def _bereich(*args):
            if len(args) == 1: return list(range(int(args[0])))
            if len(args) == 2: return list(range(int(args[0]), int(args[1])))
            if len(args) == 3: return list(range(int(args[0]), int(args[1]), int(args[2])))
            raise ZuseError(t("ERR_BEREICH_ARGS"))

        std_funcs = {
            'str': lambda x: str(x),
            'int': lambda x: int(float(x)),
            'float': lambda x: float(x),
            'len': lambda x: len(x),
            'typ': lambda x: type(x).__name__,
            'liste': lambda: [],
            'dict': lambda: {},
            # eval() entfernt — Sicherheitsrisiko (Python-Code-Injektion)
            'BEREICH': _bereich,
            'FORMAT': lambda template, *args: template.format(*args),
            # ─── Mathe-Bibliothek (4.1) ──────────────────────────
            'PI': math.pi,
            'E': math.e,
            'WURZEL': lambda x: math.sqrt(x),
            'SINUS': lambda x: math.sin(x),
            'COSINUS': lambda x: math.cos(x),
            'TANGENS': lambda x: math.tan(x),
            'RUNDEN': lambda x, n=0: round(x, int(n)),
            'ABSOLUT': lambda x: abs(x),
            'POTENZ': lambda x, y: x ** y,
            'LOGARITHMUS': lambda x, basis=None: math.log(x) if basis is None else math.log(x, basis),
            'MINIMUM': lambda *args: min(args) if len(args) > 1 else min(args[0]),
            'MAXIMUM': lambda *args: max(args) if len(args) > 1 else max(args[0]),
            'SUMME': lambda x: sum(x),
            'BODEN': lambda x: math.floor(x),
            'DECKE': lambda x: math.ceil(x),
            'ZUFALL': lambda: random.random(),
            'ZUFALL_BEREICH': lambda a, b: random.randint(int(a), int(b)),
            # ─── Text-Bibliothek (4.2) ──────────────────────────
            'GROSSBUCHSTABEN': lambda x: str(x).upper(),
            'KLEINBUCHSTABEN': lambda x: str(x).lower(),
            'ERSETZE': lambda x, alt, neu: str(x).replace(str(alt), str(neu)),
            'TEILE': lambda x, trenner=None: str(x).split(trenner),
            'TRIMME': lambda x: str(x).strip(),
            'ENTHAELT': lambda x, teil: str(teil) in str(x),
            'LAENGE': lambda x: len(x),
            'FINDE': lambda x, teil: str(x).find(str(teil)),
            'BEGINNT_MIT': lambda x, praefix: str(x).startswith(str(praefix)),
            'ENDET_MIT': lambda x, suffix: str(x).endswith(str(suffix)),
            'VERBINDE': lambda liste, trenner="": str(trenner).join(str(e) for e in liste),
            # ─── Listen-Bibliothek (4.3) ─────────────────────────
            'SORTIEREN': lambda x, schluessel=None: sorted(x, key=schluessel),
            'FILTERN': lambda x, fn: list(filter(fn, x)),
            'UMWANDELN': lambda x, fn: list(map(fn, x)),
            'UMKEHREN': lambda x: list(reversed(x)),
            'FLACH': lambda x: [e for sub in x for e in (sub if isinstance(sub, list) else [sub])],
            'EINDEUTIG': lambda x: list(dict.fromkeys(x)),
            'AUFZAEHLEN': lambda x: list(enumerate(x)),
            'KOMBINIEREN': lambda *listen: list(zip(*listen)),
            'ANHAENGEN': lambda x, *elemente: x + list(elemente),
            'BEREICH_LISTE': lambda x: list(range(int(x))),
            # ─── Datei-Bibliothek (4.4) ──────────────────────────
            'LESE_DATEI': lambda pfad, kodierung="utf-8": _lese_datei(pfad, kodierung),
            'SCHREIBE_DATEI': lambda pfad, inhalt, kodierung="utf-8": _schreibe_datei(pfad, inhalt, kodierung, 'w'),
            'ERGAENZE_DATEI': lambda pfad, inhalt, kodierung="utf-8": _schreibe_datei(pfad, inhalt, kodierung, 'a'),
            'EXISTIERT': lambda pfad: os.path.exists(str(pfad)),
            'LESE_ZEILEN': lambda pfad, kodierung="utf-8": _lese_datei(pfad, kodierung).splitlines(),
            'LOESCHE_DATEI': lambda pfad: os.remove(str(pfad)),
            # ─── Spielfeld-Bibliothek (4.5) ──────────────────────
            'Spielfeld': Spielfeld,
            # ─── Typ-Prüfung & Konvertierung (7.2) ──────────────
            'IST_ZAHL': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
            'IST_TEXT': lambda x: isinstance(x, str),
            'IST_LISTE': lambda x: isinstance(x, list),
            'IST_DICT': lambda x: isinstance(x, dict),
            'IST_BOOL': lambda x: isinstance(x, bool),
            'IST_NICHTS': lambda x: x is None,
            'ALS_ZAHL': lambda x: int(float(x)) if float(x) == int(float(x)) else float(x),
            'ALS_TEXT': lambda x: str(x),
            # ─── Erweiterte Builtins (7.3) ──────────────────────
            'ALLE': lambda x: all(x),
            'IRGENDEIN': lambda x: any(x),
            'ZEICHENCODE': lambda x: ord(str(x)[0]),
            'ZEICHEN': lambda x: chr(int(x)),
            'HEX': lambda x: hex(int(x)),
            'BIN': lambda x: bin(int(x)),
            'OKT': lambda x: oct(int(x)),
        }

        # Builtins unter deutschen Namen registrieren
        for k, v in std_funcs.items():
            self.global_env.define(k, v)

        # Mehrsprachige Builtin-Aliase registrieren
        builtin_aliases = get_builtin_aliases(sprache)
        for translated_name, de_name in builtin_aliases.items():
            if translated_name != de_name and de_name in std_funcs:
                self.global_env.define(translated_name, std_funcs[de_name])

        self.output_callback = output_callback
        self.input_callback = input_callback
        self.running = True
        self.recursion_depth = 0
        self.MAX_RECURSION = 1000
        self._aktuelle_zeile = 0

    def print_out(self, text):
        self.output_callback(str(text))

    def input_in(self, prompt, modus):
        return self.input_callback(prompt, modus)

    def _python_bridge_wrapper(self, zuse_func):
        def bridge(*p_args): return self._call_function(zuse_func, list(p_args), zuse_func.definition_env)
        return bridge

    def _prepare_python_args(self, args, kwargs):
        new_args = []
        for a in args:
            if isinstance(a, ZuseFunction): new_args.append(self._python_bridge_wrapper(a))
            else: new_args.append(a)
        new_kwargs = {}
        for k, v in kwargs.items():
            if isinstance(v, ZuseFunction): new_kwargs[k] = self._python_bridge_wrapper(v)
            else: new_kwargs[k] = v
        return new_args, new_kwargs

    def interpretiere(self, ast):
        try:
            if ast['type'] != 'PROGRAMM': raise ZuseError(t("ERR_INVALID_AST"))
            for anweisung in ast['body']:
                if not self.running: break
                self.execute_node(anweisung, self.global_env)
        except ZuseError as e: self.print_out(t("ERR_RUNTIME_ERROR", error=e))
        except RecursionError: self.print_out(t("ERR_MAX_RECURSION_CRITICAL"))
        except Exception as e:
            self.print_out(t("ERR_SYSTEM_ERROR", error=e))

    def execute_node(self, node, env):
        if not node or not self.running: return
        self.recursion_depth += 1
        if self.recursion_depth > self.MAX_RECURSION:
            self.recursion_depth -= 1
            raise ZuseError(t("ERR_MAX_RECURSION"))
        if 'line' in node:
            self._aktuelle_zeile = node['line']
        if self._debugger is not None:
            self._debugger.on_statement(self._aktuelle_zeile, env)
        try:
            return self.visit(node, env)
        finally:
            self.recursion_depth -= 1

    def generic_visit(self, node, env):
        """Fallback: Ausdrücke als Statement ausführen."""
        typ = node.get('type')
        if typ in ('FUNKTIONS_AUFRUF', 'METHODEN_AUFRUF'):
            self.evaluiere_ausdruck(node, env)
            return
        raise ZuseError(t("ERR_UNKNOWN_STATEMENT", line=self._aktuelle_zeile, type=typ))

    # ─── Visitor-Methoden für Anweisungen ────────────────────────────────────

    def _assign_to_target(self, ziel, wert, env):
        """Hilfsmethode: Wert einem Ziel zuweisen (Variable, Attribut, Index)."""
        if ziel['type'] == 'VARIABLE':
            name = ziel['name']
            try:
                is_global = env.get('__globals__')
                if is_global and name in is_global: self.global_env.set(name, wert)
                else: env.set(name, wert)
            except ZuseError: env.define(name, wert)
        elif ziel['type'] == 'ATTRIBUT_ZUGRIFF':
            obj = self.evaluiere_ausdruck(ziel['objekt'], env)
            if isinstance(obj, ZuseInstance): obj.set_attr(ziel['attribut'], wert)
            else:
                try: setattr(obj, ziel['attribut'], wert)
                except (AttributeError, TypeError): raise ZuseError(t("ERR_CANNOT_SET_ATTR", line=self._aktuelle_zeile, attr=ziel['attribut']))
        elif ziel['type'] == 'INDEX_ZUGRIFF':
            obj = self.evaluiere_ausdruck(ziel['objekt'], env)
            idx = self.evaluiere_ausdruck(ziel['index'], env)
            try: obj[idx] = wert
            except (IndexError, KeyError, TypeError) as e: raise ZuseError(t("ERR_INDEX_ASSIGN", line=self._aktuelle_zeile, error=e))
        else: raise ZuseError(t("ERR_INVALID_ASSIGN_TARGET", line=self._aktuelle_zeile, type=ziel['type']))

    def visit_ZUWEISUNG(self, node, env):
        wert = self.evaluiere_ausdruck(node['wert'], env)
        self._assign_to_target(node['ziel'], wert, env)

    def visit_MEHRFACH_ZUWEISUNG(self, node, env):
        werte = [self.evaluiere_ausdruck(w, env) for w in node['werte']]
        ziele = node['ziele']
        if len(werte) == 1 and len(ziele) > 1:
            werte = list(werte[0])
        if len(ziele) != len(werte):
            raise ZuseError(t("ERR_MULTI_ASSIGN_MISMATCH", line=self._aktuelle_zeile, targets=len(ziele), values=len(werte)))
        for ziel, wert in zip(ziele, werte):
            self._assign_to_target(ziel, wert, env)

    def visit_FUNKTIONS_DEFINITION(self, node, env):
        func = ZuseFunction(node['name'], node['parameter'], node['body'], env, defaults=node.get('defaults', {}))
        env.define(node['name'], func)

    def visit_KLASSEN_DEFINITION(self, node, env):
        wrapper = ZuseClassWrapper(node, env)
        env.define(node['name'], wrapper)

    def visit_GLOBAL_ANWEISUNG(self, node, env):
        try: globals_set = env.get('__globals__')
        except ZuseError:
            globals_set = set()
            env.define('__globals__', globals_set)
        globals_set.add(node['name'])
        if not self.global_env.has(node['name']): self.global_env.define(node['name'], None, symbol_type='global')

    def visit_WENN_ANWEISUNG(self, node, env):
        for bedingung_node, block in node['faelle']:
            if self.evaluiere_ausdruck(bedingung_node, env):
                for a in block:
                    res = self.execute_node(a, env)
                    if res: return res
                return
        if node.get('sonst_koerper'):
            for a in node['sonst_koerper']:
                res = self.execute_node(a, env)
                if res: return res

    def visit_SCHLEIFE_SOLANGE(self, node, env):
        while self.running and self.evaluiere_ausdruck(node['bedingung'], env):
            try:
                for a in node['koerper']:
                    res = self.execute_node(a, env)
                    if res: return res
            except _ZuseBreak:
                break
            except _ZuseContinue:
                continue

    def visit_SCHLEIFE_FÜR(self, node, env):
        iter_obj = self.evaluiere_ausdruck(node['liste'], env)
        var_name = node['variable']
        try: iterator = iter(iter_obj)
        except TypeError: raise ZuseError(t("ERR_NOT_ITERABLE"))
        old_val = None
        existed = env.has_recursive(var_name)
        if existed: old_val = env.get(var_name)
        try:
            for el in iterator:
                if not self.running: break
                env.set(var_name, el)
                try:
                    for a in node['koerper']:
                        res = self.execute_node(a, env)
                        if res: return res
                except _ZuseBreak:
                    break
                except _ZuseContinue:
                    continue
        finally:
            if existed: env.set(var_name, old_val)
            else: env.delete(var_name)

    def visit_ABBRUCH_ANWEISUNG(self, node, env):
        raise _ZuseBreak()

    def visit_WEITER_ANWEISUNG(self, node, env):
        raise _ZuseContinue()

    def visit_VERSUCHE_ANWEISUNG(self, node, env):
        try:
            for a in node['versuche_block']: self.execute_node(a, env)
        except Exception as e:
            # Fehlervariable definieren, falls angegeben (FANGE fehler / CATCH error)
            fehler_var = node.get('fehler_var')
            if fehler_var:
                # Fehlermeldung als String in die Variable schreiben
                fehler_msg = str(e)
                # "Laufzeitfehler: ..." Prefix entfernen falls vorhanden
                for prefix in ['Laufzeitfehler: ', 'Runtime error: ', 'Error de ejecución: ',
                               'Erreur d\'exécution: ', 'Errore di esecuzione: ', 'Erro de execução: ']:
                    if fehler_msg.startswith(prefix):
                        fehler_msg = fehler_msg[len(prefix):]
                        break
                env.set(fehler_var, fehler_msg)
            for a in node['fange_block']: self.execute_node(a, env)

    def visit_WAEHLE_ANWEISUNG(self, node, env):
        """WÄHLE/SWITCH: Vergleicht Ausdruck mit FALL-Werten, führt passenden Block aus."""
        wert = self.evaluiere_ausdruck(node['ausdruck'], env)
        gefunden = False
        for fall in node['faelle']:
            fall_wert = self.evaluiere_ausdruck(fall['wert'], env)
            if wert == fall_wert:
                gefunden = True
                for a in fall['block']:
                    result = self.execute_node(a, env)
                    if isinstance(result, tuple) and result[0] == 'RÜCKGABE':
                        return result
                break
        if not gefunden and node.get('sonst_block'):
            for a in node['sonst_block']:
                result = self.execute_node(a, env)
                if isinstance(result, tuple) and result[0] == 'RÜCKGABE':
                    return result

    def visit_AUSGABE_ANWEISUNG(self, node, env):
        val = self.evaluiere_ausdruck(node['wert'], env)
        self.print_out(val)

    def visit_ERGEBNIS_ANWEISUNG(self, node, env):
        return ('RÜCKGABE', self.evaluiere_ausdruck(node['wert'], env))

    def visit_IMPORT_ANWEISUNG(self, node, env):
        mod_name = node['modul']
        alias = node['alias']
        if mod_name in ZUSE_LIBS:
            return
        if self.safe_mode:
            allowed = False
            if mod_name in self._allowed_modules: allowed = True
            elif mod_name in SAFE_MODULES_WHITELIST: allowed = True
            if not allowed: raise ZuseError(t("ERR_SECURITY_BLOCK", name=mod_name))
        # Import-Cache prüfen
        if mod_name in self._import_cache:
            env.define(alias, self._import_cache[mod_name])
            return
        if mod_name in self._allowed_modules:
            env.define(alias, self._allowed_modules[mod_name])
        else:
            # Versuche zpkg-Paket zu laden
            try:
                from zpkg_core import finde_paket_pfad
                paket_pfad = finde_paket_pfad(mod_name, self.working_dir)
                if paket_pfad:
                    with open(paket_pfad, 'r', encoding='utf-8') as f:
                        zuse_code = f.read()
                    from language_loader import lade_sprache
                    from lexer import tokenize as ztokenize
                    from parser import Parser as ZParser
                    config = lade_sprache("deutsch")
                    tokens = ztokenize(zuse_code, config)
                    zuse_ast = ZParser(tokens).parse()
                    modul_env = SymbolTable(parent=self.global_env,
                                           scope_type='function',
                                           scope_name=f'modul:{mod_name}')
                    # Standard-Funktionen auch im Modul verfügbar machen
                    for key in list(self.global_env._symbols.keys()):
                        try:
                            modul_env.define(key, self.global_env.get(key))
                        except Exception:
                            pass
                    for stmt in zuse_ast['body']:
                        self.execute_node(stmt, modul_env)
                    modul = ZuseModul(mod_name, modul_env)
                    self._import_cache[mod_name] = modul
                    env.define(alias, modul)
                    return
            except ImportError:
                pass  # zpkg_core nicht verfügbar
            # Fallback: Python-Modul
            try:
                imported_module = importlib.import_module(mod_name)
                self._import_cache[mod_name] = imported_module
                env.define(alias, imported_module)
            except ImportError: raise ZuseError(t("ERR_MODULE_NOT_FOUND", name=mod_name))
            except Exception as e: raise ZuseError(t("ERR_IMPORT_FAILED", name=mod_name, error=e))

    def evaluiere_ausdruck(self, node, env):
        """Dispatcht Ausdrücke zum passenden eval_TYPE-Handler."""
        typ = node.get('type')
        handler = getattr(self, f'eval_{typ}', None)
        if handler:
            return handler(node, env)
        raise ZuseError(t("ERR_RUNTIME_ERROR", error=f"Unbekannter Ausdruckstyp: '{typ}'"))

    # ─── Visitor-Methoden für Ausdrücke ──────────────────────────────────────

    def eval_ZAHL_LITERAL(self, node, env):
        val = node['wert']
        return float(val) if '.' in val else int(val)

    def eval_STRING_LITERAL(self, node, env):
        raw = node['wert'][1:-1]
        return raw.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')

    def eval_LISTEN_LITERAL(self, node, env):
        return [self.evaluiere_ausdruck(e, env) for e in node['elemente']]

    def eval_DICT_LITERAL(self, node, env):
        return {self.evaluiere_ausdruck(k, env): self.evaluiere_ausdruck(v, env) for k, v in node['paare']}

    def eval_VARIABLE(self, node, env):
        name = node['name']
        if name == 'SELBST':
            try: return env.get('SELBST')
            except ZuseError: raise ZuseError(t("ERR_SELF_OUTSIDE_METHOD", line=self._aktuelle_zeile))
        if name == 'wahr': return True
        if name == 'falsch': return False
        if name == 'NICHTS': return None
        try: return env.get(name)
        except ZuseError: raise ZuseError(t("ERR_VAR_NOT_DEFINED", line=self._aktuelle_zeile, name=name))

    def eval_ELTERN_ZUGRIFF(self, node, env):
        try:
            inst = env.get('SELBST')
            return {'type': 'ELTERN_PROXY', 'instance': inst}
        except ZuseError: raise ZuseError(t("ERR_SUPER_OUTSIDE_METHOD", line=self._aktuelle_zeile))

    def eval_UNAER_NICHT(self, node, env):
        return not self.evaluiere_ausdruck(node['wert'], env)

    def eval_BINÄRER_AUSDRUCK(self, node, env):
        op = node['operator']
        if op == 'und':
            l = self.evaluiere_ausdruck(node['links'], env)
            return l and self.evaluiere_ausdruck(node['rechts'], env)
        if op == 'oder':
            l = self.evaluiere_ausdruck(node['links'], env)
            return l or self.evaluiere_ausdruck(node['rechts'], env)
        l = self.evaluiere_ausdruck(node['links'], env)
        r = self.evaluiere_ausdruck(node['rechts'], env)
        try:
            if op == '+': return (str(l)+str(r)) if (isinstance(l, str) or isinstance(r, str)) else l+r
            if op == '-': return l - r
            if op == '*': return l * r
            if op == '/': return l / r
            if op == '^': return l ** r
            if op == '%': return l % r
            if op == '==': return l == r
            if op == '!=': return l != r
            if op == '>': return l > r
            if op == '<': return l < r
            if op == '>=': return l >= r
            if op == '<=': return l <= r
            raise ZuseError(t("ERR_CALC_ERROR", line=self._aktuelle_zeile, error=f"Unbekannter Operator '{op}'"))
        except ZeroDivisionError: raise ZuseError(t("ERR_DIVISION_BY_ZERO", line=self._aktuelle_zeile))
        except TypeError as e: raise ZuseError(t("ERR_INCOMPATIBLE_TYPES", line=self._aktuelle_zeile, error=e))
        except Exception as e: raise ZuseError(t("ERR_CALC_ERROR", line=self._aktuelle_zeile, error=e))

    def eval_UNAER_MINUS(self, node, env):
        return -self.evaluiere_ausdruck(node['wert'], env)

    def eval_SLICING(self, node, env):
        obj = self.evaluiere_ausdruck(node['objekt'], env)
        start = self.evaluiere_ausdruck(node['start'], env) if node['start'] else None
        ende = self.evaluiere_ausdruck(node['ende'], env) if node['ende'] else None
        try:
            return obj[start:ende]
        except TypeError as e:
            raise ZuseError(t("ERR_RUNTIME_ERROR", error=f"Slicing nicht möglich: {e}"))
        except Exception as e:
            raise ZuseError(t("ERR_RUNTIME_ERROR", error=f"Fehler bei Slicing: {e}"))

    def eval_INDEX_ZUGRIFF(self, node, env):
        obj = self.evaluiere_ausdruck(node['objekt'], env)
        idx = self.evaluiere_ausdruck(node['index'], env)
        try: return obj[idx]
        except (IndexError, KeyError, TypeError): raise ZuseError(t("ERR_INVALID_INDEX", line=self._aktuelle_zeile, index=idx))

    def eval_ATTRIBUT_ZUGRIFF(self, node, env):
        obj = self.evaluiere_ausdruck(node['objekt'], env)
        attr = node['attribut']
        if isinstance(obj, ZuseInstance):
            val = obj.get_attr(attr)
            if val is not ZuseInstance._MISSING: return val
            method_def, def_env, owner = obj.find_method(attr)
            if method_def:
                func = ZuseFunction(method_def['name'], method_def['parameter'], method_def['body'], def_env, owner_class=owner, defaults=method_def.get('defaults', {}))
                func.bound_instance = obj
                return func
            raise ZuseError(t("ERR_ATTR_NOT_FOUND_CLASS", line=self._aktuelle_zeile, attr=attr, cls=obj._class_name))
        try: return getattr(obj, attr)
        except AttributeError: raise ZuseError(t("ERR_ATTR_NOT_FOUND", line=self._aktuelle_zeile, attr=attr))

    def eval_LAMBDA_ERSTELLUNG(self, node, env):
        return ZuseFunction("lambda", node['params'], {'type': 'ERGEBNIS_ANWEISUNG', 'wert': node['body']}, env)

    def eval_FUNKTIONS_AUFRUF(self, node, env):
        func_obj = self.evaluiere_ausdruck({'type': 'VARIABLE', 'name': node['name']}, env)
        args = [self.evaluiere_ausdruck(a, env) for a in node['args']]
        kwargs = {k: self.evaluiere_ausdruck(v, env) for k, v in node['kwargs']}
        if callable(func_obj) and not isinstance(func_obj, (ZuseFunction, ZuseClassWrapper)):
            args, kwargs = self._prepare_python_args(args, kwargs)
        return self._call_function(func_obj, args, env, kwargs=kwargs)

    def eval_METHODEN_AUFRUF(self, node, env):
        obj_eval = self.evaluiere_ausdruck(node['objekt'], env)
        args = [self.evaluiere_ausdruck(a, env) for a in node['args']]
        kwargs = {k: self.evaluiere_ausdruck(v, env) for k, v in node['kwargs']}

        if isinstance(obj_eval, dict) and obj_eval.get('type') == 'ELTERN_PROXY':
            inst = obj_eval['instance']
            try: current_class_ctx = env.get('__class_context__')
            except ZuseError: raise ZuseError(t("ERR_SUPER_OUTSIDE_CLASS", line=self._aktuelle_zeile))
            parent_name = current_class_ctx.ast.get('elternklasse')
            if not parent_name: raise ZuseError(t("ERR_NO_PARENT_CLASS", line=self._aktuelle_zeile, name=current_class_ctx.ast['name']))
            try: parent_wrapper = current_class_ctx.env.get(parent_name)
            except ZuseError: raise ZuseError(t("ERR_PARENT_CLASS_NOT_FOUND", line=self._aktuelle_zeile, name=parent_name))
            method_def, def_env, owner = inst.find_method(node['methode'], start_class_wrapper=parent_wrapper)
            if not method_def: raise ZuseError(t("ERR_METHOD_NOT_IN_PARENT", line=self._aktuelle_zeile, method=node['methode'], parent=parent_name))
            func = ZuseFunction(method_def['name'], method_def['parameter'], method_def['body'], def_env, owner_class=owner, defaults=method_def.get('defaults', {}))
            return self._call_function(func, args, env, self_obj=inst, kwargs=kwargs)

        elif isinstance(obj_eval, ZuseInstance):
            method_def, def_env, owner = obj_eval.find_method(node['methode'])
            if not method_def: raise ZuseError(t("ERR_METHOD_NOT_FOUND", line=self._aktuelle_zeile, method=node['methode'], cls=obj_eval._class_name))
            func = ZuseFunction(method_def['name'], method_def['parameter'], method_def['body'], def_env, owner_class=owner, defaults=method_def.get('defaults', {}))
            return self._call_function(func, args, env, self_obj=obj_eval, kwargs=kwargs)

        elif isinstance(obj_eval, ZuseModul):
            methode = node['methode']
            try:
                func_obj = obj_eval._env.get(methode)
            except Exception:
                raise ZuseError(t("ERR_FUNC_NOT_IN_MODULE", line=self._aktuelle_zeile, func=methode, module=obj_eval.name))
            return self._call_function(func_obj, args, env, kwargs=kwargs)

        elif isinstance(obj_eval, ZuseClassWrapper):
            is_constructor = node['methode'] in ['ERSTELLE', 'NEW', 'CREAR', 'CRIAR', 'CREER', 'CREARE']
            if is_constructor: return self._call_function(obj_eval, args, env, kwargs=kwargs)
            else: raise ZuseError(t("ERR_STATIC_METHOD_NOT_FOUND", line=self._aktuelle_zeile, method=node['methode'], cls=obj_eval.ast['name']))
        else:
            methode = node['methode']
            methode = self._methoden_map.get(methode, methode)
            args, kwargs = self._prepare_python_args(args, kwargs)
            try: return getattr(obj_eval, methode)(*args, **kwargs)
            except AttributeError: raise ZuseError(t("ERR_METHOD_NOT_EXISTS", line=self._aktuelle_zeile, method=node['methode']))
            except Exception as e: raise ZuseError(t("ERR_METHOD_CALL_FAILED", line=self._aktuelle_zeile, method=node['methode'], error=e))

    def eval_EINGABE_AUFRUF(self, node, env):
        prompt = str(self.evaluiere_ausdruck(node['prompt'], env))
        val = self.input_in(prompt, node['modus'])
        if node['modus'] == 'zahl':
            try:
                f = float(val)
                return int(f) if f.is_integer() else f
            except (ValueError, TypeError): return 0
        return val

    def _call_function(self, func, args, caller_env, self_obj=None, kwargs=None):
        if kwargs is None: kwargs = {}
        if isinstance(func, ZuseFunction):
            scope_type = 'method' if self_obj else 'function'
            local_env = SymbolTable(parent=func.definition_env, scope_type=scope_type, scope_name=func.name)
            for i, param in enumerate(func.parameter):
                if i < len(args):
                    local_env.define(param, args[i], symbol_type='parameter')
                elif param in kwargs:
                    local_env.define(param, kwargs.pop(param), symbol_type='parameter')
                elif param in func.defaults:
                    default_val = self.evaluiere_ausdruck(func.defaults[param], func.definition_env)
                    local_env.define(param, default_val, symbol_type='parameter')
            # Prüfe ob alle kwargs zu definierten Parametern passen
            for k, v in kwargs.items():
                if k not in func.parameter:
                    raise ZuseError(t("ERR_RUNTIME_ERROR", error=f"Unbekannter Parameter '{k}' für Funktion '{func.name}'"))
                local_env.define(k, v)
            if func.bound_instance: self_obj = func.bound_instance
            if self_obj: local_env.define('SELBST', self_obj)
            if func.owner_class: local_env.define('__class_context__', func.owner_class)
            if self._debugger is not None:
                self._debugger.on_call(func.name, self._aktuelle_zeile, local_env)
            try:
                if func.is_lambda:
                    res = self.execute_node(func.body, local_env)
                    return res[1] if res else None
                else:
                    for stmt in func.body:
                        res = self.execute_node(stmt, local_env)
                        if res and res[0] == 'RÜCKGABE': return res[1]
                    return None
            finally:
                if self._debugger is not None:
                    self._debugger.on_return()
        
        if isinstance(func, ZuseClassWrapper):
            inst = ZuseInstance(func, self)
            possible_constructors = ['ERSTELLE', 'NEW', 'CREAR', 'CRIAR', 'CREER', 'CREARE']
            constr = None; c_env = None; owner = None
            for c_name in possible_constructors:
                constr, c_env, owner = inst.find_method(c_name)
                if constr: break
            if constr:
                c_func = ZuseFunction(c_name, constr['parameter'], constr['body'], c_env, owner_class=owner, defaults=constr.get('defaults', {}))
                self._call_function(c_func, args, caller_env, self_obj=inst, kwargs=kwargs)
            return inst

        if callable(func):
            args, kwargs = self._prepare_python_args(args, kwargs)
            return func(*args, **kwargs)
        raise ZuseError(t("ERR_NOT_CALLABLE", line=self._aktuelle_zeile, obj=func))