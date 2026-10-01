"""Export every SVG in logo/svg to transparent PNG, PDF and (on-background) JPG.

Uses headless Chrome for rendering. Run: python3 export_logos.py
"""
import re
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "logo" / "svg"
PNG = ROOT / "logo" / "png"
PDF = ROOT / "logo" / "pdf"
JPG = ROOT / "logo" / "jpg"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for d in (PNG, PDF, JPG):
    d.mkdir(parents=True, exist_ok=True)


def size_of(svg_text):
    m = re.search(r'width="(\d+)" height="(\d+)"', svg_text)
    return int(m.group(1)), int(m.group(2))


def render_png(svg_path, out, width):
    w, h = size_of(svg_path.read_text())
    height = round(width * h / w)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(f'<html><body style="margin:0;background:transparent">'
                f'<img src="{svg_path.resolve()}" style="display:block;width:{width}px;height:{height}px"></body></html>')
        page = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000", f"--window-size={width},{height}",
                    f"--screenshot={out}", f"file://{page}"], capture_output=True)


def render_pdf(svg_path, out):
    w, h = size_of(svg_path.read_text())
    pw, ph = 1000, round(1000 * h / w)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(f'<html><head><style>@page{{size:{pw}px {ph}px;margin:0}}body{{margin:0}}</style></head>'
                f'<body><img src="{svg_path.resolve()}" style="display:block;width:{pw}px;height:{ph}px"></body></html>')
        page = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", f"file://{page}"], capture_output=True)


def main():
    for svg in sorted(SVG.glob("*.svg")):
        stem = svg.stem
        is_icon = "icon" in stem or "monogram" in stem
        widths = [1024, 512] if is_icon else [3000, 1200]
        for wpx in widths:
            render_png(svg, PNG / f"{stem}-{wpx}.png", wpx)
        render_pdf(svg, PDF / f"{stem}.pdf")
        # JPG only makes sense with a solid background
        bg = None
        if stem.endswith(("-ink", "-black")) and "icon" not in stem:
            bg = (244, 241, 236) if stem.endswith("-ink") else (255, 255, 255)
        elif stem.endswith(("-cream", "-white")) and "icon" not in stem:
            bg = (21, 21, 27) if stem.endswith("-cream") else (0, 0, 0)
        src = Image.open(PNG / f"{stem}-{widths[0]}.png").convert("RGBA")
        if "on-" in stem or "icon" in stem:
            src.convert("RGB").save(JPG / f"{stem}.jpg", quality=95)
        elif bg:
            canvas = Image.new("RGB", src.size, bg)
            canvas.paste(src, mask=src.split()[3])
            canvas.save(JPG / f"{stem}.jpg", quality=95)
        print("exported", stem)


if __name__ == "__main__":
    main()
