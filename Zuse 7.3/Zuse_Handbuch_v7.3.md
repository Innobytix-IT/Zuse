# Das offizielle Zuse-Handbuch (Version 7.3)

**Die mehrsprachige, transpilierende Programmiersprache für Bildung und Industrie.**

---

## Inhaltsverzeichnis

1. [Was ist Zuse?](#1-was-ist-zuse)
2. [Die Grundlagen (Variablen & Ein/Ausgabe)](#2-die-grundlagen)
3. [Operatoren](#3-operatoren)
4. [Logik: Bedingungen & Schleifen](#4-logik-bedingungen--schleifen)
5. [Struktur: Funktionen](#5-struktur-funktionen)
6. [Klassen & Vererbung](#6-klassen--vererbung)
7. [Listen & Wörterbücher](#7-listen--wörterbücher)
8. [Textverarbeitung (Strings)](#8-textverarbeitung-strings)
9. [Fehlerbehandlung](#9-fehlerbehandlung)
10. [Dateioperationen](#10-dateioperationen)
11. [Mathematik & Zufall](#11-mathematik--zufall)
12. [Typprüfung & Konvertierung](#12-typpruefung--konvertierung)
13. [Turtle-Grafik (Maler)](#13-turtle-grafik-maler)
14. [Spielfeld-Engine (Game Engine)](#14-spielfeld-engine-game-engine)
15. [Der Transpiler](#15-der-transpiler)
16. [Der "God Mode" (Fremde Bibliotheken)](#16-der-god-mode)
17. [Der Paketmanager (zpkg)](#17-der-paketmanager-zpkg)
18. [Zuse Studio (Die Entwicklungsumgebung)](#18-zuse-studio)
19. [Web Playground](#19-web-playground)
20. [Mehrsprachigkeit](#20-mehrsprachigkeit)
21. [Spickzettel (Cheat Sheet)](#21-spickzettel-cheat-sheet)

---

## 1. Was ist Zuse?

Zuse ist eine Programmiersprache, die entwickelt wurde, um die englische Sprachbarriere beim Programmierenlernen einzureißen. In Zuse programmierst du in deiner Muttersprache — ob Deutsch, Englisch, Spanisch, Französisch, Italienisch oder Portugiesisch.

Gleichzeitig ist Zuse kein reines Spielzeug: Unter der Haube arbeitet ein moderner Transpiler, der deinen Zuse-Code in produktionsreifes **Python**, **JavaScript**, **Java**, **C#** oder **WebAssembly** übersetzt.

**Zuse auf einen Blick:**

| Eigenschaft | Beschreibung |
|---|---|
| Sprachen | 6 (DE, EN, ES, FR, IT, PT) |
| Transpiler-Ziele | Python, JavaScript, Java, C#, WebAssembly |
| Grafik | Turtle-Grafik (Maler) + Spielfeld-Engine |
| IDE | Zuse Studio mit Debugger |
| Paketmanager | zpkg |
| Web | Playground im Browser (Pyodide) |
| Tests | 1086+ automatisierte Tests |

---

## 2. Die Grundlagen

In Zuse brauchst du keine Semikolons (`;`) am Zeilenende. Das Programm liest sich wie ein normales Buch. Kommentare beginnen mit `#`.

### 2.1 Variablen und Datentypen

Variablen sind Speicherplätze. Du weist ihnen mit einem Gleichheitszeichen (`=`) Werte zu.

```zuse
name = "Konrad"         # Text (String)
alter = 42              # Ganzzahl (Integer)
preis = 9.99            # Kommazahl (Float)
ist_aktiv = wahr        # Wahrheitswert (Boolean)
leer = NICHTS           # Kein Wert (Null/None)
```

**Datentypen im Überblick:**

| Typ | Beispiel | Beschreibung |
|---|---|---|
| Text (String) | `"Hallo"` | Zeichenkette in Anführungszeichen |
| Ganzzahl (Integer) | `42` | Ganze Zahl |
| Kommazahl (Float) | `3.14` | Dezimalzahl |
| Wahrheitswert (Boolean) | `wahr` / `falsch` | Logischer Wert |
| Liste | `[1, 2, 3]` | Geordnete Sammlung |
| Wörterbuch (Dict) | `{"name": "Zuse"}` | Schlüssel-Wert-Paare |
| Nichts (Null) | `NICHTS` | Kein Wert |

**Wahrheitswerte** können groß oder klein geschrieben werden: `wahr`/`WAHR` und `falsch`/`FALSCH`.

### 2.2 Mehrfachzuweisung

Du kannst mehrere Variablen gleichzeitig zuweisen:

```zuse
a, b = 1, 2
x, y, z = [10, 20, 30]

# Variablen tauschen — ganz einfach!
a, b = b, a
```

### 2.3 Ein- und Ausgabe

```zuse
# Text auf dem Bildschirm ausgeben
AUSGABE "Hallo Welt!"
AUSGABE "Dein Name ist: " + name

# Den Benutzer nach Text fragen
benutzer = EINGABE_TEXT "Wie heißt du? "

# Den Benutzer nach einer Zahl fragen
alter = EINGABE_ZAHL "Wie alt bist du? "
```

> **Tipp:** `ZEIGE` ist ein Alias für `AUSGABE` — beide funktionieren identisch.

### 2.4 Formatierung

Mit `FORMAT` kannst du Werte elegant in Text einsetzen:

```zuse
name = "Konrad"
alter = 42
AUSGABE FORMAT("Hallo, {}! Du bist {} Jahre alt.", name, alter)
# Ausgabe: Hallo, Konrad! Du bist 42 Jahre alt.
```

---

## 3. Operatoren

### 3.1 Arithmetische Operatoren

| Operator | Bedeutung | Beispiel |
|---|---|---|
| `+` | Addition | `5 + 3` ergibt `8` |
| `-` | Subtraktion | `5 - 3` ergibt `2` |
| `*` | Multiplikation | `5 * 3` ergibt `15` |
| `/` | Division | `10 / 3` ergibt `3.333...` |
| `%` | Modulo (Rest) | `10 % 3` ergibt `1` |
| `^` | Potenz | `2 ^ 8` ergibt `256` |

### 3.2 Vergleichsoperatoren

| Operator | Bedeutung |
|---|---|
| `==` | gleich |
| `!=` | ungleich |
| `>` | größer als |
| `<` | kleiner als |
| `>=` | größer oder gleich |
| `<=` | kleiner oder gleich |

### 3.3 Logische Operatoren

| Operator | Bedeutung | Beispiel |
|---|---|---|
| `UND` | Logisches Und | `alter > 18 UND alter < 65` |
| `ODER` | Logisches Oder | `tag == "Sa" ODER tag == "So"` |
| `NICHT` | Logische Negation | `NICHT ist_aktiv` |

---

## 4. Logik: Bedingungen & Schleifen

### 4.1 Bedingungen (WENN / DANN / SONST)

Um Entscheidungen zu treffen, nutzt Zuse logische Blöcke. Jeder Block muss mit `ENDE WENN` geschlossen werden.

```zuse
WENN alter >= 18 DANN
    AUSGABE "Du bist volljährig."
SONST WENN alter == 17 DANN
    AUSGABE "Fast geschafft!"
SONST
    AUSGABE "Du bist minderjährig."
ENDE WENN
```

### 4.2 Fallunterscheidung (WÄHLE / FALL)

Für mehrere Fälle ist `WÄHLE` übersichtlicher als viele `WENN`-Blöcke:

```zuse
note = 2

WÄHLE note
    FALL 1 DANN
        AUSGABE "Sehr gut!"
    FALL 2 DANN
        AUSGABE "Gut!"
    FALL 3 DANN
        AUSGABE "Befriedigend."
    FALL 4 DANN
        AUSGABE "Ausreichend."
    SONST
        AUSGABE "Nicht bestanden."
ENDE WÄHLE
```

### 4.3 Schleifen

Zuse kennt zwei Arten von Schleifen. Beide enden mit `ENDE SCHLEIFE`.

**Die FÜR-Schleife** (wenn die Anzahl bekannt ist):

```zuse
# Zählt von 0 bis 4
SCHLEIFE FÜR zahl IN BEREICH(5) MACHE
    AUSGABE zahl
ENDE SCHLEIFE

# BEREICH mit Start und Ende
SCHLEIFE FÜR i IN BEREICH(1, 11) MACHE
    AUSGABE i    # 1, 2, 3, ... 10
ENDE SCHLEIFE

# BEREICH mit Schrittweite
SCHLEIFE FÜR i IN BEREICH(0, 100, 10) MACHE
    AUSGABE i    # 0, 10, 20, ... 90
ENDE SCHLEIFE

# Eine Liste durchgehen
farben = ["rot", "grün", "blau"]
SCHLEIFE FÜR farbe IN farben MACHE
    AUSGABE farbe
ENDE SCHLEIFE
```

**Die SOLANGE-Schleife** (bedingungsbasiert):

```zuse
countdown = 3
SCHLEIFE SOLANGE countdown > 0 MACHE
    AUSGABE countdown
    countdown = countdown - 1
ENDE SCHLEIFE
```

### 4.4 Schleifensteuerung (ABBRUCH & WEITER)

Du kannst Schleifen vorzeitig verlassen oder Durchläufe überspringen:

```zuse
# ABBRUCH — Schleife sofort beenden
SCHLEIFE FÜR zahl IN BEREICH(100) MACHE
    WENN zahl == 5 DANN
        ABBRUCH
    ENDE WENN
    AUSGABE zahl    # 0, 1, 2, 3, 4
ENDE SCHLEIFE

# WEITER — Rest überspringen, nächster Durchlauf
SCHLEIFE FÜR zahl IN BEREICH(10) MACHE
    WENN zahl % 2 == 0 DANN
        WEITER
    ENDE WENN
    AUSGABE zahl    # 1, 3, 5, 7, 9 (nur ungerade)
ENDE SCHLEIFE
```

---

## 5. Struktur: Funktionen

### 5.1 Funktionen definieren

Wenn du Code mehrfach brauchst, verpacke ihn in eine Funktion:

```zuse
DEFINIERE addiere(zahl1, zahl2)
    summe = zahl1 + zahl2
    ERGEBNIS IST summe
ENDE FUNKTION

AUSGABE addiere(10, 5)    # Gibt 15 aus
```

### 5.2 Standardwerte (Default-Parameter)

Parameter können Standardwerte haben:

```zuse
DEFINIERE begruessung(name, gruss="Hallo")
    AUSGABE gruss + ", " + name + "!"
ENDE FUNKTION

begruessung("Anna")              # Hallo, Anna!
begruessung("Anna", "Servus")    # Servus, Anna!
```

### 5.3 Lambda-Funktionen (AKTION)

Für kurze Einzeiler-Funktionen gibt es `AKTION`:

```zuse
verdopple = AKTION(x): x * 2
AUSGABE verdopple(7)    # 14

addiere = AKTION(a, b): a + b
AUSGABE addiere(3, 4)   # 7

# Besonders nützlich mit FILTERN und UMWANDELN
zahlen = [1, 2, 3, 4, 5, 6, 7, 8]
gerade = FILTERN(zahlen, AKTION(x): x % 2 == 0)
AUSGABE gerade    # [2, 4, 6, 8]
```

### 5.4 Globale Variablen

Standardmäßig sind Variablen in Funktionen lokal. Mit `GLOBAL` kannst du auf globale Variablen zugreifen:

```zuse
zaehler = 0

DEFINIERE erhoehe()
    GLOBAL zaehler
    zaehler = zaehler + 1
ENDE FUNKTION

erhoehe()
erhoehe()
AUSGABE zaehler    # 2
```

### 5.5 Der PASS-Befehl

`PASS` ist ein Platzhalter, wenn ein Block noch leer ist:

```zuse
DEFINIERE spaeter_implementieren()
    PASS
ENDE FUNKTION
```

---

## 6. Klassen & Vererbung

### 6.1 Klassen erstellen

Zuse unterstützt professionelle Objektorientierung. Das eigene Objekt wird mit `MEIN` angesprochen.

```zuse
KLASSE Hund:
    # Der Konstruktor (wird beim Erstellen aufgerufen)
    DEFINIERE ERSTELLE(name, rasse):
        MEIN.name = name
        MEIN.rasse = rasse
    ENDE FUNKTION

    DEFINIERE bellen():
        AUSGABE MEIN.name + " sagt: Wuff!"
    ENDE FUNKTION

    DEFINIERE steckbrief():
        AUSGABE MEIN.name + " ist ein " + MEIN.rasse
    ENDE FUNKTION
ENDE KLASSE

bello = Hund("Bello", "Labrador")
bello.bellen()        # Bello sagt: Wuff!
bello.steckbrief()    # Bello ist ein Labrador
```

### 6.2 Vererbung

Eine Klasse kann von einer anderen erben. Mit `ELTERN` (oder `OBER`) rufst du die Methoden der Elternklasse auf:

```zuse
KLASSE Tier:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION

    DEFINIERE sprechen():
        AUSGABE MEIN.name + " macht ein Geräusch."
    ENDE FUNKTION
ENDE KLASSE

KLASSE Katze(Tier):
    DEFINIERE ERSTELLE(name, farbe):
        ELTERN.ERSTELLE(name)
        MEIN.farbe = farbe
    ENDE FUNKTION

    # Methode überschreiben (Polymorphie)
    DEFINIERE sprechen():
        AUSGABE MEIN.name + " sagt: Miau!"
    ENDE FUNKTION
ENDE KLASSE

mieze = Katze("Luna", "schwarz")
mieze.sprechen()    # Luna sagt: Miau!
```

---

## 7. Listen & Wörterbücher

### 7.1 Listen erstellen und nutzen

```zuse
# Liste erstellen
fruechte = ["Apfel", "Birne", "Kirsche"]

# Zugriff per Index (beginnt bei 0)
AUSGABE fruechte[0]    # Apfel
AUSGABE fruechte[2]    # Kirsche

# Wert ändern
fruechte[1] = "Banane"

# Länge
AUSGABE LAENGE(fruechte)    # 3
```

### 7.2 Listen-Methoden

| Methode | Beschreibung | Beispiel |
|---|---|---|
| `.hinzufuegen(wert)` | Element anhängen | `liste.hinzufuegen("neu")` |
| `.einfuegen(index, wert)` | An Position einfügen | `liste.einfuegen(0, "start")` |
| `.entfernen(wert)` | Element entfernen | `liste.entfernen("alt")` |
| `.sortieren()` | Liste sortieren | `liste.sortieren()` |
| `.umkehren()` | Reihenfolge umdrehen | `liste.umkehren()` |
| `.index(wert)` | Position finden | `liste.index("Apfel")` |
| `.zaehle(wert)` | Vorkommen zählen | `liste.zaehle("Apfel")` |
| `.leeren()` | Alle Elemente löschen | `liste.leeren()` |
| `.kopie()` | Flache Kopie erstellen | `neue = liste.kopie()` |

```zuse
zahlen = [3, 1, 4, 1, 5, 9]
zahlen.hinzufuegen(2)     # [3, 1, 4, 1, 5, 9, 2]
zahlen.sortieren()         # [1, 1, 2, 3, 4, 5, 9]
zahlen.umkehren()          # [9, 5, 4, 3, 2, 1, 1]
AUSGABE zahlen.zaehle(1)   # 2
```

### 7.3 Listen-Funktionen (Builtins)

| Funktion | Beschreibung |
|---|---|
| `SORTIEREN(liste)` | Sortierte Kopie zurückgeben |
| `FILTERN(liste, funktion)` | Elemente filtern |
| `UMWANDELN(liste, funktion)` | Jedes Element transformieren |
| `UMKEHREN(liste)` | Umgekehrte Kopie |
| `FLACH(liste)` | Verschachtelte Listen flach machen |
| `EINDEUTIG(liste)` | Duplikate entfernen |
| `AUFZAEHLEN(liste)` | Index-Wert-Paare erzeugen |
| `KOMBINIEREN(liste1, liste2)` | Listen zusammenführen (zip) |
| `ANHAENGEN(liste, elemente...)` | Mehrere Elemente anhängen |
| `SUMME(liste)` | Alle Elemente addieren |
| `ALLE(liste)` | Sind alle Elemente wahr? |
| `IRGENDEIN(liste)` | Ist mindestens eines wahr? |

```zuse
zahlen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Nur gerade Zahlen
gerade = FILTERN(zahlen, AKTION(x): x % 2 == 0)
AUSGABE gerade    # [2, 4, 6, 8, 10]

# Alle Zahlen verdoppeln
doppelt = UMWANDELN(zahlen, AKTION(x): x * 2)
AUSGABE doppelt   # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Verschachtelte Listen glätten
matrix = [[1, 2], [3, 4], [5, 6]]
AUSGABE FLACH(matrix)    # [1, 2, 3, 4, 5, 6]

# Duplikate entfernen
AUSGABE EINDEUTIG([1, 2, 2, 3, 3, 3])    # [1, 2, 3]
```

### 7.4 Slicing (Teilbereiche)

Mit Slicing kannst du Teilbereiche aus Listen und Texten extrahieren:

```zuse
buchstaben = ["a", "b", "c", "d", "e"]

# Von Index 1 bis 3 (exklusive)
AUSGABE buchstaben[1:3]    # ["b", "c"]

# Funktioniert auch mit Text
wort = "Programmieren"
AUSGABE wort[0:7]    # "Program"
```

### 7.5 Wörterbücher (Dictionaries)

Wörterbücher speichern Daten als Schlüssel-Wert-Paare:

```zuse
person = {
    "name": "Konrad",
    "alter": 42,
    "stadt": "Berlin"
}

# Zugriff
AUSGABE person["name"]    # Konrad

# Neuen Eintrag hinzufügen
person["beruf"] = "Ingenieur"

# Ändern
person["alter"] = 43
```

---

## 8. Textverarbeitung (Strings)

### 8.1 String-Methoden

| Methode | Beschreibung | Beispiel |
|---|---|---|
| `.gross()` | In Großbuchstaben | `"hallo".gross()` → `"HALLO"` |
| `.klein()` | In Kleinbuchstaben | `"HALLO".klein()` → `"hallo"` |
| `.ersetze(alt, neu)` | Text ersetzen | `"Hallo Welt".ersetze("Welt", "Zuse")` |
| `.teile(trenner)` | Text aufteilen | `"a,b,c".teile(",")` → `["a","b","c"]` |
| `.trimme()` | Leerzeichen entfernen | `"  Hallo  ".trimme()` → `"Hallo"` |
| `.beginnt_mit(text)` | Prüfe Anfang | `"Hallo".beginnt_mit("Hal")` → `wahr` |
| `.endet_mit(text)` | Prüfe Ende | `"Hallo".endet_mit("llo")` → `wahr` |
| `.enthaelt(text)` | Prüfe Inhalt | `"Hallo".enthaelt("all")` → `wahr` |
| `.finde(text)` | Position finden | `"Hallo".finde("ll")` → `2` |

### 8.2 String-Funktionen (Builtins)

```zuse
text = "Hallo Welt"

AUSGABE GROSSBUCHSTABEN(text)          # "HALLO WELT"
AUSGABE KLEINBUCHSTABEN(text)          # "hallo welt"
AUSGABE ERSETZE(text, "Welt", "Zuse") # "Hallo Zuse"
AUSGABE TEILE(text, " ")              # ["Hallo", "Welt"]
AUSGABE LAENGE(text)                   # 10
AUSGABE ENTHAELT(text, "Welt")         # wahr
AUSGABE VERBINDE(["A", "B", "C"], "-") # "A-B-C"
```

### 8.3 Sonderzeichen (Escape-Sequenzen)

| Sequenz | Bedeutung |
|---|---|
| `\n` | Neue Zeile |
| `\t` | Tabulator |
| `\\` | Backslash |
| `\"` | Anführungszeichen |

```zuse
AUSGABE "Zeile 1\nZeile 2"
AUSGABE "Name:\tKonrad"
```

### 8.4 Zeichencode-Funktionen

```zuse
AUSGABE ZEICHENCODE("A")    # 65
AUSGABE ZEICHEN(65)          # "A"
AUSGABE HEX(255)             # "0xff"
AUSGABE BIN(42)              # "0b101010"
AUSGABE OKT(8)               # "0o10"
```

---

## 9. Fehlerbehandlung

### 9.1 VERSUCHE / FANGE

Fehler können abgefangen werden, damit dein Programm nicht abstürzt:

```zuse
VERSUCHE
    ergebnis = 10 / 0
FANGE fehler
    AUSGABE "Ein Fehler ist aufgetreten: " + fehler
ENDE VERSUCHE
```

### 9.2 Praktisches Beispiel

```zuse
DEFINIERE sichere_division(a, b)
    VERSUCHE
        ERGEBNIS IST a / b
    FANGE fehler
        AUSGABE "Division durch 0 ist nicht erlaubt!"
        ERGEBNIS IST NICHTS
    ENDE VERSUCHE
ENDE FUNKTION

AUSGABE sichere_division(10, 2)    # 5
AUSGABE sichere_division(10, 0)    # Division durch 0 ist nicht erlaubt! → NICHTS
```

### 9.3 Fehler bei Benutzereingaben

```zuse
VERSUCHE
    alter = EINGABE_ZAHL "Wie alt bist du? "
    WENN alter < 0 DANN
        AUSGABE "Alter kann nicht negativ sein!"
    SONST
        AUSGABE "Du bist " + ALS_TEXT(alter) + " Jahre alt."
    ENDE WENN
FANGE fehler
    AUSGABE "Bitte gib eine gültige Zahl ein!"
ENDE VERSUCHE
```

---

## 10. Dateioperationen

Zuse kann Dateien lesen und schreiben — perfekt für Datenverarbeitung und Projekte.

### 10.1 Dateien lesen

```zuse
# Gesamten Inhalt lesen
inhalt = LESE_DATEI("meine_datei.txt")
AUSGABE inhalt

# Zeilenweise lesen (gibt eine Liste zurück)
zeilen = LESE_ZEILEN("meine_datei.txt")
SCHLEIFE FÜR zeile IN zeilen MACHE
    AUSGABE zeile
ENDE SCHLEIFE
```

### 10.2 Dateien schreiben

```zuse
# Datei schreiben (überschreibt vorhandene Datei)
SCHREIBE_DATEI("ausgabe.txt", "Hallo Welt!")

# An Datei anhängen
ERGAENZE_DATEI("log.txt", "Neuer Eintrag\n")
```

### 10.3 Dateien prüfen und löschen

```zuse
# Prüfen ob eine Datei existiert
WENN EXISTIERT("config.txt") DANN
    AUSGABE "Datei gefunden!"
SONST
    AUSGABE "Datei nicht vorhanden."
ENDE WENN

# Datei löschen
LOESCHE_DATEI("temp.txt")
```

> **Hinweis:** Dateioperationen stehen nur im **Profi-Modus** des Zuse Studios zur Verfügung. Im Lern-Modus sind sie aus Sicherheitsgründen gesperrt.

---

## 11. Mathematik & Zufall

### 11.1 Mathematische Funktionen

| Funktion | Beschreibung | Beispiel |
|---|---|---|
| `WURZEL(x)` | Quadratwurzel | `WURZEL(16)` → `4.0` |
| `POTENZ(x, y)` | x hoch y | `POTENZ(2, 10)` → `1024` |
| `ABSOLUT(x)` | Betrag | `ABSOLUT(-7)` → `7` |
| `RUNDEN(x, n)` | Runden auf n Stellen | `RUNDEN(3.14159, 2)` → `3.14` |
| `BODEN(x)` | Abrunden | `BODEN(3.7)` → `3` |
| `DECKE(x)` | Aufrunden | `DECKE(3.2)` → `4` |
| `MINIMUM(a, b, ...)` | Kleinster Wert | `MINIMUM(5, 3, 8)` → `3` |
| `MAXIMUM(a, b, ...)` | Größter Wert | `MAXIMUM(5, 3, 8)` → `8` |
| `SUMME(liste)` | Summe aller Elemente | `SUMME([1,2,3])` → `6` |

### 11.2 Trigonometrie

```zuse
AUSGABE SINUS(PI / 2)      # 1.0
AUSGABE COSINUS(0)          # 1.0
AUSGABE TANGENS(PI / 4)     # ~1.0
AUSGABE LOGARITHMUS(E)      # 1.0 (natürlicher Log)
AUSGABE LOGARITHMUS(100, 10) # 2.0 (Log Basis 10)
```

### 11.3 Konstanten

| Konstante | Wert | Beschreibung |
|---|---|---|
| `PI` | 3.14159... | Kreiszahl Pi |
| `E` | 2.71828... | Eulersche Zahl |

### 11.4 Zufall

```zuse
# Zufällige Kommazahl zwischen 0.0 und 1.0
AUSGABE ZUFALL()

# Zufällige Ganzzahl in einem Bereich
wuerfel = ZUFALL_BEREICH(1, 6)
AUSGABE "Du hast eine " + ALS_TEXT(wuerfel) + " gewürfelt!"
```

---

## 12. Typprüfung & Konvertierung

### 12.1 Typen prüfen

| Funktion | Prüft auf |
|---|---|
| `IST_ZAHL(x)` | Integer oder Float |
| `IST_TEXT(x)` | String |
| `IST_LISTE(x)` | Liste |
| `IST_DICT(x)` | Wörterbuch |
| `IST_BOOL(x)` | Wahrheitswert |
| `IST_NICHTS(x)` | NICHTS (None) |

```zuse
AUSGABE IST_ZAHL(42)         # wahr
AUSGABE IST_TEXT("Hallo")    # wahr
AUSGABE IST_LISTE([1, 2])    # wahr
AUSGABE IST_NICHTS(NICHTS)   # wahr
```

### 12.2 Typen konvertieren

| Funktion | Konvertiert zu |
|---|---|
| `ALS_ZAHL(x)` | Zahl (Integer oder Float) |
| `ALS_TEXT(x)` | Text (String) |

```zuse
# Text in Zahl umwandeln
zahl = ALS_ZAHL("42")
AUSGABE zahl + 8    # 50

# Zahl in Text umwandeln
text = ALS_TEXT(42)
AUSGABE "Die Antwort ist: " + text
```

---

## 13. Turtle-Grafik (Maler)

Der **Maler** ist Zuses Turtle-Grafik-System. Eine virtuelle Schildkröte zeichnet auf dem Bildschirm — perfekt zum Erlernen von Geometrie und Algorithmen.

### 13.1 Grundlagen

```zuse
BENUTZE deutsch ALS bib

stift = bib.Maler()

# Vorwärts bewegen und dabei zeichnen
stift.gehe(100)

# Drehen (in Grad)
stift.drehe_rechts(90)
stift.gehe(100)

# Fertig — Fenster bleibt offen
stift.fertig()
```

### 13.2 Maler-Befehle

| Befehl | Beschreibung |
|---|---|
| `gehe(schritte)` | Vorwärts bewegen |
| `zurueck(schritte)` | Rückwärts bewegen |
| `drehe_links(grad)` | Nach links drehen |
| `drehe_rechts(grad)` | Nach rechts drehen |
| `stift_hoch()` | Stift anheben (nicht mehr zeichnen) |
| `stift_runter()` | Stift absenken (wieder zeichnen) |
| `farbe(name)` | Stiftfarbe ändern |
| `dicke(d)` | Strichdicke ändern |
| `kreis(radius)` | Kreis zeichnen |
| `fertig()` | Zeichnung abschließen |

### 13.3 Beispiel: Ein Stern

```zuse
BENUTZE deutsch ALS bib

stift = bib.Maler()
stift.farbe("gold")
stift.dicke(3)

SCHLEIFE FÜR i IN BEREICH(5) MACHE
    stift.gehe(150)
    stift.drehe_rechts(144)
ENDE SCHLEIFE

stift.fertig()
```

### 13.4 Beispiel: Bunte Spirale

```zuse
BENUTZE deutsch ALS bib

stift = bib.Maler()
farben = ["rot", "blau", "grün", "gelb", "lila"]

SCHLEIFE FÜR i IN BEREICH(100) MACHE
    stift.farbe(farben[i % 5])
    stift.gehe(i * 2)
    stift.drehe_rechts(91)
ENDE SCHLEIFE

stift.fertig()
```

---

## 14. Spielfeld-Engine (Game Engine)

Das **Spielfeld** ist Zuses eingebaute Game-Engine. Damit kannst du 2D-Spiele und Animationen erstellen — komplett in deiner Muttersprache.

### 14.1 Ein Spielfeld erstellen

```zuse
BENUTZE deutsch ALS bib

spiel = bib.Spielfeld("Mein Spiel", 800, 600, "schwarz")
```

Die Parameter sind: **Titel**, **Breite**, **Höhe**, **Hintergrundfarbe**.

### 14.2 Sprites (Spielfiguren)

```zuse
# Rechteck-Sprite erstellen
spieler = spiel.neuer_sprite(100, 100, 40, 40, "blau")

# Text-Sprite erstellen
punkte_anzeige = spiel.neuer_text(10, 10, "Punkte: 0", "weiß", 20)
```

**Sprite-Methoden:**

| Methode | Beschreibung |
|---|---|
| `.bewege(dx, dy)` | Relativ verschieben |
| `.setze_position(x, y)` | Absolute Position setzen |
| `.kollidiert_mit(anderer)` | Kollisionsprüfung |
| `.am_rand()` | Am Fensterrand? |
| `.verstecke()` | Unsichtbar machen |
| `.zeige()` | Wieder sichtbar machen |
| `.aendere_farbe(farbe)` | Farbe ändern |
| `.entferne()` | Sprite löschen |

### 14.3 Tastatureingabe

```zuse
# In der Spielschleife prüfen
WENN spiel.taste_gedrueckt("Links") DANN
    spieler.bewege(-5, 0)
ENDE WENN
WENN spiel.taste_gedrueckt("Rechts") DANN
    spieler.bewege(5, 0)
ENDE WENN
WENN spiel.taste_gedrueckt("Hoch") DANN
    spieler.bewege(0, -5)
ENDE WENN
WENN spiel.taste_gedrueckt("Runter") DANN
    spieler.bewege(0, 5)
ENDE WENN
```

**Verfügbare Tasten:** `"Links"`, `"Rechts"`, `"Hoch"`, `"Runter"`, `"Leertaste"`, `"Eingabe"`, `"Escape"`

### 14.4 Mauseingabe

```zuse
# Mausposition abfragen
pos = spiel.maus_position()
AUSGABE pos    # [x, y]

# Mausklick prüfen
WENN spiel.maus_gedrueckt() DANN
    AUSGABE "Klick!"
ENDE WENN
```

### 14.5 Zeichenfunktionen

```zuse
spiel.zeichne_rechteck(50, 50, 200, 100, "rot")
spiel.zeichne_kreis(400, 300, 50, "gelb")
spiel.zeichne_linie(0, 0, 800, 600, "weiß", 2)
spiel.zeichne_text(100, 50, "Game Over", "rot", 48)
spiel.zeichne_polygon([[100,100], [150,50], [200,100]], "grün")
```

### 14.6 Die Spielschleife

Die Spielschleife ist das Herzstück jedes Spiels. Sie wird X-mal pro Sekunde (FPS) aufgerufen:

```zuse
BENUTZE deutsch ALS bib

spiel = bib.Spielfeld("Fangspiel", 800, 600, "schwarz")
spieler = spiel.neuer_sprite(400, 300, 30, 30, "blau")
punkte = 0

DEFINIERE aktualisiere()
    GLOBAL punkte

    # Steuerung
    WENN spiel.taste_gedrueckt("Links") DANN
        spieler.bewege(-5, 0)
    ENDE WENN
    WENN spiel.taste_gedrueckt("Rechts") DANN
        spieler.bewege(5, 0)
    ENDE WENN

    # Beenden mit Escape
    WENN spiel.taste_gedrueckt("Escape") DANN
        spiel.stoppe()
    ENDE WENN
ENDE FUNKTION

# Spielschleife mit 60 FPS starten
spiel.spielschleife(aktualisiere, 60)
spiel.starte()
```

### 14.7 Weitere Spielfeld-Funktionen

| Funktion | Beschreibung |
|---|---|
| `spiel.spielschleife(fn, fps)` | Spielschleife starten |
| `spiel.stoppe()` | Spielschleife beenden |
| `spiel.aktualisiere()` | Anzeige manuell erneuern |
| `spiel.starte()` | Hauptschleife starten |
| `spiel.nach_zeit(ms, fn)` | Funktion nach X ms ausführen |
| `spiel.schliessen()` | Fenster schließen |
| `spiel.setze_titel(titel)` | Titel ändern |
| `spiel.loesche_alles()` | Alles vom Bildschirm löschen |
| `spiel.bei_taste(taste, fn)` | Taste an Funktion binden |

---

## 15. Der Transpiler

Du hast ein Zuse-Programm geschrieben — was nun? Mit dem **Zuse Transpiler** kannst du deinen Code in andere Programmiersprachen übersetzen.

### 15.1 Unterstützte Zielsprachen

| Ziel | Dateiendung | Einsatzgebiet |
|---|---|---|
| **Python** | `.py` | Datenwissenschaft, Automatisierung, KI |
| **JavaScript** | `.js` | Webseiten, Node.js, Browser-Apps |
| **Java** | `.java` | Android, Enterprise, Server |
| **C#** | `.cs` | Unity-Spiele, Windows, .NET |
| **WebAssembly** | `.wasm` | Hochleistung im Browser |

### 15.2 Transpilieren im Zuse Studio

1. Öffne dein Programm im **Zuse Studio**.
2. Klicke auf **TRANSPILIEREN**.
3. Wähle dein Ziel aus.
4. Die übersetzte Datei wird im gleichen Ordner gespeichert.

### 15.3 Was der Transpiler kann

```zuse
# Dieses Zuse-Programm...
DEFINIERE fakultaet(n)
    WENN n <= 1 DANN
        ERGEBNIS IST 1
    SONST
        ERGEBNIS IST n * fakultaet(n - 1)
    ENDE WENN
ENDE FUNKTION

AUSGABE fakultaet(10)
```

...wird z. B. zu diesem **JavaScript**:

```javascript
function fakultaet(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * fakultaet(n - 1);
    }
}
console.log(fakultaet(10));
```

...oder zu diesem **Java**:

```java
public class Main {
    static Object fakultaet(Object n) {
        if ((int)n <= 1) {
            return 1;
        } else {
            return (int)n * (int)fakultaet((int)n - 1);
        }
    }
    public static void main(String[] args) {
        System.out.println(fakultaet(10));
    }
}
```

---

## 16. Der "God Mode" (Fremde Bibliotheken)

Zuse läuft auf einer mächtigen Python-Engine. Im **Profi-Modus** des Zuse Studios schaltet sich der "God Mode" frei. Das bedeutet: Du kannst **jede** installierte Python-Bibliothek direkt in Zuse nutzen!

### 16.1 Der BENUTZE-Befehl

```zuse
BENUTZE requests ALS netz

antwort = netz.get("https://api.github.com")
WENN antwort.status_code == 200 DANN
    AUSGABE "Internetverbindung steht!"
ENDE WENN
```

### 16.2 Weitere Beispiele

**Daten visualisieren mit matplotlib:**
```zuse
BENUTZE matplotlib.pyplot ALS plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]
plt.plot(x, y)
plt.title("Quadratzahlen")
plt.show()
```

**PDFs lesen mit pypdf2:**
```zuse
BENUTZE PyPDF2 ALS pdf

leser = pdf.PdfReader("dokument.pdf")
SCHLEIFE FÜR seite IN leser.pages MACHE
    AUSGABE seite.extract_text()
ENDE SCHLEIFE
```

### 16.3 Wichtige Einschränkung

> **Achtung:** Der "God Mode" funktioniert perfekt, wenn du dein Programm direkt in Zuse ausführst oder nach **Python** transpilierst.
> Du kannst ein Programm, das Python-Bibliotheken (wie `requests` oder `matplotlib`) importiert, **nicht** nach Java, C# oder JavaScript transpilieren, da diese Sprachen diese Bibliotheken nicht besitzen!

---

## 17. Der Paketmanager (zpkg)

**zpkg** ist der eingebaute Paketmanager von Zuse. Damit kannst du Zuse-Bibliotheken installieren, verwalten und teilen.

### 17.1 Paket-Manifest (zpkg.json)

Jedes Zuse-Paket braucht eine `zpkg.json` Datei:

```json
{
    "name": "mein_paket",
    "version": "1.0.0",
    "autor": "Dein Name",
    "beschreibung": "Was das Paket macht",
    "hauptdatei": "main.zuse",
    "sprache": "deutsch",
    "abhaengigkeiten": {
        "mathe_extra": ">=1.0.0"
    }
}
```

### 17.2 Versionierung (SemVer)

zpkg verwendet **Semantische Versionierung**:

| Format | Bedeutung |
|---|---|
| `1.0.0` | Genau diese Version |
| `>=1.0.0` | Diese Version oder neuer |
| `<2.0.0` | Unter Version 2 |
| `>=1.0.0,<2.0.0` | Bereich (ab 1.0, vor 2.0) |

### 17.3 Pakete installieren & entfernen

Pakete können über die zpkg-API im Code oder über das Zuse Studio verwaltet werden.

---

## 18. Zuse Studio (Die Entwicklungsumgebung)

Das **Zuse Studio** ist deine Kommandozentrale für alles rund um Zuse.

### 18.1 Modi

| Modus | Beschreibung |
|---|---|
| **Lern-Modus** | Sperrt gefährliche System-Bibliotheken. Perfekt für Schulen. Erlaubt nur sichere Module wie `mathe`, `zufall` oder die Grafik-Engines `Spielfeld` und `Maler`. |
| **Profi-Modus** | Schaltet den "God Mode" frei. Voller Zugriff auf das Betriebssystem und alle Python-Module. |

### 18.2 Funktionen

| Funktion | Beschreibung |
|---|---|
| **Ausführen** | Startet das Zuse-Programm |
| **Transpilieren** | Übersetzt in Python, JS, Java, C# oder WASM |
| **Debug** | Schritt-für-Schritt-Ausführung mit Breakpoints |
| **GUI-Modus** | Aktiviere dies für Programme mit grafischen Fenstern (Spielfeld, tkinter), damit das Studio nicht blockiert |

### 18.3 Debugger

1. Setze **Breakpoints** durch Klick auf die Zeilennummern (roter Punkt).
2. Klicke auf **Debug**.
3. Das Programm hält an jedem Breakpoint an.
4. Im Debug-Fenster siehst du alle Variablen und ihre aktuellen Werte.
5. Mit **Weiter** springst du zum nächsten Breakpoint.

### 18.4 Weitere IDE-Features

- **Syntax-Highlighting** für alle 6 Zuse-Sprachen
- **LSP-Server** (Language Server Protocol) für Editoren wie VS Code
- **Go-to-Definition** — Springe zur Definition einer Funktion oder Klasse
- **Hover-Dokumentation** — Zeige Info beim Überfahren mit der Maus
- **Fehlerhervorhebung** — Fehler werden direkt im Editor markiert
- **Semantische Analyse** — Erkennt Variablen-Shadowing, unerreichbaren Code und doppelte Parameter

---

## 19. Web Playground

Der **Zuse Web Playground** ermöglicht es, Zuse direkt im Browser auszuführen — ohne Installation.

### 19.1 Technologie

- **Pyodide** — Python-Interpreter im Browser (WebAssembly)
- **CodeMirror** — Editor mit Syntax-Highlighting und Zeilennummern
- **HTML5 Canvas** — Für Turtle-Grafik und Spielfeld im Browser

### 19.2 Funktionen

- Zuse-Code schreiben und sofort ausführen
- Alle Grundfunktionen verfügbar
- Turtle-Grafik (Maler) läuft direkt im Browser
- Spielfeld-Engine im Browser (Canvas-basiert)
- Dark Mode
- Kein Download, keine Installation nötig

### 19.3 Einschränkungen im Browser

- Kein Dateisystem-Zugriff (`LESE_DATEI` etc. nicht verfügbar)
- Keine externen Python-Bibliotheken (kein "God Mode")
- `EINGABE_TEXT` / `EINGABE_ZAHL` nutzen Browser-Prompts

---

## 20. Mehrsprachigkeit

Zuse unterstützt **6 Sprachen**. Alle Schlüsselwörter, Fehlermeldungen und eingebauten Funktionen sind vollständig übersetzt.

### 20.1 Sprachvergleich — Schlüsselwörter

| Konzept | Deutsch | English | Español | Français | Italiano | Português |
|---|---|---|---|---|---|---|
| Ausgabe | `AUSGABE` | `PRINT` | `MOSTRAR` | `AFFICHER` | `MOSTRA` | `MOSTRAR` |
| Wenn | `WENN` | `IF` | `SI` | `SI` | `SE` | `SE` |
| Dann | `DANN` | `THEN` | `ENTONCES` | `ALORS` | `ALLORA` | `ENTAO` |
| Sonst | `SONST` | `ELSE` | `SINO` | `SINON` | `ALTRIMENTI` | `SENAO` |
| Schleife | `SCHLEIFE` | `LOOP` | `BUCLE` | `BOUCLE` | `CICLO` | `CICLO` |
| Für | `FÜR` | `FOR` | `PARA` | `POUR` | `PER` | `PARA` |
| Solange | `SOLANGE` | `WHILE` | `MIENTRAS` | `TANT_QUE` | `FINCHE` | `ENQUANTO` |
| Funktion | `DEFINIERE` | `DEFINE` | `DEFINIR` | `DEFINIR` | `DEFINISCI` | `DEFINIR` |
| Klasse | `KLASSE` | `CLASS` | `CLASE` | `CLASSE` | `CLASSE` | `CLASSE` |
| Wahr | `wahr` | `true` | `verdadero` | `vrai` | `vero` | `verdadeiro` |
| Falsch | `falsch` | `false` | `falso` | `faux` | `falso` | `falso` |
| Und | `UND` | `AND` | `Y` | `ET` | `E` | `E` |
| Oder | `ODER` | `OR` | `O` | `OU` | `O` | `OU` |
| Nicht | `NICHT` | `NOT` | `NO` | `NON` | `NON` | `NAO` |
| Ergebnis | `ERGEBNIS IST` | `RESULT IS` | `RESULTADO ES` | `RESULTAT EST` | `RISULTATO E` | `RESULTADO E` |
| Versuche | `VERSUCHE` | `TRY` | `INTENTAR` | `ESSAYER` | `PROVA` | `TENTAR` |
| Fange | `FANGE` | `CATCH` | `CAPTURAR` | `ATTRAPER` | `CATTURA` | `CAPTURAR` |
| Wähle | `WÄHLE` | `SWITCH` | `ELEGIR` | `CHOISIR` | `SCEGLI` | `ESCOLHER` |
| Fall | `FALL` | `CASE` | `CASO` | `CAS` | `CASO` | `CASO` |
| Abbruch | `ABBRUCH` | `BREAK` | `ROMPER` | `ARRETER` | `INTERROMPI` | `PARAR` |
| Weiter | `WEITER` | `CONTINUE` | `CONTINUAR` | `CONTINUER` | `CONTINUA` | `CONTINUAR` |
| Lambda | `AKTION` | `LAMBDA` | `ACCION` | `ACTION` | `AZIONE` | `ACAO` |

### 20.2 Beispiel: Das gleiche Programm in 3 Sprachen

**Deutsch:**
```zuse
DEFINIERE begruessung(name)
    AUSGABE "Hallo, " + name + "!"
ENDE FUNKTION
begruessung("Welt")
```

**English:**
```zuse
DEFINE greeting(name)
    PRINT "Hello, " + name + "!"
END FUNCTION
greeting("World")
```

**Español:**
```zuse
DEFINIR saludo(nombre)
    MOSTRAR "Hola, " + nombre + "!"
FIN FUNCION
saludo("Mundo")
```

---

## 21. Spickzettel (Cheat Sheet)

### Grundlagen

| Konzept | Zuse Syntax |
|---|---|
| Ausgabe | `AUSGABE wert` |
| Texteingabe | `x = EINGABE_TEXT "Frage: "` |
| Zahleingabe | `x = EINGABE_ZAHL "Frage: "` |
| Kommentar | `# Dies ist ein Kommentar` |
| Nichts/Null | `NICHTS` |
| Wahrheitswerte | `wahr` / `falsch` |
| Logik | `UND`, `ODER`, `NICHT` |

### Kontrollstrukturen

| Konzept | Zuse Syntax |
|---|---|
| Bedingung | `WENN bed DANN ... SONST ... ENDE WENN` |
| Fallunterscheidung | `WÄHLE wert ... FALL x DANN ... ENDE WÄHLE` |
| Zähl-Schleife | `SCHLEIFE FÜR x IN BEREICH(10) MACHE ... ENDE SCHLEIFE` |
| Listen-Schleife | `SCHLEIFE FÜR x IN liste MACHE ... ENDE SCHLEIFE` |
| Dauer-Schleife | `SCHLEIFE SOLANGE bed MACHE ... ENDE SCHLEIFE` |
| Abbrechen | `ABBRUCH` |
| Überspringen | `WEITER` |

### Funktionen & Klassen

| Konzept | Zuse Syntax |
|---|---|
| Funktion | `DEFINIERE name(param) ... ERGEBNIS IST wert ENDE FUNKTION` |
| Standardwert | `DEFINIERE f(x, y=10) ...` |
| Lambda | `AKTION(x): x * 2` |
| Klasse | `KLASSE Name: ... ENDE KLASSE` |
| Konstruktor | `DEFINIERE ERSTELLE(param): ...` |
| Eigenes Objekt | `MEIN.attribut` |
| Vererbung | `KLASSE Kind(Elternteil): ...` |
| Elternaufruf | `ELTERN.methode()` |
| Global | `GLOBAL varname` |
| Platzhalter | `PASS` |

### Fehlerbehandlung

| Konzept | Zuse Syntax |
|---|---|
| Try/Catch | `VERSUCHE ... FANGE fehler ... ENDE VERSUCHE` |

### Datenstrukturen

| Konzept | Zuse Syntax |
|---|---|
| Liste erstellen | `[1, 2, 3]` |
| Dict erstellen | `{"key": "value"}` |
| Zugriff | `liste[0]` / `dict["key"]` |
| Slicing | `liste[1:3]` |
| Anhängen | `liste.hinzufuegen(wert)` |
| Sortieren | `liste.sortieren()` |
| Länge | `LAENGE(obj)` |

### Builtins (Auswahl)

| Funktion | Beschreibung |
|---|---|
| `LAENGE(x)` | Länge von Text/Liste |
| `BEREICH(n)` | Zahlenfolge 0..n-1 |
| `SORTIEREN(liste)` | Sortierte Kopie |
| `FILTERN(liste, fn)` | Elemente filtern |
| `UMWANDELN(liste, fn)` | Elemente transformieren |
| `FORMAT(text, ...)` | Text formatieren |
| `WURZEL(x)` | Quadratwurzel |
| `ZUFALL_BEREICH(a, b)` | Zufällige Ganzzahl |
| `ALS_ZAHL(x)` | In Zahl konvertieren |
| `ALS_TEXT(x)` | In Text konvertieren |
| `IST_ZAHL(x)` | Typprüfung |

### Dateien

| Funktion | Beschreibung |
|---|---|
| `LESE_DATEI(pfad)` | Datei lesen |
| `SCHREIBE_DATEI(pfad, inhalt)` | Datei schreiben |
| `ERGAENZE_DATEI(pfad, inhalt)` | An Datei anhängen |
| `LESE_ZEILEN(pfad)` | Zeilenweise lesen |
| `EXISTIERT(pfad)` | Datei vorhanden? |
| `LOESCHE_DATEI(pfad)` | Datei löschen |

### Import

| Konzept | Zuse Syntax |
|---|---|
| Modul laden | `BENUTZE modul` |
| Mit Alias | `BENUTZE modul ALS name` |
| Standardlib | `BENUTZE deutsch ALS bib` |

---

**Zuse 7.3** — Die mehrsprachige Programmiersprache.
Entwickelt von Innobytix IT.

Willkommen in der Zukunft der inklusiven Programmierung. Viel Spass mit Zuse!
