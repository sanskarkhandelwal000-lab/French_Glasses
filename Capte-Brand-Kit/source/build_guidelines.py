"""CAPTÉ brand guidelines — A4 landscape PDF, rendered with headless Chrome."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L = ROOT / "logo" / "svg"
IC = ROOT / "icons"
SOC = ROOT / "social"
END = ROOT / "endcards"
F = ROOT / "fonts"
TRIAL = ROOT.parent / "SkiGoggles_Trial"
OUT = ROOT / "guidelines"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

INK, CREAM, REC, DEEP, GRAPH, STONE = "#15151B", "#F4F1EC", "#FF4D2E", "#C8321A", "#2A2830", "#8A8590"
PAPER = "#FBF9F5"


def u(p):
    return Path(p).resolve().as_uri()


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cmyk(h):
    r, g, b = (c / 255 for c in rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c, m, y = ((1 - x - k) / (1 - k) for x in (r, g, b))
    return tuple(round(v * 100) for v in (c, m, y, k))


def lum(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


PALETTE = [
    ("Encre", "Ink", INK, "Primary dark — backgrounds, text, logo"),
    ("Crème", "Cream", CREAM, "Primary light — backgrounds, logo on dark"),
    ("Rouge REC", "REC red", REC, "Signature — the dot, buttons on dark, highlights"),
    ("Rouge profond", "Deep red", DEEP, "Red text & buttons on light backgrounds"),
    ("Graphite", "Graphite", GRAPH, "Body text on light backgrounds"),
    ("Galet", "Stone", STONE, "Secondary text, captions, lines"),
]
LINES = [
    ("Capté Glisse", "Masques de ski caméra", "Glacier", "#8EC5E8"),
    ("Capté Soleil", "Lunettes de soleil connectées", "Ambre", "#FFB23E"),
    ("Capté Clair", "Lunettes connectées verres clairs", "Brume", "#CFD6DE"),
]

CSS = f"""
@font-face{{font-family:'Syne';src:url('{u(F/'Syne-ExtraBold.ttf')}');font-weight:800}}
@font-face{{font-family:'DM Sans';src:url('{u(F/'DMSans-Regular.ttf')}');font-weight:400}}
@font-face{{font-family:'DM Sans';src:url('{u(F/'DMSans-Medium.ttf')}');font-weight:500}}
@font-face{{font-family:'DM Sans';src:url('{u(F/'DMSans-Bold.ttf')}');font-weight:700}}
@page{{size:297mm 210mm;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'DM Sans',Arial,sans-serif;color:{GRAPH}}}
.pg{{width:297mm;height:210mm;padding:15mm 17mm 12mm;position:relative;overflow:hidden;background:{PAPER};page-break-after:always;display:flex;flex-direction:column}}
.pg.dk{{background:{INK};color:{CREAM}}}
.top{{display:flex;justify-content:space-between;align-items:center;font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:{STONE};margin-bottom:9mm}}
.top img{{height:13px}}
.num{{font-family:'Syne';font-size:11px;color:{REC};letter-spacing:1px;margin-bottom:4px}}
h1{{font-family:'Syne';font-weight:800;font-size:40px;line-height:1.02;letter-spacing:-.5px;color:{INK};text-transform:uppercase}}
.dk h1{{color:{CREAM}}}
h2{{font-size:17px;font-weight:700;color:{INK};margin-bottom:6px}}
.dk h2{{color:{CREAM}}}
p,li{{font-size:11.5px;line-height:1.6}}
.lead{{font-size:15px;line-height:1.55;color:{GRAPH};max-width:150mm}}
.dk .lead{{color:#C9C6CF}}
.muted{{color:{STONE}}}
.row{{display:flex;gap:9mm}}
.col{{flex:1;display:flex;flex-direction:column;gap:5mm}}
.card{{background:#fff;border:1px solid #E6E0D6;border-radius:10px;padding:6mm}}
.dk .card{{background:#1D1D25;border-color:#2E2E38}}
.lbl{{font-size:9px;letter-spacing:2px;text-transform:uppercase;font-weight:700;color:{DEEP};margin-bottom:5px}}
.dk .lbl{{color:{REC}}}
.foot{{position:absolute;left:17mm;right:17mm;bottom:8mm;display:flex;justify-content:space-between;font-size:8.5px;color:{STONE};letter-spacing:1px}}
.spacer{{flex:1}}
ul{{padding-left:14px}}
.chk li::marker{{color:{REC}}}
.x li::marker{{color:{STONE};content:'×  '}}
"""


def top(section, dark=False):
    logo = L / ("capte-wordmark-cream.svg" if dark else "capte-wordmark-ink.svg")
    return f'<div class="top"><img src="{u(logo)}"><span>{section}</span></div>'


def foot(n):
    return f'<div class="foot"><span>CAPTÉ · Brand Guidelines · v1.0 · Octobre 2026</span><span>{n:02d}</span></div>'


def page(body, n, section, dark=False):
    return f'<div class="pg {"dk" if dark else ""}">{top(section, dark)}{body}{foot(n)}</div>'


def build():
    pages = []
    # 1 — Cover
    pages.append(f'''<div class="pg dk" style="justify-content:space-between">
<div style="position:absolute;right:-60mm;top:-40mm;width:170mm;height:170mm;border-radius:50%;background:radial-gradient(circle,rgba(255,77,46,.33) 0%,rgba(255,77,46,0) 68%)"></div>
<p style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:{STONE}">Brand Guidelines · Charte de marque</p>
<div><img src="{u(L/'capte-stacked-cream.svg')}" style="width:175mm"></div>
<div style="display:flex;justify-content:space-between;align-items:end">
<p style="font-size:26px;font-weight:500;color:{CREAM}">Tout est capté.</p>
<p style="font-size:10px;color:{STONE};text-align:right;line-height:1.7">Version 1.0 · Octobre 2026<br>Designed by The Fifth Kind</p></div></div>''')

    # 2 — Essence
    vals = [("Vrai", "Honest", "Real footage, real features, real prices. No fake promises."),
            ("Libre", "Free", "Hands-free. Live the moment instead of holding a phone."),
            ("Respectueux", "Respectful", "We film our adventures and our friends — never strangers."),
            ("Proche", "Close", "A French brand you can reach, that answers in French.")]
    vc = [f'<div class="card" style="flex:1"><p class="lbl">{en}</p><h2 style="font-family:Syne;font-size:20px;text-transform:uppercase">{fr}</h2><p>{t}</p></div>' for fr, en, t in vals]
    pages.append(page(f'''<p class="num">01</p><h1>L'essence de la marque</h1>
<div class="row" style="margin-top:8mm;align-items:stretch">
<div class="col" style="flex:1.1"><div class="card" style="background:{INK};border:none;color:{CREAM}"><p class="lbl" style="color:{REC}">Brand promise · Signature</p><p style="font-family:Syne;font-size:34px;line-height:1.05;text-transform:uppercase;color:{CREAM}">Tout est capté.</p><p style="color:#C9C6CF;margin-top:3mm">Everything, captured. Live your moment — your glasses keep it.</p></div>
<div class="card"><p class="lbl">Mission</p><p style="font-size:14px;line-height:1.55;color:{INK}">Permettre à chacun de vivre pleinement ses moments, mains libres, et de les garder pour toujours.</p><p class="muted" style="margin-top:2mm">To let everyone live their moments fully, hands-free, and keep them forever.</p></div></div>
<div class="col" style="flex:1"><p class="lbl" style="margin:0">Our 4 values</p><div class="row" style="gap:4mm">{vc[0]}{vc[1]}</div><div class="row" style="gap:4mm">{vc[2]}{vc[3]}</div></div></div>''', 2, "Brand essence"))

    # 3 — Story
    pages.append(page(f'''<p class="num">02</p><h1>Notre histoire</h1>
<div class="row" style="margin-top:8mm">
<div class="col" style="flex:1.35"><p class="lbl">À propos — texte du site (FR)</p>
<p style="font-size:13px;line-height:1.7;color:{INK}">Capté est né d'une idée simple : les plus beaux moments ne devraient pas se vivre derrière un écran. Une descente dans la poudreuse, un coucher de soleil entre amis, une conversation à l'autre bout du monde… On sort son téléphone, on cadre, et l'instant est déjà passé.</p>
<p style="font-size:13px;line-height:1.7;color:{INK}">Avec Capté, vos lunettes deviennent votre caméra. Vous filmez ce que vous voyez, mains libres, sans quitter le moment. Masque de ski, lunettes de soleil ou verres clairs : une même promesse — vivre pleinement, et garder le souvenir.</p>
<p style="font-size:13px;line-height:1.7;color:{INK}">Nous sommes une marque française, transparente sur nos produits, proche de nos clients et attachée à un usage respectueux : on filme ses aventures, pas les autres.</p>
<p style="font-family:Syne;font-size:18px;color:{INK};text-transform:uppercase">Capté. Tout est capté.</p></div>
<div class="col"><div class="card"><p class="lbl">In English (summary)</p><p>Capté was born from a simple idea: the best moments shouldn't be lived behind a screen. With Capté, your glasses become your camera — you film what you see, hands-free, without leaving the moment. Ski goggles, sunglasses or clear lenses: one promise. A French brand, honest about its products and committed to respectful recording.</p></div>
<img src="{u(TRIAL/'keyframes'/'k1.png')}" style="width:100%;height:58mm;object-fit:cover;border-radius:10px"></div></div>''', 3, "Brand story"))

    # 4 — Primary logo
    pages.append(page(f'''<p class="num">03</p><h1>Le logo</h1>
<div class="row" style="margin-top:7mm;flex:1">
<div class="card" style="flex:1.5;display:flex;align-items:center;justify-content:center;background:#fff"><img src="{u(L/'capte-wordmark-ink.svg')}" style="width:150mm"></div>
<div class="col" style="flex:1">
<div><p class="lbl">The REC dot</p><p>The red dot is the "recording" light of every camera. It says what Capté does, in one shape — and it is our most recognisable asset.</p></div>
<div><p class="lbl">The É</p><p>The accent keeps the name proudly French. Never drop it in the logo.</p></div>
<div><p class="lbl">The letters</p><p>Syne ExtraBold, wide and confident, tightened by hand. The letters are drawn as outlines — always use the supplied files, never retype the logo.</p></div>
<div><p class="lbl">Harmony</p><p>The REC red echoes the orange mirrored lens of the Glisse goggles.</p></div></div></div>''', 4, "Logo"))

    # 5 — Clear space & min size
    pages.append(page(f'''<p class="num">04</p><h1>Zone de protection &amp; tailles</h1>
<div class="row" style="margin-top:7mm;flex:1">
<div class="card" style="flex:1.6;display:flex;align-items:center;justify-content:center;background:#fff;position:relative">
<div style="position:relative;padding:15mm;border:1.5px dashed {REC};border-radius:4px"><img src="{u(L/'capte-wordmark-ink.svg')}" style="width:110mm;display:block">
<div style="position:absolute;left:3mm;top:3mm;width:9mm;height:9mm;border-radius:50%;border:1.5px solid {REC}"></div>
<p style="position:absolute;left:14mm;top:4.5mm;font-size:9px;color:{DEEP}">= 1 dot diameter</p></div></div>
<div class="col" style="flex:1"><div><p class="lbl">Clear space</p><p>Keep an empty margin around the logo equal to <b>the diameter of the REC dot</b> on every side (the dotted line). No text, image or edge inside it.</p></div>
<div><p class="lbl">Minimum sizes</p><table style="font-size:11px;border-collapse:collapse;width:100%"><tr><td style="padding:4px 0;border-bottom:1px solid #E6E0D6">Wordmark — screen</td><td style="text-align:right;border-bottom:1px solid #E6E0D6"><b>120 px</b> wide</td></tr><tr><td style="padding:4px 0;border-bottom:1px solid #E6E0D6">Wordmark — print</td><td style="text-align:right;border-bottom:1px solid #E6E0D6"><b>25 mm</b> wide</td></tr><tr><td style="padding:4px 0;border-bottom:1px solid #E6E0D6">Stacked (with descriptor)</td><td style="text-align:right;border-bottom:1px solid #E6E0D6"><b>180 px</b> / 35 mm</td></tr><tr><td style="padding:4px 0">Icon / monogram</td><td style="text-align:right"><b>16 px</b> / 6 mm</td></tr></table></div>
<div><p class="lbl">Below minimum size</p><p>Use the monogram instead of the wordmark (favicon, app, watch face, small labels).</p></div></div></div>''', 5, "Logo"))

    # 6 — Versions
    def tile(img, label, dark=False, w="70%"):
        bg = INK if dark else "#fff"
        col = "#A9A5B0" if dark else STONE
        return f'<div style="background:{bg};border-radius:10px;border:1px solid {"#2E2E38" if dark else "#E6E0D6"};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm;padding:5mm"><img src="{u(img)}" style="width:{w};max-height:24mm;object-fit:contain"><p style="font-size:8.5px;color:{col};letter-spacing:1px;text-transform:uppercase">{label}</p></div>'
    grid = "".join([
        tile(L/'capte-wordmark-ink.svg', 'Wordmark · primary'), tile(L/'capte-wordmark-cream.svg', 'Wordmark · on dark', True),
        tile(L/'capte-stacked-ink.svg', 'Stacked · with descriptor'), tile(L/'capte-stacked-cream.svg', 'Stacked · on dark', True),
        tile(L/'capte-horizontal-ink.svg', 'Horizontal lockup', w="80%"), tile(L/'capte-horizontal-cream.svg', 'Horizontal · on dark', True, "80%"),
        tile(L/'capte-icon-ink.svg', 'App / profile icon', w="26%"), tile(L/'capte-monogram-ink.svg', 'Monogram', w="30%"),
        tile(L/'capte-wordmark-black.svg', 'One colour · black'), tile(L/'capte-wordmark-white.svg', 'One colour · white', True),
        tile(L/'capte-icon-rec.svg', 'Icon · REC variant', w="26%"), tile(L/'capte-monogram-cream.svg', 'Monogram · on dark', True, "30%")])
    pages.append(page(f'''<p class="num">05</p><h1>Les versions du logo</h1>
<div style="display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:1fr;gap:4mm;margin-top:6mm;flex:1;margin-bottom:6mm">{grid}</div>''', 6, "Logo"))

    # 7 — Backgrounds & misuse
    don = [
        (f'<img src="{u(L/"capte-wordmark-ink.svg")}" style="width:78%;transform:scaleX(1.35) scaleY(.8)">', "Don't stretch or squash"),
        (f'<img src="{u(L/"capte-wordmark-ink.svg")}" style="width:78%;filter:hue-rotate(190deg)">', "Don't change the colours"),
        (f'<img src="{u(L/"capte-wordmark-ink.svg")}" style="width:78%;filter:drop-shadow(3px 4px 3px rgba(0,0,0,.55))">', "No shadows or effects"),
        (f'<img src="{u(L/"capte-wordmark-ink.svg")}" style="width:70%;transform:rotate(-12deg)">', "Don't rotate it"),
        (f'<p style="font-family:Syne;font-size:30px;color:{INK};letter-spacing:-1px">CAPTE</p>', "Don't drop the É or retype it"),
        (f'<div style="width:100%;height:100%;background:url({u(TRIAL/"product.jpg")}) center/cover;display:flex;align-items:center;justify-content:center"><img src="{u(L/"capte-wordmark-ink.svg")}" style="width:78%"></div>', "No low contrast on busy images"),
    ]
    dtiles = "".join(f'<div style="display:flex;flex-direction:column;gap:2mm"><div style="background:#fff;border:1px solid #E6E0D6;border-radius:10px;height:26mm;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative">{h}<div style="position:absolute;right:3mm;top:3mm;width:5mm;height:5mm;border-radius:50%;background:{DEEP};color:#fff;font-size:9px;display:flex;align-items:center;justify-content:center;font-weight:700">✕</div></div><p style="font-size:10px">{t}</p></div>' for h, t in don)
    pages.append(page(f'''<p class="num">06</p><h1>Fonds &amp; interdits</h1>
<div class="row" style="margin-top:6mm;gap:4mm">
<div style="flex:1;height:34mm;border-radius:10px;background:{INK};display:flex;align-items:center;justify-content:center"><img src="{u(L/'capte-wordmark-cream.svg')}" style="width:70%"></div>
<div style="flex:1;height:34mm;border-radius:10px;background:{CREAM};border:1px solid #E6E0D6;display:flex;align-items:center;justify-content:center"><img src="{u(L/'capte-wordmark-ink.svg')}" style="width:70%"></div>
<div style="flex:1;height:34mm;border-radius:10px;background:{REC};display:flex;align-items:center;justify-content:center"><img src="{u(L/'capte-wordmark-black.svg')}" style="width:70%;filter:invert(7%)"></div>
<div style="flex:1;height:34mm;border-radius:10px;overflow:hidden;position:relative;background:url({u(TRIAL/'keyframes'/'k1.png')}) center 30%/cover"><div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(21,21,27,.85) 0%,rgba(21,21,27,.35) 55%,rgba(21,21,27,0) 100%)"></div><img src="{u(L/'capte-wordmark-white.svg')}" style="position:absolute;left:4mm;bottom:4mm;width:62%"></div></div>
<p class="muted" style="margin:2mm 0 5mm;font-size:10px">✓ Ink · Cream · REC red (black logo) · photos only with a dark gradient behind a white logo</p>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4mm">{dtiles}</div>''', 7, "Logo"))

    # 8 — Colours
    sw = ""
    for fr, en, hx, use in PALETTE:
        r, g, b = rgb(hx)
        c, m, y, k = cmyk(hx)
        txt = CREAM if lum(hx) < 0.3 else INK
        sw += f'''<div style="display:flex;flex-direction:column;border-radius:10px;overflow:hidden;border:1px solid #E6E0D6">
<div style="height:36mm;background:{hx};padding:4mm;color:{txt}"><p style="font-family:Syne;font-size:12.5px;line-height:1.15;text-transform:uppercase;color:{txt}">{fr}</p><p style="font-size:10px;color:{txt};opacity:.8">{en}</p></div>
<div style="background:#fff;padding:3.5mm;font-size:10px;line-height:1.7"><b>HEX</b> {hx}<br><b>RGB</b> {r} {g} {b}<br><b>CMYK</b> {c} {m} {y} {k}<p class="muted" style="font-size:9px;line-height:1.4;margin-top:1.5mm">{use}</p></div></div>'''
    pages.append(page(f'''<p class="num">07</p><h1>Les couleurs</h1>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4mm;margin-top:6mm">{sw}</div>
<div class="row" style="margin-top:5mm;align-items:center"><div style="flex:1"><p class="lbl">Proportions</p><div style="display:flex;height:9mm;border-radius:6px;overflow:hidden"><div style="flex:55;background:{INK}"></div><div style="flex:30;background:{CREAM};border-top:1px solid #E6E0D6;border-bottom:1px solid #E6E0D6"></div><div style="flex:8;background:{GRAPH}"></div><div style="flex:5;background:{REC}"></div><div style="flex:2;background:{STONE}"></div></div></div>
<div style="flex:1"><p style="font-size:10.5px"><b>Rule:</b> REC red is a signal, not a background colour — keep it to ~5% (the dot, buttons, highlights). On light backgrounds, use <b>Rouge profond</b> for red text (contrast {contrast(DEEP, CREAM):.1f}:1). CMYK values are conversions — confirm with the printer.</p></div></div>''', 8, "Colour"))

    # 9 — Product line system
    lt = "".join(f'''<div class="card" style="flex:1;padding:0;overflow:hidden"><div style="height:30mm;background:{hx};display:flex;align-items:center;justify-content:center"><p style="font-family:Syne;font-size:24px;color:{INK};text-transform:uppercase">{n.split()[1]}</p></div>
<div style="padding:5mm"><p class="lbl">{n}</p><p style="color:{INK};font-weight:500">{d}</p><p class="muted" style="margin-top:2mm">Accent colour: {c} · {hx}</p></div></div>''' for n, d, c, hx in LINES)
    pages.append(page(f'''<p class="num">08</p><h1>Les gammes</h1>
<p class="lead" style="margin-top:4mm">One brand, three lines. The name is always "Capté" + one simple French word. Each line has a light accent colour used for its tags, category banners and packaging details — the logo itself never changes colour.</p>
<div class="row" style="margin-top:6mm;gap:5mm">{lt}</div>
<p class="muted" style="margin-top:5mm;font-size:10px">Clear-lens line: always described as non-prescription unless the supplier confirms prescription compatibility; never claim vision correction.</p>''', 9, "Product lines"))

    # 10 — Typography
    pages.append(page(f'''<p class="num">09</p><h1>Typographie</h1>
<div class="row" style="margin-top:6mm;align-items:stretch">
<div class="card" style="flex:1"><p class="lbl">Display — Syne ExtraBold</p><p style="font-family:Syne;font-size:52px;line-height:1;color:{INK};text-transform:uppercase">Aa Éé</p><p style="font-family:Syne;font-size:15px;color:{INK};margin-top:3mm;text-transform:uppercase">ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789</p><p class="muted" style="margin-top:3mm">Big, short headlines only — always uppercase, tight spacing. Never for paragraphs.</p></div>
<div class="card" style="flex:1"><p class="lbl">Text — DM Sans</p><p style="font-size:52px;line-height:1;color:{INK};font-weight:500">Aa Éé</p><p style="font-size:14px;color:{INK};margin-top:3mm">Regular · <b style="font-weight:500">Medium</b> · <b>Bold</b></p><p class="muted" style="margin-top:3mm">Everything else: sub-titles, body text, buttons, prices, captions. Clear and friendly on every screen.</p></div>
<div class="card" style="flex:1.2;background:{INK};border:none"><p class="lbl" style="color:{REC}">Hierarchy — example</p><p style="font-family:Syne;font-size:28px;line-height:1.02;color:{CREAM};text-transform:uppercase">Tout est capté.</p><p style="font-size:14px;font-weight:500;color:{CREAM};margin-top:3mm">Capté Glisse — le masque de ski qui filme</p><p style="color:#C9C6CF;margin-top:2mm">Filmez vos descentes en vue subjective, mains libres, et partagez-les depuis l'appli.</p><p style="margin-top:4mm;display:inline-block;background:{REC};color:{INK};font-weight:700;font-size:11px;padding:2.5mm 5mm;border-radius:99px;width:max-content">Découvrir</p></div></div>
<p class="muted" style="margin-top:4mm;font-size:10px">Both fonts are free Google Fonts (SIL Open Font License) — free for commercial use, web and print. Fallback: Arial.</p>''', 10, "Typography"))

    # 11 — Voice
    pages.append(page(f'''<p class="num">10</p><h1>La voix de la marque</h1>
<div class="row" style="margin-top:6mm">
<div class="col" style="flex:1.1"><div class="card" style="background:{INK};border:none"><p class="lbl" style="color:{REC}">Tagline (signature)</p><p style="font-family:Syne;font-size:26px;color:{CREAM};text-transform:uppercase">Tout est capté.</p><p style="color:#C9C6CF">Everything, captured.</p></div>
<div class="card"><p class="lbl">Campaign slogans</p><ul class="chk" style="font-size:11.5px">
<li><b>« Chaque piste, captée. »</b> — Glisse / ski season</li><li><b>« L'été, capté. »</b> — Soleil / summer</li><li><b>« Votre quotidien, capté. »</b> — Clair / everyday</li>
<li><b>« T'as capté ? Maintenant, oui. »</b> — translation feature</li><li><b>« Sans les mains. Sans rien rater. »</b> — hands-free</li><li><b>« Ça tourne. »</b> — launch / teasers</li></ul></div></div>
<div class="col"><div class="card"><p class="lbl">Tone: direct · complice · vrai</p><p>Like a friend who loves tech and the outdoors. Short sentences, concrete facts, a smile — never hype.</p><p style="margin-top:2mm"><b>« tu »</b> on TikTok &amp; Instagram · <b>« vous »</b> on the website, emails &amp; customer service.</p></div>
<div class="row" style="gap:4mm"><div class="card" style="flex:1"><p class="lbl">We say</p><ul class="chk"><li>filmer, capter, vivre</li><li>mains libres, vue subjective</li><li>vos aventures, vos proches</li><li>real specs &amp; real prices</li></ul></div>
<div class="card" style="flex:1"><p class="lbl">We never say</p><ul class="x"><li>espion, caché, discret</li><li>« à leur insu », « sans être vu »</li><li>révolutionnaire, -80 %</li><li>« dernières pièces » (fake urgency)</li></ul></div></div></div></div>''', 11, "Voice"))

    # 12 — Icons & UI
    icons = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:2mm"><img src="{u(IC/f"icon-{n}-ink.svg")}" style="width:15mm"><p style="font-size:9.5px">{lbl}</p></div>' for n, lbl in [("camera", "Caméra"), ("app", "Appli"), ("controls", "Commandes"), ("sound", "Son"), ("translation", "Traduction"), ("transfer", "Transfert"), ("battery", "Batterie")])
    pages.append(page(f'''<p class="num">11</p><h1>Icônes &amp; interface</h1>
<div class="card" style="margin-top:6mm"><p class="lbl">Feature icons — 24 px grid, 1.75 px rounded line, REC dot accent</p><div style="display:flex;justify-content:space-between;padding:3mm 4mm 0">{icons}</div></div>
<div class="row" style="margin-top:5mm">
<div class="card" style="flex:1"><p class="lbl">Buttons</p><div style="display:flex;gap:3mm;flex-wrap:wrap;align-items:center">
<span style="background:{INK};color:{CREAM};font-weight:700;font-size:11px;padding:3mm 6mm;border-radius:99px">Ajouter au panier</span>
<span style="background:{DEEP};color:#fff;font-weight:700;font-size:11px;padding:3mm 6mm;border-radius:99px">Acheter</span>
<span style="border:1.5px solid {INK};color:{INK};font-weight:700;font-size:11px;padding:3mm 6mm;border-radius:99px">En savoir plus</span></div>
<p class="muted" style="margin-top:3mm">Pill shape, bold DM Sans. On dark backgrounds the main button is REC red with ink text.</p></div>
<div class="card" style="flex:1"><p class="lbl">Badges &amp; the REC motif</p><div style="display:flex;gap:3mm;flex-wrap:wrap;align-items:center">
<span style="background:{INK};color:{CREAM};font-size:10px;font-weight:700;padding:1.8mm 3.5mm;border-radius:99px"><span style="color:{REC}">●</span> REC</span>
<span style="background:#E8F3FB;color:{INK};font-size:10px;font-weight:700;padding:1.8mm 3.5mm;border-radius:99px">GLISSE</span>
<span style="background:#FFF1DA;color:{INK};font-size:10px;font-weight:700;padding:1.8mm 3.5mm;border-radius:99px">SOLEIL</span>
<span style="background:#EEF1F4;color:{INK};font-size:10px;font-weight:700;padding:1.8mm 3.5mm;border-radius:99px">CLAIR</span>
<span style="background:{CREAM};border:1px solid #E6E0D6;color:{INK};font-size:10px;font-weight:700;padding:1.8mm 3.5mm;border-radius:99px">NOUVEAU</span></div>
<p class="muted" style="margin-top:3mm">The "● REC" badge and the dot can mark live content, new videos and highlights — our visual signature.</p></div></div>''', 12, "Icons & UI"))

    # 13 — Photo & video
    pages.append(page(f'''<p class="num">12</p><h1>Photo &amp; vidéo</h1>
<div class="row" style="margin-top:6mm;flex:1">
<div class="col" style="flex:1.4"><div class="row" style="gap:4mm;flex:1"><img src="{u(TRIAL/'keyframes'/'k1.png')}" style="flex:1;width:0;height:100%;object-fit:cover;border-radius:10px"><img src="{u(TRIAL/'product.jpg')}" style="flex:1;width:0;height:100%;object-fit:cover;border-radius:10px"></div>
<p class="muted" style="font-size:10px">Real light, real places, the product clearly visible, people living the moment.</p></div>
<div class="col"><div class="card"><p class="lbl">Do</p><ul class="chk"><li>POV clips filmed <b>with the glasses</b> for image quality</li><li>Natural light, warm cinematic grade</li><li>People filming themselves, friends who agree, landscapes, activities</li><li>Show the product sharp and real</li><li>Add "Images virtuelles" on AI-made faces</li></ul></div>
<div class="card"><p class="lbl">Don't</p><ul class="x"><li>Scenes of filming strangers or "without being seen"</li><li>AI-simulated "camera footage" to show quality</li><li>Supplier logos, Chinese text, QR codes</li></ul></div>
<div class="row" style="gap:3mm;align-items:center"><img src="{u(END/'capte-endcard-1080x1920.png')}" style="width:17mm;border-radius:4px"><p style="font-size:10px"><b>End card</b> on every video: stacked logo + « Tout est capté. » (9:16, 4:5, 16:9 supplied).</p></div></div></div>''', 13, "Photo & video"))

    # 14 — Social kit
    hls = "".join(f'<img src="{u(SOC/f"capte-highlight-{n}.png")}" style="width:13mm;height:13mm;object-fit:cover;border-radius:50%">' for n in ["avis", "faq", "livraison", "glisse", "soleil", "clair"])
    pages.append(page(f'''<p class="num">13</p><h1>Réseaux sociaux</h1>
<div class="row" style="margin-top:6mm;flex:1">
<div class="col" style="flex:.8"><p class="lbl">Profile picture (all platforms)</p><div class="row" style="gap:4mm"><img src="{u(SOC/'capte-profile-1080.png')}" style="width:30mm;border-radius:50%"><img src="{u(SOC/'capte-profile-rec-1080.png')}" style="width:30mm;border-radius:50%"></div>
<p class="muted">Instagram · TikTok · TikTok Shop · Facebook — 1080×1080, safe for the round crop.</p>
<p class="lbl" style="margin-top:3mm">Instagram highlight covers</p><div style="display:flex;gap:2.5mm">{hls}</div><p class="muted">Avis · FAQ · Livraison · Glisse · Soleil · Clair</p></div>
<div class="col" style="flex:1.4"><p class="lbl">Facebook cover — 1640×624</p><img src="{u(SOC/'capte-facebook-cover-1640x624.png')}" style="width:100%;border-radius:8px">
<div class="card"><p class="lbl">Handles to secure (same name everywhere)</p><p>@capte.lunettes (or closest available) on Instagram, TikTok, TikTok Shop and Facebook. Bio line: <b>« Lunettes caméra · Tout est capté. »</b></p></div></div></div>''', 14, "Social media"))

    # 15 — Website + files
    pages.append(page(f'''<p class="num">14</p><h1>Sur le site</h1>
<div class="row" style="margin-top:6mm;flex:1">
<div style="flex:1.5;border-radius:10px;overflow:hidden;background:{INK};display:flex;flex-direction:column;border:1px solid #2E2E38">
<div style="display:flex;justify-content:space-between;align-items:center;padding:3.5mm 5mm;border-bottom:1px solid #2E2E38"><img src="{u(L/'capte-wordmark-cream.svg')}" style="height:4.5mm"><p style="font-size:9px;color:#C9C6CF;letter-spacing:1px">GLISSE &nbsp; SOLEIL &nbsp; CLAIR &nbsp; À PROPOS</p></div>
<div style="display:flex;flex:1"><div style="flex:1;padding:8mm 6mm;display:flex;flex-direction:column;justify-content:center;gap:3mm"><p style="font-size:9px;color:{REC};font-weight:700;letter-spacing:2px">● CAPTÉ GLISSE</p><p style="font-family:Syne;font-size:30px;line-height:1;color:{CREAM};text-transform:uppercase">Chaque piste, captée.</p><p style="font-size:10.5px;color:#C9C6CF">Le masque de ski qui filme vos descentes, mains libres.</p><span style="background:{REC};color:{INK};font-weight:700;font-size:10px;padding:2.5mm 5mm;border-radius:99px;width:max-content">Découvrir</span></div>
<img src="{u(TRIAL/'product.jpg')}" style="width:48%;object-fit:cover"></div></div>
<div class="col" style="flex:1"><div class="card"><p class="lbl">Brand files delivered</p><ul class="chk" style="font-size:10.5px"><li><b>Logos</b> — 20 versions in SVG, PDF, PNG (transparent) &amp; JPG</li><li><b>Icons</b> — 7 feature icons, ink &amp; cream (SVG)</li><li><b>Social kit</b> — profile pictures, Facebook cover, 6 highlight covers</li><li><b>Video end cards</b> — 9:16, 4:5, 16:9</li><li><b>Fonts</b> — Syne &amp; DM Sans + licence</li><li><b>Source</b> — editable generator files</li></ul></div>
<div class="card"><p class="lbl">Questions</p><p>The Fifth Kind — uday.khandelwal@the5thkind.in · +91 82960 08838</p></div></div></div>''', 15, "Application"))

    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    OUT.mkdir(exist_ok=True)
    src = OUT / "Capte-Brand-Guidelines.html"
    src.write_text(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                    f"--print-to-pdf={OUT/'Capte-Brand-Guidelines.pdf'}", src.as_uri()], capture_output=True)
    print("built", OUT / "Capte-Brand-Guidelines.pdf")


if __name__ == "__main__":
    build()
