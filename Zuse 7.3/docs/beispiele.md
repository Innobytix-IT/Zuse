# Zuse Beispielprogramme

Eine Sammlung von Programmen zum Lernen und Ausprobieren.

---

## Anfaenger

### Hallo Welt

```
AUSGABE "Hallo Welt!"
```

### Taschenrechner

```
AUSGABE "=== Taschenrechner ==="
a = EINGABE_ZAHL("Erste Zahl: ")
b = EINGABE_ZAHL("Zweite Zahl: ")

AUSGABE "Summe:      " + str(a + b)
AUSGABE "Differenz:  " + str(a - b)
AUSGABE "Produkt:    " + str(a * b)
WENN b != 0 DANN
    AUSGABE "Quotient:   " + str(a / b)
SONST
    AUSGABE "Division durch 0 nicht moeglich!"
ENDE WENN
```

### Zahlenraten

```
geheim = ZUFALL_BEREICH(1, 100)
versuche = 0

AUSGABE "Ich denke an eine Zahl zwischen 1 und 100..."

SOLANGE wahr MACHE
    tipp = EINGABE_ZAHL("Dein Tipp: ")
    versuche = versuche + 1

    WENN tipp == geheim DANN
        AUSGABE "Richtig! Du hast " + str(versuche) + " Versuche gebraucht."
        ABBRUCH
    SONST WENN tipp < geheim DANN
        AUSGABE "Zu niedrig!"
    SONST
        AUSGABE "Zu hoch!"
    ENDE WENN
ENDE SCHLEIFE
```

---

## Fortgeschritten

### FizzBuzz

```
SCHLEIFE FÜR i IN BEREICH(1, 101) MACHE
    WENN i % 15 == 0 DANN
        AUSGABE "FizzBuzz"
    SONST WENN i % 3 == 0 DANN
        AUSGABE "Fizz"
    SONST WENN i % 5 == 0 DANN
        AUSGABE "Buzz"
    SONST
        AUSGABE i
    ENDE WENN
ENDE SCHLEIFE
```

### Fibonacci

```
DEFINIERE fibonacci(n):
    WENN n <= 1 DANN
        ERGEBNIS IST n
    ENDE WENN
    ERGEBNIS IST fibonacci(n - 1) + fibonacci(n - 2)
ENDE FUNKTION

SCHLEIFE FÜR i IN BEREICH(15) MACHE
    AUSGABE str(i) + ": " + str(fibonacci(i))
ENDE SCHLEIFE
```

### Bubble Sort

```
DEFINIERE bubble_sort(liste):
    n = len(liste)
    SCHLEIFE FÜR i IN BEREICH(n) MACHE
        SCHLEIFE FÜR j IN BEREICH(0, n - i - 1) MACHE
            WENN liste[j] > liste[j + 1] DANN
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
            ENDE WENN
        ENDE SCHLEIFE
    ENDE SCHLEIFE
    ERGEBNIS IST liste
ENDE FUNKTION

zahlen = [64, 34, 25, 12, 22, 11, 90]
AUSGABE "Vorher:  " + str(zahlen)
AUSGABE "Nachher: " + str(bubble_sort(zahlen))
```

### Listen-Verarbeitung mit AKTION

```
schueler = [
    {"name": "Max", "note": 2},
    {"name": "Anna", "note": 1},
    {"name": "Tim", "note": 4},
    {"name": "Lisa", "note": 3},
    {"name": "Jan", "note": 5}
]

# Nur bestandene Schueler (Note <= 4)
bestanden = FILTERN(schueler, AKTION(s): s["note"] <= 4)

# Namen extrahieren
namen = UMWANDELN(bestanden, AKTION(s): s["name"])

AUSGABE "Bestanden: " + VERBINDE(namen, ", ")
```

---

## Klassen und OOP

### Bankkonto

```
KLASSE Konto:
    DEFINIERE ERSTELLE(inhaber, kontostand=0):
        MEIN.inhaber = inhaber
        MEIN.kontostand = kontostand
    ENDE FUNKTION

    DEFINIERE einzahlen(betrag):
        WENN betrag > 0 DANN
            MEIN.kontostand = MEIN.kontostand + betrag
            AUSGABE str(betrag) + " EUR eingezahlt."
        ENDE WENN
    ENDE FUNKTION

    DEFINIERE abheben(betrag):
        WENN betrag > MEIN.kontostand DANN
            AUSGABE "Nicht genug Guthaben!"
        SONST
            MEIN.kontostand = MEIN.kontostand - betrag
            AUSGABE str(betrag) + " EUR abgehoben."
        ENDE WENN
    ENDE FUNKTION

    DEFINIERE stand():
        AUSGABE MEIN.inhaber + ": " + str(MEIN.kontostand) + " EUR"
    ENDE FUNKTION
ENDE KLASSE

konto = Konto("Max", 100)
konto.stand()           # Max: 100 EUR
konto.einzahlen(50)     # 50 EUR eingezahlt.
konto.abheben(30)       # 30 EUR abgehoben.
konto.stand()           # Max: 120 EUR
```

---

## Grafik-Programme

### Der Maler — Haus mit Sonne

Ein Turtle-Grafik-Programm, das ein Haus mit Dach und Sonne zeichnet.

```
pablo = Maler()

# Haus (Quadrat)
pablo.farbe("blau")
pablo.dicke(5)
SCHLEIFE FÜR i IN [1, 2, 3, 4] MACHE
    pablo.gehe(150)
    pablo.drehe_rechts(90)
ENDE SCHLEIFE

# Dach (Dreieck)
pablo.farbe("rot")
pablo.drehe_links(45)
pablo.gehe(106)
pablo.drehe_rechts(90)
pablo.gehe(106)

# Sonne
pablo.stift_hoch()
pablo.drehe_rechts(135)
pablo.gehe(200)
pablo.drehe_links(90)
pablo.gehe(100)
pablo.stift_runter()
pablo.farbe("gelb")
pablo.dicke(10)
pablo.kreis(40)

pablo.fertig()
```

### ZuseSnake

Ein vollstaendiges Snake-Spiel mit der Spielfeld-Engine. Verwendet Klassen, Schleifen, Tasteneingaben und Timer.

Datei: `Zuse Programme/ZuseSnake.zuse`

---

## Mehrsprachige Beispiele

Dasselbe Programm in allen 6 Sprachen:

### Deutsch
```
DEFINIERE fakultaet(n):
    WENN n <= 1 DANN
        ERGEBNIS IST 1
    ENDE WENN
    ERGEBNIS IST n * fakultaet(n - 1)
ENDE FUNKTION
AUSGABE fakultaet(10)
```

### English
```
DEFINE factorial(n):
    IF n <= 1 THEN
        RETURN 1
    END IF
    RETURN n * factorial(n - 1)
END FUNCTION
PRINT factorial(10)
```

### Espanol
```
DEFINIR factorial(n):
    SI n <= 1 ENTONCES
        RESULTADO ES 1
    FIN SI
    RESULTADO ES n * factorial(n - 1)
FIN FUNCION
MOSTRAR factorial(10)
```

### Francais
```
DEFINIR factorielle(n):
    SI n <= 1 ALORS
        RESULTAT EST 1
    FIN SI
    RESULTAT EST n * factorielle(n - 1)
FIN FONCTION
AFFICHER factorielle(10)
```

### Italiano
```
DEFINISCI fattoriale(n):
    SE n <= 1 ALLORA
        RISULTATO E 1
    FINE SE
    RISULTATO E n * fattoriale(n - 1)
FINE FUNZIONE
MOSTRA fattoriale(10)
```

### Portugues
```
DEFINIR fatorial(n):
    SE n <= 1 ENTAO
        RESULTADO E 1
    FIM SE
    RESULTADO E n * fatorial(n - 1)
FIM FUNCAO
MOSTRAR fatorial(10)
```

---

## Weitere Ideen

- **Passwort-Generator**: Zufaellige Zeichen kombinieren
- **Todo-Liste**: Dateien zum Speichern nutzen
- **Vokabel-Trainer**: Woerterbuch + Zufallsauswahl
- **Tic-Tac-Toe**: 2-Spieler auf der Konsole
- **Grafik-Muster**: Spiralen und Muster mit dem Maler
