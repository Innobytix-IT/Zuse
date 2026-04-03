# Zuse Architektur

## Pipeline-Übersicht

```
Quellcode (.zuse)
    │
    ▼
┌─────────┐     ┌──────────┐     ┌──────────────┐
│  Lexer   │────▶│  Parser  │────▶│ Interpreter  │────▶ Ausgabe
│ lexer.py │     │ parser.py│     │interpreter.py│
└─────────┘     └──────────┘     └──────────────┘
    │                │
    │                │           ┌──────────────────┐
    │                └──────────▶│ Semantische       │
    │                            │ Analyse           │
    │                            │semantic_analyzer.py│
    │                            └──────────────────┘
    │                │
    │                ▼
    │           ┌──────────────┐
    │           │  Transpiler  │
    │           │transpiler.py │
    │           └──────┬───────┘
    │                  │
    │    ┌─────────────┼─────────────┐─────────────┐
    │    ▼             ▼             ▼             ▼
    │ Python        JavaScript     Java          C#
    │ Backend       Backend        Backend       Backend
    │
    │    ▼
    │ WebAssembly
    │ Backend
```

---

## 1. Lexer (`lexer.py`)

**Aufgabe:** Wandelt Quelltext in Token-Liste um.

- Liest Sprach-Konfiguration (JSON) mit übersetzten Keywords
- Generiert Regex dynamisch aus Sprach-Config + statischen Tokens
- Normalisiert Keyword-Aliase auf kanonische Form (z.B. `ZEIGE → AUSGABE`)
- Unterstützt Unicode Latin Extended (äöüéçñ etc.)
- Gibt Zeilen- und Spaltenposition pro Token zurück

**Eingabe:** `"AUSGABE 42"` → **Ausgabe:** `[{type:'KEYWORD', value:'KW_AUSGABE'}, {type:'ZAHL', value:'42'}, {type:'EOF'}]`

---

## 2. Parser (`parser.py`)

**Aufgabe:** Baut aus Tokens einen AST (Abstract Syntax Tree).

- Recursive-Descent-Parser
- Operatoren-Präzedenz über geschachtelte Parse-Funktionen
- Error-Recovery: Sammelt mehrere Fehler statt beim ersten abzubrechen
- Prüft auf doppelte Parameternamen

**AST-Knotentypen:**

| Anweisungen | Ausdrücke |
|-------------|-----------|
| PROGRAMM | ZAHL_LITERAL |
| ZUWEISUNG | STRING_LITERAL |
| AUSGABE_ANWEISUNG | VARIABLE |
| WENN_ANWEISUNG | BINÄRER_AUSDRUCK |
| SCHLEIFE_SOLANGE | UNAER_MINUS / UNAER_NICHT |
| SCHLEIFE_FÜR | FUNKTIONS_AUFRUF |
| FUNKTIONS_DEFINITION | METHODEN_AUFRUF |
| KLASSEN_DEFINITION | INDEX_ZUGRIFF / SLICING |
| VERSUCHE_ANWEISUNG | ATTRIBUT_ZUGRIFF |
| WAEHLE_ANWEISUNG | LISTEN_LITERAL / DICT_LITERAL |
| IMPORT_ANWEISUNG | LAMBDA_ERSTELLUNG |
| ERGEBNIS_ANWEISUNG | EINGABE_AUFRUF |
| ABBRUCH/WEITER_ANWEISUNG | ELTERN_ZUGRIFF |

---

## 3. Interpreter (`interpreter.py`)

**Aufgabe:** Führt den AST direkt aus (Tree-Walking Interpreter).

### Architektur-Muster: Visitor Pattern

```python
class Interpreter(NodeVisitor):
    def visit_ZUWEISUNG(self, node, env): ...
    def visit_AUSGABE_ANWEISUNG(self, node, env): ...
    def eval_BINÄRER_AUSDRUCK(self, node, env): ...
```

### Scope-Verwaltung: SymbolTable

```
global_env
    └── funktion:rechne
        └── schleife_env
    └── klasse:Tier
        └── methode:spreche
```

- `SymbolTable` mit Parent-Chain (lexikalisches Scoping)
- `GLOBAL`-Anweisung hebt Variable in globalen Scope

### Python-Bridge

```python
def _python_bridge_wrapper(self, zuse_func):
    def bridge(*args): return self._call_function(zuse_func, list(args), ...)
    return bridge
```

Ermöglicht, dass Zuse-Funktionen als Python-Callables an `importlib`-Module übergeben werden.

### Klassen-System

- `ZuseClassWrapper` — Hält AST-Node + Definition-Environment
- `ZuseInstance` — Instanz mit `_attributes` Dict
- `find_method()` — Methodenauflösung mit Vererbungskette + Zykluserkennung
- Konstruktor: `ERSTELLE` (oder sprachspezifisches Äquivalent)

### Import-System

1. Zuse-Bibliotheken (deutsch.zuse etc.) → Sprach-Keywords laden
2. zpkg-Pakete → .zuse Datei parsen + in Modul-Scope ausführen
3. Python-Module → `importlib.import_module()` mit direktem Zugriff
4. Import-Cache verhindert mehrfaches Parsen

---

## 4. Transpiler (`transpiler.py` + `backends/`)

**Aufgabe:** Übersetzt AST in Zielsprachen.

### BaseBackend (Visitor Pattern)

```python
class BaseBackend(NodeVisitor):
    def _gen_stmt(self, node): ...   # Dispatch nach Anweisungstyp
    def _gen_expr(self, node): ...   # Dispatch nach Ausdruckstyp
    def _emit(self, line): ...       # Zeile mit Einrückung ausgeben
```

### Backend-Status

| Backend | Datei | Vollständigkeit |
|---------|-------|----------------|
| Python 3 | `python_backend.py` | Komplett |
| JavaScript ES6+ | `javascript_backend.py` | Komplett |
| C# 10+ | `csharp_backend.py` | Komplett |
| Java 11+ | `java_backend.py` | Komplett (Konstruktoren repariert) |
| WebAssembly | `wasm_backend.py` | Nur numerische Operationen |

---

## 5. Spielfeld-Engine

### Desktop (`spielfeld.py`)
- Basiert auf `tkinter.Canvas`
- Sprite-Klasse mit AABB-Kollisionserkennung
- `spielschleife()` nutzt `root.after()` für nicht-blockierendes Game-Loop

### Web (`spielfeld_web.py`)
- Pyodide JS-Bridge: Python → `js.window._zuseCanvas.*`
- `spielschleife()` nutzt `setInterval` im Browser
- `create_proxy()` für Python-Callbacks in JavaScript

### Gleiche API
Derselbe Zuse-Code funktioniert auf beiden Plattformen:
```zuse
spiel = Spielfeld("Test", 400, 300, "schwarz")
s = spiel.neuer_sprite(100, 100, 20, 20, "gruen")
```

---

## 6. Weitere Komponenten

| Komponente | Datei | Zweck |
|-----------|-------|-------|
| Semantische Analyse | `semantic_analyzer.py` | Undefinierte Variablen, Break außerhalb Schleife, Shadowing |
| Debugger | `debugger.py` | Breakpoints, Schritt-für-Schritt, Watch |
| LSP Server | `lsp/zuse_server.py` | Diagnosen, Hover, Completion, Go-to-Definition |
| Paketmanager | `zpkg_core.py`, `zpkg.py` | Init, Install, Remove, Abhängigkeiten |
| Studio IDE | `zuse_studio.py` | tkinter-basierte Desktop-IDE |
| Playground | `playground/index.html` | Browser-IDE mit Pyodide |
| Fehler-i18n | `error_i18n.py` | 6-sprachige Fehlermeldungen |
| Sprach-Loader | `language_loader.py` | JSON-Sprachkonfigurationen laden |

---

## 7. Dateistruktur

```
Zuse 7.3/
├── lexer.py                 # Tokenizer
├── parser.py                # AST-Erzeugung
├── interpreter.py           # Ausführung
├── transpiler.py            # Transpiler-Dispatcher
├── backends/
│   ├── base_backend.py      # Abstrakte Basis
│   ├── python_backend.py
│   ├── javascript_backend.py
│   ├── java_backend.py
│   ├── csharp_backend.py
│   └── wasm_backend.py
├── spielfeld.py             # Desktop-Grafik (tkinter)
├── spielfeld_web.py         # Web-Grafik (Pyodide)
├── lsp/
│   └── zuse_server.py       # Language Server
├── sprachen/
│   ├── deutsch.json         # Keyword-Übersetzungen
│   ├── english.json
│   └── ... (6 Sprachen)
├── bibliothek/
│   ├── deutsch.zuse         # Standardbibliothek
│   └── ... (6 Sprachen)
├── playground/
│   └── index.html           # Web-Playground
├── docs/
│   ├── tutorial.md
│   ├── referenz.md
│   ├── spielfeld_api.md
│   └── architektur.md
├── tests/                   # 1049+ Tests
└── beispiele/               # 15 Beispielprogramme
```
