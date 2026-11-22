from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Презентация_монетизация" / "media" / "metric_tree.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1800, 760
BG = "#FFFFFF"
INK = "#172B3A"
MUTED = "#536674"
NAVY = "#184B68"
NAVY_2 = "#2E6B88"
PALE = "#EAF2F6"
PALE_2 = "#F5F8FA"
LINE = "#B8C8D2"
WHITE = "#FFFFFF"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
font_dir = Path("C:/Windows/Fonts")

def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(font_dir / name), size)

F_ROOT = font(39, True)
F_ROOT_SUB = font(25)
F_HEAD = font(31, True)
F_FORMULA = font(24, True)
F_BODY = font(24)
F_BODY_BOLD = font(24, True)
F_SMALL = font(22)


def center_text(box, text, fnt, fill=INK, spacing=7):
    x0, y0, x1, y1 = box
    bb = d.multiline_textbbox((0, 0), text, font=fnt, spacing=spacing, align="center")
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.multiline_text(((x0 + x1 - tw) / 2, (y0 + y1 - th) / 2 - bb[1]), text,
                     font=fnt, fill=fill, spacing=spacing, align="center")


def box(rect, fill=WHITE, outline=LINE, width=2):
    d.rectangle(rect, fill=fill, outline=outline, width=width)


def line(points, fill=LINE, width=3):
    d.line(points, fill=fill, width=width)

# Root
root = (210, 22, 1590, 145)
box(root, fill=PALE, outline=NAVY, width=4)
center_text((230, 30, 1570, 88), "Инкрементальная маржа на eligible-продавца за 56 дней", F_ROOT, NAVY)
center_text((230, 88, 1570, 136), "Маржа подписки на всех eligible + разница маржи маркетплейса между тестом и контролем", F_ROOT_SUB, MUTED)

# Connectors
line([(900, 145), (900, 182)], NAVY_2, 4)
line([(300, 182), (1500, 182)], NAVY_2, 4)
for cx in (300, 900, 1500):
    line([(cx, 182), (cx, 210)], NAVY_2, 4)

cols = [
    {
        "x": 30, "w": 540, "title": "1. Маржа подписки",
        "formula": "S / N × (ARPPU - 250 - 3Q - b)",
        "blocks": [
            ("Первая ценность", "Paywall и конверсия\nАктивация за 7 дней\nИспользование функций"),
            ("Повторное поведение", "Продление и churn\n3 активные недели из 4\nUpgrade, downgrade, ARPPU"),
        ],
    },
    {
        "x": 630, "w": 540, "title": "2. Маржа маркетплейса",
        "formula": "CM test / N - CM control / N",
        "blocks": [
            ("Наличие и продажи", "Применение рекомендаций\nSKU-дни в наличии\nЗаказы и GMV"),
            ("Активность продавцов", "Уход с площадки\nВозвраты заказов\nПеременные расходы"),
        ],
    },
    {
        "x": 1230, "w": 540, "title": "3. Guardrails",
        "formula": "Активные: не хуже -2%\nДоступность: не хуже -1 п. п.",
        "blocks": [
            ("Площадка", "GMV на eligible\nВозвраты и активность"),
            ("Сервис и доверие", "Жалобы и поддержка\nВнешние сервисы\nИспользование около лимита"),
        ],
    },
]

for col in cols:
    x, w = col["x"], col["w"]
    header = (x, 210, x + w, 350)
    box(header, fill=WHITE, outline=NAVY, width=3)
    d.rectangle((x, 210, x + w, 218), fill=NAVY)
    center_text((x + 16, 225, x + w - 16, 274), col["title"], F_HEAD, NAVY)
    center_text((x + 16, 276, x + w - 16, 340), col["formula"], F_FORMULA, INK)
    y = 370
    for title, body in col["blocks"]:
        h = 142 if y == 370 else 150
        rect = (x, y, x + w, y + h)
        box(rect, fill=PALE_2, outline=LINE, width=2)
        d.text((x + 20, y + 14), title, font=F_BODY_BOLD, fill=NAVY)
        d.multiline_text((x + 20, y + 52), body, font=F_BODY, fill=MUTED, spacing=6)
        y += h + 16

# Bottom rule
d.rectangle((30, 686, 1770, 731), fill=PALE)
center_text((45, 687, 1755, 730), "Поведение объясняет маржу. Guardrails ограничивают запуск. Постоянные затраты оцениваются отдельно.", F_SMALL, NAVY)

img.save(OUT, optimize=True)
print(OUT)
print(f"{W}x{H}; {OUT.stat().st_size} bytes")
