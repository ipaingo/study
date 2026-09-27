# -*- coding: utf-8 -*-
"""ДЗ 2, часть 1: модель анализа стратегии TechGourmet и бизнес-цели (+300% прибыли).
Сборка 01_Анализ_стратегии.xlsx: driver-based упрощённый ОПиУ, эластичность рычагов,
сценарий стратегии (по кварталам + мост), анти-сценарий (привлечение), юнит-экономика.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.chart import BarChart, LineChart, Reference, Series

ACCENT = "1F4E79"      # тёмно-синий
ACCENT_LT = "DDEBF7"   # светло-синий
GREY = "F2F2F2"
BLUE_IN = Font(color="0000CC")            # входные допущения
GREEN_X = Font(color="008000")            # чистый cross-sheet перенос
BLACK_F = Font(color="000000")            # формулы внутри листа
BOLD = Font(bold=True)
WHITE_B = Font(bold=True, color="FFFFFF")
TITLE_F = Font(bold=True, size=14, color=ACCENT)
SUB_F = Font(bold=True, size=11, color=ACCENT)
HDR_FILL = PatternFill("solid", fgColor=ACCENT)
LT_FILL = PatternFill("solid", fgColor=ACCENT_LT)
GREY_FILL = PatternFill("solid", fgColor=GREY)
WARN_FILL = PatternFill("solid", fgColor="FCE4D6")
GOOD_FILL = PatternFill("solid", fgColor="E2EFDA")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOTTOM = Border(bottom=Side(style="medium", color=ACCENT))

MONEY = '#,##0.0'      # млн руб.
MONEY2 = '#,##0.00'
NUM = '#,##0'
PCT = '0.0%'
PCT2 = '0.00%'

wb = Workbook()

def add_name(name, ref):
    dn = DefinedName(name, attr_text=ref)
    try:
        wb.defined_names[name] = dn
    except TypeError:
        wb.defined_names.append(dn)

def set_cell(ws, addr, value, font=None, fill=None, fmt=None, align=None, border=None, wrap=False):
    c = ws[addr]
    c.value = value
    if font: c.font = font
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if border: c.border = border
    return c

def header_row(ws, row, cols_vals, start_col=2):
    for i, v in enumerate(cols_vals):
        col = get_column_letter(start_col + i)
        set_cell(ws, f"{col}{row}", v, font=WHITE_B, fill=HDR_FILL, align="center", border=BORDER, wrap=True)

def widths(ws, wd):
    for col, w in wd.items():
        ws.column_dimensions[col].width = w

def no_grid(ws):
    ws.sheet_view.showGridLines = False

# =====================================================================
# Лист: Исходные данные
# =====================================================================
ws = wb.active
ws.title = "Исходные данные"
no_grid(ws)
widths(ws, {"A": 2, "B": 52, "C": 16, "D": 16, "E": 46})
set_cell(ws, "B2", "Исходные данные брифа TechGourmet", font=TITLE_F)
set_cell(ws, "B3", "Все значения — из файла «Сервис TechGourmet.md» (папка дз 2). Синим цветом — входные данные.", font=Font(italic=True, size=9, color="808080"))
header_row(ws, 5, ["Показатель", "Значение", "Единица", "Источник"])
rows = [
    ("Активные пользователи (MAU)", 100000, NUM, "пользователей/мес", "Бриф TechGourmet"),
    ("Frequency (заказов на пользователя в месяц)", 1.2, MONEY2, "заказов/мес", "Бриф TechGourmet"),
    ("Заказы в месяц", 120000, NUM, "заказов/мес", "Бриф TechGourmet"),
    ("Средний чек", 1400, NUM, "руб.", "Бриф TechGourmet"),
    ("Месячная выручка", 180000000, NUM, "руб./мес", "Бриф TechGourmet"),
    ("Gross Margin (доля выручки)", 0.18, PCT, "доля", "Бриф TechGourmet"),
    ("Новые пользователи в месяц", 12000, NUM, "пользователей/мес", "Бриф TechGourmet"),
    ("Конверсия регистрация → первая покупка", 0.10, PCT, "доля", "Бриф TechGourmet"),
    ("Месячный Retention Rate", 0.32, PCT, "доля", "Бриф TechGourmet"),
    ("Доля заказов, доставленных вовремя", 0.89, PCT, "доля", "Бриф TechGourmet"),
    ("Среднее время доставки", 48, NUM, "минут", "Бриф TechGourmet"),
    ("Доля отменённых заказов", 0.06, PCT, "доля", "Бриф TechGourmet"),
    ("NPS", 35, NUM, "баллов", "Бриф TechGourmet"),
    ("Доля возвратов и жалоб", 0.03, PCT, "доля", "Бриф TechGourmet"),
    ("CPA (стоимость привлечения платящего)", 1200, NUM, "руб.", "Бриф TechGourmet"),
    ("Доля органического трафика", 0.15, PCT, "доля", "Бриф TechGourmet"),
    ("Conversion Rate на главной странице", 0.15, PCT, "доля", "Бриф TechGourmet"),
]
name_map = ["in_MAU","in_FREQ","in_ORDERS","in_CHECK","in_REV","in_GMPCT","in_NEWUSERS",
            "in_CONV","in_RET","in_ONTIME","in_DELIVMIN","in_CANCEL","in_NPS",
            "in_COMPLAINT","in_CPA","in_ORGANIC","in_CR"]
for i, (label, val, fmt, unit, src) in enumerate(rows):
    r = 6 + i
    set_cell(ws, f"B{r}", label, border=BORDER)
    set_cell(ws, f"C{r}", val, font=BLUE_IN, fmt=fmt, border=BORDER, align="right")
    set_cell(ws, f"D{r}", unit, border=BORDER)
    set_cell(ws, f"E{r}", src, border=BORDER)
    add_name(name_map[i], f"'Исходные данные'!$C${r}")
set_cell(ws, "B24", "Примечание о согласованности данных: 120 000 заказов × 1 400 руб. = 168 млн руб. GMV, "
                    "что на 12 млн руб. (6,7%) ниже заявленной выручки 180 млн руб. Разница трактуется в модели "
                    "как прочая выручка (сервисный сбор, доставка, продвижение ресторанов): 12 млн руб./мес.",
         font=Font(italic=True, size=9, color="808080"), wrap=True)
ws.row_dimensions[24].height = 40
ws.merge_cells("B24:E24")

# =====================================================================
# Лист: Базовый ОПиУ
# =====================================================================
ws = wb.create_sheet("Базовый ОПиУ")
no_grid(ws)
widths(ws, {"A": 2, "B": 52, "C": 46, "D": 18, "E": 18})
set_cell(ws, "B2", "Базовый упрощённый ОПиУ TechGourmet (месяц / год)", font=TITLE_F)
set_cell(ws, "B3", "Метод: driver-based модель «снизу вверх» (McKinsey, CFI — см. лист «Источники»). "
                    "Денежные потоки — в млн руб.", font=Font(italic=True, size=9, color="808080"))
header_row(ws, 5, ["Статья", "Логика расчёта", "Месяц", "Год"])
drv = [
    ("Активные клиенты, шт", "перенос из брифа", "=in_MAU", NUM),
    ("Frequency, заказов/мес", "перенос из брифа", "=in_FREQ", MONEY2),
    ("Заказы, шт/мес", "клиенты × frequency", "=D6*D7", NUM),
    ("Средний чек, руб.", "перенос из брифа", "=in_CHECK", NUM),
    ("GMV (заказы × чек), млн руб./мес", "заказы × чек / 1 000 000", "=D8*D9/1000000", MONEY),
]
for i, (a, b, f, fmt) in enumerate(drv):
    r = 6 + i
    set_cell(ws, f"B{r}", a, border=BORDER)
    set_cell(ws, f"C{r}", b, font=Font(size=9, color="808080"), border=BORDER)
    pure_cross = f.startswith("=in_")
    set_cell(ws, f"D{r}", f, font=(GREEN_X if pure_cross else BLACK_F), fmt=fmt, border=BORDER, align="right")
    set_cell(ws, f"E{r}", "", border=BORDER)
set_cell(ws, "B11", "Выручка и прибыль", font=SUB_F)
pnl = [
    (12, "GMV, млн руб.", "перенос расчёта выше", "=D10", MONEY, False),
    (13, "Выручка по брифу, млн руб.", "перенос из брифа", "=in_REV/1000000", MONEY, True),
    (14, "Прочая выручка, млн руб.", "выручка по брифу − GMV", "=D13-D12", MONEY, False),
    (15, "Выручка, млн руб.", "GMV + прочая выручка", "=D12+D14", MONEY, False),
    (16, "Валовая прибыль, млн руб.", "выручка × Gross Margin", "=D15*in_GMPCT", MONEY, False),
    (17, "Постоянные OPEX, млн руб.", "допущение (синий), обоснование ниже", 22.4, MONEY, False),
    (18, "Операционная прибыль, млн руб.", "валовая прибыль − OPEX", "=D16-D17", MONEY, False),
    (19, "Маржинальность прибыли", "прибыль / выручка", "=D18/D15", PCT, False),
]
for r, a, b, f, fmt, cross in pnl:
    set_cell(ws, f"B{r}", a, border=BORDER, font=BOLD if r in (15, 18) else Font())
    set_cell(ws, f"C{r}", b, font=Font(size=9, color="808080"), border=BORDER)
    if r == 17:
        set_cell(ws, f"D{r}", f, font=BLUE_IN, fmt=fmt, border=BORDER, align="right")
    else:
        pure = isinstance(f, str) and f.startswith("=in_")
        set_cell(ws, f"D{r}", f, font=(GREEN_X if (cross or pure) else BLACK_F), fmt=fmt, border=BORDER, align="right")
    if r in (12, 13, 14, 15, 16, 17, 18):
        set_cell(ws, f"E{r}", f"=D{r}*12", font=BLACK_F, fmt=fmt, border=BORDER, align="right")
    else:
        set_cell(ws, f"E{r}", "", border=BORDER)
add_name("asm_OPEX", "'Базовый ОПиУ'!$D$17")
add_name("base_GMVP", "'Базовый ОПиУ'!$D$12")
add_name("base_OTHER", "'Базовый ОПиУ'!$D$14")
add_name("base_PROFIT", "'Базовый ОПиУ'!$D$18")
add_name("base_GP", "'Базовый ОПиУ'!$D$16")
set_cell(ws, "B21", "Обоснование допущения по OPEX (22,4 млн руб./мес ≈ 12,4% выручки): в брифе нет структуры "
                    "расходов, поэтому постоянные OPEX (офис, разработка, поддержка, базовый маркетинг, IT) заданы "
                    "допущением так, чтобы операционная прибыль составляла 10 млн руб./мес (5,6% выручки) — "
                    "правдоподобный уровень для маркетплейса доставки еды после масштабирования. Допущение "
                    "подлежит уточнению с финансовой командой; целевые значения (+300%) не зависят от его уровня: "
                    "при любом OPEX цель формулируется через рост валовой прибыли на +92,6%.",
         font=Font(italic=True, size=9, color="808080"), wrap=True)
ws.merge_cells("B21:E21")
ws.row_dimensions[21].height = 66

# =====================================================================
# Лист: Цель и рычаги
# =====================================================================
ws = wb.create_sheet("Цель и рычаги")
no_grid(ws)
widths(ws, {"A": 2, "B": 46, "C": 16, "D": 16, "E": 16, "F": 52})
set_cell(ws, "B2", "Цель +300% и анализ рычагов роста прибыли", font=TITLE_F)
set_cell(ws, "B4", "Блок 1. Целевые значения", font=SUB_F)
tgt = [
    (5, "Базовая операционная прибыль, млн руб./мес", "=base_PROFIT", MONEY),
    (6, "Целевая прибыль (×4, +300%), млн руб./мес", "=D5*4", MONEY),
    (7, "Требуемая валовая прибыль, млн руб./мес", "=D6+asm_OPEX", MONEY),
    (8, "Требуемый рост валовой прибыли", "=D7/base_GP-1", PCT),
]
for r, a, f, fmt in tgt:
    set_cell(ws, f"B{r}", a, border=BORDER)
    set_cell(ws, f"D{r}", f, fmt=fmt, border=BORDER, align="right", font=BOLD if r == 6 else Font())
set_cell(ws, "B10", "Блок 2. Требуемое изменение каждого рычага ПО ОТДЕЛЬНОСТИ (остальные на базе)", font=SUB_F)
header_row(ws, 11, ["Рычаг", "База", "Требуемое значение", "Изменение", "Оценка реалистичности"])
# D7 = target GP; фактор роста GMV: (targetGP/GM − other)/GMV
tblA = [
    ("Frequency, заказов/мес", "=in_FREQ", f"=in_FREQ*('Цель и рычаги'!$D$7/in_GMPCT-base_OTHER)/base_GMVP", MONEY2,
     "1,2 → 2,39 заказа/мес — физически невозможно без смены модели"),
    ("Средний чек, руб.", "=in_CHECK", f"=in_CHECK*('Цель и рычаги'!$D$7/in_GMPCT-base_OTHER)/base_GMVP", NUM,
     "1 400 → 2 788 руб. (+99%) — нереально на рынке без скидочных войн"),
    ("Активные клиенты, шт", "=in_MAU", f"=in_MAU*('Цель и рычаги'!$D$7/in_GMPCT-base_OTHER)/base_GMVP", NUM,
     "100 000 → 199 167 (+99%) — только платным привлечением при LTV/CAC ≈ 0,4; см. «Анти-сценарий»"),
    ("Gross Margin, %", "=in_GMPCT", "=D7/(base_GMVP+base_OTHER)", PCT,
     "18% → 34,7% (+16,7 п.п.) — за один год недостижимо"),
    ("Прочая выручка, млн руб./мес", "=base_OTHER", "=D7/in_GMPCT-base_GMVP", MONEY,
     "12 → 178,7 млн руб. (×15) — не является продуктовым рычагом"),
]
for i, (a, base_f, req_f, fmt, comm) in enumerate(tblA):
    r = 12 + i
    set_cell(ws, f"B{r}", a, border=BORDER)
    set_cell(ws, f"C{r}", base_f, font=GREEN_X, fmt=fmt, border=BORDER, align="right")
    set_cell(ws, f"D{r}", req_f, fmt=fmt, border=BORDER, align="right")
    set_cell(ws, f"E{r}", f"=D{r}/C{r}-1", fmt=PCT, border=BORDER, align="right")
    set_cell(ws, f"F{r}", comm, font=Font(size=9, color="808080"), border=BORDER, wrap=True)
set_cell(ws, "B18", "Вывод блока 2: ни один рычаг в отдельности не даёт +300% реалистично — цель достигается "
                    "только комбинацией рычагов (см. лист «Сценарий стратегии»).",
         font=Font(italic=True, size=9, color="C00000"), wrap=True)
ws.merge_cells("B18:F18"); ws.row_dimensions[18].height = 28
set_cell(ws, "B20", "Блок 3. Эластичность: эффект роста рычага на 10% (остальные на базе)", font=SUB_F)
header_row(ws, 21, ["Рычаг (+10%)", "Δ валовой прибыли, млн/мес", "Δ прибыли, млн/мес", "Δ прибыли, %", "Эластичность (Δ% прибыли / 10%)"])
tblB = [
    ("Frequency ×1,10", "=0.1*base_GMVP*in_GMPCT"),
    ("Средний чек ×1,10", "=0.1*base_GMVP*in_GMPCT"),
    ("Активные клиенты ×1,10", "=0.1*base_GMVP*in_GMPCT"),
    ("Gross Margin ×1,10 (+1,8 п.п.)", "=0.1*in_GMPCT*(base_GMVP+base_OTHER)"),
    ("Прочая выручка ×1,10", "=0.1*base_OTHER*in_GMPCT"),
]
for i, (a, dgp) in enumerate(tblB):
    r = 22 + i
    set_cell(ws, f"B{r}", a, border=BORDER)
    set_cell(ws, f"C{r}", dgp, fmt=MONEY2, border=BORDER, align="right")
    set_cell(ws, f"D{r}", f"=C{r}", fmt=MONEY2, border=BORDER, align="right")
    set_cell(ws, f"E{r}", f"=D{r}/base_PROFIT", fmt=PCT, border=BORDER, align="right")
    set_cell(ws, f"F{r}", f"=E{r}/0.1", fmt='0.00', border=BORDER, align="right")
set_cell(ws, "B28", "Эластичность клиенто-зависимых рычагов (frequency, чек, база) одинакова — все действуют "
                    "через GMV; маржа эластичнее (действует на всю выручку), но её рост ограничен операционно. "
                    "Численно цель требует произведения факторов ≈ 1,93 к валовой прибыли.",
         font=Font(italic=True, size=9, color="808080"), wrap=True)
ws.merge_cells("B28:F28"); ws.row_dimensions[28].height = 40

# =====================================================================
# Лист: Сценарий стратегии
# =====================================================================
ws = wb.create_sheet("Сценарий стратегии")
no_grid(ws)
widths(ws, {"A": 2, "B": 44, "C": 13, "D": 13, "E": 13, "F": 13, "G": 13, "H": 14})
set_cell(ws, "B2", "Сценарий «повторные заказы»: выход на прибыль ×4 к концу года", font=TITLE_F)
set_cell(ws, "B3", "Драйверы нарастают равномерно по кварталам (линейная рампа). Целевые значения (синие) "
                    "выбраны по стратегии: главный вклад — frequency и маржа, умеренный — база и чек.",
         font=Font(italic=True, size=9, color="808080"))
set_cell(ws, "B5", "Драйверы (значения на конец квартала)", font=SUB_F)
header_row(ws, 6, ["Драйвер", "Q0 (база)", "Q1", "Q2", "Q3", "Q4 (цель)"], start_col=2)
# ширина: B..G
drivers = [
    ("Frequency, заказов/мес", "=in_FREQ", 1.68, MONEY2),
    ("Средний чек, руб.", "=in_CHECK", 1470, NUM),
    ("Gross Margin, %", "=in_GMPCT", 0.22, PCT),
    ("Активные клиенты, шт", "=in_MAU", 112000, NUM),
]
for i, (a, base_f, tgt_v, fmt) in enumerate(drivers):
    r = 7 + i
    set_cell(ws, f"B{r}", a, border=BORDER)
    set_cell(ws, f"C{r}", base_f, font=GREEN_X, fmt=fmt, border=BORDER, align="right")
    for q in range(1, 5):
        col = get_column_letter(3 + q)
        f = f"=C${r}+($G${r}-C${r})*{q}/4"
        if q < 4:
            set_cell(ws, f"{col}{r}", f, fmt=fmt, border=BORDER, align="right")
        else:
            set_cell(ws, f"{col}{r}", tgt_v, font=BLUE_IN, fmt=fmt, border=BORDER, align="right")
    # перезаписать Q1-Q3 формулами относительно C и G (G теперь значение)
    for q in range(1, 4):
        col = get_column_letter(3 + q)
        ws[f"{col}{r}"] = f"=C${r}+($G${r}-C${r})*{q}/4"
set_cell(ws, "B12", "Поквартальный ОПиУ (средние драйверы квартала = середина интервала)", font=SUB_F)
set_cell(ws, "B13", "Статья", font=WHITE_B, fill=HDR_FILL, align="center", border=BORDER)
set_cell(ws, "C13", "", fill=HDR_FILL, border=BORDER)
for q in range(1, 5):
    set_cell(ws, f"{get_column_letter(3 + q)}13", f"Q{q}", font=WHITE_B, fill=HDR_FILL, align="center", border=BORDER)
# средние драйверы квартала в строках 14-17 (скрытая вспомогательная зона, видимая — это нормально)
aux = [
    (14, "Frequency (среднее)", "=({c}7+{p}7)/2", MONEY2),
    (15, "Средний чек (среднее)", "=({c}8+{p}8)/2", NUM),
    (16, "Gross Margin (среднее)", "=({c}9+{p}9)/2", PCT),
    (17, "Активные клиенты (среднее)", "=({c}10+{p}10)/2", NUM),
]
for r, label, tpl, fmt in aux:
    set_cell(ws, f"B{r}", label, font=Font(size=9, color="808080"), border=BORDER)
    for q in range(1, 5):
        col = get_column_letter(3 + q)   # D..G
        prev = get_column_letter(2 + q)  # C..F
        set_cell(ws, f"{col}{r}", tpl.format(c=col, p=prev), fmt=fmt, border=BORDER, align="right",
                 font=Font(size=9, color="808080"))
pnl_q = [
    (18, "Заказы/мес, шт", "={c}17*{c}14", NUM),
    (19, "GMV/мес, млн руб.", "={c}18*{c}15/1000000", MONEY),
    (20, "Выручка/мес, млн руб.", "={c}19+base_OTHER", MONEY),
    (21, "Валовая прибыль/мес, млн руб.", "={c}20*{c}16", MONEY),
    (22, "Операционная прибыль/мес, млн руб.", "={c}21-asm_OPEX", MONEY),
    (23, "Операционная прибыль за квартал, млн руб.", "={c}22*3", MONEY),
]
for r, label, tpl, fmt in pnl_q:
    bold = r in (22, 23)
    set_cell(ws, f"B{r}", label, border=BORDER, font=BOLD if bold else Font())
    for q in range(1, 5):
        col = get_column_letter(3 + q)
        set_cell(ws, f"{col}{r}", tpl.format(c=col), fmt=fmt, border=BORDER, align="right",
                 font=BOLD if bold else Font())
    if r in (20, 21, 23):
        set_cell(ws, f"H{r}", f"=SUM(D{r}:G{r})", fmt=fmt, border=BORDER, align="right", font=BOLD)
    elif r == 22:
        set_cell(ws, f"H{r}", f"=H23/12", fmt=fmt, border=BORDER, align="right", font=BOLD)
    else:
        set_cell(ws, f"H{r}", "", border=BORDER)
set_cell(ws, "H13", "Год", font=WHITE_B, fill=HDR_FILL, align="center", border=BORDER)
set_cell(ws, "B25", "Проверка цели (run-rate на выходе года, по целевым значениям драйверов Q4):",
         font=SUB_F)
set_cell(ws, "B26", "Прибыль/мес по целевым драйверам, млн руб.", border=BORDER)
set_cell(ws, "D26", "=(G10*G7*G8/1000000+base_OTHER)*G9-asm_OPEX", fmt=MONEY, border=BORDER, align="right", font=BOLD)
set_cell(ws, "B27", "Прирост к базе (цель ≥ +300%)", border=BORDER)
set_cell(ws, "D27", "=D26/base_PROFIT-1", fmt=PCT, border=BORDER, align="right", font=BOLD, fill=GOOD_FILL)
set_cell(ws, "F27", "цель достигнута", font=Font(size=9, color="375623"), fill=GOOD_FILL)
set_cell(ws, "B28", "Годовая прибыль в год рампы, млн руб. (≈ +144% к базовому году) — ожидаемо ниже run-rate: "
                    "цель формулируется как выход на ежемесячную прибыль ×4.", font=Font(italic=True, size=9, color="808080"), wrap=True)
ws.merge_cells("B28:H28"); ws.row_dimensions[28].height = 28
# Мост роста
set_cell(ws, "B30", "Мост роста прибыли (месяц, выход на целевые значения; накопительное применение рычагов)",
         font=SUB_F)
header_row(ws, 31, ["Шаг", "Прибыль, млн/мес", "Прирост шага, млн/мес"], start_col=2)
bridge = [
    ("База", "=(base_GMVP+base_OTHER)*in_GMPCT-asm_OPEX"),
    ("+ Frequency ×1,40", "=(base_GMVP*1.4+base_OTHER)*in_GMPCT-asm_OPEX"),
    ("+ Средний чек ×1,05", "=(base_GMVP*1.4*1.05+base_OTHER)*in_GMPCT-asm_OPEX"),
    ("+ Gross Margin → 22%", "=(base_GMVP*1.4*1.05+base_OTHER)*0.22-asm_OPEX"),
    ("+ Клиенты ×1,12", "=(base_GMVP*1.4*1.05*1.12+base_OTHER)*0.22-asm_OPEX"),
]
for i, (a, f) in enumerate(bridge):
    r = 32 + i
    set_cell(ws, f"B{r}", a, border=BORDER, font=BOLD if i == 4 else Font())
    set_cell(ws, f"C{r}", f, fmt=MONEY, border=BORDER, align="right")
    if i == 0:
        set_cell(ws, f"D{r}", "", border=BORDER)
    else:
        set_cell(ws, f"D{r}", f"=C{r}-C{r-1}", fmt=MONEY, border=BORDER, align="right")
set_cell(ws, "B38", "Проверка дерева: любой операционный рычаг (напр., доля вовремя-доставок) ведёт к frequency → "
                    "заказы → GMV → валовая прибыль → операционная прибыль. Цепочка замкнута.",
         font=Font(italic=True, size=9, color="808080"), wrap=True)
ws.merge_cells("B38:H38"); ws.row_dimensions[38].height = 28

chart = BarChart()
chart.type = "col"
chart.title = "Мост роста операционной прибыли, млн руб./мес"
chart.y_axis.title = "млн руб./мес"
chart.height = 8
chart.width = 16
chart.legend = None
data = Reference(ws, min_col=3, min_row=31, max_row=36)
cats = Reference(ws, min_col=2, min_row=32, max_row=36)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "B40")

lchart = LineChart()
lchart.title = "Операционная прибыль по кварталам рампы, млн руб."
lchart.y_axis.title = "млн руб. за квартал"
lchart.height = 8
lchart.width = 16
s = Series(Reference(ws, min_col=4, max_col=7, min_row=23), title="Прибыль за квартал")
s.smooth = False
lchart.append(s)
lchart.set_categories(Reference(ws, min_col=4, max_col=7, min_row=13))
ws.add_chart(lchart, "J40")

# =====================================================================
# Лист: Юнит-экономика
# =====================================================================
ws = wb.create_sheet("Юнит-экономика")
no_grid(ws)
widths(ws, {"A": 2, "B": 52, "C": 16, "D": 16, "E": 16, "F": 16, "G": 40})
set_cell(ws, "B2", "Юнит-экономика клиента: почему привлечение не может быть главным рычагом", font=TITLE_F)
set_cell(ws, "B4", "Блок 1. LTV и CAC (текущие значения)", font=SUB_F)
tbl = [
    (5, "Средняя lifetime клиента, мес", "=1/(1-in_RET)", MONEY2, "при retention 32%/мес"),
    (6, "Заказов за lifetime", "=C5*in_FREQ", MONEY2, "lifetime × frequency"),
    (7, "Средний доход с заказа, руб.", "=in_CHECK+base_OTHER*1000000/in_ORDERS", NUM, "чек + прочая выручка на заказ (100 руб.)"),
    (8, "LTV (валовая прибыль), руб.", "=C6*C7*in_GMPCT", NUM, "заказы × доход × маржа"),
    (9, "CAC (CPA), руб.", "=in_CPA", NUM, "из брифа"),
    (10, "LTV / CAC", "=C8/C9", '0.00', "бенчмарк зрелого бизнеса ≥ 3:1 (McKinsey)"),
    (11, "Окупаемость CAC из GP, мес", "=C9/(in_FREQ*C7*in_GMPCT)", MONEY2, "средний срок жизни клиента — 1,47 мес < 3,7 мес: не окупается"),
]
for r, a, f, fmt, comm in tbl:
    set_cell(ws, f"B{r}", a, border=BORDER, font=BOLD if r == 10 else Font())
    pure = f == "=in_CPA"
    set_cell(ws, f"C{r}", f, font=(GREEN_X if pure else Font()), fmt=fmt, border=BORDER, align="right",
             fill=WARN_FILL if r == 10 else None)
    set_cell(ws, f"D{r}", comm, font=Font(size=9, color="808080"), border=BORDER, wrap=True)
set_cell(ws, "B13", "Блок 2. Чувствительность LTV/CAC к retention и frequency (стратегия — в колонке «+ F=1,68»)",
         font=SUB_F)
header_row(ws, 14, ["Retention", "Lifetime, мес", "LTV, руб. (F=1,2)", "LTV/CAC (F=1,2)", "LTV, руб. (F=1,68)", "LTV/CAC (F=1,68)"], start_col=2)
rets = [0.32, 0.35, 0.40, 0.45, 0.50]
for i, rv in enumerate(rets):
    r = 15 + i
    set_cell(ws, f"B{r}", rv, font=BLUE_IN, fmt=PCT, border=BORDER, align="right")
    set_cell(ws, f"C{r}", f"=1/(1-B{r})", fmt=MONEY2, border=BORDER, align="right")
    set_cell(ws, f"D{r}", f"=C{r}*in_FREQ*$C$7*in_GMPCT", fmt=NUM, border=BORDER, align="right")
    set_cell(ws, f"E{r}", f"=D{r}/in_CPA", fmt='0.00', border=BORDER, align="right")
    set_cell(ws, f"F{r}", f"=C{r}*1.68*$C$7*in_GMPCT", fmt=NUM, border=BORDER, align="right")
    set_cell(ws, f"G{r}", f"=F{r}/in_CPA", fmt='0.00', border=BORDER, align="right",
             fill=GOOD_FILL if rv == 0.40 else None)
set_cell(ws, "B21", "Вывод: даже при retention 50% и frequency 1,68 LTV/CAC ≈ 0,76 — платное привлечение по CPA "
                    "1 200 руб. разрушает стоимость. Параллельно нужно снижать CAC (рост органики с 15%, "
                    "реферальные механики) до ~500 руб., тогда LTV/CAC при целевых метриках превысит 1,9.",
         font=Font(italic=True, size=9, color="808080"), wrap=True)
ws.merge_cells("B21:G21"); ws.row_dimensions[21].height = 42
# --- Компактный анти-сценарий: почему рост через привлечение противоречит стратегии ---
set_cell(ws, "B23", "Почему рост через привлечение противоречит стратегии (мини-анти-сценарий)", font=SUB_F)
tbl4 = [
    (24, "Клиентская база для +300% только привлечением, шт",
     "='Цель и рычаги'!D14", NUM, "тот же фактор 1,99, что и для frequency/чека"),
    (25, "Gross-привлечения (замещение оттока 68%/мес + net-рост), шт/мес",
     "=(1-in_RET)*(in_MAU+C24)/2+(C24-in_MAU)/12", NUM, "оценка снизу: реактивации не учтены"),
    (26, "Маркетинговые затраты, млн руб./мес",
     "=C25*in_CPA/1000000", MONEY, "по CPA 1 200 руб. из брифа"),
    (27, "Прибыль после маркетинга, млн руб./мес",
     "='Цель и рычаги'!D6-C26", MONEY, "убыток: привлечение «в вакууме» даёт цель, в реальности — нет"),
]
for r, a, f, fmt, comm in tbl4:
    set_cell(ws, f"B{r}", a, border=BORDER)
    set_cell(ws, f"C{r}", f, fmt=fmt, border=BORDER, align="right",
             font=BOLD if r == 27 else Font(), fill=WARN_FILL if r == 27 else None)
    set_cell(ws, f"D{r}", comm, font=Font(size=9, color="808080"), border=BORDER, wrap=True)
set_cell(ws, "B29", "Демпинг (GM −3 п.п.):", border=BORDER)
set_cell(ws, "C29", 0.15, font=BLUE_IN, fmt=PCT2, border=BORDER, align="right")
set_cell(ws, "D29", "=(base_GMVP+base_OTHER)*C29-asm_OPEX", fmt=MONEY, border=BORDER, align="right",
         font=BOLD, fill=WARN_FILL)
set_cell(ws, "E29", "прибыль при демпинге, млн руб./мес (−54%)", font=Font(size=9, color="808080"), border=BORDER, wrap=True)

# =====================================================================
# Лист: Источники
# =====================================================================
ws = wb.create_sheet("Источники")
no_grid(ws)
widths(ws, {"A": 2, "B": 56, "C": 70})
set_cell(ws, "B2", "Источники данных и методологии", font=TITLE_F)
header_row(ws, 4, ["Source Name", "Source URL / путь"])
srcs = [
    ("Бриф кейса TechGourmet (все исходные метрики)", "дз 2\\Сервис TechGourmet.md"),
    ("Материалы курса «Стратегия продукта», модуль 2, «Введение»: 4 вопроса анализа бизнес-стратегии", "материалы\\модуль 2\\введение 1.md"),
    ("Материалы курса, модуль 1, «1.4 Бизнес-модель как ограничение стратегии»", "материалы\\модуль 1\\1.4. Бизнес-модель как ограничение стратегии.md"),
    ("McKinsey — Planning for uncertainty: driver-based model from revenue to cash (метод driver-based модели)",
     "https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/planning-for-uncertainty-performance-management-under-covid-19"),
    ("Corporate Finance Institute — Driver-Based Planning in FP&A (драйверы: объём, цена, конверсия, удержание)",
     "https://corporatefinanceinstitute.com/resources/fpa/driver-based-planning-guide/"),
    ("McKinsey — Digitally native brands (бенчмарк LTV:CAC ≥ 3:1 для зрелого бизнеса)",
     "https://www.mckinsey.com/industries/private-capital/our-insights/digitally-native-brands-born-digital-but-ready-to-take-on-the-world"),
]
for i, (n, u) in enumerate(srcs):
    r = 5 + i
    set_cell(ws, f"B{r}", n, border=BORDER, wrap=True)
    c = set_cell(ws, f"C{r}", u, border=BORDER, wrap=True, font=Font(size=9, color="0563C1", underline="single"))
    if u.startswith("http"):
        c.hyperlink = u
    ws.row_dimensions[r].height = 30

# =====================================================================
# Лист: Обложка (первая)
# =====================================================================
ws = wb.create_sheet("Обложка", 0)
no_grid(ws)
widths(ws, {"A": 2, "B": 30, "C": 90})
set_cell(ws, "B2", "ДЗ 2 «От стратегии — к дереву метрик и целям команды»", font=Font(bold=True, size=16, color=ACCENT))
set_cell(ws, "B3", "Часть 1. Анализ стратегии и бизнес-цель — сервис TechGourmet", font=Font(bold=True, size=12))
set_cell(ws, "B4", "Выполнила: Зименкова Софья · сентябрь 2026", font=Font(size=10, color="808080"))
set_cell(ws, "B6", "Ключевые результаты", font=SUB_F)
res = [
    ("Базовая операционная прибыль", "=base_PROFIT", MONEY, "млн руб./мес (driver-based ОПиУ, лист «Базовый ОПиУ»)"),
    ("Целевая прибыль (+300%)", "=base_PROFIT*4", MONEY, "млн руб./мес — выход к концу года"),
    ("Требуемый рост валовой прибыли", "='Цель и рычаги'!D8", PCT, "ни один рычаг отдельно не даёт цели — нужна комбинация"),
    ("Формула цели", None, None, "F ×1,40 · чек ×1,05 · GM 18→22% · клиенты ×1,12 → run-rate +311%"),
    ("LTV/CAC сейчас", "='Юнит-экономика'!C10", '0.00', "привлечение убыточно → рост через повторные заказы"),
]
for i, (a, f, fmt, comm) in enumerate(res):
    r = 7 + i
    set_cell(ws, f"B{r}", a, border=BORDER, font=BOLD)
    if f:
        set_cell(ws, f"C{r}", f, fmt=fmt, border=BORDER, align="left")
    else:
        set_cell(ws, f"C{r}", comm, border=BORDER)
    if f:
        set_cell(ws, f"D{r}", comm, font=Font(size=9, color="808080"), border=BORDER)
widths(ws, {"D": 60})
set_cell(ws, "B14", "Состав книги", font=SUB_F)
toc = [
    ("1. Исходные данные", "все метрики брифа + примечание о расхождении GMV и выручки (168 vs 180 млн руб.)"),
    ("2. Базовый ОПиУ", "упрощённый отчёт о прибылях и убытках на driver-based драйверах (месяц/год)"),
    ("3. Цель и рычаги", "декомпозиция цели +300%; требуемое изменение рычагов по отдельности; эластичность +10%"),
    ("4. Сценарий стратегии", "поквартальная рампа драйверов, проверка run-rate, мост роста прибыли (график)"),
    ("5. Юнит-экономика", "LTV/CAC, чувствительность к retention и frequency, мини-анти-сценарий"),
    ("6. Источники", "бриф, материалы курса, McKinsey, CFI"),
]
for i, (a, b) in enumerate(toc):
    r = 15 + i
    set_cell(ws, f"B{r}", a, border=BORDER, font=BOLD)
    set_cell(ws, f"C{r}", b, font=Font(size=9, color="808080"), border=BORDER)
set_cell(ws, "B23", "Методология", font=SUB_F)
set_cell(ws, "B24", "Driver-based модель (McKinsey; CFI): прибыль собирается из операционных драйверов "
                    "(клиенты × frequency × чек × маржа), а не экстраполяцией прошлых периодов — такая модель "
                    "связывает продуктовые метрики с бизнес-результатом и позволяет считать эластичности рычагов. "
                    "Структура расходов в брифе не дана, поэтому постоянные OPEX заданы допущением (22,4 млн руб./мес).",
         font=Font(size=9, color="808080"), wrap=True)
ws.merge_cells("B24:D24"); ws.row_dimensions[24].height = 56

wb.calculation.fullCalcOnLoad = True
wb.save(r"дз 2\01_Анализ_стратегии.xlsx")
print("saved")
