# Zuse Sprachreferenz

Vollstaendige Referenz aller Keywords, Typen, Operatoren und eingebauten Funktionen.

---

## 1. Grundlagen

### Ausgabe

```
AUSGABE "Hallo Welt!"
AUSGABE 42
AUSGABE 3.14
```

### Variablen

```
name = "Zuse"
alter = 7
pi = 3.14159
aktiv = wahr
```

Variablen werden durch Zuweisung erzeugt. Kein Typ muss angegeben werden.

### Kommentare

```
# Das ist ein Kommentar
x = 42  # Kommentar am Zeilenende
```

### Datentypen

| Typ | Beispiel | Beschreibung |
|-----|----------|--------------|
| Zahl (int) | `42` | Ganzzahl |
| Zahl (float) | `3.14` | Dezimalzahl |
| Text (string) | `"Hallo"` | Zeichenkette |
| Wahrheitswert | `wahr`, `falsch` | Boolean |
| Liste | `[1, 2, 3]` | Geordnete Sammlung |
| Woerterbuch | `{"a": 1, "b": 2}` | Schluessel-Wert-Paare |

### String-Escape-Sequenzen

| Sequenz | Bedeutung |
|---------|-----------|
| `\n` | Neue Zeile |
| `\t` | Tabulator |
| `\\` | Backslash |
| `\"` | Anfuehrungszeichen |

---

## 2. Operatoren

### Arithmetik

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| `+` | Addition | `3 + 4` → `7` |
| `-` | Subtraktion | `10 - 3` → `7` |
| `*` | Multiplikation | `3 * 4` → `12` |
| `/` | Division | `10 / 3` → `3.33...` |
| `%` | Modulo (Rest) | `10 % 3` → `1` |
| `^` | Potenz | `2 ^ 3` → `8` |

### Vergleich

| Operator | Bedeutung |
|----------|-----------|
| `==` | Gleich |
| `!=` | Ungleich |
| `<` | Kleiner |
| `>` | Groesser |
| `<=` | Kleiner oder gleich |
| `>=` | Groesser oder gleich |

### Logik

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| `UND` | Logisches Und | `wahr UND falsch` → `falsch` |
| `ODER` | Logisches Oder | `wahr ODER falsch` → `wahr` |
| `NICHT` | Logische Negation | `NICHT wahr` → `falsch` |

---

## 3. Kontrollstrukturen

### Bedingung (WENN)

```
WENN alter >= 18 DANN
    AUSGABE "Erwachsen"
SONST WENN alter >= 13 DANN
    AUSGABE "Jugendlich"
SONST
    AUSGABE "Kind"
ENDE WENN
```

### Solange-Schleife

```
x = 0
SOLANGE x < 10 MACHE
    AUSGABE x
    x = x + 1
ENDE SCHLEIFE
```

### Fuer-Schleife

```
SCHLEIFE FÜR i IN BEREICH(10) MACHE
    AUSGABE i
ENDE SCHLEIFE

SCHLEIFE FÜR element IN [1, 2, 3] MACHE
    AUSGABE element
ENDE SCHLEIFE
```

### BEREICH-Funktion

```
BEREICH(5)          # [0, 1, 2, 3, 4]
BEREICH(2, 8)       # [2, 3, 4, 5, 6, 7]
BEREICH(0, 10, 2)   # [0, 2, 4, 6, 8]
```

### Schleifensteuerung

```
SOLANGE wahr MACHE
    WENN bedingung DANN
        ABBRUCH      # Schleife verlassen
    ENDE WENN
    WEITER           # Naechster Durchlauf
ENDE SCHLEIFE
```

---

## 4. Funktionen

### Definition und Aufruf

```
DEFINIERE quadrat(x):
    ERGEBNIS IST x * x
ENDE FUNKTION

AUSGABE quadrat(5)   # 25
```

### Default-Parameter

```
DEFINIERE gruss(name, laut=falsch):
    WENN laut DANN
        AUSGABE "HALLO " + name + "!!!"
    SONST
        AUSGABE "Hallo " + name
    ENDE WENN
ENDE FUNKTION

gruss("Welt")          # Hallo Welt
gruss("Welt", wahr)    # HALLO Welt!!!
```

### Lambda (AKTION)

```
verdopple = AKTION(x): x * 2
AUSGABE verdopple(21)   # 42
```

### Mehrfach-Zuweisung

```
a, b = 1, 2
a, b = b, a   # Swap
```

---

## 5. Klassen (OOP)

### Klasse definieren

```
KLASSE Tier:
    DEFINIERE ERSTELLE(name, art):
        MEIN.name = name
        MEIN.art = art
    ENDE FUNKTION

    DEFINIERE vorstellen():
        AUSGABE MEIN.name + " ist ein " + MEIN.art
    ENDE FUNKTION
ENDE KLASSE

hund = Tier("Rex", "Hund")
hund.vorstellen()   # Rex ist ein Hund
```

### Vererbung

```
KLASSE Hund(Tier):
    DEFINIERE ERSTELLE(name):
        ELTERN.ERSTELLE(name, "Hund")
    ENDE FUNKTION

    DEFINIERE bellen():
        AUSGABE MEIN.name + " sagt: Wuff!"
    ENDE FUNKTION
ENDE KLASSE
```

---

## 6. Listen und Woerterbuecher

### Listen

```
zahlen = [1, 2, 3, 4, 5]
AUSGABE zahlen[0]       # 1
AUSGABE len(zahlen)     # 5

zahlen.append(6)        # [1, 2, 3, 4, 5, 6]
```

### Woerterbuecher

```
person = {"name": "Max", "alter": 20}
AUSGABE person["name"]   # Max
```

---

## 7. Fehlerbehandlung

```
VERSUCHE
    ergebnis = 10 / 0
FANGE fehler
    AUSGABE "Fehler: " + str(fehler)
ENDE VERSUCHE
```

---

## 8. Module

### Import

```
BENUTZE mathe
BENUTZE mathe ALS m

# zpkg-Pakete
BENUTZE mathe_extra
AUSGABE mathe_extra.fibonacci(10)
```

---

## 9. Eingebaute Funktionen

### Standard

| Funktion | Beschreibung |
|----------|--------------|
| `AUSGABE(x)` | Gibt x auf der Konsole aus |
| `EINGABE_TEXT("Prompt")` | Liest Text vom Benutzer |
| `EINGABE_ZAHL("Prompt")` | Liest eine Zahl vom Benutzer |
| `str(x)` | Konvertiert x zu Text |
| `int(x)` | Konvertiert x zu Ganzzahl |
| `float(x)` | Konvertiert x zu Dezimalzahl |
| `len(x)` | Laenge von String oder Liste |
| `typ(x)` | Typ von x als Text |
| `BEREICH(...)` | Zahlenbereich erzeugen |
| `FORMAT("...", x)` | String-Formatierung mit `{}` |

### Mathematik

| Funktion | Beschreibung |
|----------|--------------|
| `WURZEL(x)` | Quadratwurzel |
| `ABSOLUT(x)` | Absolutwert |
| `RUNDEN(x, n)` | Runden auf n Stellen |
| `BODEN(x)` | Abrunden |
| `DECKE(x)` | Aufrunden |
| `POTENZ(x, y)` | x hoch y |
| `SINUS(x)` | Sinus (Bogenmass) |
| `COSINUS(x)` | Cosinus (Bogenmass) |
| `TANGENS(x)` | Tangens (Bogenmass) |
| `LOGARITHMUS(x)` | Natuerlicher Logarithmus |
| `MINIMUM(a, b)` | Kleinerer Wert |
| `MAXIMUM(a, b)` | Groesserer Wert |
| `SUMME(liste)` | Summe aller Elemente |
| `ZUFALL()` | Zufallszahl 0..1 |
| `ZUFALL_BEREICH(a, b)` | Zufalls-Ganzzahl a..b |
| `PI` | 3.14159... |
| `E` | 2.71828... |

### Text

| Funktion | Beschreibung |
|----------|--------------|
| `GROSSBUCHSTABEN(text)` | Text in Grossbuchstaben |
| `KLEINBUCHSTABEN(text)` | Text in Kleinbuchstaben |
| `ERSETZE(text, alt, neu)` | Ersetzt alt durch neu |
| `TEILE(text, trenner)` | Teilt Text an Trenner |
| `TRIMME(text)` | Entfernt Leerzeichen am Rand |
| `ENTHAELT(text, teil)` | Prueft ob teil in text |
| `LAENGE(x)` | Laenge von String oder Liste |
| `FINDE(text, teil)` | Position von teil in text |
| `BEGINNT_MIT(text, praefix)` | Prueft Anfang |
| `ENDET_MIT(text, suffix)` | Prueft Ende |
| `VERBINDE(liste, trenner)` | Verbindet Liste zu String |

### Listen

| Funktion | Beschreibung |
|----------|--------------|
| `SORTIEREN(liste)` | Sortierte Kopie |
| `FILTERN(liste, fn)` | Filtert Elemente |
| `UMWANDELN(liste, fn)` | Wandelt jedes Element um |
| `UMKEHREN(liste)` | Umgekehrte Kopie |
| `FLACH(liste)` | Verschachtelte Liste flach machen |
| `EINDEUTIG(liste)` | Nur einzigartige Elemente |
| `AUFZAEHLEN(liste)` | (Index, Wert) Paare |
| `ANHAENGEN(liste, elem)` | Neue Liste mit Element |

### Dateien

| Funktion | Beschreibung |
|----------|--------------|
| `LESE_DATEI(pfad)` | Liest Datei als Text |
| `SCHREIBE_DATEI(pfad, inhalt)` | Schreibt Text in Datei |
| `EXISTIERT(pfad)` | Prueft ob Datei existiert |
| `LESE_ZEILEN(pfad)` | Liest Datei als Zeilen-Liste |

---

## 10. Schluesselwort-Tabelle (alle 6 Sprachen)

| Funktion | Deutsch | English | Espanol | Francais | Italiano | Portugues |
|----------|---------|---------|---------|----------|----------|-----------|
| Definiere | `DEFINIERE` | `DEFINE` | `DEFINIR` | `DEFINIR` | `DEFINISCI` | `DEFINIR` |
| Wenn | `WENN` | `IF` | `SI` | `SI` | `SE` | `SE` |
| Dann | `DANN` | `THEN` | `ENTONCES` | `ALORS` | `ALLORA` | `ENTAO` |
| Sonst | `SONST` | `ELSE` | `SINO` | `SINON` | `ALTRIMENTI` | `SENAO` |
| Solange | `SOLANGE` | `WHILE` | `MIENTRAS` | `TANT_QUE` | `MENTRE` | `ENQUANTO` |
| Fuer | `FUER` | `FOR` | `PARA` | `POUR` | `PER` | `PARA` |
| Ausgabe | `AUSGABE` | `PRINT` | `MOSTRAR` | `AFFICHER` | `MOSTRA` | `MOSTRAR` |
| Ergebnis | `ERGEBNIS IST` | `RETURN` | `RESULTADO ES` | `RESULTAT EST` | `RISULTATO E` | `RESULTADO E` |
| Klasse | `KLASSE` | `CLASS` | `CLASE` | `CLASSE` | `CLASSE` | `CLASSE` |
| Wahr | `wahr` | `true` | `verdadero` | `vrai` | `vero` | `verdadeiro` |
| Falsch | `falsch` | `false` | `falso` | `faux` | `falso` | `falso` |
