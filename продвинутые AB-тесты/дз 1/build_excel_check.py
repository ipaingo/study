# -*- coding: utf-8 -*-
"""Создаёт workbook с данными preperiod_data.csv и расчётами строго на формулах Excel."""
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CSV = r"D:\Софья Зименкова\учёба\магистратура\study\продвинутые AB-тесты\дз 1\preperiod_data.csv"
OUT = r"D:\Софья Зименкова\учёба\магистратура\study\продвинутые AB-тесты\дз 1\проверка расчетов.xlsx"

df = pd.read_csv(CSV)
n = len(df)  # 83880
first, last = 2, n + 1  # строки данных на листе data

wb = Workbook()

# ---------- Лист data: сырые данные ----------
ws = wb.active
ws.title = "data"
headers = list(df.columns)
ws.append(headers)
for row in df.itertuples(index=False):
    ws.append(list(row))
ws.freeze_panes = "A2"

# ---------- Лист calc: все значения — формулы, ссылающиеся на data ----------
c = wb.create_sheet("calc")
accent = PatternFill("solid", fgColor="1F4E79")
accent_font = Font(color="FFFFFF", bold=True)
header_font = Font(bold=True, size=12)
thin_bottom = Border(bottom=Side(style="thin", color="999999"))

c["B2"] = "Пересчёт в Excel (формулы → лист data) для сверки с выводом ИИ"
c["B2"].font = Font(bold=True, size=14)

c["B4"] = "Сколько строк (COUNT)";                          c["D4"] = f"=COUNT(data!B{first}:B{last})"
c["B5"] = "Среднее revenue на пользователя (AVERAGE)";      c["D5"] = f"=AVERAGE(data!B{first}:B{last})"
c["B6"] = "Ст. отклонение revenue, выборочное (STDEV.S)";   c["D6"] = f"=_xlfn.STDEV.S(data!B{first}:B{last})"
c["B7"] = "Медиана revenue (MEDIAN)";                       c["D7"] = f"=MEDIAN(data!B{first}:B{last})"
c["B8"] = "Доля revenue>0 (COUNTIF/COUNT)";                 c["D8"] = f'=COUNTIF(data!B{first}:B{last},">0")/COUNT(data!B{first}:B{last})'
c["B9"] = "Конверсия orders>0 (COUNTIF/COUNT)";             c["D9"] = f'=COUNTIF(data!C{first}:C{last},">0")/COUNT(data!C{first}:C{last})'
c["B10"] = "Несовпадений: revenue>0 и orders=0";            c["D10"] = f'=COUNTIFS(data!B{first}:B{last},">0",data!C{first}:C{last},"=0")'
c["B11"] = "Несовпадений: orders>0 и revenue=0";            c["D11"] = f'=COUNTIFS(data!C{first}:C{last},">0",data!B{first}:B{last},"=0")'
c["B12"] = "Сумма revenue (SUM)";                           c["D12"] = f"=SUM(data!B{first}:B{last})"
c["B13"] = "Сумма orders (SUM)";                            c["D13"] = f"=SUM(data!C{first}:C{last})"
c["B14"] = "Средний чек на заказ (SUM/SUM)";                c["D14"] = "=D12/D13"
c["B15"] = "Коэфф. вариации (std/среднее)";                 c["D15"] = "=D6/D5"

for r in range(4, 16):
    c.cell(row=r, column=2).border = thin_bottom

# --- Распределения ---
c["B17"] = "Распределения (COUNTIF/COUNT)"
c["B17"].font = header_font
for col_idx, name in ((3, "Значение"), (4, "Число пользователей"), (5, "Доля")):
    cell = c.cell(row=18, column=col_idx, value=name)
    cell.fill = accent; cell.font = accent_font

platforms = [("android", "android"), ("ios", "ios"), ("web", "web")]
countries = [("RU", "RU"), ("KZ", "KZ"), ("BY", "BY"), ("UZ", "UZ")]
isnew = [("TRUE", "True"), ("FALSE", "False")]
blocks = [("platform", "F", platforms), ("country", "G", countries), ("is_new", "H", isnew)]
# COUNTIF не сравнивает булевы TRUE/FALSE с текстовым критерием надёжно → для is_new SUMPRODUCT
r = 19
for bname, dcol, vals in blocks:
    for v, label in vals:
        c.cell(row=r, column=2, value=bname).border = thin_bottom
        c.cell(row=r, column=3, value=label).border = thin_bottom
        if bname == "is_new":
            c.cell(row=r, column=4, value=f"=SUMPRODUCT(--(data!{dcol}{first}:{dcol}{last}={v}))").border = thin_bottom
        else:
            c.cell(row=r, column=4, value=f'=COUNTIF(data!{dcol}{first}:{dcol}{last},"{v}")').border = thin_bottom
        c.cell(row=r, column=5, value=f"=D{r}/$D$4").border = thin_bottom
        r += 1

# --- Ожидания ИИ (входные данные для сверки, из ответа нейросети) ---
c["G4"] = "Ожидание ИИ"
c["G4"].font = accent_font; c["G4"].fill = accent
pairs = [("D5", 1004.34), ("D6", 1746.73), ("D7", 0.00),
         ("D8", 0.4257), ("D9", 0.4257), ("D10", 0), ("D11", 0),
         ("D12", 84243664.77), ("D13", 61244), ("D14", 1375.54), ("D15", 1.74)]
r = 5
c["F4"] = "Ячейка"; c["H4"] = "Значение ИИ"; c["I4"] = "Расхождение"
for col in ("F4", "H4", "I4"):
    c[col].font = accent_font; c[col].fill = accent
for ref, val in pairs:
    c.cell(row=r, column=6, value=ref)
    c.cell(row=r, column=7, value=f"={ref}")
    c.cell(row=r, column=8, value=val)
    r += 1

# --- Расхождения по распределениям ---
c["F18"] = "Доля ИИ"; c["G18"] = "Δ (п.п.)"
for col in ("F18", "G18"):
    c[col].font = accent_font; c[col].fill = accent
ai_shares = [("android", 0.5009), ("ios", 0.4011), ("web", 0.0980),
             ("RU", 0.5473), ("KZ", 0.2017), ("BY", 0.1492), ("UZ", 0.1018),
             ("is_new True", 0.1299), ("is_new False", 0.8701)]
r = 19
for name, v in ai_shares:
    c.cell(row=r, column=6, value=name)
    c.cell(row=r, column=7, value=v)
    c.cell(row=r, column=9, value=f"=E{r}-G{r}")
    r += 1

# ---------- Форматирование ----------
c.sheet_view.showGridLines = False
for r_ in range(5, 16):
    c[f"D{r_}"].number_format = "#,##0.00"
for r_ in (8, 9):
    c[f"D{r_}"].number_format = "0.00%"
c["D4"].number_format = "#,##0"
c["D12"].number_format = "#,##0.00"
c["D13"].number_format = "#,##0"
c["D14"].number_format = "#,##0.00"
c["D15"].number_format = "0.00"
for r_ in range(19, 28):
    c[f"D{r_}"].number_format = "#,##0"
    c[f"E{r_}"].number_format = "0.00%"
    c[f"I{r_}"].number_format = "0.0000%"
for r_ in range(5, 16):
    c[f"G{r_}"].number_format = "#,##0.00" if r_ not in (8, 9) else "0.00%"
    c[f"H{r_}"].number_format = "#,##0.00" if r_ not in (8, 9) else "0.00%"
for r_ in range(19, 28):
    c[f"G{r_}"].number_format = "0.00%"
for col, w in (("A", 3), ("B", 46), ("C", 16), ("D", 22), ("E", 12), ("F", 14), ("G", 16), ("H", 14), ("I", 12)):
    c.column_dimensions[col].width = w

wb.save(OUT)
print("saved:", OUT)
