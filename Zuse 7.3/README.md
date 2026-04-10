# Zuse — Die mehrsprachige Programmiersprache

**Programmieren in deiner Muttersprache.**

Zuse ist eine Bildungs-Programmiersprache, mit der Anfaenger in 6 Sprachen programmieren lernen koennen. Der Code wird direkt ausgefuehrt oder in Python, JavaScript, Java, C# und WebAssembly transpiliert.

```
AUSGABE "Hallo Welt!"

x = 10
SOLANGE x > 0 MACHE
    AUSGABE x
    x = x - 1
ENDE SCHLEIFE

AUSGABE "Start!"
```

## Funktionen

- **6 Sprachen**: Deutsch, English, Espanol, Francais, Italiano, Portugues
- **5 Transpiler-Backends**: Python, JavaScript, Java, C#, WebAssembly (WAT)
- **Grafische IDE**: Zuse Studio mit Syntax-Highlighting und Transpiler-Integration
- **Web-Playground**: Zuse im Browser ohne Installation (Pyodide + CodeMirror)
- **Turtle-Grafik**: Maler/Pintor/Painter — zeichne Grafiken in jeder Sprache (Desktop + Web)
- **Spielfeld-Engine**: 2D-Grafik-API mit Sprites, Tastatur- und Maus-Steuerung
- **Debugger**: Breakpoints, Einzelschritt, Variablen-Inspektion
- **Paket-Manager**: `zpkg` mit SemVer-Versionsaufloesung und Abhaengigkeitsmanagement
- **LSP-Server**: VS Code Integration mit Autovervollstaendigung, Hover-Doku und Go-to-Definition
- **Semantische Analyse**: Warnungen fuer undefinierte Variablen, Shadowing, unerreichbaren Code
- **Mehrsprachige Fehlermeldungen**: Fehler und Tipps in allen 6 Sprachen
- **1086 Tests**: Umfangreiche Testabdeckung

## Installation

```bash
# Mit pip (empfohlen)
pip install -e .

# Oder direkt ausfuehren
python zuse_cli.py run mein_programm.zuse
```

## Schnellstart

### 1. Programm ausfuehren

```bash
zuse run hallo.zuse
```

### 2. In eine andere Sprache transpilieren

```bash
zuse transpile hallo.zuse --ziel javascript
zuse transpile hallo.zuse --ziel java
zuse transpile hallo.zuse --ziel csharp
zuse transpile hallo.zuse --ziel wasm
```

### 3. Im Debugger starten

```bash
zuse debug hallo.zuse
```

### 4. Syntax pruefen

```bash
zuse check hallo.zuse
```

### 5. Studio starten

```bash
zuse studio
```

## Dasselbe Programm in 6 Sprachen

**Deutsch:**
```
DEFINIERE gruss(name):
    AUSGABE "Hallo, " + name + "!"
ENDE FUNKTION
gruss("Welt")
```

**English:**
```
DEFINE greet(name):
    PRINT "Hello, " + name + "!"
END FUNCTION
greet("World")
```

**Espanol:**
```
DEFINIR saludo(nombre):
    MOSTRAR "Hola, " + nombre + "!"
FIN FUNCION
saludo("Mundo")
```

## Projektstruktur

```
zuse_cli.py            # CLI-Einstiegspunkt (zuse run/studio/transpile/debug/check)
interpreter.py         # Interpreter (Visitor Pattern + Symbol Table)
lexer.py               # Lexer (Token-Erzeugung)
parser.py              # Parser (AST-Erzeugung mit Error-Recovery)
transpiler.py          # Transpiler-Orchestrator
ir.py                  # Intermediate Representation
optimizer.py           # IR-Optimierer (Constant Folding, Dead Code Elimination)
semantic_analyzer.py   # Semantische Analyse (Warnungen)
backends/              # 5 Transpiler-Backends (Python, JS, Java, C#, WASM)
sprachen/              # 6 Sprach-Konfigurationen (JSON)
bibliothek/            # Standard-Bibliothek (.zuse Dateien)
spielfeld.py           # 2D-Grafik-Engine (Desktop, tkinter)
spielfeld_web.py       # 2D-Grafik-Engine (Browser, Canvas)
maler_web.py           # Turtle-Grafik (Browser, Canvas)
error_messages.py      # Mehrsprachige Fehlermeldungen
error_hints.py         # Anfaengerfreundliche Fehlertipps
error_i18n.py          # i18n-Framework
builtin_i18n.py        # Mehrsprachige Builtin-Uebersetzungen
debugger.py            # Debugger-Kern
zuse_debug.py          # CLI-Debugger
zuse_studio.py         # Grafische IDE (tkinter)
zpkg_core.py           # Paket-Manager Kern
zpkg.py                # Paket-Manager CLI
lsp/                   # Language Server Protocol
playground/            # Web-Playground (Pyodide + CodeMirror)
tests/                 # 1086 Tests
docs/                  # Dokumentation
```

## Dokumentation

- [Sprachreferenz](docs/referenz.md) — Alle Keywords, Typen und Builtins
- [Tutorial](docs/tutorial.md) — 10 Lektionen von Hallo Welt bis Klassen
- [Beispiele](docs/beispiele.md) — Katalog aller Beispielprogramme
- [Spielfeld-API](docs/spielfeld_api.md) — 2D-Grafik-Engine Referenz
- [Architektur](docs/architektur.md) — Technische Architektur und Pipeline

## Voraussetzungen

- Python 3.10 oder neuer
- tkinter (fuer Zuse Studio, in den meisten Python-Installationen enthalten)
- Optional: `pygls` und `lsprotocol` fuer den LSP-Server

```bash
# LSP-Unterstuetzung installieren
pip install -e ".[lsp]"
```

## Lizenz

GNU GPL v3 License

---

*Benannt nach [Konrad Zuse](https://de.wikipedia.org/wiki/Konrad_Zuse), dem Erfinder des ersten funktionsfaehigen Computers.*
