"""CAPTÉ logo system generator.

Builds every logo version as outlined SVG (no font needed), from Syne ExtraBold
and DM Sans Medium glyph outlines. Run: python3 build_logo.py
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
OUT = ROOT / "logo" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

# ---- Brand colours -------------------------------------------------------
INK = "#15151B"      # Encre
CREAM = "#F4F1EC"    # Crème
REC = "#FF4D2E"      # Rouge REC (signature)
BLACK = "#000000"
WHITE = "#FFFFFF"

SYNE = TTFont(FONTS / "Syne-ExtraBold.ttf")
DMS = TTFont(FONTS / "DMSans-Medium.ttf")


def glyph_d(font, ch, x, y_base, scale=1.0):
    """SVG path for one character, baseline at y_base, left edge at x (SVG coords)."""
    gs = font.getGlyphSet()
    name = font.getBestCmap()[ord(ch)]
    pen = SVGPathPen(gs)
    # flip y: svg_y = y_base - font_y * scale
    tpen = TransformPen(pen, (scale, 0, 0, -scale, x, y_base))
    gs[name].draw(tpen)
    return pen.getCommands(), font["hmtx"][name][0] * scale


def text_paths(font, text, x, y_base, scale=1.0, tracking=0, kern=None):
    kern = kern or {}
    ds, cx = [], x
    for i, ch in enumerate(text):
        if ch == " ":
            cx += font["hmtx"][font.getBestCmap()[32]][0] * scale + tracking
            continue
        d, adv = glyph_d(font, ch, cx, y_base, scale)
        ds.append(d)
        pair = text[i:i + 2]
        cx += adv + tracking + kern.get(pair, 0) * scale
    return " ".join(ds), cx - tracking


# ---- Wordmark geometry (font units, 1000 upm) ---------------------------
CAP = 650                     # cap height
ACCENT_TOP = 842              # top of the É accent
BASE = ACCENT_TOP             # baseline in svg coords (accent top sits at y=0)
TRACK = -40                   # tight tracking
KERN = {"CA": -20, "AP": -10, "PT": -35, "TÉ": -45}
DOT_D = 275                   # REC dot diameter
DOT_GAP = 75                  # space between É and dot


def wordmark_parts():
    d, end_x = text_paths(SYNE, "CAPTÉ", 0, BASE, 1.0, TRACK, KERN)
    # trim right side bearing of É (advance 1140, ink ends 1080)
    ink_end = end_x - (1140 - 1080)
    cx = ink_end + DOT_GAP + DOT_D / 2
    cy = (BASE - CAP) + DOT_D / 2          # dot top aligned to cap height
    width = cx + DOT_D / 2
    return d, (cx, cy, DOT_D / 2), width


def svg(w, h, body, bg=None, pad=0):
    vb = f"{-pad} {-pad} {w + 2 * pad:.1f} {h + 2 * pad:.1f}"
    rect = f'<rect x="{-pad}" y="{-pad}" width="{w + 2*pad:.1f}" height="{h + 2*pad:.1f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'width="{w + 2*pad:.0f}" height="{h + 2*pad:.0f}">{rect}{body}</svg>\n')


def wordmark_svg(fg, dot, bg=None, pad=120):
    d, (cx, cy, r), w = wordmark_parts()
    x0 = 60  # C left side bearing
    body = (f'<g transform="translate({-x0},0)"><path d="{d}" fill="{fg}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{dot}"/></g>')
    return svg(w - x0, BASE, body, bg, pad), w - x0


def stacked_svg(fg, dot, sub, bg=None, pad=120):
    """Wordmark + 'LUNETTES CAMÉRA' descriptor, justified to the wordmark width."""
    d, (cx, cy, r), w = wordmark_parts()
    x0 = 60
    ww = w - x0
    sub_scale = 0.42
    txt = "LUNETTES CAMÉRA"
    _, raw = text_paths(DMS, txt, 0, 0, sub_scale, 0)
    n_gaps = len(txt) - 1
    tracking = (ww - raw) / n_gaps
    y_sub = BASE + 400
    sd, _ = text_paths(DMS, txt, 0, y_sub, sub_scale, tracking)
    body = (f'<g transform="translate({-x0},0)"><path d="{d}" fill="{fg}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{dot}"/></g>'
            f'<path d="{sd}" fill="{sub}"/>')
    return svg(ww, y_sub + 10, body, bg, pad)


def monogram_parts(size=1000):
    """The C with the REC dot in its counter — the lens that records."""
    gs = SYNE.getGlyphSet()
    # C ink box: x 60..1256, y -20..660 -> centre it in a square
    cw, ch_ = 1256 - 60, 660 + 20
    s = size * 0.74 / cw
    x = (size - cw * s) / 2 - 60 * s
    yb = (size + ch_ * s) / 2 - 20 * s
    d, _ = glyph_d(SYNE, "C", x, yb, s)
    # optical centre of the counter, nudged right toward the opening
    ccx = x + (60 + (1256 - 60) * 0.47) * s
    ccy = yb - (660 - 20) / 2 * s - 20 * s + 10 * s
    r = DOT_D / 2 * s * 1.05
    return d, (ccx, ccy, r)


def icon_svg(fg, dot, bg, radius=0.22, size=1000, circle=False):
    d, (cx, cy, r) = monogram_parts(size)
    if circle:
        shape = f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>'
    elif bg:
        shape = f'<rect width="{size}" height="{size}" rx="{size*radius:.0f}" fill="{bg}"/>'
    else:
        shape = ""
    body = f'{shape}<path d="{d}" fill="{fg}"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{dot}"/>'
    return svg(size, size, body)


def horizontal_svg(fg, dot, bg=None, pad=120):
    """Monogram mark + wordmark side by side."""
    md, (mcx, mcy, mr) = monogram_parts(1000)
    d, (cx, cy, r), w = wordmark_parts()
    x0 = 60
    mark_h = BASE          # scale mark to wordmark height region
    ms = (CAP * 1.75) / 1000
    mark_y = BASE - CAP / 2 - 1000 * ms / 2
    gap = 150
    mark_w = 1000 * ms
    body = (f'<g transform="translate(0,{mark_y:.1f}) scale({ms:.4f})">'
            f'<rect width="1000" height="1000" rx="220" fill="{fg}"/>'
            f'<path d="{md}" fill="{bg or ("#FFFFFF" if fg != "#FFFFFF" else "#000000")}"/>'
            f'<circle cx="{mcx:.1f}" cy="{mcy:.1f}" r="{mr:.1f}" fill="{dot}"/></g>'
            f'<g transform="translate({mark_w + gap - x0:.1f},0)"><path d="{d}" fill="{fg}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{dot}"/></g>')
    return svg(mark_w + gap + w - x0, BASE, body, None, pad)


def main():
    files = {}
    # Primary wordmark
    files["capte-wordmark-ink.svg"] = wordmark_svg(INK, REC)[0]
    files["capte-wordmark-cream.svg"] = wordmark_svg(CREAM, REC)[0]
    files["capte-wordmark-black.svg"] = wordmark_svg(BLACK, BLACK)[0]
    files["capte-wordmark-white.svg"] = wordmark_svg(WHITE, WHITE)[0]
    files["capte-wordmark-on-ink.svg"] = wordmark_svg(CREAM, REC, bg=INK)[0]
    files["capte-wordmark-on-cream.svg"] = wordmark_svg(INK, REC, bg=CREAM)[0]
    # Stacked with descriptor
    files["capte-stacked-ink.svg"] = stacked_svg(INK, REC, "#6B6773")
    files["capte-stacked-cream.svg"] = stacked_svg(CREAM, REC, "#A9A5B0")
    files["capte-stacked-black.svg"] = stacked_svg(BLACK, BLACK, BLACK)
    files["capte-stacked-white.svg"] = stacked_svg(WHITE, WHITE, WHITE)
    # Monogram / icon
    files["capte-icon-ink.svg"] = icon_svg(CREAM, REC, INK)
    files["capte-icon-cream.svg"] = icon_svg(INK, REC, CREAM)
    files["capte-icon-rec.svg"] = icon_svg(CREAM, INK, REC)
    files["capte-icon-round-ink.svg"] = icon_svg(CREAM, REC, INK, circle=True)
    files["capte-monogram-ink.svg"] = icon_svg(INK, REC, None)
    files["capte-monogram-cream.svg"] = icon_svg(CREAM, REC, None)
    files["capte-monogram-black.svg"] = icon_svg(BLACK, BLACK, None)
    files["capte-monogram-white.svg"] = icon_svg(WHITE, WHITE, None)
    # Horizontal lockup
    files["capte-horizontal-ink.svg"] = horizontal_svg(INK, REC, CREAM)
    files["capte-horizontal-cream.svg"] = horizontal_svg(CREAM, REC, INK)
    for name, s in files.items():
        (OUT / name).write_text(s)
    print(f"wrote {len(files)} SVGs to {OUT}")


if __name__ == "__main__":
    main()
