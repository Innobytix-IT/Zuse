# FILE: maler_web.py
# Browser-basierte Maler/Pintor-Engine für den Zuse Web-Playground.
# Gleiche API wie die Maler/Pintor-Klasse in bibliothek/*.zuse,
# aber nutzt HTML5 Canvas via Pyodide JS-Bridge statt turtle/tkinter.

import math
import js


class MalerWeb:
    """Turtle-Grafik im Browser via HTML5 Canvas."""

    def __init__(self):
        self._x = 0.0
        self._y = 0.0
        self._winkel = 0.0  # 0 = rechts, 90 = oben (turtle-Konvention)
        self._stift_unten = True
        self._farbe = 'white'
        self._dicke = 1
        self._linien = []  # [(x1,y1,x2,y2,farbe,dicke), ...]
        self._kreise = []  # [(cx,cy,radius,farbe,dicke), ...]

        # Canvas initialisieren
        js.window._zuseCanvas.init("Escola de Arte Zuse", 600, 500, "white")

    # ─── Bewegung ────────────────────────────────────────────

    def mover(self, schritte):
        """vorwärts / forward / mover"""
        rad = math.radians(self._winkel)
        nx = self._x + schritte * math.cos(rad)
        ny = self._y - schritte * math.sin(rad)  # Canvas Y ist invertiert
        if self._stift_unten:
            self._linien.append((self._x, self._y, nx, ny, self._farbe, self._dicke))
        self._x = nx
        self._y = ny
        self._render()

    # Aliase für alle Sprachen
    vorwaerts = mover
    forward = mover

    def voltar(self, schritte):
        """rückwärts / backward / voltar"""
        self.mover(-schritte)

    rueckwaerts = voltar
    backward = voltar

    def virar_esquerda(self, grad):
        """links drehen / left / virar_esquerda"""
        self._winkel += grad

    links = virar_esquerda
    left = virar_esquerda
    gauche = virar_esquerda
    sinistra = virar_esquerda

    def virar_direita(self, grad):
        """rechts drehen / right / virar_direita"""
        self._winkel -= grad

    rechts = virar_direita
    right = virar_direita
    droite = virar_direita
    destra = virar_direita

    # ─── Stift ───────────────────────────────────────────────

    def caneta_sobe(self):
        """Stift heben / pen up"""
        self._stift_unten = False

    stift_hoch = caneta_sobe
    pen_up = caneta_sobe
    lever_stylo = caneta_sobe
    penna_su = caneta_sobe

    def caneta_desce(self):
        """Stift senken / pen down"""
        self._stift_unten = True

    stift_runter = caneta_desce
    pen_down = caneta_desce
    baisser_stylo = caneta_desce
    penna_giu = caneta_desce

    # ─── Farbe & Dicke ──────────────────────────────────────

    def cor(self, farbe):
        """Farbe setzen"""
        _FARB_MAP = {
            # Portugiesisch
            'vermelho': 'red', 'azul': 'blue', 'verde': 'green',
            'amarelo': 'yellow', 'preto': 'black', 'branco': 'white',
            'laranja': 'orange', 'roxo': 'purple', 'rosa': 'pink',
            # Deutsch
            'rot': 'red', 'blau': 'blue', 'gruen': '#22c55e',
            'gelb': 'yellow', 'schwarz': 'black', 'weiss': 'white',
            # Spanisch
            'rojo': 'red', 'negro': 'black', 'blanco': 'white',
            # Französisch
            'rouge': 'red', 'noir': 'black', 'blanc': 'white',
            'jaune': 'yellow', 'vert': 'green',
            # Italienisch
            'rosso': 'red', 'nero': 'black', 'bianco': 'white',
            'giallo': 'yellow',
        }
        self._farbe = _FARB_MAP.get(str(farbe).strip(), str(farbe).strip())

    farbe = cor
    color = cor
    couleur = cor
    colore = cor

    def espessura(self, dicke):
        """Stiftdicke setzen"""
        self._dicke = max(1, int(dicke))

    dicke = espessura
    thickness = espessura
    epaisseur = espessura
    spessore = espessura

    # ─── Formen ──────────────────────────────────────────────

    def circulo(self, radius):
        """Kreis zeichnen"""
        # Turtle zeichnet Kreis links vom aktuellen Punkt
        cx = self._x
        cy = self._y - radius  # Mittelpunkt ist radius nach oben
        if self._stift_unten:
            self._kreise.append((cx, cy, abs(radius), self._farbe, self._dicke))
            self._render()

    kreis = circulo
    circle = circulo
    cercle = circulo
    cerchio = circulo

    # ─── Fertig ──────────────────────────────────────────────

    def pronto(self):
        """Zeichnung abschließen (Turtle mainloop-Äquivalent)."""
        self._render()

    fertig = pronto
    done = pronto
    termine = pronto
    fatto = pronto

    # ─── Rendering ───────────────────────────────────────────

    def _canvas_coords(self, x, y):
        """Konvertiert Turtle-Koordinaten (Mitte=0,0) zu Canvas-Koordinaten."""
        cx = 300 + x   # Canvas-Mitte bei 300 (600/2)
        cy = 250 + y   # Canvas-Mitte bei 250 (500/2)
        return cx, cy

    def _render(self):
        """Zeichnet alles neu auf dem Canvas."""
        js.window._zuseCanvas.clearAll()

        # Linien
        for (x1, y1, x2, y2, farbe, dicke) in self._linien:
            cx1, cy1 = self._canvas_coords(x1, y1)
            cx2, cy2 = self._canvas_coords(x2, y2)
            js.window._zuseCanvas.drawLine(cx1, cy1, cx2, cy2, farbe, dicke)

        # Kreise
        for (cx, cy, r, farbe, dicke) in self._kreise:
            ccx, ccy = self._canvas_coords(cx, cy)
            js.window._zuseCanvas.drawCircle(ccx, ccy, r, farbe)

        # Turtle-Cursor (kleines Dreieck)
        tx, ty = self._canvas_coords(self._x, self._y)
        rad = math.radians(self._winkel)
        size = 8
        p1x = tx + size * math.cos(rad)
        p1y = ty - size * math.sin(rad)
        p2x = tx + size * math.cos(rad + math.radians(140))
        p2y = ty - size * math.sin(rad + math.radians(140))
        p3x = tx + size * math.cos(rad - math.radians(140))
        p3y = ty - size * math.sin(rad - math.radians(140))

        from pyodide.ffi import to_js
        pts = to_js([p1x, p1y, p2x, p2y, p3x, p3y])
        js.window._zuseCanvas.drawPolygon(pts, self._farbe)

        js.window._zuseCanvas.render()
