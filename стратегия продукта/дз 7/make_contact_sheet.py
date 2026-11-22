from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
shots = root / "Презентация_монетизация-screenshots"
out = shots / "overview.png"
thumb_w, thumb_h = 480, 270
sheet = Image.new("RGB", (thumb_w * 2, thumb_h * 5), "white")
for i in range(1, 11):
    image = Image.open(shots / f"page-{i}.png").convert("RGB")
    image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = ((i - 1) % 2) * thumb_w
    y = ((i - 1) // 2) * thumb_h
    sheet.paste(image, (x, y))
sheet.save(out, optimize=True)
print(out)
print(out.stat().st_size)
