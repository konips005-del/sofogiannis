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

PURPLE, PURPLE_D, GREEN, GREEN_L, WHITE = "#6b3f9e", "#4e2a78", "#2f7d46", "#7cbf8c", "#ffffff"


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
        f'<circle cx="{cx}" cy="{cy}" r="92.5" fill="none" stroke="{WHITE}" stroke-width="1.6" opacity=".9"/>',
        f'<circle cx="{cx}" cy="{cy}" r="61" fill="{WHITE}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="57.5" fill="{GREEN}"/>',
        leaves(cx, cy),
        f'<path d="{monogram(cx, cy, 64)}" fill="{WHITE}"/>',
    ]
    if with_text:
        parts.append(f'<path d="{arc_text(REGULAR, "Γραφείο Τελετών", 16.5, cx, cy, 70.5, top=True, track=0.6)}" fill="{WHITE}"/>')
        parts.append(f'<path d="{arc_text(ITALIC, "Σοφογιάννης", 16.5, cx, cy, 82, top=False, track=0.3)}" fill="{WHITE}"/>')
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
    f'<circle cx="100" cy="100" r="74" fill="{GREEN}"/>',
    f'<path d="{monogram(100, 100, 92)}" fill="{WHITE}"/>',
]
write("favicon.svg", "".join(fav))
# Καλλιγραφική υπογραφή «Σοφογιάννης» ως paths (για og-image και όπου δεν φορτώνει webfont)
wm = text_line(ITALIC, "Σοφογιάννης", 100, 300, 105, 0.5)
write("images/wordmark.svg", f'<path d="{wm}" fill="{GREEN}"/>', "0 0 600 140")
