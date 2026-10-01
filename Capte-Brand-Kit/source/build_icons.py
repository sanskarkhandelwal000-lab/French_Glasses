"""CAPTÉ feature icon set — 24px grid, 1.75px rounded stroke, REC dot accent.

Only for features the products really have (as listed by the client):
camera, app connection, touch controls, sound, translation, file transfer, battery.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "icons"
OUT.mkdir(exist_ok=True)
REC = "#FF4D2E"

ICONS = {
    # name: (stroke paths, optional rec-dot (cx, cy, r))
    "camera": ('<rect x="2.5" y="6.5" width="19" height="13" rx="3.5"/>'
               '<path d="M8.5 6.5 10 4h4l1.5 2.5"/><circle cx="12" cy="13" r="3.6"/>', (18.4, 9.6, 1.25)),
    "app": ('<rect x="6.5" y="2.5" width="11" height="19" rx="2.8"/><path d="M10.5 18.5h3"/>'
            '<path d="M9.2 9.2a4 4 0 0 1 5.6 0"/><path d="M10.6 11.1a1.9 1.9 0 0 1 2.8 0"/>', (12, 13.2, 0.95)),
    "controls": ('<path d="M3 9.5h18"/><path d="M5.5 9.5v5.5a2.5 2.5 0 0 0 5 0V9.5"/>'
                 '<circle cx="17" cy="15" r="2.2"/><path d="M13.6 18.4a4.8 4.8 0 0 0 6.8 0"/>', (17, 15, 0.9)),
    "sound": ('<path d="M4 9.5h3.2L12 5.5v13l-4.8-4H4z"/><path d="M15.5 9a4.3 4.3 0 0 1 0 6"/>'
              '<path d="M18 6.5a8 8 0 0 1 0 11"/>', None),
    "translation": ('<path d="M3.5 5.5h9a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H9l-3.5 3v-3h-2a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2z"/>'
                    '<path d="M16.5 9.5h2a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-1v2.5l-3-2.5h-2.5a2 2 0 0 1-1.6-.8"/>'
                    '<path d="M5.8 10h4.4"/>', (18, 13.5, 0.95)),
    "transfer": ('<rect x="2.5" y="4.5" width="7" height="13" rx="2"/><rect x="14.5" y="6.5" width="7" height="13" rx="2"/>'
                 '<path d="M11 9.5h2.5m0 0-1.3-1.3m1.3 1.3-1.3 1.3"/><path d="M13 14.5h-2.5m0 0 1.3-1.3m-1.3 1.3 1.3 1.3"/>', None),
    "battery": ('<rect x="2.5" y="7.5" width="17" height="9" rx="2.5"/><path d="M21.5 10.5v3"/>'
                '<path d="M5.5 10.5v3M8.5 10.5v3M11.5 10.5v3"/>', None),
}


def icon(body, dot, color):
    d = f'<circle cx="{dot[0]}" cy="{dot[1]}" r="{dot[2]}" fill="{REC}" stroke="none"/>' if dot else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="96" height="96" fill="none" '
            f'stroke="{color}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{body}{d}</svg>\n')


for name, (body, dot) in ICONS.items():
    (OUT / f"icon-{name}-ink.svg").write_text(icon(body, dot, "#15151B"))
    (OUT / f"icon-{name}-cream.svg").write_text(icon(body, dot, "#F4F1EC"))
print("wrote", len(ICONS) * 2, "icons to", OUT)
