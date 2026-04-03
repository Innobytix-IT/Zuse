# ZUSE v7.3
> **"Einfach weil 'Einfach' einfach ist."**

![Version](https://img.shields.io/badge/Version-7.3-blue) ![Language](https://img.shields.io/badge/Made_with-Python-yellow) ![Status](https://img.shields.io/badge/Status-Stable-green) ![Tests](https://img.shields.io/badge/Tests-1086+-brightgreen)

**Zuse** ist eine objektorientierte, transpilierende Programmiersprache, die entwickelt wurde, um die Barriere zwischen "Lern-Sprachen" (wie Scratch) und "Profi-Sprachen" (wie Python/C++) zu durchbrechen.

Sie ermöglicht Programmierung in der Muttersprache (DE, EN, ES, FR, IT, PT), bietet einen nahtlosen Übergang von einfacher Grafik-Programmierung zur Steuerung komplexer Hardware und übersetzt Zuse-Code in 5 Zielsprachen.

---

## Features

*   **Multilingual:** Der Interpreter versteht 6 Sprachen nativ (Deutsch, Englisch, Spanisch, Französisch, Italienisch, Portugiesisch).
*   **Dual Mode:**
    *   **Lern-Modus:** Sandbox-Umgebung für Kinder/Anfänger (nur sichere Befehle).
    *   **Profi-Modus ("God Mode"):** Vollständiger Zugriff auf die Python-Runtime (inkl. Hardware-Steuerung).
*   **5 Transpiler-Backends:** Übersetze Zuse-Code nach Python, JavaScript, Java, C# oder WebAssembly.
*   **Spielfeld-Engine:** Vollständige 2D-Game-Engine mit Sprites, Kollisionserkennung, Tastatur-/Mauseingabe und Spielschleife (60 FPS).
*   **Turtle-Grafik (Maler):** Zeichne Sterne, Spiralen und Fraktale — in deiner Muttersprache.
*   **Zuse Studio:** Eine eigene IDE mit Syntax-Highlighting, Debugger, Live-Übersetzer und integriertem Transpiler.
*   **Debugger:** Breakpoints, Schritt-für-Schritt-Ausführung, Variablen-Inspektion.
*   **LSP-Server:** Language Server Protocol für VS Code und andere Editoren (Go-to-Definition, Hover-Doku).
*   **Semantische Analyse:** Erkennt Variablen-Shadowing, unerreichbaren Code und doppelte Parameter.
*   **Web Playground:** Zuse im Browser ausführen — ohne Installation (Pyodide + CodeMirror).
*   **Paketmanager (zpkg):** Pakete installieren und teilen mit SemVer-Versionierung.
*   **Environment Aware:** Zuse erkennt automatisch, ob es in der IDE, als Standalone oder im Browser läuft und passt sich dynamisch an.
*   **50+ eingebaute Funktionen:** Mathematik, Text, Listen, Dateien, Zufall, Typprüfung, Formatierung.
*   **1086+ automatisierte Tests** in 31 Testmodulen.

---

## System-Architektur

Zuse basiert auf einer **mehrstufigen Pipeline-Architektur**:

### 1. Der Kern (Lexer → Parser → AST)
Der **Lexer** (`lexer.py`) erkennt Keywords anhand austauschbarer Sprach-Mappings (JSON) und erzeugt kanonische Tokens. Der **Parser** (`parser.py`) erzeugt daraus einen sprachunabhängigen AST (Abstract Syntax Tree).

### 2. Der Interpreter (Visitor Pattern)
Die Engine (`interpreter.py`) führt den AST aus. Sie verfügt über einen **Smart Import Mechanismus**, ein **Sentinel Pattern** für sichere Attribut-Zugriffe, und erkennt Konstruktoren sprachübergreifend (`ERSTELLE`, `CREATE`, `CREAR`, `CREER`, `CREA`, `CRIAR`).

### 3. Der Transpiler (5 Backends)
Der AST wird von spezialisierten Backends in **Python**, **JavaScript**, **Java**, **C#** oder **WebAssembly** übersetzt. Java- und C#-Backends verwenden **Variable Tracking** um doppelte Deklarationen zu vermeiden.

### 4. Die IDE (Zuse Studio)
Das Studio (`zuse_studio.py`) ist Thread-Safe und verfügt über Lern-/Profi-Modus, **Debugger** mit Breakpoints, **Pre-Flight-Check**-Logik und integrierte Transpiler-Steuerung.

### 5. Die Standard-Bibliothek (6 Sprachen)
Die `.zuse`-Dateien im Ordner `bibliothek/` stellen **Maler** (Turtle-Grafik) und **Spielfeld** (2D-Game-Engine) in allen 6 Sprachen bereit.

### 6. Weitere Werkzeuge
*   **LSP-Server** (`zuse_lsp_server.py`) für Editor-Integration
*   **Semantische Analyse** für Code-Qualitätsprüfungen
*   **Web Playground** (`playground/`) für den Browser
*   **Paketmanager** (`zpkg_core.py`) für Paketverwaltung

---

## Syntax Beispiele (Deutsch)

### Hallo Welt & Logik
```zuse
text = "Hallo Zuse"
zahl = 42

WENN zahl > 10 DANN
    AUSGABE text
SONST
    AUSGABE "Zahl ist klein"
ENDE WENN
```

### Schleifen
```zuse
SCHLEIFE FÜR i IN BEREICH(5) MACHE
    AUSGABE "Durchlauf: " + ALS_TEXT(i)
ENDE SCHLEIFE
```

### Funktionen mit Lambda
```zuse
DEFINIERE quadrat(x)
    ERGEBNIS IST x ^ 2
ENDE FUNKTION

zahlen = [1, 2, 3, 4, 5]
gerade = FILTERN(zahlen, AKTION(x): x % 2 == 0)
AUSGABE gerade    # [2, 4]
```

### Objektorientierung mit Vererbung
```zuse
KLASSE Tier:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION

    DEFINIERE sprechen():
        AUSGABE MEIN.name + " macht ein Geräusch."
    ENDE FUNKTION
ENDE KLASSE

KLASSE Hund(Tier):
    DEFINIERE sprechen():
        AUSGABE MEIN.name + " sagt: Wuff!"
    ENDE FUNKTION
ENDE KLASSE

bello = Hund("Bello")
bello.sprechen()    # Bello sagt: Wuff!
```

### Fehlerbehandlung
```zuse
VERSUCHE
    ergebnis = 10 / 0
FANGE fehler
    AUSGABE "Fehler: " + fehler
ENDE VERSUCHE
```

### Grafik (Der Maler)
```zuse
BENUTZE deutsch ALS bib
stift = bib.Maler()

stift.farbe("blau")
stift.dicke(5)

SCHLEIFE FÜR i IN BEREICH(4) MACHE
    stift.gehe(100)
    stift.drehe_rechts(90)
ENDE SCHLEIFE

stift.fertig()
```

### Spielfeld (Game Engine)
```zuse
BENUTZE deutsch ALS bib

spiel = bib.Spielfeld("Mein Spiel", 800, 600, "schwarz")
spieler = spiel.neuer_sprite(400, 300, 30, 30, "blau")

DEFINIERE aktualisiere()
    WENN spiel.taste_gedrueckt("Links") DANN
        spieler.bewege(-5, 0)
    ENDE WENN
    WENN spiel.taste_gedrueckt("Rechts") DANN
        spieler.bewege(5, 0)
    ENDE WENN
ENDE FUNKTION

spiel.spielschleife(aktualisiere, 60)
spiel.starte()
```

---

## Nutzung

### Starten der IDE
```bash
python zuse_studio.py
```

### Ausführen eines Programms (Standalone)
```bash
python main.py mein_skript.zuse deutsch
```

### Web Playground starten
```bash
python playground/server.py
```

---

## Hardware & Deployment

Dank des **Profi-Modus** kann Zuse direkt auf Hardware zugreifen.

**Beispiel: Arduino steuern**
```zuse
BENUTZE pyfirmata
board = pyfirmata.Arduino("COM3")
led = board.get_pin("d:13:o")
led.write(1)
```

---

## Transpiler — Zuse-Code übersetzen

```zuse
# Dieses Zuse-Programm...
DEFINIERE fakultaet(n)
    WENN n <= 1 DANN
        ERGEBNIS IST 1
    SONST
        ERGEBNIS IST n * fakultaet(n - 1)
    ENDE WENN
ENDE FUNKTION
```

...wird z. B. zu **JavaScript**:
```javascript
function fakultaet(n) {
    if (n <= 1) { return 1; }
    else { return n * fakultaet(n - 1); }
}
```

...oder zu **Java**:
```java
static Object fakultaet(Object n) {
    if ((int)n <= 1) { return 1; }
    else { return (int)n * (int)fakultaet((int)n - 1); }
}
```

---

## Roadmap (Zuse: The Universal Vision)

*   [x] **v6.9:** Stabiler Interpreter, IDE, Bibliotheken (DE/EN/ES/PT/FR/IT).
*   [x] **v7.3:** 5 Transpiler-Backends (Python, JS, Java, C#, WASM), Spielfeld-Engine, Debugger, LSP-Server, Web Playground, Paketmanager, Semantische Analyse, 1086+ Tests.
*   [ ] **vNext (Zuse Universal):** Weitere Optimierung, zusätzliche Sprachen, erweiterte IDE-Features.

<img width="585" height="584" alt="image" src="https://github.com/user-attachments/assets/1e5649a9-1c79-4b5c-8149-b0f0329211a7" />

---

**Architekt:** Manuel Person
**Co-Coding:** Gemini, Claude
**Lizenz:** Open Source MIT
