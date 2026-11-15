# -*- coding: utf-8 -*-
"""Строит check.xlsx: лист 'data' с preperiod_data.csv и лист 'calc'
со статистикой, посчитанной ТОЛЬКО формулами Excel (ссылки на data!),
без зашитых чисел."""
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

CSV = "preperiod_data.csv"
N = None  # узнаем после чтения

df = pd.read_csv(CSV)
df["is_new"] = df["is_new"].astype(str)  # True/False -> текст для Excel
n = len(df)
last = n + 1  # последняя строка данных на листе

wb = Workbook()
ws = wb.active
ws.title = "data"

cols = list(df.columns)
ws.append(cols)
for row in df.itertuples(index=False):
    ws.append(list(row))

calc = wb.create_sheet("calc")
L = lambda col: f"data!{col}2:{col}{last}"

rows = [
    ("Показатель", "Значение (формула)"),
    ("Число строк (пользователей)", f"=COUNTA({L('A')})"),
    ("Среднее revenue на пользователя", f"=ROUND(AVERAGE({L('B')}),2)"),
    ("Ст. отклонение revenue (выборочное, STDEV.S)", f"=ROUND(STDEV.S({L('B')}),2)"),
    ("Медиана revenue", f"=MEDIAN({L('B')})"),
    ("Доля платящих (revenue>0), %", f"=ROUND(COUNTIF({L('B')},\">0\")/COUNTA({L('A')})*100,2)"),
    ("Конверсия в заказ (orders>0), %", f"=ROUND(COUNTIF({L('C')},\">0\")/COUNTA({L('A')})*100,2)"),
    ("Число несовпадений revenue>0 vs orders>0",
     f"=SUMPRODUCT((({L('B')}>0)+({L('C')}>0)=1)*1)"),
    ("Сумма revenue", f"=SUM({L('B')})"),
    ("Сумма orders", f"=SUM({L('C')})"),
    ("Средний чек на заказ (revenue/orders)", f"=ROUND(SUM({L('B')})/SUM({L('C')}),2)"),
    ("Коэффициент вариации revenue (std/mean)", f"=ROUND(STDEV.S({L('B')})/AVERAGE({L('B')}),2)"),
    ("", ""),
    ("Распределение platform (доля, %)", ""),
]
for r in rows:
    calc.append(list(r))

start = calc.max_row + 1
for i, val in enumerate(sorted(df["platform"].unique()), start=start):
    calc.cell(row=i, column=1, value=f"platform = {val} (%)")
    calc.cell(row=i, column=2,
              value=f"=ROUND(COUNTIF({L('F')},\"{val}\")/COUNTA({L('A')})*100,2)")

j = start
for val in sorted(df["country"].unique()):
    calc.cell(row=j, column=4, value=f"country = {val} (%)")
    calc.cell(row=j, column=5,
              value=f"=ROUND(COUNTIF({L('G')},\"{val}\")/COUNTA({L('A')})*100,2)")
    j += 1

j = start
for val in ["True", "False"]:
    calc.cell(row=j, column=7, value=f"is_new = {val} (%)")
    calc.cell(row=j, column=8,
              value=f"=ROUND(COUNTIF({L('H')},\"{val}\")/COUNTA({L('A')})*100,2)")
    j += 1

# ожидаемые значения (pandas) — на отдельный лист для сверки
exp = wb.create_sheet("expected_pandas")
exp.append(["Показатель", "Значение (pandas)"])
exp.append(["n", n])
exp.append(["mean_revenue", round(df.revenue.mean(), 2)])
exp.append(["std_revenue_ddof1", round(df.revenue.std(ddof=1), 2)])
exp.append(["median_revenue", df.revenue.median()])
exp.append(["share_paying_%", round((df.revenue > 0).mean() * 100, 2)])
exp.append(["conv_orders_%", round((df.orders > 0).mean() * 100, 2)])
exp.append(["mismatch_rev_vs_orders", int(((df.revenue > 0) != (df.orders > 0)).sum())])
exp.append(["sum_revenue", round(df.revenue.sum(), 2)])
exp.append(["sum_orders", int(df.orders.sum())])
exp.append(["avg_check_per_order", round(df.revenue.sum() / df.orders.sum(), 2)])
exp.append(["cv", round(df.revenue.std(ddof=1) / df.revenue.mean(), 2)])
exp.append(["max_orders_per_user", int(df.orders.max())])
for p in sorted(df.platform.unique()):
    exp.append([f"platform {p} %", round((df.platform == p).mean() * 100, 2)])
for c in sorted(df.country.unique()):
    exp.append([f"country {c} %", round((df.country == c).mean() * 100, 2)])
for v in [True, False]:
    exp.append([f"is_new {v} %", round((df.is_new == str(v)).mean() * 100, 2)])

wb.save("check_formulas.xlsx")
print("saved, rows:", n)
