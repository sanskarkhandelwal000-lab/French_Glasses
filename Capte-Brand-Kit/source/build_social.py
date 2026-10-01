"""CAPTÉ social kit + video end cards, rendered with headless Chrome."""
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOC = ROOT / "social"
END = ROOT / "endcards"
LOGO = ROOT / "logo" / "svg"
FONTS = ROOT / "fonts"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
INK, CREAM, REC, MUTED = "#15151B", "#F4F1EC", "#FF4D2E", "#A9A5B0"

HEAD = f"""<style>
@font-face{{font-family:'Syne';src:url('{FONTS/'Syne-ExtraBold.ttf'}');font-weight:800}}
@font-face{{font-family:'DM Sans';src:url('{FONTS/'DMSans-Regular.ttf'}');font-weight:400}}
@font-face{{font-family:'DM Sans';src:url('{FONTS/'DMSans-Medium.ttf'}');font-weight:500}}
@font-face{{font-family:'DM Sans';src:url('{FONTS/'DMSans-Bold.ttf'}');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{INK};color:{CREAM};font-family:'DM Sans',Arial,sans-serif;overflow:hidden}}
.glow{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,77,46,.32) 0%,rgba(255,77,46,0) 68%)}}
</style>"""


def shot(html, out, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(f"<html><head>{HEAD}</head><body style='width:{w}px;height:{h}px;position:relative'>{html}</body></html>")
        page = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    "--virtual-time-budget=2000", f"--screenshot={out}", f"file://{page}"], capture_output=True)
    print("rendered", out.name)


# Simple line icons for Instagram highlight covers (same stroke style as the feature set)
HL = {
    "avis": '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.9z"/>',
    "faq": '<circle cx="12" cy="12" r="9"/><path d="M9.3 9.3a2.8 2.8 0 1 1 3.9 2.6c-.8.4-1.2 1-1.2 1.8v.6"/><path d="M12 17.2h.01"/>',
    "livraison": '<path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3v3h-7z"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/>',
    "glisse": '<path d="M2.5 19.5 9 8l3.5 5.5L15 10l6.5 9.5z"/><path d="M7.3 11l1.7 1.2 1.5-1.4"/>',
    "soleil": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.5 1.5M17.2 17.2l1.5 1.5M5.3 18.7l1.5-1.5M17.2 6.8l1.5-1.5"/>',
    "clair": '<circle cx="7" cy="13" r="3.8"/><circle cx="17" cy="13" r="3.8"/><path d="M10.8 12.3a2 2 0 0 1 2.4 0"/><path d="M3.2 12.2 2 8.5M20.8 12.2 22 8.5"/>',
}


def hl_svg(body, dot=True):
    d = f'<circle cx="20.6" cy="3.4" r="1.2" fill="{REC}" stroke="none"/>' if dot else ""
    return (f'<svg viewBox="0 0 24 24" width="470" height="470" fill="none" stroke="{CREAM}" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}{d}</svg>')


def main():
    SOC.mkdir(exist_ok=True)
    END.mkdir(exist_ok=True)
    mono = (LOGO / "capte-monogram-cream.svg").resolve()
    word = (LOGO / "capte-wordmark-cream.svg").resolve()
    stacked = (LOGO / "capte-stacked-cream.svg").resolve()

    # 1. Profile picture — safe for circle crop on every platform
    shot(f'<div class="glow" style="left:140px;top:140px;width:800px;height:800px;opacity:.55"></div>'
         f'<img src="{mono}" style="position:absolute;left:190px;top:190px;width:700px;height:700px">',
         SOC / "capte-profile-1080.png", 1080, 1080)
    shot(f'<div style="position:absolute;inset:0;background:{REC}"></div>'
         f'<img src="{(LOGO / "capte-monogram-black.svg").resolve()}" style="position:absolute;left:190px;top:190px;width:700px;height:700px;filter:invert(8%)">',
         SOC / "capte-profile-rec-1080.png", 1080, 1080)

    # 2. Facebook cover 1640x624 — content kept in the centre safe zone
    shot(f'<div class="glow" style="left:1050px;top:-260px;width:900px;height:900px"></div>'
         f'<div style="position:absolute;left:0;right:0;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px">'
         f'<img src="{word}" style="width:640px">'
         f'<p style="font-size:40px;font-weight:500;color:{CREAM}">Tout est capté.</p>'
         f'<p style="font-size:24px;letter-spacing:6px;text-transform:uppercase;color:{MUTED}">Lunettes caméra · Glisse · Soleil · Clair</p></div>',
         SOC / "capte-facebook-cover-1640x624.png", 1640, 624)

    # 3. Instagram highlight covers 1080x1920
    for name, body in HL.items():
        shot(f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{hl_svg(body, name != "soleil")}</div>',
             SOC / f"capte-highlight-{name}.png", 1080, 1920)

    # 4. Video end cards (9:16, 4:5, 16:9)
    for w, h, ww in [(1080, 1920, 760), (1080, 1350, 700), (1920, 1080, 900)]:
        shot(f'<div class="glow" style="left:{w/2-450}px;top:{h/2-560}px;width:900px;height:900px;opacity:.7"></div>'
             f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{int(ww*0.08)}px">'
             f'<img src="{stacked}" style="width:{ww}px">'
             f'<p style="font-size:{int(ww*0.066)}px;font-weight:500;color:{CREAM}">Tout est capté.</p></div>',
             END / f"capte-endcard-{w}x{h}.png", w, h)


if __name__ == "__main__":
    main()
