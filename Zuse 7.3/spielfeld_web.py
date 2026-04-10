# FILE: spielfeld_web.py
# Browser-basierte Spielfeld-Engine fuer den Zuse Web-Playground.
# Gleiche API wie spielfeld.py, aber nutzt HTML5 Canvas via Pyodide JS-Bridge.

from pyodide.ffi import create_proxy  # noqa: F401
import js


class Sprite:
    """Ein Sprite auf dem Spielfeld (Canvas-Version)."""
    _next_id = 1

    def __init__(self, spielfeld, x, y, breite, hoehe, farbe="blue"):
        self.spielfeld = spielfeld
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.farbe = farbe
        self.sichtbar = True
        self.id = Sprite._next_id
        Sprite._next_id += 1
        js.window._zuseCanvas.addSprite(self.id, x, y, breite, hoehe, farbe)

    def bewege(self, dx, dy):
        """Bewegt den Sprite um dx, dy Pixel."""
        self.x += dx
        self.y += dy
        js.window._zuseCanvas.moveSprite(self.id, self.x, self.y)

    def setze_position(self, x, y):
        """Setzt den Sprite auf eine absolute Position."""
        self.x = x
        self.y = y
        js.window._zuseCanvas.moveSprite(self.id, self.x, self.y)

    def kollidiert_mit(self, anderer):
        """Prueft Kollision mit einem anderen Sprite (AABB)."""
        return (self.x < anderer.x + anderer.breite and
                self.x + self.breite > anderer.x and
                self.y < anderer.y + anderer.hoehe and
                self.y + self.hoehe > anderer.y)

    def am_rand(self):
        """Prueft ob der Sprite den Rand des Spielfelds beruehrt."""
        sf = self.spielfeld
        return (self.x <= 0 or self.y <= 0 or
                self.x + self.breite >= sf.breite or
                self.y + self.hoehe >= sf.hoehe)

    def verstecke(self):
        """Versteckt den Sprite."""
        self.sichtbar = False
        js.window._zuseCanvas.hideSprite(self.id)

    def zeige(self):
        """Zeigt den Sprite."""
        self.sichtbar = True
        js.window._zuseCanvas.showSprite(self.id)

    def aendere_farbe(self, farbe):
        """Aendert die Farbe des Sprites."""
        self.farbe = farbe
        js.window._zuseCanvas.colorSprite(self.id, farbe)

    def entferne(self):
        """Entfernt den Sprite vom Spielfeld."""
        self.sichtbar = False
        js.window._zuseCanvas.removeSprite(self.id)


class TextSprite:
    """Ein Text-Sprite auf dem Spielfeld."""
    _next_id = 100000

    def __init__(self, spielfeld, x, y, text, farbe="white", groesse=16):
        self.spielfeld = spielfeld
        self.x = x
        self.y = y
        self.text = text
        self.farbe = farbe
        self.groesse = groesse
        self.id = TextSprite._next_id
        TextSprite._next_id += 1
        js.window._zuseCanvas.addText(self.id, x, y, text, farbe, groesse)

    def setze_text(self, text):
        """Aendert den angezeigten Text."""
        self.text = text
        js.window._zuseCanvas.updateText(self.id, text)

    def setze_position(self, x, y):
        """Setzt den Text auf eine absolute Position."""
        self.x = x
        self.y = y
        js.window._zuseCanvas.moveText(self.id, x, y)

    def entferne(self):
        """Entfernt den Text vom Spielfeld."""
        js.window._zuseCanvas.removeText(self.id)


class Spielfeld:
    """Das Spielfeld — HTML5 Canvas fuer den Web-Playground."""

    # Referenz auf den Zuse-Interpreter (wird vom Playground gesetzt)
    _interpreter = None

    @classmethod
    def _set_interpreter(cls, interp):
        cls._interpreter = interp

    def __init__(self, titel="Zuse Spiel", breite=600, hoehe=400, farbe="black"):
        self.breite = int(breite)
        self.hoehe = int(hoehe)
        self.farbe = farbe
        self._tasten = {}
        self._tick_proxy = None
        Sprite._next_id = 1
        TextSprite._next_id = 100000
        js.window._zuseCanvas.init(str(titel), self.breite, self.hoehe, str(farbe))

    def taste_gedrueckt(self, taste):
        """Prueft ob eine Taste gerade gedrueckt ist."""
        key_map = {
            "Links": "ArrowLeft", "Rechts": "ArrowRight",
            "Hoch": "ArrowUp", "Runter": "ArrowDown",
            "Leertaste": " ", "Eingabe": "Enter",
            "Escape": "Escape",
            # Englische Aliase
            "Left": "ArrowLeft", "Right": "ArrowRight",
            "Up": "ArrowUp", "Down": "ArrowDown",
            "Space": " ",
        }
        mapped = key_map.get(str(taste), str(taste))
        return js.window._zuseCanvas.isKeyPressed(mapped)

    def bei_taste(self, taste, aktion):
        """Registriert eine Aktion fuer eine Taste."""
        key_map = {
            "Links": "ArrowLeft", "Rechts": "ArrowRight",
            "Hoch": "ArrowUp", "Runter": "ArrowDown",
            "Leertaste": " ", "Eingabe": "Enter",
            "Escape": "Escape",
            "Left": "ArrowLeft", "Right": "ArrowRight",
            "Up": "ArrowUp", "Down": "ArrowDown",
            "Space": " ",
        }
        self._tasten[key_map.get(str(taste), str(taste))] = aktion

    def neuer_sprite(self, x, y, breite, hoehe, farbe="blue"):
        """Erstellt einen neuen rechteckigen Sprite."""
        return Sprite(self, float(x), float(y), float(breite), float(hoehe), str(farbe))

    def neuer_text(self, x, y, text, farbe="white", groesse=16):
        """Erstellt einen neuen Text-Sprite."""
        return TextSprite(self, float(x), float(y), str(text), str(farbe), int(groesse))

    def spielschleife(self, funktion, fps=10):
        """Startet die Spielschleife. Ruft 'funktion' fps-mal pro Sekunde auf.
        Im Browser wird JavaScript setInterval genutzt, sodass zwischen Frames
        Tastatur-Events verarbeitet werden koennen."""
        interp = Spielfeld._interpreter
        if not interp:
            return

        interval_ms = max(16, int(1000 / fps))

        def _tick():
            try:
                interp._call_function(funktion, [], interp.global_env)
            except Exception as e:
                js.window._zuseCanvas.stopGameLoop()
                js.console.error(f"Spielschleife Fehler: {e}")

        self._tick_proxy = create_proxy(_tick)
        js.window._zuseCanvas.startGameLoop(self._tick_proxy, interval_ms)

    def stoppe(self):
        """Stoppt die Spielschleife."""
        js.window._zuseCanvas.stopGameLoop()
        if self._tick_proxy is not None:
            self._tick_proxy.destroy()
            self._tick_proxy = None

    def nach_zeit(self, ms, funktion):
        """Ruft eine Funktion nach ms Millisekunden auf."""
        interp = Spielfeld._interpreter
        if not interp:
            return

        def _timeout():
            try:
                interp._call_function(funktion, [], interp.global_env)
            except Exception as e:
                js.console.error(f"nach_zeit Fehler: {e}")

        proxy = create_proxy(_timeout)
        js.window.setTimeout(proxy, int(ms))

    def aktualisiere(self):
        """Aktualisiert die Anzeige (Canvas wird automatisch neu gezeichnet)."""
        js.window._zuseCanvas.render()

    def starte(self):
        """Startet die Hauptschleife (im Browser: kein Blocking-Loop)."""
        js.window._zuseCanvas.render()

    def schliessen(self):
        """Schliesst das Spielfeld."""
        js.window._zuseCanvas.destroy()

    def setze_titel(self, titel):
        """Aendert den Titel."""
        js.window._zuseCanvas.setTitle(str(titel))

    def loesche_alles(self):
        """Loescht alle Objekte vom Canvas."""
        js.window._zuseCanvas.clearAll()

    def zeichne_rechteck(self, x, y, breite, hoehe, farbe="white"):
        """Zeichnet ein Rechteck (kein Sprite, nur Grafik)."""
        js.window._zuseCanvas.drawRect(
            float(x), float(y), float(breite), float(hoehe), str(farbe)
        )

    def zeichne_kreis(self, x, y, radius, farbe="white"):
        """Zeichnet einen Kreis."""
        js.window._zuseCanvas.drawCircle(
            float(x), float(y), float(radius), str(farbe)
        )

    def zeichne_linie(self, x1, y1, x2, y2, farbe="white", dicke=1):
        """Zeichnet eine Linie."""
        js.window._zuseCanvas.drawLine(
            float(x1), float(y1), float(x2), float(y2), str(farbe), float(dicke)
        )

    def zeichne_text(self, x, y, text, farbe="white", groesse=16):
        """Zeichnet Text (statisch, kein Sprite)."""
        js.window._zuseCanvas.drawText(
            float(x), float(y), str(text), str(farbe), int(groesse)
        )

    def zeichne_polygon(self, punkte, farbe="white"):
        """Zeichnet ein Polygon. punkte ist eine Liste von [x, y] Paaren."""
        from pyodide.ffi import to_js
        flat = []
        for p in punkte:
            flat.extend([float(p[0]), float(p[1])])
        js.window._zuseCanvas.drawPolygon(to_js(flat), str(farbe))

    def maus_position(self):
        """Gibt [x, y] der aktuellen Mausposition zurück."""
        x = js.window._zuseCanvas.getMouseX()
        y = js.window._zuseCanvas.getMouseY()
        return [x, y]

    def maus_gedrueckt(self):
        """Prüft ob die linke Maustaste gedrückt ist."""
        return js.window._zuseCanvas.isMousePressed()
