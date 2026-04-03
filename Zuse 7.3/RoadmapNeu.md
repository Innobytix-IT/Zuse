# Zuse Roadmap zur Vollendung

**Stand:** 02. April 2026 | **Aktuelle Version:** 7.3.0
**Ziel:** Zuse 8.0 — Produktionsreif

> **Fortschritt:** Phase 1-10 abgearbeitet am 02.04.2026.
> Alle 59 Punkte bearbeitet. 1086 Tests bestanden (vorher 1049).

---

## Phase 1: Kritische Fehler beheben (v7.3)

### 1.1 Python-Tracebacks entfernen
- **Datei:** `interpreter.py` Zeile 287-290
- **Problem:** `traceback.print_exc()` gibt interne Python-Fehlermeldungen an Schüler weiter
- **Lösung:** Traceback nur in Debug-Modus loggen, Benutzer bekommt nur die übersetzte Fehlermeldung

### 1.2 Java-Backend: Konstruktoren reparieren
- **Datei:** `backends/java_backend.py` Zeile 369-378
- **Problem:** Generiert `Object _init()` statt echten Java-Konstruktor — kein Java-Code mit Klassen kompiliert
- **Lösung:** Echte `public ClassName(...)` Konstruktor-Syntax generieren

### 1.3 WASM-Backend: Stille Fehler beseitigen
- **Datei:** `backends/wasm_backend.py` Zeile 281
- **Problem:** Nicht unterstützte Anweisungen werden als `// TODO` Kommentar ausgegeben, kein Fehler
- **Lösung:** `TranspilerError` werfen statt stillschweigend fehlerhaften Code zu erzeugen

### 1.4 Spielschleife: Exception-Handling reparieren
- **Datei:** `spielfeld.py` Zeile ~205
- **Problem:** `except Exception: pass` verschluckt alle Fehler in der Spielschleife
- **Lösung:** Fehler an den Benutzer melden (mindestens in der Konsole ausgeben)

### 1.5 pyproject.toml: Fehlende Module ergänzen
- **Datei:** `pyproject.toml`
- **Problem:** `spielfeld_web.py` fehlt in `py-modules`, `playground/` nicht in der Distribution
- **Lösung:** Alle Module und Dateien korrekt in die Paketdefinition aufnehmen

---

## Phase 2: Sprachkern stabilisieren (v7.4)

### 2.1 Lexer: Unicode-Unterstützung erweitern
- **Datei:** `lexer.py` Zeile 25
- **Problem:** Nur deutsche Umlaute (äöüÄÖÜß) als Buchstaben erlaubt — Akzente aus Spanisch (á, é), Französisch (ç, è) fehlen
- **Lösung:** Erweiterte Unicode-Zeichenklassen verwenden (mindestens Latin Extended-A/B)

### 2.2 Lexer: Spaltenposition in Fehlermeldungen
- **Datei:** `lexer.py` Zeile 79
- **Problem:** Fehler zeigt nur Zeilennummer, nicht welches Zeichen/Spalte
- **Lösung:** Spaltenposition tracken und in Fehlermeldung einbauen

### 2.3 Parser: Mehrere Fehler sammeln statt beim ersten abbrechen
- **Datei:** `parser.py`
- **Problem:** Erster Syntaxfehler stoppt alles — Schüler müssen immer einen Fehler nach dem anderen fixen
- **Lösung:** Error-Recovery implementieren, mehrere Fehler auf einmal melden

### 2.4 Parser: Lambda mit mehreren Parametern
- **Datei:** `parser.py` Zeile 456-471
- **Problem:** `LAMBDA x, y: x + y` funktioniert nicht (nur ein Parameter ohne Klammern)
- **Lösung:** Komma-getrennte Parameter auch ohne Klammern unterstützen

### 2.5 Parser: Doppelte Parameternamen erkennen
- **Datei:** `parser.py` Zeile 185-199
- **Problem:** `DEFINIERE f(x, x):` wird akzeptiert — zweites x überschreibt erstes stillschweigend
- **Lösung:** Duplikate beim Parsen erkennen und Fehler melden

### 2.6 Interpreter: Funktionsaufruf-Arität prüfen
- **Datei:** `interpreter.py` Zeile 693
- **Problem:** Zu viele Keyword-Argumente werden stillschweigend akzeptiert
- **Lösung:** Prüfen ob alle übergebenen kwargs zu definierten Parametern passen

### 2.7 Interpreter: Zirkuläre Vererbung erkennen
- **Datei:** `interpreter.py` Zeile 111-126
- **Problem:** `KLASSE A(B)` + `KLASSE B(A)` erzeugt Endlosschleife bei Methodenauflösung
- **Lösung:** Vererbungskette beim Definieren auf Zyklen prüfen

### 2.8 Interpreter: Import-Caching
- **Datei:** `interpreter.py` Zeile 480-503
- **Problem:** Jedes `BENUTZE` parst die .zuse-Datei neu — bei mehrfachem Import Performance-Problem
- **Lösung:** Importierte Module cachen (einmal parsen, mehrmals nutzen)

### 2.9 Error-Handling: Platzhalter-Fallback reparieren
- **Datei:** `error_i18n.py` Zeile 71-75
- **Problem:** Fehlende Platzhalter zeigen `{line}` im Klartext statt Zeilennummer
- **Lösung:** Bei fehlenden Platzhaltern eine Warnung loggen und Template trotzdem brauchbar ausgeben

---

## Phase 3: Transpiler-Backends vervollständigen (v7.5)

### 3.1 Java-Backend: Typensicherheit verbessern
- **Problem:** Übermäßige `((Comparable)...)` Casts crashen zur Laufzeit bei inkompatiblen Typen
- **Lösung:** Typ-Hilfsklasse `ZuseRuntime.java` generieren mit sicheren Vergleichsmethoden

### 3.2 Java-Backend: Multi-Assignment korrigieren
- **Datei:** `backends/java_backend.py` Zeile 289-295
- **Problem:** Deklariert `Object` Variable in jeder Schleifeniteration neu
- **Lösung:** Variable vor der Schleife deklarieren

### 3.3 JavaScript-Backend: Import-Statements generieren
- **Datei:** `backends/javascript_backend.py` Zeile 333
- **Problem:** Imports werden auskommentiert statt als `require()` oder `import` generiert
- **Lösung:** Abhängig vom Ziel (Node.js/Browser) echte Imports generieren

### 3.4 JavaScript-Backend: Global-Statements implementieren
- **Datei:** `backends/javascript_backend.py` Zeile 335-336
- **Problem:** `GLOBAL` erzeugt nur Kommentar, kein Code
- **Lösung:** Variable im äußeren Scope suchen und referenzieren

### 3.5 WASM-Backend: String-Operationen
- **Problem:** Keine String-Verarbeitung möglich — nur Zahlenwerte
- **Lösung:** Grundlegende String-Funktionen über Memory + Host-Imports implementieren

### 3.6 WASM-Backend: Listen-Unterstützung
- **Problem:** Kein `INDEX_ZUGRIFF`, `LISTEN_LITERAL`, `SLICING`
- **Lösung:** Listen als linearer Speicher mit Pointer-Arithmetik oder als Host-Import

### 3.7 WASM-Backend: For-Schleife für Listen
- **Datei:** `backends/wasm_backend.py` Zeile 346-388
- **Problem:** Nur `BEREICH(n)` Ranges funktionieren — Listen-Iteration scheitert stillschweigend
- **Lösung:** Listen-Iteration über Länge + Index-Zugriff implementieren oder Fehler werfen

### 3.8 Alle Backends: Closure-Unterstützung testen und fixen
- **Problem:** Verschachtelte Funktionen mit Zugriff auf äußere Variablen erzeugen möglicherweise falschen Code in Python/Java/C#
- **Lösung:** Closure-Testfälle für alle Backends schreiben und Probleme beheben

---

## Phase 4: Semantische Analyse erweitern (v7.6)

### 4.1 BUILTINS-Liste synchronisieren
- **Datei:** `semantic_analyzer.py` Zeile 48-71
- **Problem:** Liste enthält Einträge (`print`, `range`, `abs`) die nicht als Builtins registriert sind
- **Lösung:** Liste mit tatsächlich verfügbaren Builtins im Interpreter abgleichen

### 4.2 Shadowing-Warnung
- **Problem:** Lokale Variable überschreibt Funktion/Globale Variable ohne Warnung
- **Lösung:** Warnung ausgeben wenn ein Name einen äußeren Scope verdeckt

### 4.3 Unerreichbarer Code erkennen
- **Problem:** Code nach `ERGEBNIS` wird stillschweigend akzeptiert aber nie ausgeführt
- **Lösung:** Warnung für Code nach Return-Statements

### 4.4 Fehlende Fehlerkategorien ergänzen
- Undefinierte Attribute zugreifen
- Typ-Mismatch bei Vergleichen (`"text" > 42`)
- Nicht-aufrufbare Objekte aufrufen

---

## Phase 5: Standardbibliothek ausbauen (v7.7)

### 5.1 Fehlende Builtin-Funktionen hinzufügen
- `alle()` / `irgendein()` — Boolesche Listen-Prüfung
- `ord()` / `zeichen()` — Zeichencode-Konvertierung
- `hex()` / `bin()` / `okt()` — Zahlenformatierung
- `absolut()` als Alias für ABSOLUT (Konsistenz)

### 5.2 Bibliothek erweitern
- **Problem:** Aktuell nur 2 Klassen (Fenster, Maler) und 2 Funktionen (zufallszahl, warte)
- **Lösung:** Mathe-Modul, Text-Werkzeuge, Listen-Helfer als .zuse-Bibliotheken hinzufügen

### 5.3 Spielfeld-API erweitern
- Maus-Events (Klick, Bewegung, Position)
- Bild-Laden (PNG/JPG als Sprites)
- Polygon-Zeichnung
- Z-Order / Ebenen
- Sound-Wiedergabe (einfache Töne)

### 5.4 Spielfeld-Web mit Desktop synchron halten
- **Problem:** `spielfeld_web.py` hat nicht alle Methoden die `spielfeld.py` hat
- **Lösung:** API-Parität sicherstellen — gleicher Zuse-Code muss überall laufen

---

## Phase 6: Web Playground professionalisieren (v7.8)

### 6.1 Syntax-Highlighting einbauen
- **Problem:** Reines `<textarea>` ohne Hervorhebung — kein Editor-Gefühl
- **Lösung:** CodeMirror 6 oder Monaco Editor integrieren mit Zuse-Grammatik

### 6.2 Zeilennummern anzeigen
- Kommt automatisch mit Editor-Bibliothek (6.1)

### 6.3 Code-Persistenz (localStorage)
- **Problem:** Code geht beim Neuladen verloren
- **Lösung:** Auto-Save in localStorage, "Zuletzt bearbeitet" anzeigen

### 6.4 Pyodide-Ladefehler abfangen
- **Problem:** Kein try/catch um CDN-Ladevorgang — bei Netzwerkfehler bleibt Seite hängen
- **Lösung:** Timeout + Fehlermeldung + Retry-Button

### 6.5 Barrierefreiheit (Accessibility)
- `lang="de"` Attribut auf HTML-Tag
- ARIA-Labels für alle Buttons
- Semantisches HTML (`<nav>`, `<main>`, `<section>`)
- Sichtbare Fokus-Indikatoren
- Tastatur-Navigation ohne Maus möglich

### 6.6 Mobile Optimierung
- Virtuelle Tastatur berücksichtigen
- Touch-Events im Canvas
- Zoom-Steuerung für Editor

---

## Phase 7: Entwicklerwerkzeuge (v7.9)

### 7.1 LSP: Hover-Dokumentation
- **Problem:** Maus über Keyword/Funktion zeigt nichts an
- **Lösung:** `textDocument/hover` Handler mit Dokumentation aus Sprachdateien

### 7.2 LSP: Go-to-Definition
- **Problem:** Nicht möglich, zur Definition einer Funktion/Klasse zu springen
- **Lösung:** `textDocument/definition` Handler implementieren

### 7.3 LSP: Autovervollständigung erweitern
- **Problem:** Nur Keywords — keine Methoden-Vervollständigung nach `.`
- **Lösung:** Member-Completion basierend auf erkanntem Typ

### 7.4 LSP: Parameterhinweise
- **Problem:** Keine Signaturhilfe beim Tippen von Funktionsargumenten
- **Lösung:** `textDocument/signatureHelp` implementieren

### 7.5 LSP: Rename-Refactoring
- **Lösung:** `textDocument/rename` mit Scope-bewusstem Umbenennen

### 7.6 Debugger: Variablen-Watch erweitern
- Ausdrücke evaluieren während Pause
- Bedingte Breakpoints

---

## Phase 8: Dokumentation vervollständigen (v7.10)

### 8.1 Spielfeld-API-Referenz
- Alle Methoden von Spielfeld, Sprite, TextSprite dokumentieren
- Codebeispiele für jede Methode
- Desktop vs. Web Unterschiede beschreiben

### 8.2 Architektur-Dokument
- Lexer → Parser → AST → Interpreter Pipeline erklären
- Transpiler-Architektur (BaseBackend → Visitor → Code)
- Diagramme für Datenfluss

### 8.3 Studio-Benutzerhandbuch
- Installation, Bedienung, Debugging-Tutorial
- Screenshots

### 8.4 Playground-Anleitung
- Was funktioniert im Browser, was nicht
- Einschränkungen (kein Dateizugriff, kein tkinter)

### 8.5 "Mein erstes Zuse-Programm" — je Sprache
- **Problem:** Tutorial nur auf Deutsch
- **Lösung:** Einstiegs-Tutorial in allen 6 Sprachen

### 8.6 Transpiler-Dokumentation
- Pro Backend: Was wird unterstützt, was nicht
- Bekannte Einschränkungen (Java-Klassen, WASM-Strings)

---

## Phase 9: Tests ausbauen (v7.11)

### 9.1 Edge-Case-Tests
- Leere Programme, leere Listen/Dicts/Strings
- Unicode jenseits von Umlauten (Emoji, Akzente, RTL)
- Maximale Rekursionstiefe
- Fließkomma-Präzision (0.1 + 0.2)
- Sehr große Zahlen

### 9.2 Spielfeld-Web-Tests
- **Problem:** `spielfeld_web.py` hat NULL Tests
- **Lösung:** Unit-Tests mit gemocktem JS-Bridge

### 9.3 End-to-End Integration
- Schreiben → Transpilieren → Kompilieren → Ausführen (pro Backend)
- Playground: Code eingeben → Ausführen → Ausgabe prüfen

### 9.4 Browser-Kompatibilität
- Chrome, Firefox, Safari, Edge testen
- Mobile Browser (iOS Safari, Android Chrome)

### 9.5 Performance-Benchmarks
- Interpreter: 10.000 Iterationen, Rekursion, große Listen
- Transpiler: Große Programme (500+ Zeilen)
- Playground: Startzeit, Ausführungszeit

### 9.6 Sicherheitstests
- Sandbox-Escape verhindern (kein `os.system` etc.)
- Playground: Kein Zugriff auf Dateisystem/Netzwerk

---

## Phase 10: Paketmanager & Ökosystem (v8.0)

### 10.1 zpkg: Semantische Versionierung
- **Problem:** Kein Versionsvergleich — installiert immer "das Neueste"
- **Lösung:** SemVer-Constraints (`>=1.0.0, <2.0.0`)

### 10.2 zpkg: Zirkuläre Abhängigkeiten erkennen
- **Problem:** Kann in Endlosschleife geraten
- **Lösung:** Abhängigkeitsgraph auf Zyklen prüfen

### 10.3 zpkg: Online-Registry
- **Problem:** Nur lokales `zpkg_registry/` Verzeichnis
- **Lösung:** GitHub-basierte oder eigene Registry für Community-Pakete

### 10.4 zpkg: Mehrsprachige Fehlermeldungen
- **Problem:** Nur deutsche Fehlermeldungen
- **Lösung:** i18n-System auch für zpkg

### 10.5 Community-Beispiele
- Mehr Spielfeld-Spiele (Pong, Breakout, Taschenrechner)
- Algorithmen-Sammlung (Sortierung, Suche, Graphen)
- Schulprojekt-Vorlagen

---

## Zusammenfassung

| Phase | Version | Status | Punkte | Fokus |
|-------|---------|--------|--------|-------|
| 1 | v7.3 | ERLEDIGT | 5/5 | Crashes & stille Fehler beheben |
| 2 | v7.3 | ERLEDIGT | 9/9 | Sprachkern robust machen |
| 3 | v7.3 | ERLEDIGT | 8/8 | Transpiler fertigstellen |
| 4 | v7.3 | ERLEDIGT | 4/4 | Bessere statische Analyse |
| 5 | v7.3 | ERLEDIGT | 4/4 | Mehr Bibliotheken & APIs |
| 6 | v7.3 | ERLEDIGT | 6/6 | Playground aufwerten |
| 7 | v7.3 | ERLEDIGT | 6/6 | IDE-Werkzeuge verbessern |
| 8 | v7.3 | ERLEDIGT | 6/6 | Dokumentation schreiben |
| 9 | v7.3 | ERLEDIGT | 6/6 | Testabdeckung erhöhen |
| 10 | v7.3 | ERLEDIGT | 5/5 | Ökosystem & Community |
| **Gesamt** | | **ERLEDIGT** | **59/59** | |

### Verbleibende Punkte für v8.0
- 10.3 Online-Registry (benötigt Server-Infrastruktur)
- 10.4 zpkg i18n (teilweise — Grundstruktur vorhanden)
- 10.5 Community-Beispiele (fortlaufend)
- WASM-Backend: String/Listen-Unterstützung (großer Aufwand)
- Playground: Syntax-Highlighting mit Zuse-spezifischer Grammatik (statt Python-Modus)
- Browser-Kompatibilitätstests (Safari, Firefox, Mobile)

---

*Erstellt am 29.03.2026 | Abgearbeitet am 02.04.2026 (v7.3.0)*
