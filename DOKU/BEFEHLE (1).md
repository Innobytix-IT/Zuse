# Zuse Befehls-Referenz (Version 7.3)

Diese Referenz gilt für die **deutsche Spracheinstellung**. In anderen Sprachen (Englisch, Spanisch, Französisch, Italienisch, Portugiesisch, Hindi, Chinesisch) ändert sich nur das Schlüsselwort (z.B. `WENN` -> `IF`), die Logik bleibt identisch.

## 1. Kern-Syntax (Schlüsselwörter)
Diese Befehle sind fest im **Parser** verankert und bilden das Gerüst der Sprache.

| Befehl | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| **Kommentare** | | |
| `# <Text>` | Alles nach `#` wird ignoriert. | `# Das ist ein Kommentar` |
| **Ausgabe & Eingabe** | | |
| `AUSGABE <Wert>` | Gibt Text oder Zahlen in der Konsole aus. | `AUSGABE "Hallo"` |
| `ZEIGE <Wert>` | Alias für `AUSGABE`. | `ZEIGE 42` |
| `EINGABE_TEXT(<Frage>)` | Fragt den Benutzer nach einem Text (String). | `name = EINGABE_TEXT("Name?")` |
| `EINGABE_ZAHL(<Frage>)` | Fragt den Benutzer nach einer Zahl (Integer/Float). | `alter = EINGABE_ZAHL("Alter?")` |
| **Logik & Bedingungen** | | |
| `WENN <Bedingung> DANN` | Startet eine Bedingung. | `WENN x > 5 DANN` |
| `SONST WENN <Bedingung> DANN` | Zusätzliche Bedingung (else if). | `SONST WENN x == 3 DANN` |
| `SONST` | Alternative, wenn keine Bedingung zutrifft. | `SONST` |
| `ENDE WENN` | Beendet den Bedingungs-Block. | `ENDE WENN` |
| `wahr` / `WAHR` | Boolean: Wahrheitswert wahr. | `läuft = wahr` |
| `falsch` / `FALSCH` | Boolean: Wahrheitswert falsch. | `aktiv = falsch` |
| `NICHTS` | Null-Wert (None). | `ergebnis = NICHTS` |
| **Fallunterscheidung (Switch/Case)** | | |
| `WÄHLE <Ausdruck>` | Startet eine Fallunterscheidung. | `WÄHLE note` |
| `FALL <Wert> DANN` | Definiert einen Fall. | `FALL 1 DANN` |
| `SONST` | Standard-Fall (Default). | `SONST` |
| `ENDE WÄHLE` | Beendet die Fallunterscheidung. | `ENDE WÄHLE` |
| **Schleifen** | | |
| `SCHLEIFE FÜR <Var> IN <Liste> MACHE` | Wiederholt für jedes Element einer Liste. | `SCHLEIFE FÜR i IN [1,2,3] MACHE` |
| `SCHLEIFE FÜR <Var> IN BEREICH(...) MACHE` | Wiederholt mit Zahlenbereich. | `SCHLEIFE FÜR i IN BEREICH(10) MACHE` |
| `SCHLEIFE SOLANGE <Bedingung> MACHE` | Wiederholt, solange die Bedingung wahr ist. | `SCHLEIFE SOLANGE x < 10 MACHE` |
| `ENDE SCHLEIFE` | Beendet den Schleifen-Block. | `ENDE SCHLEIFE` |
| `ABBRUCH` | Bricht die Schleife sofort ab (break). | `ABBRUCH` |
| `WEITER` | Springt zum nächsten Schleifendurchlauf (continue). | `WEITER` |
| **Funktionen** | | |
| `DEFINIERE <Name>(<Params>):` | Erstellt eine neue Funktion. | `DEFINIERE hallo(name):` |
| `DEFINIERE <Name>(<P>, <P>=<Std>):` | Funktion mit Standardwert (Default-Parameter). | `DEFINIERE f(x, y=10):` |
| `ERGEBNIS IST <Wert>` | Gibt einen Wert aus einer Funktion zurück (Return). | `ERGEBNIS IST x + y` |
| `ENDE FUNKTION` | Beendet die Funktions-Definition. | `ENDE FUNKTION` |
| `AKTION(<Params>): <Ausdruck>` | Erstellt eine anonyme Funktion (Lambda). | `doppelt = AKTION(x): x * 2` |
| `GLOBAL <Name>` | Macht eine Variable in einer Funktion global verfügbar. | `GLOBAL punktestand` |
| `PASS` | Platzhalter für leere Blöcke (No-Op). | `PASS` |
| **Objektorientierung** | | |
| `KLASSE <Name>:` | Definiert eine neue Klasse. | `KLASSE Hund:` |
| `KLASSE <Name>(<Eltern>):` | Definiert eine Klasse mit Vererbung. | `KLASSE Dackel(Hund):` |
| `DEFINIERE ERSTELLE(...):` | Der Konstruktor. Wird beim Erzeugen aufgerufen. | `DEFINIERE ERSTELLE(name):` |
| `MEIN` | Referenz auf die eigene Instanz (wie `self` / `this`). | `MEIN.name = name` |
| `ELTERN` | Zugriff auf Methoden der Elternklasse (super). | `ELTERN.ERSTELLE(name)` |
| `OBER` | Alias für `ELTERN`. | `OBER.methode()` |
| `ENDE KLASSE` | Beendet die Klassen-Definition. | `ENDE KLASSE` |
| **Fehlerbehandlung** | | |
| `VERSUCHE` | Startet einen Block, in dem Fehler auftreten dürfen. | `VERSUCHE` |
| `FANGE <Variable>` | Fängt den Fehler ab und speichert ihn optional in einer Variable. | `FANGE fehler` |
| `ENDE VERSUCHE` | Beendet den Fehler-Block. | `ENDE VERSUCHE` |
| **Module & Importe** | | |
| `BENUTZE <Modul>` | Lädt ein Modul. | `BENUTZE deutsch` |
| `BENUTZE <Modul> ALS <Alias>` | Lädt ein Modul mit Alias. | `BENUTZE requests ALS netz` |
| `LADE <Modul>` | Alias für `BENUTZE`. | `LADE mathe` |

---

## 2. Eingebaute Funktionen (Global)
Diese Funktionen sind im **Interpreter** definiert und stehen immer zur Verfügung.

### 2.1 Typkonvertierung & Prüfung

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `ALS_TEXT(wert)` | Wandelt einen Wert in Text um. | `t = ALS_TEXT(42)` → `"42"` |
| `ALS_ZAHL(wert)` | Wandelt Text in eine Zahl um (int oder float). | `z = ALS_ZAHL("10")` → `10` |
| `IST_ZAHL(wert)` | Prüft ob der Wert eine Zahl ist. | `IST_ZAHL(42)` → `wahr` |
| `IST_TEXT(wert)` | Prüft ob der Wert ein Text ist. | `IST_TEXT("hi")` → `wahr` |
| `IST_LISTE(wert)` | Prüft ob der Wert eine Liste ist. | `IST_LISTE([1,2])` → `wahr` |
| `IST_DICT(wert)` | Prüft ob der Wert ein Wörterbuch ist. | `IST_DICT({})` → `wahr` |
| `IST_BOOL(wert)` | Prüft ob der Wert ein Boolean ist. | `IST_BOOL(wahr)` → `wahr` |
| `IST_NICHTS(wert)` | Prüft ob der Wert NICHTS (None) ist. | `IST_NICHTS(NICHTS)` → `wahr` |

### 2.2 Mathematik

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `WURZEL(x)` | Quadratwurzel. | `WURZEL(16)` → `4.0` |
| `POTENZ(x, y)` | x hoch y. | `POTENZ(2, 10)` → `1024` |
| `ABSOLUT(x)` | Betrag (Absolutwert). | `ABSOLUT(-7)` → `7` |
| `RUNDEN(x, n)` | Rundet auf n Dezimalstellen. | `RUNDEN(3.14159, 2)` → `3.14` |
| `BODEN(x)` | Abrunden (Floor). | `BODEN(3.7)` → `3` |
| `DECKE(x)` | Aufrunden (Ceil). | `DECKE(3.2)` → `4` |
| `MINIMUM(a, b, ...)` | Kleinster Wert. | `MINIMUM(5, 3, 8)` → `3` |
| `MAXIMUM(a, b, ...)` | Größter Wert. | `MAXIMUM(5, 3, 8)` → `8` |
| `SUMME(liste)` | Summe aller Elemente. | `SUMME([1,2,3])` → `6` |
| `SINUS(x)` | Sinus (Bogenmaß). | `SINUS(PI / 2)` → `1.0` |
| `COSINUS(x)` | Cosinus (Bogenmaß). | `COSINUS(0)` → `1.0` |
| `TANGENS(x)` | Tangens (Bogenmaß). | `TANGENS(PI / 4)` → `~1.0` |
| `LOGARITHMUS(x, basis)` | Logarithmus (optional mit Basis). | `LOGARITHMUS(E)` → `1.0` |
| `PI` | Kreiszahl Pi (3.14159...). | `AUSGABE PI` |
| `E` | Eulersche Zahl (2.71828...). | `AUSGABE E` |

### 2.3 Zufall

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `ZUFALL()` | Zufällige Kommazahl zwischen 0.0 und 1.0. | `ZUFALL()` → `0.7382...` |
| `ZUFALL_BEREICH(a, b)` | Zufällige Ganzzahl im Bereich [a, b]. | `ZUFALL_BEREICH(1, 6)` → `4` |

### 2.4 Text (Strings)

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `LAENGE(objekt)` | Länge eines Textes oder einer Liste. | `LAENGE("Hallo")` → `5` |
| `GROSSBUCHSTABEN(text)` | Text in Großbuchstaben. | `GROSSBUCHSTABEN("hi")` → `"HI"` |
| `KLEINBUCHSTABEN(text)` | Text in Kleinbuchstaben. | `KLEINBUCHSTABEN("HI")` → `"hi"` |
| `ERSETZE(text, alt, neu)` | Ersetzt Teiltext. | `ERSETZE("Hallo", "ll", "LL")` |
| `TEILE(text, trenner)` | Spaltet Text in Liste. | `TEILE("a,b,c", ",")` → `["a","b","c"]` |
| `TRIMME(text)` | Entfernt Leerzeichen am Rand. | `TRIMME("  hi  ")` → `"hi"` |
| `VERBINDE(liste, trenner)` | Verbindet Liste zu Text. | `VERBINDE(["a","b"], "-")` → `"a-b"` |
| `ENTHAELT(text, teil)` | Prüft ob Teiltext enthalten ist. | `ENTHAELT("Hallo", "all")` → `wahr` |
| `FINDE(text, teil)` | Position des Teiltexts. | `FINDE("Hallo", "ll")` → `2` |
| `BEGINNT_MIT(text, praefix)` | Prüft Textanfang. | `BEGINNT_MIT("Hallo", "Hal")` → `wahr` |
| `ENDET_MIT(text, suffix)` | Prüft Textende. | `ENDET_MIT("Hallo", "llo")` → `wahr` |
| `FORMAT(vorlage, ...)` | Formatiert Text mit Platzhaltern. | `FORMAT("Hallo, {}!", "Welt")` |
| `ZEICHENCODE(zeichen)` | Unicode-Code eines Zeichens (ord). | `ZEICHENCODE("A")` → `65` |
| `ZEICHEN(code)` | Zeichen aus Unicode-Code (chr). | `ZEICHEN(65)` → `"A"` |
| `HEX(zahl)` | Hexadezimal-Darstellung. | `HEX(255)` → `"0xff"` |
| `BIN(zahl)` | Binär-Darstellung. | `BIN(42)` → `"0b101010"` |
| `OKT(zahl)` | Oktal-Darstellung. | `OKT(8)` → `"0o10"` |

### 2.5 Listen

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `BEREICH(n)` | Zahlenfolge [0, 1, ..., n-1]. | `BEREICH(5)` → `[0,1,2,3,4]` |
| `BEREICH(start, ende)` | Zahlenfolge [start, ..., ende-1]. | `BEREICH(2, 5)` → `[2,3,4]` |
| `BEREICH(start, ende, schritt)` | Zahlenfolge mit Schrittweite. | `BEREICH(0, 10, 2)` → `[0,2,4,6,8]` |
| `SORTIEREN(liste)` | Gibt sortierte Kopie zurück. | `SORTIEREN([3,1,2])` → `[1,2,3]` |
| `FILTERN(liste, fn)` | Filtert Elemente mit Funktion. | `FILTERN([1,2,3], AKTION(x): x>1)` |
| `UMWANDELN(liste, fn)` | Transformiert jedes Element. | `UMWANDELN([1,2,3], AKTION(x): x*2)` |
| `UMKEHREN(liste)` | Umgekehrte Kopie. | `UMKEHREN([1,2,3])` → `[3,2,1]` |
| `FLACH(liste)` | Verschachtelte Listen glätten. | `FLACH([[1,2],[3]])` → `[1,2,3]` |
| `EINDEUTIG(liste)` | Duplikate entfernen. | `EINDEUTIG([1,1,2])` → `[1,2]` |
| `AUFZAEHLEN(liste)` | Index-Wert-Paare. | `AUFZAEHLEN(["a","b"])` → `[[0,"a"],[1,"b"]]` |
| `KOMBINIEREN(l1, l2)` | Listen zusammenführen (zip). | `KOMBINIEREN([1,2],["a","b"])` |
| `ANHAENGEN(liste, ...)` | Elemente anhängen. | `ANHAENGEN(liste, 4, 5)` |
| `ALLE(liste)` | Sind alle Elemente wahr? | `ALLE([wahr, wahr])` → `wahr` |
| `IRGENDEIN(liste)` | Ist mindestens eines wahr? | `IRGENDEIN([falsch, wahr])` → `wahr` |

### 2.6 Dateioperationen (nur Profi-Modus)

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `LESE_DATEI(pfad)` | Liest gesamte Datei als Text. | `inhalt = LESE_DATEI("data.txt")` |
| `LESE_ZEILEN(pfad)` | Liest Datei als Liste von Zeilen. | `zeilen = LESE_ZEILEN("data.txt")` |
| `SCHREIBE_DATEI(pfad, inhalt)` | Schreibt/überschreibt Datei. | `SCHREIBE_DATEI("out.txt", "Hallo")` |
| `ERGAENZE_DATEI(pfad, inhalt)` | Hängt Text an Datei an. | `ERGAENZE_DATEI("log.txt", "Neu\n")` |
| `EXISTIERT(pfad)` | Prüft ob Datei existiert. | `EXISTIERT("config.txt")` → `wahr` |
| `LOESCHE_DATEI(pfad)` | Löscht eine Datei. | `LOESCHE_DATEI("temp.txt")` |

---

## 3. Objekt-Methoden

### 3.1 Listen-Methoden

| Methode | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `.hinzufuegen(wert)` | Element anhängen (append). | `liste.hinzufuegen(4)` |
| `.einfuegen(index, wert)` | An Position einfügen (insert). | `liste.einfuegen(0, "start")` |
| `.entfernen(wert)` | Element entfernen (remove). | `liste.entfernen(3)` |
| `.sortieren()` | Liste in-place sortieren. | `liste.sortieren()` |
| `.umkehren()` | Reihenfolge umdrehen. | `liste.umkehren()` |
| `.index(wert)` | Position eines Elements finden. | `liste.index("a")` → `0` |
| `.zaehle(wert)` | Vorkommen zählen. | `liste.zaehle(1)` → `2` |
| `.leeren()` | Alle Elemente löschen. | `liste.leeren()` |
| `.kopie()` | Flache Kopie erstellen. | `neu = liste.kopie()` |

### 3.2 String-Methoden

| Methode | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `.gross()` | In Großbuchstaben. | `"hallo".gross()` → `"HALLO"` |
| `.klein()` | In Kleinbuchstaben. | `"HALLO".klein()` → `"hallo"` |
| `.ersetze(alt, neu)` | Text ersetzen. | `"Hallo".ersetze("ll", "LL")` |
| `.teile(trenner)` | Text aufteilen. | `"a,b".teile(",")` → `["a","b"]` |
| `.trimme()` | Leerzeichen entfernen. | `"  hi  ".trimme()` → `"hi"` |
| `.beginnt_mit(text)` | Prüfe Textanfang. | `"Hallo".beginnt_mit("Hal")` |
| `.endet_mit(text)` | Prüfe Textende. | `"Hallo".endet_mit("llo")` |
| `.enthaelt(text)` | Prüfe ob enthalten. | `"Hallo".enthaelt("all")` |
| `.finde(text)` | Position finden. | `"Hallo".finde("ll")` → `2` |

---

## 4. Standard-Bibliothek: Turtle-Grafik (`KLASSE Maler`)
Diese Befehle stehen zur Verfügung, wenn `stift = Maler()` erstellt wurde.
*Voraussetzung:* `BENUTZE deutsch` (oder entsprechende Spracheinstellung).

| Methode | Beschreibung | Parameter |
| :--- | :--- | :--- |
| `gehe(schritte)` | Bewegt den Maler vorwärts. | Zahl (Pixel) |
| `zurueck(schritte)` | Bewegt den Maler rückwärts. | Zahl (Pixel) |
| `drehe_rechts(grad)` | Dreht den Maler nach rechts. | Zahl (Grad) |
| `drehe_links(grad)` | Dreht den Maler nach links. | Zahl (Grad) |
| `stift_hoch()` | Hebt den Stift (kein Zeichnen). | (Keine) |
| `stift_runter()` | Senkt den Stift (Zeichnen aktiv). | (Keine) |
| `farbe(f)` | Setzt die Malfarbe. | Text ("rot", "#FF0000") |
| `dicke(d)` | Setzt die Strichstärke. | Zahl |
| `kreis(radius)` | Malt einen Kreis. | Zahl |
| `fertig()` | Beendet das Zeichnen. | (Keine) |

---

## 5. Standard-Bibliothek: Spielfeld-Engine (`KLASSE Spielfeld`)
Vollständige 2D-Game-Engine für Spiele und Animationen.
*Voraussetzung:* `BENUTZE deutsch` (oder entsprechende Spracheinstellung).

### 5.1 Spielfeld erstellen

| Methode | Beschreibung | Parameter |
| :--- | :--- | :--- |
| `Spielfeld(titel, breite, hoehe, farbe)` | Erstellt ein Spielfenster. | Text, Zahl, Zahl, Text |

### 5.2 Sprites

| Methode | Beschreibung | Parameter |
| :--- | :--- | :--- |
| `neuer_sprite(x, y, b, h, farbe)` | Erstellt ein Rechteck-Sprite. | Zahl, Zahl, Zahl, Zahl, Text |
| `neuer_text(x, y, text, farbe, groesse)` | Erstellt ein Text-Sprite. | Zahl, Zahl, Text, Text, Zahl |

### 5.3 Sprite-Methoden

| Methode | Beschreibung |
| :--- | :--- |
| `.bewege(dx, dy)` | Relativ verschieben. |
| `.setze_position(x, y)` | Absolute Position setzen. |
| `.kollidiert_mit(anderer)` | Kollisionsprüfung (AABB). |
| `.am_rand()` | Am Fensterrand? |
| `.verstecke()` | Unsichtbar machen. |
| `.zeige()` | Wieder sichtbar machen. |
| `.aendere_farbe(farbe)` | Farbe ändern. |
| `.entferne()` | Sprite löschen. |

### 5.4 Eingabe

| Methode | Beschreibung | Parameter |
| :--- | :--- | :--- |
| `taste_gedrueckt(taste)` | Prüft ob Taste gedrückt ist. | "Links", "Rechts", "Hoch", "Runter", "Leertaste", "Eingabe", "Escape" |
| `bei_taste(taste, funktion)` | Bindet Taste an Funktion. | Text, Funktion |
| `maus_position()` | Gibt [x, y] der Maus zurück. | (Keine) |
| `maus_gedrueckt()` | Prüft ob linke Maustaste gedrückt. | (Keine) |

### 5.5 Zeichenfunktionen

| Methode | Beschreibung |
| :--- | :--- |
| `zeichne_rechteck(x, y, b, h, farbe)` | Zeichnet ein Rechteck. |
| `zeichne_kreis(x, y, radius, farbe)` | Zeichnet einen Kreis. |
| `zeichne_linie(x1, y1, x2, y2, farbe, dicke)` | Zeichnet eine Linie. |
| `zeichne_text(x, y, text, farbe, groesse)` | Zeichnet Text. |
| `zeichne_polygon(punkte, farbe)` | Zeichnet ein Polygon (Liste von [x,y]). |

### 5.6 Spielsteuerung

| Methode | Beschreibung |
| :--- | :--- |
| `spielschleife(funktion, fps)` | Startet die Spielschleife. |
| `stoppe()` | Stoppt die Spielschleife. |
| `aktualisiere()` | Erzwingt Bildschirm-Aktualisierung. |
| `starte()` | Startet die Hauptschleife. |
| `nach_zeit(ms, funktion)` | Führt Funktion nach X ms aus. |
| `schliessen()` | Schließt das Fenster. |
| `setze_titel(titel)` | Ändert den Fenstertitel. |
| `loesche_alles()` | Löscht alles vom Bildschirm. |

---

## 6. Operatoren & Datenzugriff

| Operator | Bedeutung | Beispiel |
| :--- | :--- | :--- |
| `+` | Plus (oder Text zusammenfügen) | `5 + 5` oder `"A" + "B"` |
| `-` | Minus | `10 - 2` |
| `*` | Mal | `4 * 4` |
| `/` | Geteilt | `20 / 5` |
| `^` | Hoch (Potenz) | `2 ^ 3` (ergibt 8) |
| `%` | Modulo (Rest bei Division) | `10 % 3` (ergibt 1) |
| `==` | Ist gleich | `a == b` |
| `!=` | Ist ungleich | `a != b` |
| `<` / `>` | Kleiner / Größer | `5 < 10` |
| `<=` / `>=` | Kleiner gleich / Größer gleich | `x >= 0` |
| `UND` | Logisches Und | `x > 0 UND x < 10` |
| `ODER` | Logisches Oder | `a == 1 ODER a == 2` |
| `NICHT` | Logische Negation | `NICHT aktiv` |
| `[` ... `]` | Liste erstellen | `liste = [1, 2, 3]` |
| `{` ... `}` | Dictionary erstellen | `daten = {"a": 1}` |
| `objekt.attribut` | Zugriff auf Methoden oder Attribute. | `hund.name` |
| `objekt[index]` | Zugriff auf Listen-Element oder Dict-Wert. | `liste[0]` oder `daten["a"]` |
| `objekt[start:ende]` | **Slicing**: Schneidet Teile aus Listen/Texten. | `text[0:3]` |
| `a, b = x, y` | **Mehrfachzuweisung**: Mehrere Werte gleichzeitig. | `a, b = b, a` |

---

## 7. Transpiler (5 Backends)

Zuse-Code kann in andere Programmiersprachen übersetzt werden:

| Ziel | Dateiendung | Einsatzgebiet |
| :--- | :--- | :--- |
| **Python** | `.py` | Datenwissenschaft, KI, Automatisierung |
| **JavaScript** | `.js` | Webseiten, Node.js, Browser-Apps |
| **Java** | `.java` | Android, Enterprise, Server |
| **C#** | `.cs` | Unity-Spiele, Windows, .NET |
| **WebAssembly** | `.wasm` | Hochleistung im Browser |

---

## 8. Profi-Modus ("God Mode")
Wenn der Modus im Studio auf "Profi" steht, sind **alle** Python-Module importierbar.

**Beispiele:**
* `BENUTZE requests ALS netz` (HTTP-Anfragen)
* `BENUTZE matplotlib.pyplot ALS plt` (Diagramme)
* `BENUTZE pandas ALS pd` (Datenanalyse)
* `BENUTZE pyfirmata` (Arduino-Steuerung)
* `BENUTZE serial` (Serielle Schnittstelle)
* `BENUTZE os` (Dateisystem)
* `BENUTZE math` (Erweiterte Mathematik)

> **Achtung:** Programme mit Python-Bibliotheken können nur nach **Python** transpiliert werden, nicht nach Java, C# oder JavaScript.

---

## 9. Werkzeuge

| Werkzeug | Beschreibung |
| :--- | :--- |
| **Zuse Studio** | IDE mit Syntax-Highlighting, Lern-/Profi-Modus, Transpiler |
| **Debugger** | Breakpoints, Schritt-für-Schritt, Variablen-Inspektion |
| **LSP-Server** | Language Server Protocol für VS Code und andere Editoren |
| **Semantische Analyse** | Erkennt Shadowing, unerreichbaren Code, doppelte Parameter |
| **Web Playground** | Zuse im Browser (Pyodide + CodeMirror), ohne Installation |
| **Paketmanager (zpkg)** | Pakete installieren und teilen, SemVer-Versionierung |
