# Changelog

## v7.3.0 (2026-04-03)

### Neue Features
- **Turtle-Grafik im Browser**: `maler_web.py` — Maler/Pintor/Painter funktioniert jetzt im Web-Playground
- **CodeMirror 5 Integration**: Syntax-Highlighting, Zeilennummern und Dark Theme im Playground
- **Spielfeld-Erweiterungen**: `zeichne_polygon()`, `maus_position()`, `maus_gedrueckt()` (Desktop + Web)
- **Parser Error-Recovery**: Sammelt mehrere Fehler pro Datei statt beim ersten abzubrechen
- **7 neue Builtins**: `ALLE`, `IRGENDEIN`, `ZEICHENCODE`, `ZEICHEN`, `HEX`, `BIN`, `OKT`
- **8 neue Typ-Pruefungen**: `IST_ZAHL`, `IST_TEXT`, `IST_LISTE`, `IST_DICT`, `IST_BOOL`, `IST_NICHTS`, `ALS_ZAHL`, `ALS_TEXT`
- **Semantische Analyse**: Warnungen fuer Variable-Shadowing und unerreichbaren Code
- **SemVer im Paketmanager**: `zpkg` unterstuetzt jetzt Versionsconstraints (`>=1.0.0,<2.0.0`)
- **Import-Caching**: Module werden nur einmal geladen
- **Zirkulaere Vererbungserkennung**: Verhindert Endlosschleifen bei Klassen
- **Doppelte Parameter-Erkennung**: Parser warnt bei `DEFINIERE f(x, x)`
- **Lambda mit mehreren Parametern**: `x, y => x + y` ohne Klammern
- **LSP Go-to-Definition**: Springt zu Funktions-/Klassendefinitionen
- **LSP 17 neue Builtin-Docs**: Hover-Dokumentation fuer alle neuen Builtins
- **Spaltenposition in Lexer-Fehlern**: Zeigt genaue Position unbekannter Zeichen

### Bugfixes
- **Attribut-Null-Check**: `MEIN.x = NICHTS` wird jetzt korrekt gespeichert und abgerufen
- **Operator-Fallback**: Unbekannte Operatoren werfen jetzt klare Fehlermeldung statt silent None
- **Ausdruckstyp-Fallback**: Unbekannte AST-Knoten werfen jetzt Fehler statt silent None
- **Lexer Zeilennummer**: NEUEZEILE-Token bekommt korrekte Zeile (Off-by-One behoben)
- **Turtle-Cursor**: Pfeildreieck wird jetzt korrekt gezeichnet (Winkelberechnung korrigiert)
- **Vererbungs-Fehler**: `find_method()` verschluckt keine ZuseErrors mehr bei Elternklassen
- **Java-Backend**: Variablen werden nicht mehr doppelt deklariert (`Object x` nur beim ersten Mal)
- **C#-Backend**: Variablen werden nicht mehr doppelt deklariert (`dynamic x` nur beim ersten Mal)
- **JS-Backend**: Import-Alias wird jetzt korrekt unterschieden
- **Slicing-Fehler**: Werden jetzt als Zuse-Fehlermeldung ausgegeben statt Python-TypeError
- **Datei-Handles**: `LESE_DATEI`/`SCHREIBE_DATEI` schliessen jetzt korrekt via `with`-Statement
- **Fehlertipps**: Fallback-Matching erkennt jetzt das ERWARTETE Token korrekt (nicht das gefundene)
- **FUER vs FUeR**: Alle Hints verwenden jetzt einheitlich `FUeR` statt `FUER`
- **Python-Traceback**: Interne Tracebacks werden nicht mehr an Benutzer durchgereicht

### Sicherheit
- **`eval()` entfernt**: Python `eval()` ist nicht mehr als Builtin verfuegbar
- **Pfad-Traversal blockiert**: `zpkg install ../../../etc` wird jetzt abgelehnt

### Sprachkonsistenz
- **CONST_WAHR_GROSS / CONST_FALSCH_GROSS**: Jetzt in allen 6 Sprachen verfuegbar
  - ES: VERDADERO/FALSO, FR: VRAI/FAUX, IT: VERO/FALSO, PT: VERDADEIRO/FALSO
- **Franzoesische Accents korrigiert**: `etre` -> `etre`, `utilise` -> `utilise` in Fehlermeldungen
- **Spanische Accents korrigiert**: `modulo` -> `modulo`, `esta` -> `esta`, `Funcion` -> `Funcion`
- **Semantic Analyzer Builtins**: Synchronisiert mit Interpreter (62 Builtins)

### Dokumentation
- Neue Datei: `docs/spielfeld_api.md` — Vollstaendige Spielfeld-API-Referenz
- Neue Datei: `docs/architektur.md` — Technische Architektur-Uebersicht

### Tests
- **1086 Tests** (vorher 771) — 315 neue Tests
- Neue Testdatei: `tests/test_edge_cases.py` (37 Tests fuer Randfaelle)
- Playground-Tests aktualisiert fuer CodeMirror-Integration

---

## v7.2.0

- Initiales Release mit 6 Sprachen und 5 Transpiler-Backends
- Zuse Studio (tkinter GUI)
- Web-Playground (Pyodide)
- Debugger mit Breakpoints
- Paketmanager zpkg
- LSP-Server
- 771 Tests
