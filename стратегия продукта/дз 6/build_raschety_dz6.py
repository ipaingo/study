# -*- coding: utf-8 -*-
"""Сборка Расчеты_ДЗ6.xlsx: лист 'Данные' (CSV + неделя) и лист 'Расчеты' (формулы)."""
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = "/Users/szime/git/study/стратегия продукта/дз 6"
CSV = BASE + "/variant2_test_results.csv"
OUT = BASE + "/Расчеты_ДЗ6.xlsx"

wb = Workbook()

# ---------- Лист «Данные» ----------
ws = wb.active
ws.title = "Данные"
ws.sheet_view.showGridLines = False
headers = ["день", "группа", "пользователи_с_экспозицией", "первые_заказы_за_7д", "отменённые_первые_заказы", "неделя"]
for j, h in enumerate(headers, start=1):
    c = ws.cell(row=1, column=j, value=h)
    c.font = Font(bold=True)
with open(CSV, encoding="utf-8") as f:
    rows = list(csv.reader(f, delimiter=";"))[1:]
for i, row in enumerate(rows, start=2):
    ws.cell(row=i, column=1, value=int(row[0]))
    ws.cell(row=i, column=2, value=row[1])
    ws.cell(row=i, column=3, value=int(row[2]))
    ws.cell(row=i, column=4, value=int(row[3]))
    ws.cell(row=i, column=5, value=int(row[4]))
    ws.cell(row=i, column=6, value=f"=INT((A{i}-1)/7)+1")
last = len(rows) + 1  # последняя строка с данными
for col, w in zip("ABCDEF", [8, 14, 26, 22, 28, 10]):
    ws.column_dimensions[col].width = w

# ---------- Лист «Расчеты» ----------
ws = wb.create_sheet("Расчеты")
ws.sheet_view.showGridLines = False

bold = Font(bold=True)
h2 = Font(bold=True, size=12)
title = Font(bold=True, size=14)
pct = "0.00%"
pp = "0.00"
num = "#,##0"

D = "Данные"  # имя листа с данными

def put(r, c, v, fmt=None, b=False):
    cell = ws.cell(row=r, column=c, value=v)
    if fmt: cell_fmt = c
    if fmt: ws.cell(row=r, column=c).number_format = fmt
    if b: ws.cell(row=r, column=c).font = bold
    return ws.cell(row=r, column=c)

ws.cell(row=2, column=2, value="Расчеты по A/B-тесту (часть 2 ДЗ 6, TechGourmet)").font = title
ws.cell(row=3, column=2, value="Все значения считаются формулами из листа «Данные» и мини-таблицы констант ниже.")

# --- Константы ---
r = 5
ws.cell(row=r, column=2, value="Константы (зафиксированы в пакете запуска, часть 1)").font = h2
consts = [
    ("Порог относительного роста primary", 0.20, pct),
    ("Лимит guardrail по отменам (п. п.)", 0.01, pct),
    ("Kill-порог по отменам (п. п.)", 0.03, pct),
    ("z для 95% CI", 1.96, "0.00"),
    ("Порог SRM (p-value)", 0.01, "0.00"),
    ("Последний день набора (созревшие когорты)", 35, num),
    ("День-выброс (контрольная проверка)", 20, num),
]
for i, (label, v, fmt) in enumerate(consts, start=r+1):
    ws.cell(row=i, column=2, value=label)
    ws.cell(row=i, column=3, value=v).number_format = fmt
C_TRESH, C_G1, C_KILL, C_Z, C_SRM, C_DAY, C_OUT = "$C$6", "$C$7", "$C$8", "$C$9", "$C$10", "$C$11", "$C$12"

# --- Совокупности, дни 1-35 ---
r = 13
ws.cell(row=r, column=2, value="Совокупности: созревшие когорты (дни 1-35)").font = h2
ws.cell(row=r+1, column=3, value="A (контроль)").font = bold
ws.cell(row=r+1, column=4, value="B (тест)").font = bold
labels = ["Экспозиции", "Первые заказы", "Отмененные первые заказы"]
cols = ["C", "D", "E"]
for k, (lab, dcol) in enumerate(zip(labels, cols)):
    rr = r + 2 + k
    ws.cell(row=rr, column=2, value=lab)
    ws.cell(row=rr, column=3, value=f"=SUMIFS({D}!{dcol}:{dcol},{D}!$B:$B,\"A (контроль)\",{D}!$A:$A,\"<=\"&{C_DAY})").number_format = num
    ws.cell(row=rr, column=4, value=f"=SUMIFS({D}!{dcol}:{dcol},{D}!$B:$B,\"B (тест)\",{D}!$A:$A,\"<=\"&{C_DAY})").number_format = num
E_A, E_B = "$C$15", "$D$15"   # экспозиции
O_A, O_B = "$C$16", "$D$16"   # заказы
X_A, X_B = "$C$17", "$D$17"   # отмены

# --- SRM ---
r = 19
ws.cell(row=r, column=2, value="SRM (хи-квадрат против 50/50)").font = h2
ws.cell(row=r+1, column=2, value="Ожидаемое число на группу")
ws.cell(row=r+1, column=3, value=f"=({E_A}+{E_B})/2").number_format = num
ws.cell(row=r+2, column=2, value="Хи-квадрат")
ws.cell(row=r+2, column=3, value=f"=({E_A}-C{r+1})^2/C{r+1}+({E_B}-C{r+1})^2/C{r+1}").number_format = "0.000"
ws.cell(row=r+3, column=2, value="p-value")
ws.cell(row=r+3, column=3, value=f"=CHISQ.DIST.RT(C{r+2},1)").number_format = "0.000"
ws.cell(row=r+4, column=2, value="Вывод")
ws.cell(row=r+4, column=3, value=f"=IF(C{r+3}<{C_SRM},\"SRM ОБНАРУЖЕН\",\"SRM нет, сплит корректен\")").font = bold

# --- Primary ---
r = 25
ws.cell(row=r, column=2, value="Primary-метрика: конверсия в первый заказ за 7 дней (созревшие когорты)").font = h2
ws.cell(row=r+1, column=2, value="Конверсия")
ws.cell(row=r+1, column=3, value=f"={O_A}/{E_A}").number_format = pct
ws.cell(row=r+1, column=4, value=f"={O_B}/{E_B}").number_format = pct
CR_A, CR_B = "$C$26", "$D$26"
ws.cell(row=r+2, column=2, value="Абсолютная разница (п. п.)")
ws.cell(row=r+2, column=3, value=f"=({CR_B}-{CR_A})*100").number_format = pp
ws.cell(row=r+3, column=2, value="Относительный рост")
ws.cell(row=r+3, column=3, value=f"={CR_B}/{CR_A}-1").number_format = pct
ws.cell(row=r+4, column=2, value="Объединенная доля (для z)")
ws.cell(row=r+4, column=3, value=f"=({O_A}+{O_B})/({E_A}+{E_B})").number_format = pct
ws.cell(row=r+5, column=2, value="SE (z-критерий)")
ws.cell(row=r+5, column=3, value=f"=SQRT(C{r+4}*(1-C{r+4})*(1/{E_A}+1/{E_B}))").number_format = "0.00000"
ws.cell(row=r+6, column=2, value="z")
ws.cell(row=r+6, column=3, value=f"=({CR_B}-{CR_A})/C{r+5}").number_format = "0.00"
ws.cell(row=r+7, column=2, value="p-value (двусторонний)")
ws.cell(row=r+7, column=3, value=f"=2*(1-NORM.S.DIST(C{r+6},TRUE))").number_format = "0.00000"
ws.cell(row=r+8, column=2, value="SE разности (для CI)")
ws.cell(row=r+8, column=3, value=f"=SQRT({CR_A}*(1-{CR_A})/{E_A}+{CR_B}*(1-{CR_B})/{E_B})").number_format = "0.00000"
ws.cell(row=r+9, column=2, value="95% CI разницы, нижняя (п. п.)")
ws.cell(row=r+9, column=3, value=f"=(({CR_B}-{CR_A})-{C_Z}*C{r+8})*100").number_format = pp
ws.cell(row=r+10, column=2, value="95% CI разницы, верхняя (п. п.)")
ws.cell(row=r+10, column=3, value=f"=(({CR_B}-{CR_A})+{C_Z}*C{r+8})*100").number_format = pp
ws.cell(row=r+11, column=2, value="95% CI относительного эффекта, нижняя")
ws.cell(row=r+11, column=3, value=f"=(({CR_B}-{CR_A})-{C_Z}*C{r+8})/{CR_A}").number_format = pct
ws.cell(row=r+12, column=2, value="95% CI относительного эффекта, верхняя")
ws.cell(row=r+12, column=3, value=f"=(({CR_B}-{CR_A})+{C_Z}*C{r+8})/{CR_A}").number_format = pct
ws.cell(row=r+13, column=2, value="Порог +20% пройден точечно?")
ws.cell(row=r+13, column=3, value=f"=IF(C{r+3}>={C_TRESH},\"да\",\"нет\")").font = bold

# --- Guardrail по отменам ---
r = 40
ws.cell(row=r, column=2, value="Guardrail: доля отмененных первых заказов (базис: отмены / все первые заказы группы)").font = h2
ws.cell(row=r+1, column=2, value="Доля отмен")
ws.cell(row=r+1, column=3, value=f"={X_A}/{O_A}").number_format = pct
ws.cell(row=r+1, column=4, value=f"={X_B}/{O_B}").number_format = pct
ws.cell(row=r+2, column=2, value="Разница (п. п.)")
ws.cell(row=r+2, column=3, value=f"=($D${r+1}-$C${r+1})*100").number_format = pp
ws.cell(row=r+3, column=2, value="Проверка лимита +1 п. п.")
ws.cell(row=r+3, column=3, value=f"=IF($D${r+1}-$C${r+1}<={C_G1},\"в норме\",\"НАРУШЕН\")").font = bold
ws.cell(row=r+4, column=2, value="Проверка Kill-порога +3 п. п.")
ws.cell(row=r+4, column=3, value=f"=IF($D${r+1}-$C${r+1}>={C_KILL},\"KILL\",\"Kill не требуется\")").font = bold
ws.cell(row=r+5, column=2, value="Объединенная доля отмен (для z)")
ws.cell(row=r+5, column=3, value=f"=({X_A}+{X_B})/({O_A}+{O_B})").number_format = pct
ws.cell(row=r+6, column=2, value="z (разница отмен)")
ws.cell(row=r+6, column=3, value=f"=($D${r+1}-$C${r+1})/SQRT(C{r+5}*(1-C{r+5})*(1/{O_A}+1/{O_B}))").number_format = "0.00"
ws.cell(row=r+7, column=2, value="p-value (двусторонний)")
ws.cell(row=r+7, column=3, value=f"=2*(1-NORM.S.DIST(C{r+6},TRUE))").number_format = "0.000"

# --- Контроль: без дня 20 ---
r = 49
ws.cell(row=r, column=2, value="Контроль устойчивости: группа B без выброса (день 20)").font = h2
ws.cell(row=r+1, column=2, value="B: экспозиции без дня 20")
ws.cell(row=r+1, column=3, value=f"={E_B}-SUMIFS({D}!C:C,{D}!$B:$B,\"B (тест)\",{D}!$A:$A,{C_OUT})").number_format = num
ws.cell(row=r+2, column=2, value="B: первые заказы без дня 20")
ws.cell(row=r+2, column=3, value=f"={O_B}-SUMIFS({D}!D:D,{D}!$B:$B,\"B (тест)\",{D}!$A:$A,{C_OUT})").number_format = num
ws.cell(row=r+3, column=2, value="Конверсия B без дня 20")
ws.cell(row=r+3, column=3, value=f"=C{r+2}/C{r+1}").number_format = pct
ws.cell(row=r+4, column=2, value="Относительный рост к контролю")
ws.cell(row=r+4, column=3, value=f"=C{r+3}/{CR_A}-1").number_format = pct

# --- Контрольный расчет: все 42 дня ---
r = 55
ws.cell(row=r, column=2, value="Контрольный расчет: все 42 дня (для сравнения; primary считается по созревшим когортам)").font = h2
ws.cell(row=r+1, column=3, value="A (контроль)").font = bold
ws.cell(row=r+1, column=4, value="B (тест)").font = bold
ws.cell(row=r+2, column=2, value="Экспозиции")
ws.cell(row=r+2, column=3, value=f"=SUMIFS({D}!C:C,{D}!$B:$B,\"A (контроль)\")").number_format = num
ws.cell(row=r+2, column=4, value=f"=SUMIFS({D}!C:C,{D}!$B:$B,\"B (тест)\")").number_format = num
ws.cell(row=r+3, column=2, value="Первые заказы")
ws.cell(row=r+3, column=3, value=f"=SUMIFS({D}!D:D,{D}!$B:$B,\"A (контроль)\")").number_format = num
ws.cell(row=r+3, column=4, value=f"=SUMIFS({D}!D:D,{D}!$B:$B,\"B (тест)\")").number_format = num
ws.cell(row=r+4, column=2, value="Отмененные первые заказы")
ws.cell(row=r+4, column=3, value=f"=SUMIFS({D}!E:E,{D}!$B:$B,\"A (контроль)\")").number_format = num
ws.cell(row=r+4, column=4, value=f"=SUMIFS({D}!E:E,{D}!$B:$B,\"B (тест)\")").number_format = num
ws.cell(row=r+5, column=2, value="Конверсия")
ws.cell(row=r+5, column=3, value=f"=C{r+3}/C{r+2}").number_format = pct
ws.cell(row=r+5, column=4, value=f"=D{r+3}/D{r+2}").number_format = pct
ws.cell(row=r+6, column=2, value="Относительный рост")
ws.cell(row=r+6, column=3, value=f"=D{r+5}/C{r+5}-1").number_format = pct
ws.cell(row=r+7, column=2, value="Доля отмен")
ws.cell(row=r+7, column=3, value=f"=C{r+4}/C{r+3}").number_format = pct
ws.cell(row=r+7, column=4, value=f"=D{r+4}/D{r+3}").number_format = pct
ws.cell(row=r+8, column=2, value="Разница отмен (п. п.)")
ws.cell(row=r+8, column=3, value=f"=(D{r+7}-C{r+7})*100").number_format = pp

# --- Понедельный разрез ---
r = 65
ws.cell(row=r, column=2, value="Понедельный разрез (созревшие когорты, недели 1-5)").font = h2
heads = ["Неделя", "A: экспозиции", "A: заказы", "A: конверсия", "B: экспозиции", "B: заказы", "B: конверсия", "Разница (п. п.)"]
for j, h in enumerate(heads, start=2):
    ws.cell(row=r+1, column=j, value=h).font = bold
for wk in range(1, 6):
    rr = r + 1 + wk
    ws.cell(row=rr, column=2, value=wk)
    ws.cell(row=rr, column=3, value=f"=SUMIFS({D}!C:C,{D}!$B:$B,\"A (контроль)\",{D}!$F:$F,$B{rr})").number_format = num
    ws.cell(row=rr, column=4, value=f"=SUMIFS({D}!D:D,{D}!$B:$B,\"A (контроль)\",{D}!$F:$F,$B{rr})").number_format = num
    ws.cell(row=rr, column=5, value=f"=D{rr}/C{rr}").number_format = pct
    ws.cell(row=rr, column=6, value=f"=SUMIFS({D}!C:C,{D}!$B:$B,\"B (тест)\",{D}!$F:$F,$B{rr})").number_format = num
    ws.cell(row=rr, column=7, value=f"=SUMIFS({D}!D:D,{D}!$B:$B,\"B (тест)\",{D}!$F:$F,$B{rr})").number_format = num
    ws.cell(row=rr, column=8, value=f"=G{rr}/F{rr}").number_format = pct
    ws.cell(row=rr, column=9, value=f"=(H{rr}-E{rr})*100").number_format = pp

ws.cell(row=r+8, column=2, value="Источник данных: variant2_test_results.csv (сырые результаты эксперимента из условия ДЗ 6). Итог: primary пройден точечно, guardrail по отменам нарушен -> исход Adapt.")

# ширины
widths = {"A": 2, "B": 52, "C": 16, "D": 14, "E": 14, "F": 14, "G": 12, "H": 14, "I": 14}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

wb.properties.creator = "Софья Зименкова"
wb.properties.lastModifiedBy = "Софья Зименкова"
wb.properties.title = "ДЗ 6. Расчеты по результатам A/B-теста (TechGourmet)"

wb.save(OUT)
print("saved:", OUT)
