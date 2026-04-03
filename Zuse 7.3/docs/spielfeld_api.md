# Spielfeld-API-Referenz

Die Spielfeld-Bibliothek ermöglicht Spiele und grafische Programme in Zuse.
Gleicher Code funktioniert im Desktop-Studio (tkinter) und im Web-Playground (HTML5 Canvas).

---

## Spielfeld erstellen

```zuse
spiel = Spielfeld("Mein Spiel", 800, 600, "schwarz")
```

| Parameter | Typ    | Standard      | Beschreibung |
|-----------|--------|---------------|--------------|
| titel     | Text   | "Zuse Spiel"  | Fenstertitel |
| breite    | Zahl   | 600           | Breite in Pixeln |
| hoehe     | Zahl   | 400           | Höhe in Pixeln |
| farbe     | Text   | "black"       | Hintergrundfarbe |

---

## Sprites

### neuer_sprite(x, y, breite, hoehe, farbe)
Erstellt ein Rechteck auf dem Spielfeld.

```zuse
spieler = spiel.neuer_sprite(100, 200, 30, 30, "gruen")
```

### Sprite-Methoden

| Methode | Beschreibung |
|---------|-------------|
| `bewege(dx, dy)` | Bewegt um dx/dy Pixel |
| `setze_position(x, y)` | Setzt auf absolute Position |
| `kollidiert_mit(anderer)` | Prüft Kollision (AABB) |
| `am_rand()` | Prüft ob am Spielfeldrand |
| `verstecke()` | Versteckt den Sprite |
| `zeige()` | Zeigt den Sprite |
| `aendere_farbe(farbe)` | Ändert die Farbe |
| `entferne()` | Entfernt vom Spielfeld |

### Sprite-Eigenschaften

| Eigenschaft | Beschreibung |
|-------------|-------------|
| `x`, `y` | Position (links oben) |
| `breite`, `hoehe` | Größe |
| `farbe` | Aktuelle Farbe |
| `sichtbar` | Ob sichtbar (wahr/falsch) |

---

## Text-Sprites

### neuer_text(x, y, text, farbe, groesse)
Erstellt einen Text auf dem Spielfeld.

```zuse
punkte = spiel.neuer_text(400, 20, "Punkte: 0", "weiss", 20)
```

### TextSprite-Methoden

| Methode | Beschreibung |
|---------|-------------|
| `setze_text(text)` | Ändert den angezeigten Text |
| `setze_position(x, y)` | Setzt auf neue Position |
| `entferne()` | Entfernt vom Spielfeld |

---

## Tastatur

### taste_gedrueckt(taste)
Prüft ob eine Taste gerade gedrückt ist. Gibt `wahr` oder `falsch` zurück.

```zuse
WENN spiel.taste_gedrueckt("Links") DANN
    spieler.bewege(-5, 0)
ENDE WENN
```

| Taste | Wert |
|-------|------|
| Pfeiltaste links | `"Links"` |
| Pfeiltaste rechts | `"Rechts"` |
| Pfeiltaste hoch | `"Hoch"` |
| Pfeiltaste runter | `"Runter"` |
| Leertaste | `"Leertaste"` |
| Enter | `"Eingabe"` |
| Escape | `"Escape"` |
| Buchstabe (z.B. a) | `"a"` |

### bei_taste(taste, aktion)
Registriert eine Funktion die bei Tastendruck aufgerufen wird.

```zuse
DEFINIERE schiessen():
    AUSGABE "Pew!"
ENDE FUNKTION

spiel.bei_taste("Leertaste", schiessen)
```

---

## Maus

### maus_position()
Gibt `[x, y]` der aktuellen Mausposition zurück.

```zuse
pos = spiel.maus_position()
AUSGABE FORMAT("Maus bei {}, {}", pos[0], pos[1])
```

### maus_gedrueckt()
Prüft ob die linke Maustaste gedrückt ist.

```zuse
WENN spiel.maus_gedrueckt() DANN
    AUSGABE "Klick!"
ENDE WENN
```

---

## Zeichenfunktionen

Statische Zeichnungen (werden nicht als Sprites verwaltet).

| Funktion | Beschreibung |
|----------|-------------|
| `zeichne_rechteck(x, y, breite, hoehe, farbe)` | Rechteck |
| `zeichne_kreis(x, y, radius, farbe)` | Kreis |
| `zeichne_linie(x1, y1, x2, y2, farbe, dicke)` | Linie |
| `zeichne_text(x, y, text, farbe, groesse)` | Text |
| `zeichne_polygon(punkte, farbe)` | Polygon (Liste von [x,y]) |

```zuse
spiel.zeichne_rechteck(10, 10, 50, 50, "rot")
spiel.zeichne_kreis(200, 200, 30, "blau")
spiel.zeichne_linie(0, 0, 400, 300, "weiss", 2)
spiel.zeichne_polygon([[100,100], [150,50], [200,100]], "gelb")
```

---

## Spielschleife

### spielschleife(funktion, fps)
Startet die Spielschleife. Die übergebene Funktion wird `fps`-mal pro Sekunde aufgerufen.

```zuse
DEFINIERE spielschritt():
    # Logik hier
    WENN spiel.taste_gedrueckt("Rechts") DANN
        spieler.bewege(3, 0)
    ENDE WENN
ENDE FUNKTION

spiel.spielschleife(spielschritt, 30)
```

### stoppe()
Stoppt die Spielschleife.

### loesche_alles()
Löscht alle Zeichnungen vom Canvas (nützlich für Neuzeichnung pro Frame).

---

## Verwaltung

| Methode | Beschreibung |
|---------|-------------|
| `aktualisiere()` | Erzwingt Neuzeichnung |
| `starte()` | Startet die Hauptschleife |
| `schliessen()` | Schliesst das Fenster |
| `setze_titel(titel)` | Ändert den Fenstertitel |

---

## Farben

Alle Funktionen akzeptieren Farbnamen in mehreren Sprachen:

| Deutsch | Englisch | CSS |
|---------|----------|-----|
| schwarz | black | black |
| weiss | white | white |
| rot | red | red |
| gruen | green | #22c55e |
| blau | blue | blue |
| gelb | yellow | yellow |
| grau | gray | gray |
| orange | orange | orange |
| lila | purple | purple |
| rosa | pink | pink |
| braun | brown | brown |
| cyan | cyan | cyan |
| gold | gold | gold |
| dunkelgruen | — | #166534 |
| hellgruen | — | #86efac |
| dunkelblau | — | darkblue |
| hellblau | — | lightblue |

Auch spanische (negro, rojo, verde), französische (noir, rouge, vert), italienische und portugiesische Farbnamen werden unterstützt.

---

## Vollständiges Beispiel

```zuse
spiel = Spielfeld("Fang-Spiel", 600, 400, "schwarz")

spieler = spiel.neuer_sprite(280, 350, 40, 40, "gruen")
ziel = spiel.neuer_sprite(280, 50, 20, 20, "rot")
punkte_text = spiel.neuer_text(300, 20, "Punkte: 0", "weiss", 18)

punkte = 0

DEFINIERE spielschritt():
    GLOBAL punkte
    WENN spiel.taste_gedrueckt("Links") DANN
        spieler.bewege(-5, 0)
    ENDE WENN
    WENN spiel.taste_gedrueckt("Rechts") DANN
        spieler.bewege(5, 0)
    ENDE WENN

    WENN spieler.kollidiert_mit(ziel) DANN
        punkte = punkte + 1
        punkte_text.setze_text(FORMAT("Punkte: {}", punkte))
        ziel.setze_position(ZUFALL_BEREICH(20, 560), ZUFALL_BEREICH(20, 200))
    ENDE WENN
ENDE FUNKTION

spiel.spielschleife(spielschritt, 30)
```
