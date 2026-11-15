"""Bouwt het dashboard (GitHub Pages, repo 'dashboard') uit dashboard.html.

Gebruik (vanuit de hoofdmap): python3 bron/build_dashboard.py  ->  index.html + icoon
"""
import hashlib
from pathlib import Path

try:  # Pillow is alleen nodig om het icoon opnieuw te tekenen
    from PIL import Image, ImageDraw
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "dashboard.html"
OUT = ROOT.parent  # de gebouwde site staat in de hoofdmap van de repository


def build_html() -> None:
    src = SRC.read_text(encoding="utf-8")
    version = hashlib.sha1(src.encode("utf-8")).hexdigest()[:10]
    html = src.replace("<!--VERSION-->", f'<meta name="dashboard-versie" content="{version}">', 1)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    print("versie", version)


def build_icon(size: int = 180) -> None:
    if Image is None:
        print("(Pillow ontbreekt: bestaand icoon blijft staan)")
        return
    # Donkerblauw vlak met een stijgende lijn en drie staafjes
    scale = 4
    s = size * scale
    img = Image.new("RGB", (s, s), (16, 34, 60))
    d = ImageDraw.Draw(img)
    # zachte verloop-indruk met twee lagen
    d.rectangle([0, 0, s, s * 0.55], fill=(22, 52, 92))
    bars = [0.30, 0.48, 0.38]
    bw, gap = s * 0.11, s * 0.06
    x0 = s * 0.20
    base = s * 0.80
    for i, h in enumerate(bars):
        x = x0 + i * (bw + gap)
        d.rounded_rectangle([x, base - h * s * 0.5, x + bw, base], radius=bw * 0.3, fill=(120, 170, 235))
    pts = [(s * 0.18, s * 0.58), (s * 0.40, s * 0.40), (s * 0.58, s * 0.48), (s * 0.82, s * 0.22)]
    d.line(pts, fill=(255, 255, 255), width=int(s * 0.045), joint="curve")
    r = s * 0.045
    ex, ey = pts[-1]
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 255, 255))
    img = img.resize((size, size), Image.LANCZOS)
    img.save(OUT / "apple-touch-icon.png")


if __name__ == "__main__":
    build_html()
    build_icon()
    print("Klaar:", OUT)
