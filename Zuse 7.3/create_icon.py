"""
Zuse Icon Generator
Erstellt zuse_icon.ico in mehreren Größen (16, 32, 48, 64, 128, 256).
Benötigt: pip install pillow
"""
from PIL import Image, ImageDraw, ImageFont
import os

SIZES   = [16, 32, 48, 64, 128, 256]
OUTPUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zuse_icon.ico")

# ── Farbpalette (passend zum Zuse Studio Theme) ──────────────────────────────
BG       = (18, 18, 34, 255)     # #12122 – tiefes Dunkelblau
CARD     = (30, 30, 46, 255)     # #1e1e2e
ACCENT_A = (79, 195, 247)        # #4FC3F7  hellblau
ACCENT_B = (124, 77, 255)        # #7C4DFF  violett
WHITE    = (255, 255, 255, 255)
SHADOW   = (0, 0, 0, 120)

# ── Hilfsfunktionen ───────────────────────────────────────────────────────────

def rounded_rect(draw, x0, y0, x1, y1, r, fill):
    """Gefülltes Rechteck mit abgerundeten Ecken."""
    draw.rectangle([x0 + r, y0,     x1 - r, y1    ], fill=fill)
    draw.rectangle([x0,     y0 + r, x1,     y1 - r], fill=fill)
    draw.ellipse  ([x0,           y0,           x0 + 2*r, y0 + 2*r], fill=fill)
    draw.ellipse  ([x1 - 2*r,    y0,           x1,       y0 + 2*r], fill=fill)
    draw.ellipse  ([x0,           y1 - 2*r,    x0 + 2*r, y1      ], fill=fill)
    draw.ellipse  ([x1 - 2*r,    y1 - 2*r,    x1,       y1      ], fill=fill)


def gradient_bar(draw, x0, x1, y, h, color_a, color_b):
    """Horizontaler Farbverlauf-Balken."""
    width = x1 - x0
    if width <= 0:
        return
    for i in range(width):
        t = i / width
        r = int(color_a[0] * (1 - t) + color_b[0] * t)
        g = int(color_a[1] * (1 - t) + color_b[1] * t)
        b = int(color_a[2] * (1 - t) + color_b[2] * t)
        draw.line([(x0 + i, y), (x0 + i, y + h - 1)], fill=(r, g, b, 255))


def load_font(size):
    """Lädt die beste verfügbare fette Systemschrift."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ── Icon-Rendering ─────────────────────────────────────────────────────────────

def make_icon(size):
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = max(1, size // 20)
    r   = max(3, size // 7)

    # ── Hintergrund ──────────────────────────────────────────────────────────
    # Äußerer Schatten (nur bei ≥ 32px sichtbar)
    if size >= 32:
        rounded_rect(draw, pad + 2, pad + 2, size - pad + 2, size - pad + 2, r, (0, 0, 0, 60))

    # Haupt-Karte
    rounded_rect(draw, pad, pad, size - pad, size - pad, r, CARD)

    # Subtile innere Vignette (dunkler Rand)
    if size >= 64:
        for offset, alpha in [(0, 40), (1, 20)]:
            vignette_color = (10, 10, 20, alpha)
            rounded_rect(draw, pad + offset, pad + offset,
                         size - pad - offset, size - pad - offset,
                         max(1, r - offset), vignette_color)

    # ── "Z" Buchstabe ────────────────────────────────────────────────────────
    font_size = max(8, int(size * 0.62))
    font = load_font(font_size)

    bbox = draw.textbbox((0, 0), "Z", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) // 2 - bbox[0]
    ty = (size - th) // 2 - bbox[1] - max(1, size // 20)

    # Schatten
    if size >= 32:
        draw.text((tx + max(1, size // 64), ty + max(1, size // 64)),
                  "Z", font=font, fill=SHADOW)

    # Haupt-Text weiß
    draw.text((tx, ty), "Z", font=font, fill=WHITE)

    # ── Gradient-Akzentbalken (nur ≥ 48px) ───────────────────────────────────
    if size >= 48:
        bar_h  = max(3, size // 20)
        bar_y  = size - pad - bar_h - max(2, size // 24)
        bar_x0 = pad + r
        bar_x1 = size - pad - r
        gradient_bar(draw, bar_x0, bar_x1, bar_y, bar_h, ACCENT_A, ACCENT_B)

    # ── Kleiner Punkt oben links (Branding-Detail, nur ≥ 64px) ───────────────
    if size >= 64:
        dot = max(2, size // 40)
        dx  = pad + r + dot
        dy  = pad + r + dot
        draw.ellipse([dx, dy, dx + dot * 2, dy + dot * 2], fill=ACCENT_A)

    return img


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Erstelle Zuse Icon ...")

    # Bevorzuge das originale Logo-PNG wenn vorhanden
    logo_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Zuse_Logo_Neu.png")
    if os.path.exists(logo_png):
        print(f"  Verwende Logo: {logo_png}")
        img = Image.open(logo_png).convert("RGBA")
        w, h = img.size
        side = min(w, h)
        left, top = (w - side) // 2, (h - side) // 2
        square = img.crop((left, top, left + side, top + side))
        bg = Image.new("RGBA", (side, side), (30, 30, 46, 255))
        bg.alpha_composite(square)
        master = bg.convert("RGB")
    else:
        print("  Logo-PNG nicht gefunden, erstelle programmatisches Icon ...")
        master = make_icon(256)

    master.save(OUTPUT, format="ICO", sizes=[(s, s) for s in SIZES])
    print(f"  -> {OUTPUT}")

    preview = OUTPUT.replace(".ico", "_preview.png")
    master.resize((256, 256), Image.LANCZOS).save(preview, format="PNG")
    print(f"  -> {preview}")
    print("Fertig!")
