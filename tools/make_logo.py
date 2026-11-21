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
BOLD = TTFont(sys.argv[3]) if len(sys.argv) > 3 else REGULAR

PURPLE, PURPLE_D, GREEN, GREEN_L, WHITE = "#7347a5", "#4a2a72", "#2f7d46", "#7cbf8c", "#ffffff"


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


DISC_BG = "#4f8f63"

def flower(cx, cy, r):
    """Μεγάλα λευκά/μέντα πέταλα σε πράσινο φόντο, όπως στην κάρτα."""
    k = r / 57.5
    defs = (f'<defs><clipPath id="disc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            '<radialGradient id="bg" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#8cc29b"/><stop offset="1" stop-color="#3f7c53"/></radialGradient>'
            '<radialGradient id="pet" cx="40%" cy="35%" r="85%"><stop offset="0" stop-color="#ffffff"/>'
            '<stop offset=".5" stop-color="#eef6ef"/><stop offset="1" stop-color="#b9d8c0"/></radialGradient>'
            '<radialGradient id="pet2" cx="45%" cy="40%" r="80%"><stop offset="0" stop-color="#f4faf5"/>'
            '<stop offset="1" stop-color="#a5cbb0"/></radialGradient>'
            '<filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation=".7"/></filter></defs>')
    petal = "M0 0 C 4 -22, 30 -36, 52 -22 C 64 -14, 64 6, 54 18 C 44 30, 24 30, 12 22 C 5 16, 1 8, 0 0 Z"
    petals = [(-150, .98, "pet2"), (-70, 1.02, "pet2"), (5, .96, "pet2"), (75, 1.0, "pet2"), (150, .95, "pet2"),
              (-110, .72, "pet"), (-30, .75, "pet"), (40, .7, "pet"), (115, .74, "pet"), (190, .7, "pet")]
    body = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bg)"/>', '<g clip-path="url(#disc)"><g filter="url(#soft)">']
    for rot, sc, g in petals:
        body.append(f'<path transform="translate({cx} {cy}) rotate({rot}) scale({sc*k:.3f})" d="{petal}" '
                    f'fill="url(#{g})" stroke="#c4dfca" stroke-width="{.5/(sc*k):.2f}" opacity=".95"/>')
    body.append('</g></g>')
    return defs + "".join(body)


# Καλλιγραφικό ΝΣ (κεντραρισμένο περίπου στο 100,100). Η αντίθεση χοντρού/λεπτού βγαίνει με «πένα» (στοίβα μετατοπισμένων πινελιών).
SCRIPT = [
    # Ν: αριστερή κεραία από κάτω αριστερά προς τα πάνω
    "M 56 130 C 63 131, 70 124, 74 112 C 78 99, 80 88, 84 78 C 86 72, 91 71, 93 77",
    # διαγώνιος προς τα κάτω
    "M 93 77 C 95 92, 97 110, 100 126",
    # δεξιά κεραία προς τα πάνω, γυρίζει στο Σ
    "M 100 126 C 104 108, 108 90, 113 76 C 115 71, 119 69, 123 70",
    # Σ: πάνω οριζόντια μακριά πινελιά
    "M 116 74 C 128 71, 139 70, 149 65",
    # Σ: διαγώνιος προς τα κάτω αριστερά
    "M 149 65 C 138 78, 125 92, 113 104",
    # Σ: κάτω καμπύλη (κοιλιά) και ουρά προς τα αριστερά
    "M 113 104 C 128 100, 144 108, 141 122 C 138 136, 118 140, 100 135 C 90 132, 84 127, 89 122",
]

def script_monogram(scale=1.0, cx=100, cy=100):
    t = f'transform="translate({cx} {cy}) scale({scale}) translate(-104 -100)"'
    nib = [(i / 8 * 2.4, -i / 8 * 1.6) for i in range(9)]  # πένα 34°
    def stack(col, w):
        return "".join(f'<g transform="translate({dx:.2f} {dy:.2f})"><path d="{" ".join(SCRIPT)}"/></g>' for dx, dy in nib)
    out = f'<g {t} fill="none" stroke-linecap="round" stroke-linejoin="round">'
    out += f'<g stroke="#3c7650" stroke-width="3.1">{stack("", 0)}</g>'
    out += f'<g stroke="#ffffff" stroke-width="1.9">{stack("", 0)}</g>'
    return out + '</g>'


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
        f'<circle cx="{cx}" cy="{cy}" r="99" fill="{PURPLE_D}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="97.6" fill="{WHITE}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="95.4" fill="{PURPLE}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="59" fill="{WHITE}"/>',
        flower(cx, cy, 54),
        script_monogram(.94, cx, cy),
    ]
    if with_text:
        parts.append(f'<path d="{arc_text(BOLD, "Γραφείο Τελετών", 17.5, cx, cy, 70.5, top=True, track=0.5)}" fill="#efe6f8" stroke="#3d2160" stroke-width=".7" paint-order="stroke"/>')
        parts.append(f'<path d="{arc_text(ITALIC, "Σοφογιάννης", 18.5, cx, cy, 83, top=False, track=0.3)}" fill="#efe6f8" stroke="#3d2160" stroke-width=".7" paint-order="stroke"/>')
        parts.append(f'<circle cx="{cx-78.5}" cy="{cy}" r="2" fill="#efe6f8"/><circle cx="{cx+78.5}" cy="{cy}" r="2" fill="#efe6f8"/>')
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
