#!/usr/bin/env python3
"""Παράγει το έμβλημα (images/logo-emblem.svg) και το favicon.svg ως καθαρά paths.

Χρειάζεται fontTools και τα TTF της Bona Nova:
    python tools/make_logo.py <BonaNova-Italic.ttf> <BonaNova-Regular.ttf>
Το έμβλημα αναπαράγει τη σφραγίδα της επαγγελματικής κάρτας: μωβ δακτύλιος με
«Γραφείο Τελετών» πάνω και «Σοφογιάννης» κάτω, πράσινος δίσκος με φύλλα και μονόγραμμα ΝΣ.
"""
import math
import os
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITALIC, REGULAR = TTFont(sys.argv[1]), TTFont(sys.argv[2])

PURPLE, PURPLE_D, GREEN, GREEN_L, WHITE = "#5e3a8f", "#4e2a78", "#2f7d46", "#7cbf8c", "#ffffff"


def glyph_d(font, ch, size, tx, ty, rot=0.0, anchor=0.5):
    """Path ενός χαρακτήρα με baseline στο (tx,ty), περιστροφή rot (μοίρες)."""
    gs = font.getGlyphSet()
    name = font.getBestCmap()[ord(ch)]
    adv = font["hmtx"][name][0]
    k = size / font["head"].unitsPerEm
    r = math.radians(rot)
    c, s = math.cos(r), math.sin(r)
    ox = -adv * anchor
    # x' = R * (k*x + ox*k), y' = R * (-k*y)  → affine (a,b,c,d,e,f)
    a, b = c * k, s * k
    cc, d = s * k, -c * k
    e = tx + c * ox * k
    f = ty + s * ox * k
    pen = SVGPathPen(gs)
    gs[name].draw(TransformPen(pen, (a, b, cc, d, e, f)))
    return pen.getCommands(), adv * k


def advance(font, ch, size):
    name = font.getBestCmap()[ord(ch)]
    return font["hmtx"][name][0] * size / font["head"].unitsPerEm


def text_line(font, text, size, x, y, track=0.0):
    """Οριζόντιο κείμενο κεντραρισμένο στο x."""
    w = sum(advance(font, ch, size) for ch in text) + track * (len(text) - 1)
    cur = x - w / 2
    out = []
    for ch in text:
        adv = advance(font, ch, size)
        if ch != " ":
            out.append(glyph_d(font, ch, size, cur, y, 0, 0)[0])
        cur += adv + track
    return "".join(out)


def arc_text(font, text, size, cx, cy, R, top=True, track=0.0):
    widths = [advance(font, ch, size) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    pos = -total / 2
    out = []
    for ch, w in zip(text, widths):
        mid = pos + w / 2
        a = mid / R
        if top:
            px, py, rot = cx + R * math.sin(a), cy - R * math.cos(a), math.degrees(a)
        else:
            px, py, rot = cx + R * math.sin(a), cy + R * math.cos(a), -math.degrees(a)
        if ch != " ":
            out.append(glyph_d(font, ch, size, px, py, rot)[0])
        pos += w + track
    return "".join(out)


def leaves(cx, cy, n=6, r=44, fill=GREEN_L, op=0.55):
    """Διακοσμητικά φύλλα/πέταλα στον πράσινο δίσκο (όπως στο λογότυπο της κάρτας)."""
    out = []
    for i in range(n):
        ang = 360 / n * i + 15
        out.append(
            f'<path transform="translate({cx} {cy}) rotate({ang:.1f})" '
            f'd="M0 -6 C {r*0.32:.1f} -{r*0.38:.1f}, {r*0.22:.1f} -{r*0.9:.1f}, 0 -{r:.1f} '
            f'C -{r*0.22:.1f} -{r*0.9:.1f}, -{r*0.32:.1f} -{r*0.38:.1f}, 0 -6 Z" fill="{fill}" opacity="{op}"/>'
            f'<path transform="translate({cx} {cy}) rotate({ang:.1f})" d="M0 -8 L0 -{r*0.9:.1f}" '
            f'stroke="{GREEN}" stroke-width="0.9" opacity="{op}" fill="none"/>')
    return "".join(out)


DISC_BG = "#4d574b"

def flower(cx, cy, r):
    """Λευκό λουλούδι (γαρδένια) σε σκούρο φόντο, όπως στο πραγματικό λογότυπο."""
    defs = (f'<defs><clipPath id="disc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            '<radialGradient id="pet" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#ffffff"/>'
            '<stop offset=".55" stop-color="#e4e7e0"/><stop offset="1" stop-color="#a9b1a5"/></radialGradient>'
            '<radialGradient id="pet2" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="#f3f4ef"/>'
            '<stop offset="1" stop-color="#8f988b"/></radialGradient></defs>')
    petal = "M0 0 C 6 -20, 30 -32, 50 -18 C 60 -10, 60 6, 52 16 C 44 26, 26 28, 14 20 C 6 14, 2 8, 0 0 Z"
    petals = [  # (rotation, scale, gradient) — εξωτερικά σκούρα, εσωτερικά φωτεινά
        (-160, 1.0, "pet2"), (-85, .96, "pet2"), (-15, 1.04, "pet2"), (60, .98, "pet2"), (130, 1.0, "pet2"),
        (-120, .82, "pet"), (-45, .85, "pet"), (25, .8, "pet"), (100, .84, "pet"), (175, .8, "pet"),
        (-70, .45, "pet"), (40, .42, "pet"), (150, .44, "pet"),
    ]
    body = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{DISC_BG}"/>', f'<g clip-path="url(#disc)">']
    k = r / 57.5
    for rot, sc, g in petals:
        body.append(f'<path transform="translate({cx} {cy}) rotate({rot}) scale({sc*k:.3f})" d="{petal}" '
                    f'fill="url(#{g})" stroke="#6f786b" stroke-width="{.9/(sc*k):.2f}" opacity=".96"/>')
    body.append('</g>')
    return defs + "".join(body)


SCRIPT_N = ("M 56 126 C 64 134, 73 127, 76 114 C 79 98, 80 86, 86 76 C 90 70, 94 73, 95 81 "
            "L 101 117 C 103 125, 108 124, 110 116 L 117 80 C 118 72, 115 68, 111 71")
SCRIPT_S = ("M 113 79 C 124 72, 134 78, 145 71 C 137 83, 128 92, 120 100 C 135 97, 147 108, 142 122 "
            "C 137 136, 116 140, 98 136 C 84 133, 72 135, 63 141")

def script_monogram(scale=1.0, cx=100, cy=100):
    t = f'transform="translate({cx} {cy}) scale({scale}) skewX(-8) translate(-100 -104)"'
    out = ""
    for w, col in ((7, "#2b3029"), (3.4, "#ffffff")):
        out += (f'<g {t} fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">'
                f'<path d="{SCRIPT_N}"/><path d="{SCRIPT_S}"/></g>')
    return out


def monogram(cx, cy, size):
    # Ν και Σ ελαφρώς επικαλυπτόμενα, όπως το καλλιγραφικό ΝΣ της κάρτας
    n_adv = advance(ITALIC, "Ν", size)
    s_adv = advance(ITALIC, "Σ", size)
    overlap = size * 0.16
    w = n_adv + s_adv - overlap
    x0 = cx - w / 2
    base = cy + size * 0.34
    d = glyph_d(ITALIC, "Ν", size, x0, base - size * 0.06, 0, 0)[0]
    d += glyph_d(ITALIC, "Σ", size, x0 + n_adv - overlap, base + size * 0.06, 0, 0)[0]
    return d


def emblem(with_text=True):
    cx = cy = 100
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="98" fill="{PURPLE}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="93" fill="none" stroke="{WHITE}" stroke-width="1.6" opacity=".9"/>',
        f'<circle cx="{cx}" cy="{cy}" r="61" fill="{WHITE}"/>',
        flower(cx, cy, 57.5),
        script_monogram(1.0, cx, cy),
    ]
    if with_text:
        parts.append(f'<path d="{arc_text(REGULAR, "Γραφείο Τελετών", 16.5, cx, cy, 70.5, top=True, track=0.6)}" fill="#e6dbf3"/>')
        parts.append(f'<path d="{arc_text(ITALIC, "Σοφογιάννης", 16.5, cx, cy, 82, top=False, track=0.3)}" fill="#e6dbf3"/>')
        parts.append(f'<circle cx="{cx-78}" cy="{cy}" r="2.2" fill="{WHITE}"/><circle cx="{cx+78}" cy="{cy}" r="2.2" fill="{WHITE}"/>')
    return parts


def write(name, body, vb="0 0 200 200"):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Γραφείο Τελετών Σοφογιάννης">{body}</svg>\n'
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name, len(svg), "bytes")


write("images/logo-emblem.svg", "".join(emblem(True)))
# favicon: χωρίς κυκλικό κείμενο, μεγαλύτερο μονόγραμμα για ευκρίνεια σε μικρά μεγέθη
fav = [
    f'<circle cx="100" cy="100" r="98" fill="{PURPLE}"/>',
    f'<circle cx="100" cy="100" r="80" fill="{WHITE}"/>',
    flower(100, 100, 74),
    script_monogram(1.3),
]
write("favicon.svg", "".join(fav))
# Καλλιγραφική υπογραφή «Σοφογιάννης» ως paths (για og-image και όπου δεν φορτώνει webfont)
wm = text_line(ITALIC, "Σοφογιάννης", 100, 300, 105, 0.5)
write("images/wordmark.svg", f'<path d="{wm}" fill="{GREEN}"/>', "0 0 600 140")
