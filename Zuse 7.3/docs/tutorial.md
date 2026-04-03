# Zuse Tutorial — In 10 Lektionen Programmieren lernen

Dieses Tutorial fuehrt dich Schritt fuer Schritt durch die Programmiersprache Zuse. Keine Vorkenntnisse noetig!

---

## Lektion 1: Hallo Welt!

Jedes Programm beginnt mit einer Ausgabe.

```
AUSGABE "Hallo Welt!"
```

**Probiere aus:**
```
AUSGABE "Ich lerne Zuse!"
AUSGABE 42
AUSGABE 3 + 4
```

`AUSGABE` gibt einen Wert auf dem Bildschirm aus. Du kannst Text (in Anfuehrungszeichen), Zahlen oder Berechnungen ausgeben.

---

## Lektion 2: Variablen

Variablen speichern Werte unter einem Namen.

```
name = "Max"
alter = 15
groesse = 1.75

AUSGABE name
AUSGABE "Du bist " + str(alter) + " Jahre alt."
```

**Regeln:**
- Variablennamen bestehen aus Buchstaben, Zahlen und `_`
- Sie duerfen nicht mit einer Zahl beginnen
- `str()` wandelt eine Zahl in Text um (noetig zum Verbinden mit `+`)

**Probiere aus:**
```
vorname = "Anna"
nachname = "Mueller"
AUSGABE vorname + " " + nachname

x = 10
x = x + 5
AUSGABE x   # 15
```

---

## Lektion 3: Eingabe vom Benutzer

Programme koennen den Benutzer nach Werten fragen.

```
name = EINGABE_TEXT("Wie heisst du? ")
AUSGABE "Hallo " + name + "!"

alter = EINGABE_ZAHL("Wie alt bist du? ")
AUSGABE "In 10 Jahren bist du " + str(alter + 10)
```

- `EINGABE_TEXT` liest einen Text
- `EINGABE_ZAHL` liest eine Zahl

---

## Lektion 4: Bedingungen

Programme treffen Entscheidungen mit WENN.

```
alter = EINGABE_ZAHL("Dein Alter? ")

WENN alter >= 18 DANN
    AUSGABE "Du darfst waehlen!"
SONST WENN alter >= 16 DANN
    AUSGABE "Fast erwachsen!"
SONST
    AUSGABE "Du bist noch jung."
ENDE WENN
```

**Vergleiche:** `==` (gleich), `!=` (ungleich), `<`, `>`, `<=`, `>=`

**Logik:** `UND`, `ODER`, `NICHT`

```
note = 2
bestanden = note <= 4

WENN bestanden UND note <= 2 DANN
    AUSGABE "Sehr gut!"
SONST WENN bestanden DANN
    AUSGABE "Bestanden."
SONST
    AUSGABE "Leider durchgefallen."
ENDE WENN
```

---

## Lektion 5: Schleifen

Schleifen wiederholen Code.

### SOLANGE-Schleife (wiederholt solange Bedingung wahr ist)

```
countdown = 5
SOLANGE countdown > 0 MACHE
    AUSGABE countdown
    countdown = countdown - 1
ENDE SCHLEIFE
AUSGABE "Start!"
```

### FUER-Schleife (zaehlt durch einen Bereich)

```
SCHLEIFE FÜR i IN BEREICH(5) MACHE
    AUSGABE "Durchlauf " + str(i)
ENDE SCHLEIFE
```

```
# Durch eine Liste laufen
farben = ["rot", "gruen", "blau"]
SCHLEIFE FÜR farbe IN farben MACHE
    AUSGABE farbe
ENDE SCHLEIFE
```

**Schleifensteuerung:**
```
SCHLEIFE FÜR i IN BEREICH(100) MACHE
    WENN i == 5 DANN
        ABBRUCH     # Schleife sofort verlassen
    ENDE WENN
    AUSGABE i       # 0, 1, 2, 3, 4
ENDE SCHLEIFE
```

---

## Lektion 6: Funktionen

Funktionen buendeln Code, den du mehrfach verwenden willst.

```
DEFINIERE begruessung(name):
    AUSGABE "Willkommen, " + name + "!"
ENDE FUNKTION

begruessung("Max")     # Willkommen, Max!
begruessung("Anna")    # Willkommen, Anna!
```

### Rueckgabewerte

```
DEFINIERE quadrat(x):
    ERGEBNIS IST x * x
ENDE FUNKTION

ergebnis = quadrat(7)
AUSGABE ergebnis   # 49
```

### Default-Parameter

```
DEFINIERE wiederhole(text, anzahl=3):
    SCHLEIFE FÜR i IN BEREICH(anzahl) MACHE
        AUSGABE text
    ENDE SCHLEIFE
ENDE FUNKTION

wiederhole("Hallo")       # 3x Hallo
wiederhole("Hey", 5)      # 5x Hey
```

---

## Lektion 7: Listen

Listen speichern mehrere Werte in einer geordneten Sammlung.

```
noten = [1, 2, 3, 2, 1, 4]

AUSGABE noten[0]      # 1 (erstes Element)
AUSGABE len(noten)    # 6 (Anzahl)

# Element hinzufuegen
noten = ANHAENGEN(noten, 2)

# Sortieren
sortiert = SORTIEREN(noten)
AUSGABE sortiert   # [1, 1, 2, 2, 2, 3, 4]
```

### Listen mit AKTION (Lambda)

```
zahlen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Nur gerade Zahlen
gerade = FILTERN(zahlen, AKTION(x): x % 2 == 0)
AUSGABE gerade   # [2, 4, 6, 8, 10]

# Jede Zahl verdoppeln
doppelt = UMWANDELN(zahlen, AKTION(x): x * 2)
AUSGABE doppelt   # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
```

---

## Lektion 8: Woerterbuecher

Woerterbuecher speichern Schluessel-Wert-Paare.

```
person = {
    "name": "Max",
    "alter": 20,
    "stadt": "Berlin"
}

AUSGABE person["name"]    # Max
AUSGABE person["alter"]   # 20
```

---

## Lektion 9: Klassen

Klassen definieren eigene Datentypen mit Eigenschaften und Methoden.

```
KLASSE Haustier:
    DEFINIERE ERSTELLE(name, art, alter):
        MEIN.name = name
        MEIN.art = art
        MEIN.alter = alter
    ENDE FUNKTION

    DEFINIERE vorstellen():
        AUSGABE MEIN.name + " ist ein " + MEIN.art + " (" + str(MEIN.alter) + " Jahre)"
    ENDE FUNKTION

    DEFINIERE geburtstag():
        MEIN.alter = MEIN.alter + 1
        AUSGABE MEIN.name + " ist jetzt " + str(MEIN.alter) + "!"
    ENDE FUNKTION
ENDE KLASSE

rex = Haustier("Rex", "Hund", 5)
rex.vorstellen()    # Rex ist ein Hund (5 Jahre)
rex.geburtstag()    # Rex ist jetzt 6!
```

### Vererbung

```
KLASSE Hund(Haustier):
    DEFINIERE ERSTELLE(name, alter):
        ELTERN.ERSTELLE(name, "Hund", alter)
    ENDE FUNKTION

    DEFINIERE bellen():
        AUSGABE MEIN.name + ": Wuff wuff!"
    ENDE FUNKTION
ENDE KLASSE

bello = Hund("Bello", 3)
bello.vorstellen()   # Bello ist ein Hund (3 Jahre)
bello.bellen()       # Bello: Wuff wuff!
```

---

## Lektion 10: Fehlerbehandlung und Dateien

### Fehler abfangen

```
VERSUCHE
    zahl = int("abc")
FANGE fehler
    AUSGABE "Das war keine Zahl!"
ENDE VERSUCHE
```

### Dateien lesen und schreiben

```
# In Datei schreiben
SCHREIBE_DATEI("notizen.txt", "Meine erste Notiz")

# Datei lesen
inhalt = LESE_DATEI("notizen.txt")
AUSGABE inhalt   # Meine erste Notiz

# Text anhaengen
ERGAENZE_DATEI("notizen.txt", "\nZweite Zeile")

# Pruefen ob Datei existiert
WENN EXISTIERT("notizen.txt") DANN
    zeilen = LESE_ZEILEN("notizen.txt")
    SCHLEIFE FÜR zeile IN zeilen MACHE
        AUSGABE zeile
    ENDE SCHLEIFE
ENDE WENN
```

---

## Naechste Schritte

Du kennst jetzt die Grundlagen von Zuse! Hier sind Ideen zum Weitermachen:

1. **Beispielprogramme anschauen** — Siehe [beispiele.md](beispiele.md)
2. **Sprachreferenz nutzen** — Siehe [referenz.md](referenz.md) fuer alle Funktionen
3. **Spielfeld ausprobieren** — Erstelle einfache Spiele mit Grafik
4. **Andere Sprache testen** — Schreibe dein Programm in English, Espanol oder Francais
5. **Transpilieren** — Uebersetze dein Zuse-Programm nach Python oder JavaScript
