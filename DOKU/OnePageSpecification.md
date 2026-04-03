# Zuse 7.3 – One-Page Specification

## Ziel

Zuse 7.3 ist eine **mehrsprachige, transpilierende Programmiersprache**, deren **natürliche Sprache der Keywords austauschbar** ist, ohne Semantik, AST oder Laufzeit zu verändern. Sie trennt strikt **Oberflächensyntax** (Landessprache) von **kanonischer Sprachrepräsentation** und erzeugt produktionsreifen Code in 5 Zielsprachen.

---

## Kernidee

* **Kanonische Sprache**: Alle Sprachkonstrukte werden intern über feste Schlüssel (`KW_WENN`, `KW_FANGE`, …) repräsentiert.
* **Sprach-Mapping**: Natürliche Sprachen sind externe Konfigurationen (JSON), die kanonische Schlüssel auf konkrete Wörter abbilden.
* **AST-Stabilität**: Parser und Interpreter arbeiten ausschließlich mit kanonischen Symbolen.
* **Übersetzbarkeit**: Quellcode kann verlustfrei zwischen Landessprachen übersetzt werden.
* **Transpilierung**: Ein sprachunabhängiger AST wird von 5 Backends in Python, JavaScript, Java, C# und WebAssembly übersetzt.

---

## Architektur

**Pipeline**

1. **Language Loader** lädt Sprach-Mapping (z. B. `deutsch.json`).
2. **Lexer** erkennt Keywords anhand des Mappings und erzeugt Tokens mit kanonischen Typen.
3. **Parser** erzeugt einen sprachunabhängigen **AST**.
4. **Interpreter** (Visitor Pattern) führt den AST aus (semantisch invariant).
5. **Transpiler** (5 Backends) übersetzt den AST in Python, JavaScript, Java, C# oder WebAssembly.
6. **Studio/IDE** erlaubt Live-Übersetzung, Debugging und Ausführung.

**Trennung der Ebenen**

* Oberfläche: natürliche Sprache (6 Sprachen)
* Syntax: kanonische Tokens
* Semantik: AST + Interpreter / Transpiler

---

## Sprachmerkmale

* **Imperativ & objektorientiert** (Klassen, Methoden, Vererbung, Polymorphie, `MEIN`, `ELTERN`).
* **Kontrollstrukturen**: `WENN/SONST`, `WÄHLE/FALL` (Switch/Case), Schleifen (`SOLANGE`, `FÜR`), `ABBRUCH`, `WEITER`.
* **Fehlerbehandlung**: `VERSUCHE/FANGE`.
* **Funktionen & Lambdas** (`AKTION`), Default-Parameter, `GLOBAL`.
* **Datenstrukturen**: Listen, Dictionaries, Slicing, Mehrfachzuweisung.
* **50+ eingebaute Funktionen**: Mathematik, Text, Listen, Dateien, Zufall, Typprüfung, Formatierung.
* **Ein-/Ausgabe**: Text/Zahl.
* **Python-Bridge (God Mode)**: Zugriff auf das gesamte Python-Ökosystem.

---

## Grafik & Spiele

* **Turtle-Grafik (Maler)**: Zeichenbefehle in der Muttersprache, Browser-Unterstützung via HTML5 Canvas.
* **Spielfeld-Engine**: Vollständige 2D-Game-Engine mit Sprites, Kollisionserkennung, Tastatur-/Mauseingabe, Spielschleife (60 FPS), Zeichenfunktionen.

---

## Transpiler (5 Backends)

| Backend | Ziel | Einsatzgebiet |
| :--- | :--- | :--- |
| Python | `.py` | Datenwissenschaft, KI, Automatisierung |
| JavaScript | `.js` | Web, Node.js, Browser |
| Java | `.java` | Android, Enterprise |
| C# | `.cs` | Unity, .NET, Windows |
| WebAssembly | `.wasm` | Hochleistung im Browser |

---

## Mehrsprachigkeit

* **6 Landessprachen**: Deutsch, Englisch, Spanisch, Französisch, Italienisch, Portugiesisch.
* **Kein Neu-Parsen** der Semantik beim Sprachwechsel.
* **Deterministische Übersetzung** zwischen Sprachen (kanonische Zwischenschicht).
* **Beliebig erweiterbar** über zusätzliche JSON-Dateien.

---

## Werkzeuge

* **Zuse Studio (IDE)**: Syntax-Highlighting, Lern-/Profi-Modus, integrierter Transpiler, GUI-Block-Modus.
* **Debugger**: Breakpoints, Schritt-für-Schritt-Ausführung, Variablen-Inspektion.
* **LSP-Server**: Language Server Protocol für VS Code und andere Editoren (Go-to-Definition, Hover-Doku).
* **Semantische Analyse**: Variable-Shadowing, unerreichbarer Code, doppelte Parameter, zirkuläre Vererbung.
* **Web Playground**: Zuse im Browser (Pyodide + CodeMirror + HTML5 Canvas), ohne Installation.
* **Paketmanager (zpkg)**: Pakete installieren und teilen, Semantic Versioning, Pfad-Traversal-Schutz.

---

## Laufzeit & Sicherheit

* **Sandbox-Interpreter** mit kontrolliertem Modulimport (Lern-Modus).
* **Rekursionstiefen-Limit**.
* **Thread-sichere GUI-Integration** (nicht blockierende Eingaben).
* **Pfad-Traversal-Schutz** im Paketmanager.
* **Sichere Dateioperationen** (with-Statements).

---

## Qualität

* **1086+ automatisierte Tests** in 31 Testmodulen.
* **6 umfassende Dokumentationen** (Tutorial, Referenz, Architektur, Spielfeld-API, Sprachvergleich, Beispiele).
* **Sentinel Pattern** für sichere Attribut-Zugriffe.
* **Variable Tracking** in Java/C#-Backends (keine doppelten Deklarationen).

---

## Design-Prinzipien

* Sprachneutraler Kern
* Erweiterbarkeit statt Monolith
* Lesbarkeit vor Kürze
* Bildung & Exploration als Primärziel

---

## Abgrenzung

* Keine reine Keyword-Übersetzung: **kanonischer Sprachkernel**.
* Keine visuelle Sprache: **vollwertige Textsprache**.
* Keine Editor-Lokalisierung: **sprachliche Semantik bleibt identisch**.

---

## Einsatzgebiete

* Bildung & Lehre in der Muttersprache
* Mehrsprachige Teams & Dokumentation
* Sprach- und Compilerforschung
* Rapid Prototyping mit Python-Ökosystem
* Spieleentwicklung (Spielfeld-Engine)
* Web-Deployment (Transpiler → JS/WASM)

---

## Status

* Funktionsfähiger Interpreter, Transpiler & IDE
* 5 Transpiler-Backends produktiv
* Mehrsprachige Syntax produktiv (6 Sprachen)
* 2D-Game-Engine & Turtle-Grafik
* Debugger, LSP-Server, Web Playground
* 1086+ Tests bestanden

---

## Ausblick für die Zukunft

Zuse soll in Zukunft weiter ausgebaut werden, so dass es auch auf weiteren Programmiersprachen aufsetzen kann.

Dieses Konzept nennen wir:
**"double multilingual"**

<img width="800" height="810" alt="image" src="https://github.com/user-attachments/assets/4f2eaad8-9a04-4fc3-8a67-aadbfec8988e" />
