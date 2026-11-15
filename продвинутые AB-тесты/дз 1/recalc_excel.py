# -*- coding: utf-8 -*-
"""Открывает check_formulas.xlsx в Excel, заставляет пересчитать формулы
и сохраняет значения в check_values.xlsx."""
import os, win32com.client

base = os.path.abspath(".")
src = os.path.join(base, "check_formulas.xlsx")
dst = os.path.join(base, "check_values.xlsx")

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
try:
    wb = excel.Workbooks.Open(src)
    excel.CalculateFullRebuild()
    wb.SaveAs(dst, FileFormat=51)  # xlsx
    wb.Close(False)
finally:
    excel.Quit()
print("recalculated ->", dst)
