# FILE: spielfeld.py
# Einfache Sprite-/Kollisions-Engine für Zuse (Phase 4.5)
# Basiert auf tkinter Canvas.

import tkinter as tk

# Farb-Übersetzung: Mehrsprachige Farbnamen → tkinter/CSS-Farben
_FARB_MAP = {
    # Deutsch
    'schwarz': 'black', 'weiss': 'white', 'rot': 'red',
    'gruen': '#22c55e', 'blau': 'blue', 'gelb': 'yellow',
    'grau': 'gray', 'orange': 'orange', 'lila': 'purple',
    'rosa': 'pink', 'braun': 'brown', 'cyan': 'cyan',
    'magenta': 'magenta', 'gold': 'gold',
    'dunkelgruen': '#166534', 'hellgruen': '#86efac',
    'dunkelblau': 'darkblue', 'hellblau': 'lightblue',
    'dunkelrot': 'darkred', 'hellrot': '#fca5a5',
    'dunkelgrau': '#444444', 'hellgrau': '#cccccc',
    # Spanisch
    'negro': 'black', 'blanco': 'white', 'rojo': 'red',
    'verde': '#22c55e', 'azul': 'blue', 'amarillo': 'yellow',
    # Französisch
    'noir': 'black', 'blanc': 'white', 'rouge': 'red',
    'vert': '#22c55e', 'jaune': 'yellow',
    # Italienisch
    'nero': 'black', 'bianco': 'white', 'rosso': 'red',
    'giallo': 'yellow',
    # Portugiesisch
    'preto': 'black', 'branco': 'white', 'vermelho': 'red',
    'amarelo': 'yellow',
}

def _farbe(name):
    """Übersetzt mehrsprachige Farbnamen in tkinter-kompatible Farben."""
    return _FARB_MAP.get(str(name), str(name))


class Sprite:
    """Ein Sprite auf dem Spielfeld."""
    def __init__(self, spielfeld, x, y, breite, hoehe, farbe="blue"):
        self.spielfeld = spielfeld
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.farbe = farbe
        self.id = spielfeld.canvas.create_rectangle(
            x, y, x + breite, y + hoehe, fill=_farbe(farbe), outline=""
        )
        self.sichtbar = True

    def bewege(self, dx, dy):
        """Bewegt den Sprite um dx, dy Pixel."""
        self.x += dx
        self.y += dy
        self.spielfeld.canvas.move(self.id, dx, dy)

    def setze_position(self, x, y):
        """Setzt den Sprite auf eine absolute Position."""
        dx = x - self.x
        dy = y - self.y
        self.bewege(dx, dy)

    def kollidiert_mit(self, anderer):
        """Prüft Kollision mit einem anderen Sprite (AABB)."""
        return (self.x < anderer.x + anderer.breite and
                self.x + self.breite > anderer.x and
                self.y < anderer.y + anderer.hoehe and
                self.y + self.hoehe > anderer.y)

    def am_rand(self):
        """Prüft ob der Sprite den Rand des Spielfelds berührt."""
        sf = self.spielfeld
        return (self.x <= 0 or self.y <= 0 or
                self.x + self.breite >= sf.breite or
                self.y + self.hoehe >= sf.hoehe)

    def verstecke(self):
        """Versteckt den Sprite."""
        self.spielfeld.canvas.itemconfigure(self.id, state='hidden')
        self.sichtbar = False

    def zeige(self):
        """Zeigt den Sprite."""
        self.spielfeld.canvas.itemconfigure(self.id, state='normal')
        self.sichtbar = True

    def aendere_farbe(self, farbe):
        """Ändert die Farbe des Sprites."""
        self.farbe = farbe
        self.spielfeld.canvas.itemconfigure(self.id, fill=_farbe(farbe))

    def entferne(self):
        """Entfernt den Sprite vom Spielfeld."""
        self.spielfeld.canvas.delete(self.id)


class TextSprite:
    """Ein Text-Sprite auf dem Spielfeld."""
    def __init__(self, spielfeld, x, y, text, farbe="white", groesse=16):
        self.spielfeld = spielfeld
        self.x = x
        self.y = y
        self.text = text
        self.id = spielfeld.canvas.create_text(
            x, y, text=text, fill=_farbe(farbe), font=("Arial", groesse)
        )

    def setze_text(self, text):
        """Ändert den angezeigten Text."""
        self.text = text
        self.spielfeld.canvas.itemconfigure(self.id, text=text)

    def setze_position(self, x, y):
        """Setzt den Text auf eine absolute Position."""
        self.x = x
        self.y = y
        self.spielfeld.canvas.coords(self.id, x, y)

    def entferne(self):
        """Entfernt den Text vom Spielfeld."""
        self.spielfeld.canvas.delete(self.id)


class Spielfeld:
    """Das Spielfeld — ein Fenster mit Canvas für Spiele."""
    def __init__(self, titel="Zuse Spiel", breite=600, hoehe=400, farbe="black"):
        self.breite = int(breite)
        self.hoehe = int(hoehe)
        self.farbe = farbe
        self._tasten = {}
        self._gedrueckte_tasten = set()
        self._laeuft = True

        self.root = tk.Tk()
        self.root.title(str(titel))
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(
            self.root, width=self.breite, height=self.hoehe, bg=_farbe(farbe)
        )
        self.canvas.pack()

        # Tastenereignisse global tracken
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)

    def _on_key_press(self, event):
        self._gedrueckte_tasten.add(event.keysym)
        callback = self._tasten.get(event.keysym)
        if callback:
            callback()

    def _on_key_release(self, event):
        self._gedrueckte_tasten.discard(event.keysym)

    def taste_gedrueckt(self, taste):
        """Prüft ob eine Taste gerade gedrückt ist."""
        key_map = {
            "Links": "Left", "Rechts": "Right",
            "Hoch": "Up", "Runter": "Down",
            "Leertaste": "space", "Eingabe": "Return",
            "Escape": "Escape",
        }
        return key_map.get(str(taste), str(taste)) in self._gedrueckte_tasten

    def bei_taste(self, taste, aktion):
        """Registriert eine Aktion für eine Taste."""
        key_map = {
            "Links": "Left", "Rechts": "Right",
            "Hoch": "Up", "Runter": "Down",
            "Leertaste": "space", "Eingabe": "Return",
            "Escape": "Escape",
        }
        self._tasten[key_map.get(str(taste), str(taste))] = aktion

    def neuer_sprite(self, x, y, breite, hoehe, farbe="blue"):
        """Erstellt einen neuen rechteckigen Sprite."""
        return Sprite(self, float(x), float(y), float(breite), float(hoehe), str(farbe))

    def neuer_text(self, x, y, text, farbe="white", groesse=16):
        """Erstellt einen neuen Text-Sprite."""
        return TextSprite(self, float(x), float(y), str(text), str(farbe), int(groesse))

    def nach_zeit(self, ms, funktion):
        """Ruft eine Funktion nach ms Millisekunden auf."""
        self.root.after(int(ms), funktion)

    def aktualisiere(self):
        """Aktualisiert die Anzeige."""
        self.root.update()

    def starte(self):
        """Startet die Hauptschleife."""
        self.root.mainloop()

    def spielschleife(self, funktion, fps=10):
        """Startet die Spielschleife: ruft funktion fps-mal pro Sekunde auf."""
        interval = max(16, int(1000 / fps))
        def tick():
            if not self._laeuft:
                return
            try:
                funktion()
                self.root.after(interval, tick)
            except Exception as e:
                self._laeuft = False
                print(f"Spielschleife Fehler: {e}")
                self.root.title(f"FEHLER: {e}")
        self.root.after(interval, tick)
        self.root.mainloop()

    def stoppe(self):
        """Stoppt die Spielschleife."""
        self._laeuft = False

    def schliessen(self):
        """Schliesst das Spielfeld."""
        self.root.destroy()

    def setze_titel(self, titel):
        """Ändert den Fenstertitel."""
        self.root.title(str(titel))

    def loesche_alles(self):
        """Löscht alle Objekte vom Canvas."""
        self.canvas.delete("all")

    def zeichne_rechteck(self, x, y, breite, hoehe, farbe="white"):
        """Zeichnet ein Rechteck (kein Sprite, nur Grafik)."""
        return self.canvas.create_rectangle(
            x, y, x + breite, y + hoehe, fill=_farbe(farbe), outline=""
        )

    def zeichne_kreis(self, x, y, radius, farbe="white"):
        """Zeichnet einen Kreis."""
        return self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=_farbe(farbe), outline=""
        )

    def zeichne_linie(self, x1, y1, x2, y2, farbe="white", dicke=1):
        """Zeichnet eine Linie."""
        return self.canvas.create_line(
            x1, y1, x2, y2, fill=_farbe(farbe), width=dicke
        )

    def zeichne_text(self, x, y, text, farbe="white", groesse=16):
        """Zeichnet Text (statisch, kein Sprite)."""
        return self.canvas.create_text(
            x, y, text=str(text), fill=_farbe(farbe), font=("Arial", int(groesse))
        )

    def zeichne_polygon(self, punkte, farbe="white"):
        """Zeichnet ein Polygon. punkte ist eine Liste von [x, y] Paaren."""
        flat = []
        for p in punkte:
            flat.extend([p[0], p[1]])
        return self.canvas.create_polygon(*flat, fill=_farbe(farbe), outline="")

    # ─── Maus-Events ───────────────────────────────────────────────────

    def _init_maus(self):
        """Initialisiert Maus-Tracking (lazy, nur wenn gebraucht)."""
        if not hasattr(self, '_maus_x'):
            self._maus_x = 0
            self._maus_y = 0
            self._maus_klick = False
            self.canvas.bind("<Motion>", self._on_maus_bewegt)
            self.canvas.bind("<Button-1>", self._on_maus_klick)
            self.canvas.bind("<ButtonRelease-1>", self._on_maus_los)

    def _on_maus_bewegt(self, event):
        self._maus_x = event.x
        self._maus_y = event.y

    def _on_maus_klick(self, event):
        self._maus_x = event.x
        self._maus_y = event.y
        self._maus_klick = True

    def _on_maus_los(self, event):
        self._maus_klick = False

    def maus_position(self):
        """Gibt [x, y] der aktuellen Mausposition zurück."""
        self._init_maus()
        return [self._maus_x, self._maus_y]

    def maus_gedrueckt(self):
        """Prüft ob die linke Maustaste gedrückt ist."""
        self._init_maus()
        return self._maus_klick
