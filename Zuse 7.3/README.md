# ZUSE v7.3 — Multilingual Edition

![Version](https://img.shields.io/badge/Version-7.3-blue) ![Language](https://img.shields.io/badge/Made_with-Python-yellow) ![Status](https://img.shields.io/badge/Status-Stable-green) ![Tests](https://img.shields.io/badge/Tests-1086+-brightgreen)
(English translation below!)

**Die mehrsprachige, transpilierende Programmiersprache für Bildung und Industrie.**
*Built on the power of Python.*

**Zuse** is an object-oriented, transpiling programming language designed to break the barrier between "Learning Languages" (like Scratch) and "Pro Languages" (like Python/C++).

---

## Demos

### Multilingual programming language Zuse

https://github.com/user-attachments/assets/4cd4c600-b687-4666-b50b-2a62dd66fe54



### Multilingual programming language Zuse DEMO 2

https://github.com/user-attachments/assets/4e110498-f6c1-4df8-a8d2-e0db3fb881e9

---

## Was ist Zuse?

Willkommen bei **Zuse**! Zuse ist eine moderne, mehrsprachige Programmiersprache (**Deutsch**, **English**, **Español**, **Français**, **Italiano**, **Português**, **Hindi & 中文**), die speziell für Bildungszwecke, Rapid Prototyping und den professionellen Einsatz entwickelt wurde. Sie ermöglicht alles — von einfachen Rechnungen bis hin zu komplexen Spielen, grafischen Oberflächen und transpiliertem Produktionscode.

Der Name **"Zuse"** geht auf **Konrad Zuse** zurück, der 1941 mit dem **Z3** den weltweit ersten funktionsfähigen programmgesteuerten Computer entwickelte und mit dem **Plankalkül** die erste höhere Programmiersprache entwarf. Dieses Projekt greift bewusst den Ansatz der Einfachheit von Konrad Zuse auf.

> Die daraus resultierende Philosophie
> **„weil 'Einfach', einfach einfach ist"**
> bildet wie bei allen anderen Innobytix-IT Projekten das Fundament.

---

## Features

### Kernsprache
- **8 Sprachen:** Programmiere in Deutsch, Englisch, Spanisch, Französisch, Italienisch, Portugiesisch Hindi oder 中文 — alle Schlüsselwörter, Fehlermeldungen und Builtins sind vollständig übersetzt
- **Objektorientierung:** Klassen, Vererbung, Polymorphie, Konstruktoren (`KLASSE`, `MEIN`, `ELTERN`)
- **Fehlerbehandlung:** `VERSUCHE` / `FANGE` (Try/Catch)
- **Lambda-Funktionen:** `AKTION(x): x * 2`
- **Switch/Case:** `WÄHLE` / `FALL` für elegante Fallunterscheidungen
- **Slicing:** `liste[1:3]` für Listen und Strings
- **Default-Parameter:** `DEFINIERE f(x, y=10)`
- **Mehrfachzuweisung:** `a, b = b, a`
- **Typprüfung:** `IST_ZAHL()`, `IST_TEXT()`, `IST_LISTE()`, `ALS_ZAHL()`, `ALS_TEXT()`
- **50+ eingebaute Funktionen:** Mathematik, Text, Listen, Dateien, Zufall, Formatierung

### Transpiler (5 Backends)
- **Python** — Saubere, ausführbare `.py`-Skripte
- **JavaScript** — Für Webseiten und Node.js
- **Java** — Für Android und Enterprise
- **C#** — Für Unity-Spiele und .NET
- **WebAssembly** — Hochleistung im Browser

### Grafik & Spiele
- **Turtle-Grafik (Maler):** Zeichne Sterne, Spiralen, Fraktale — in deiner Muttersprache
- **Spielfeld-Engine:** Vollständige 2D-Game-Engine mit Sprites, Kollisionserkennung, Tastatur-/Mauseingabe und Spielschleife (60 FPS)
- **GUI-Modus:** Grafische Fenster mit tkinter-Unterstützung

### Werkzeuge
- **Zuse Studio (IDE):** Syntax-Highlighting, Lern-/Profi-Modus, integrierter Transpiler
- **Debugger:** Breakpoints, Schritt-für-Schritt-Ausführung, Variablen-Inspektion
- **LSP-Server:** Language Server Protocol für VS Code und andere Editoren
- **Semantische Analyse:** Erkennt Variablen-Shadowing, unerreichbaren Code, doppelte Parameter
- **Web Playground:** Zuse im Browser ausführen — ohne Installation (Pyodide + CodeMirror)
- **Paketmanager (zpkg):** Pakete installieren, verwalten und teilen mit SemVer-Versionierung

### "God Mode" (Python-Bridge)
- **Voller Python-Zugriff:** Nutze jede installierte Python-Bibliothek direkt in Zuse (`requests`, `pandas`, `matplotlib`, `tkinter`, ...)
- **Sicherheitssystem:** Lern-Modus sperrt gefährliche Module — perfekt für Schulen

### Qualität
- **1086+ automatisierte Tests** in 31 Testmodulen
- **6 umfassende Dokumentationen** (Tutorial, Referenz, Architektur, Spielfeld-API, Sprachvergleich, Beispiele)
- **Pfad-Traversal-Schutz** im Paketmanager
- **Sichere Dateioperationen** (with-Statements)

---

## Schnellstart

```zuse
# Hallo Welt
AUSGABE "Hallo Welt!"

# Variablen
name = EINGABE_TEXT "Wie heißt du? "
AUSGABE "Willkommen, " + name + "!"

# Schleifen
SCHLEIFE FÜR i IN BEREICH(5) MACHE
    AUSGABE i
ENDE SCHLEIFE

# Funktionen
DEFINIERE quadrat(x)
    ERGEBNIS IST x ^ 2
ENDE FUNKTION

AUSGABE quadrat(7)    # 49

# Klassen
KLASSE Roboter:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION

    DEFINIERE gruss():
        AUSGABE "Ich bin " + MEIN.name + "!"
    ENDE FUNKTION
ENDE KLASSE

r = Roboter("Zuse")
r.gruss()
```

---

## Projektstruktur

```
Zuse 7.3/
├── interpreter.py          # Interpreter (Visitor Pattern)
├── lexer.py                # Tokenizer
├── parser.py               # AST-Parser
├── error_messages.py       # Fehlermeldungen (8 Sprachen)
├── builtin_i18n.py         # Eingebaute Funktionen (i18n)
├── zpkg_core.py            # Paketmanager
├── maler_web.py            # Turtle-Grafik (Browser)
├── zuse_studio.py          # IDE (Zuse Studio)
├── zuse_lsp_server.py      # LSP-Server
├── sprachen/               # Sprachdefinitionen (JSON)
│   ├── deutsch.json
│   ├── english.json
│   ├── espaniol.json
│   ├── francais.json
│   ├── italiano.json
│   ├── hindi.json
│   ├── chinese.json
│   └── portugues.json
├── bibliothek/             # Standardbibliothek (8 Sprachen)
│   ├── deutsch.zuse        # Maler + Spielfeld
│   ├── english.zuse
│   ├── espaniol.zuse
│   ├── francais.zuse
│   ├── italiano.zuse
│   ├── hindi.zuse
│   ├── chinese.zuse
│   └── portugues.zuse
├── backends/               # Transpiler-Backends
│   ├── python_backend.py
│   ├── javascript_backend.py
│   ├── java_backend.py
│   ├── csharp_backend.py
│   └── wasm_backend.py
├── tests/                  # 31 Testmodule (1086+ Tests)
├── docs/                   # Dokumentation
│   ├── tutorial.md
│   ├── referenz.md
│   ├── architektur.md
│   ├── spielfeld_api.md
│   ├── sprachvergleich.md
│   └── beispiele.md
└── playground/             # Web Playground
    ├── index.html
    └── server.py
```

---

## Architektur

```
┌──────────────┐
│   Zuse IDE   │  (Zuse Studio / Web Playground / VS Code + LSP)
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌───────────────────┐
│    Lexer     │◄────│  Sprachdateien    │
│  (Tokenizer) │     │  deutsch.json     │
└──────┬───────┘     │  english.json ... │
       │             └───────────────────┘
       ▼
┌──────────────┐
│    Parser    │
│    (AST)     │
└──────┬───────┘
       │
       ├─────────────────────┐
       ▼                     ▼
┌──────────────┐     ┌──────────────────┐
│ Interpreter  │     │   Transpiler     │
│  (Visitor)   │     │   (5 Backends)   │
└──────┬───────┘     └──────┬───────────┘
       │                    │
       ▼                    ├──► Python (.py)
┌──────────────┐            ├──► JavaScript (.js)
│ Python-Bridge│            ├──► Java (.java)
│ ("God Mode") │            ├──► C# (.cs)
└──────────────┘            └──► WebAssembly (.wasm)
```

---

## Mehrsprachigkeit — Codebeispiel

**Deutsch:**
```zuse
WENN alter >= 18 DANN
    AUSGABE "Willkommen!"
ENDE WENN
```

**English:**
```zuse
IF age >= 18 THEN
    PRINT "Welcome!"
END IF
```

**Español:**
```zuse
SI edad >= 18 ENTONCES
    MOSTRAR "Bienvenido!"
FIN SI
```

**Français:**
```zuse
SI age >= 18 ALORS
    AFFICHER "Bienvenue!"
FIN SI
```

---

## Mitwirken

Dieses Projekt ist **Open-Source** und freut sich über jede Form der Unterstützung!
Zuse v7.3 kommt mit einer **GPL v3** (siehe Lizenz-Datei).

Wenn du dieses Projekt nutzt oder weiterentwickelst, freuen wir uns über eine namentliche Erwähnung in der README (*"Zuse von Innobytix-it.de"*), dies ist jedoch keine Pflicht.

---

## Danksagung & Projektphilosophie

Dieses Projekt ist das Ergebnis einer Vision, die durch den Einsatz moderner KI-Werkzeuge Wirklichkeit werden konnte. Es ist ein Beispiel für Selbstverwirklichung und den Wunsch, nützliche und freie Software für alle zugänglich zu machen.

Mein aufrichtiger Dank gilt den Entwicklern und Forschern, deren Arbeit diese Werkzeuge ermöglicht hat. In diesem Projekt fungierten sie als unermüdliche digitale Assistenten, die den Code schrieben, während die Vision, die Architektur und die Leitung des Projekts in meiner Verantwortung lagen. Gott sei Dank konnte ich dadurch meine persönlichen Ressourcen hauptsächlich auf Design- und Architekturfragen, die Funktionsweisen und den Inhalt der Software konzentrieren, anstatt mühevoll Codezeile für Codezeile selbst zu schreiben.

Ich bin zutiefst dankbar für die Möglichkeit, meine Ideen auf diese Weise umsetzen und teilen zu dürfen. Dieses Projekt soll ein demütiger Beweis dafür sein, wie Leidenschaft und moderne KI-Technologie zusammenkommen können, um nützliche und offene Alternativen zu schaffen. Durch den modularen Aufbau wurde das Projekt von Anfang an so konzipiert, dass Erweiterungen und Ergänzungen jederzeit möglich sind. Jeder, der möchte, ist herzlich eingeladen, seine eigenen Ideen und Visionen mit einzubringen und umzusetzen.

**Manuel Person**
GPL v3
---

# ZUSE v7.3 — Multilingual Edition (English)

**The multilingual, transpiling programming language for education and industry.**
*Built on the power of Python.*

---

## Demos

### Multilingual programming language Zuse

https://github.com/user-attachments/assets/03e8e32d-35db-4854-aa98-44cb26ff9e0f

### Multilingual programming language Zuse DEMO 2

https://github.com/user-attachments/assets/4e110498-f6c1-4df8-a8d2-e0db3fb881e9

---

## What is Zuse?

Welcome to **Zuse**! Zuse is a modern, multilingual programming language (**German**, **English**, **Spanish**, **French**, **Italian**, **Portuguese**, **Hindi & 中文**) designed for education, rapid prototyping, and professional use. It covers everything — from simple calculations to complex games, graphical interfaces, and transpiled production code.

The name **"Zuse"** refers to **Konrad Zuse**, who in 1941 developed the **Z3**, the world's first functional program-controlled computer, and designed **Plankalkül**, the first high-level programming language. This project consciously adopts Konrad Zuse's principle of simplicity.

> The resulting philosophy —
> **"because 'simple' is simply simple"** —
> forms the foundation of this project.

---

## Features

### Core Language
- **8 Languages:** Program in German, English, Spanish, French, Italian, Portuguese, Hindi or 中文  — all keywords, error messages, and builtins are fully translated
- **Object Orientation:** Classes, inheritance, polymorphism, constructors (`CLASS`, `MY`, `PARENT`)
- **Error Handling:** `TRY` / `CATCH`
- **Lambda Functions:** `LAMBDA(x): x * 2`
- **Switch/Case:** `SWITCH` / `CASE` for elegant branching
- **Slicing:** `list[1:3]` for lists and strings
- **Default Parameters:** `DEFINE f(x, y=10)`
- **Multiple Assignment:** `a, b = b, a`
- **Type Checking:** `IS_NUMBER()`, `IS_TEXT()`, `IS_LIST()`, `AS_NUMBER()`, `AS_TEXT()`
- **50+ built-in functions:** Math, text, lists, files, random, formatting

### Transpiler (5 Backends)
- **Python** — Clean, executable `.py` scripts
- **JavaScript** — For websites and Node.js
- **Java** — For Android and enterprise
- **C#** — For Unity games and .NET
- **WebAssembly** — High-performance in the browser

### Graphics & Games
- **Turtle Graphics (Painter):** Draw stars, spirals, fractals — in your native language
- **Game Engine (Spielfeld):** Full 2D game engine with sprites, collision detection, keyboard/mouse input, and game loop (60 FPS)
- **GUI Mode:** Graphical windows with tkinter support

### Tools
- **Zuse Studio (IDE):** Syntax highlighting, learning/professional mode, integrated transpiler
- **Debugger:** Breakpoints, step-by-step execution, variable inspection
- **LSP Server:** Language Server Protocol for VS Code and other editors
- **Semantic Analysis:** Detects variable shadowing, unreachable code, duplicate parameters
- **Web Playground:** Run Zuse in the browser — no installation needed (Pyodide + CodeMirror)
- **Package Manager (zpkg):** Install, manage, and share packages with SemVer versioning

### "God Mode" (Python Bridge)
- **Full Python Access:** Use any installed Python library directly in Zuse (`requests`, `pandas`, `matplotlib`, `tkinter`, ...)
- **Security System:** Learning mode blocks dangerous modules — perfect for schools

### Quality
- **1086+ automated tests** across 31 test modules
- **6 comprehensive documentations** (tutorial, reference, architecture, game engine API, language comparison, examples)
- **Path traversal protection** in the package manager
- **Safe file operations** (with-statements)

---

## Quick Start

```zuse
# Hello World
PRINT "Hello World!"

# Variables
name = INPUT_TEXT "What is your name? "
PRINT "Welcome, " + name + "!"

# Loops
LOOP FOR i IN RANGE(5) DO
    PRINT i
END LOOP

# Functions
DEFINE square(x)
    RESULT IS x ^ 2
END FUNCTION

PRINT square(7)    # 49

# Classes
CLASS Robot:
    DEFINE CREATE(name):
        MY.name = name
    END FUNCTION

    DEFINE greet():
        PRINT "I am " + MY.name + "!"
    END FUNCTION
END CLASS

r = Robot("Zuse")
r.greet()
```

---

## Project Structure

```
Zuse 7.3/
├── interpreter.py          # Interpreter (Visitor Pattern)
├── lexer.py                # Tokenizer
├── parser.py               # AST Parser
├── error_messages.py       # Error messages (8 languages)
├── builtin_i18n.py         # Built-in functions (i18n)
├── zpkg_core.py            # Package manager
├── maler_web.py            # Turtle graphics (browser)
├── zuse_studio.py          # IDE (Zuse Studio)
├── zuse_lsp_server.py      # LSP Server
├── sprachen/               # Language definitions (JSON)
│   ├── deutsch.json
│   ├── english.json
│   ├── espaniol.json
│   ├── francais.json
│   ├── italiano.json
│   ├── hindi.json
│   ├── chinese.json
│   └── portugues.json
├── bibliothek/             # Standard library (8 languages)
│   ├── deutsch.zuse        # Painter + Game Engine
│   ├── english.zuse
│   ├── espaniol.zuse
│   ├── francais.zuse
│   ├── italiano.zuse
│   ├── hindi.zuse
│   ├── chinese.zuse
│   └── portugues.zuse
├── backends/               # Transpiler backends
│   ├── python_backend.py
│   ├── javascript_backend.py
│   ├── java_backend.py
│   ├── csharp_backend.py
│   └── wasm_backend.py
├── tests/                  # 31 test modules (1086+ tests)
├── docs/                   # Documentation
│   ├── tutorial.md
│   ├── referenz.md
│   ├── architektur.md
│   ├── spielfeld_api.md
│   ├── sprachvergleich.md
│   └── beispiele.md
└── playground/             # Web Playground
    ├── index.html
    └── server.py
```

---

## Architecture

```
┌──────────────┐
│   Zuse IDE   │  (Zuse Studio / Web Playground / VS Code + LSP)
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌───────────────────┐
│    Lexer     │◄────│  Language Files   │
│  (Tokenizer) │     │  deutsch.json     │
└──────┬───────┘     │  english.json ... │
       │             └───────────────────┘
       ▼
┌──────────────┐
│    Parser    │
│    (AST)     │
└──────┬───────┘
       │
       ├─────────────────────┐
       ▼                     ▼
┌──────────────┐     ┌──────────────────┐
│ Interpreter  │     │   Transpiler     │
│  (Visitor)   │     │   (5 Backends)   │
└──────┬───────┘     └──────┬───────────┘
       │                    │
       ▼                    ├──► Python (.py)
┌──────────────┐            ├──► JavaScript (.js)
│ Python Bridge│            ├──► Java (.java)
│ ("God Mode") │            ├──► C# (.cs)
└──────────────┘            └──► WebAssembly (.wasm)
```

---

## Multilingual — Code Example

**Deutsch:**
```zuse
WENN alter >= 18 DANN
    AUSGABE "Willkommen!"
ENDE WENN
```

**English:**
```zuse
IF age >= 18 THEN
    PRINT "Welcome!"
END IF
```

**Español:**
```zuse
SI edad >= 18 ENTONCES
    MOSTRAR "Bienvenido!"
FIN SI
```

**Français:**
```zuse
SI age >= 18 ALORS
    AFFICHER "Bienvenue!"
FIN SI
```

---

## Contribute

This project is **open-source** and we welcome any form of support!
Zuse v7.3 is released under the **GPL v3** (see License file).

If you use or extend this project, attribution in your README (*"Zuse by Innobytix-it.de"*) is appreciated, but not required.

---

## Acknowledgments & Project Philosophy

This project is the result of a vision made possible through the use of modern AI tools. It is an example of self-actualization and the desire to create useful, free software accessible to everyone.

My sincere gratitude goes to the developers and researchers whose work made these tools possible. In this project, they served as tireless digital assistants who wrote the code, while the vision, architecture, and project leadership remained my responsibility. Thanks to this, I was able to focus my personal resources primarily on design and architectural decisions, functionality, and the content of the software, rather than laboriously writing code line by line.

I am deeply grateful for the opportunity to realize and share my ideas in this way. This project is meant to be a humble proof of how passion and modern AI technology can come together to create useful and open alternatives. Through its modular design, the project was conceived from the start to allow extensions and additions at any time. Everyone who wishes to is warmly invited to contribute their own ideas and visions.

**Manuel Person**

---

**Architect:** Manuel Person


**License:** Open Source GPL v3
