# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference, Series
from openpyxl.chart.marker import Marker
from openpyxl.chart.axis import ChartLines
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

FN = 'Сфера_Пульс_графики.xlsx'
OUT = '_staging.xlsx'
wb = openpyxl.load_workbook(FN)   # 6 старых чартов openpyxl не сохранит — пересоздаём ниже
if 'Дашборд' in wb.sheetnames:    # повторный запуск: пересобираем лист заново
    del wb['Дашборд']
src = wb['Пульс. Графики']
G = "'Пульс. Графики'"

# ---------- 0. Вспомогательные колонки на листе «Пульс. Графики» ----------
src['L3'] = 'Выручка, млн ₽'; src['M3'] = 'План, млн ₽'
src['N3'] = 'План-факт, %';   src['O3'] = 'Цель, %'
for r in range(4, 28):
    src.cell(r, 12).value = '=D%d/1000000' % r
    src.cell(r, 13).value = '=E%d/1000000' % r
    src.cell(r, 14).value = '=D%d/E%d*100' % (r, r)
    src.cell(r, 15).value = 100

# ---------- 1. Лист «Дашборд» ----------
dash = wb.create_sheet('Дашборд', 0)
dash.sheet_view.showGridLines = False
dash.sheet_properties.tabColor = '217346'

GREEN_D, GREEN_L = '1E7A3C', 'E7F2EA'
GRAY, LGRAY = '595959', 'F5F5F5'
thin = Side(style='thin', color='D9D9D9')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

for col in range(1, 15):
    dash.column_dimensions[get_column_letter(col)].width = 10.5

dash['B1'] = '="Сфера · Дашборд продукта «"&%s!B1&"» · январь 2024 — декабрь 2025"' % G
dash['B1'].font = Font(size=16, bold=True, color='1F3864')
dash.row_dimensions[1].height = 24
dash['N1'] = 'PoC «Сферы» · данные из 6 систем · гранулярность: месяц'
dash['N1'].font = Font(size=9, italic=True, color=GRAY)
dash['N1'].alignment = Alignment(horizontal='right')

# Вердикт
dash.merge_cells('B2:M3')
dash['B2'] = ('="ВЫВОД ЗА 30 СЕКУНД: продукт эффективен и развивается. Прибылен весь 2025 год '
              '(средняя маржа "&TEXT(AVERAGE(' + G + '!F16:F27),"0,0")&"%"), план выручки выполнен на "'
              '&TEXT(SUM(' + G + '!D16:D27)/SUM(' + G + '!E16:E27)*100,"0,0")&"%", аудитория выросла в "'
              '&TEXT(' + G + '!B27/' + G + '!B4,"0,0")&" раза, удержание и разработка растут."')
dash['B2'].font = Font(size=12, bold=True, color='0B3D1E')
dash['B2'].fill = PatternFill('solid', fgColor=GREEN_L)
dash['B2'].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
for row in dash['B2:M3']:
    for c in row:
        c.border = border
dash.row_dimensions[2].height = 20
dash.row_dimensions[3].height = 20

# ---------- 2. KPI-карточки ----------
cards = [
    ('МАРЖА, ср. 2025', '=AVERAGE(%s!F16:F27)' % G, '0.0"%"', '2024: −22,3% → весь 2025 в плюсе'),
    ('ПЛАН-ФАКТ 2025', '=SUM(%s!D16:D27)/SUM(%s!E16:E27)*100' % (G, G), '0.0"%"', 'Σвыручка / Σплан за 12 мес.'),
    ('РОСТ АУДИТОРИИ', '=%s!B27/%s!B4' % (G, G), '"×"0.0', '+290% за 24 месяца'),
    ('УДЕРЖАНИЕ M1', '=AVERAGE(%s!K16:K27)-AVERAGE(%s!K4:K15)' % (G, G), '+0.0" п.п.";-0.0" п.п."', 'ср. 2025 против ср. 2024'),
    ('КОММИТЫ', '=AVERAGE(%s!G16:G27)/AVERAGE(%s!G4:G15)-1' % (G, G), '+0%;-0%', 'ср./мес, 2025 к 2024'),
    ('ДЕПЛОИ В ПРОД', '=AVERAGE(%s!H16:H27)/AVERAGE(%s!H4:H15)-1' % (G, G), '+0%;-0%', 'ср./мес, 2025 к 2024'),
]
dash.row_dimensions[5].height = 14
dash.row_dimensions[6].height = 30
dash.row_dimensions[7].height = 13
for i, (label, formula, fmt, sub) in enumerate(cards):
    c1 = get_column_letter(2 + i * 2)
    c2 = get_column_letter(3 + i * 2)
    dash.merge_cells('%s5:%s5' % (c1, c2))
    dash.merge_cells('%s6:%s6' % (c1, c2))
    dash.merge_cells('%s7:%s7' % (c1, c2))
    L, V, S = dash['%s5' % c1], dash['%s6' % c1], dash['%s7' % c1]
    L.value = label; V.value = formula; S.value = sub
    L.font = Font(size=8, bold=True, color=GRAY)
    V.font = Font(size=20, bold=True, color=GREEN_D)
    V.number_format = fmt
    S.font = Font(size=8, color=GRAY)
    for rng in ('%s5:%s5' % (c1, c2), '%s6:%s6' % (c1, c2), '%s7:%s7' % (c1, c2)):
        for row in dash[rng]:
            for c in row:
                c.fill = PatternFill('solid', fgColor=LGRAY)
                c.border = border
    L.alignment = Alignment(horizontal='center')
    V.alignment = Alignment(horizontal='center')
    S.alignment = Alignment(horizontal='center')

# ---------- 3. Графики ----------
from openpyxl.chart.text import RichText
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties

C_GREEN  = '2E8B57'   # маржа / выручка
C_BLUE   = '6B8FC7'   # MAU / коммиты / план-факт
C_ORANGE = 'C08552'   # платящие / деплои
C_PURPLE = '8A7CA8'   # retention
C_GRAY   = '808080'   # план / цель
C_DARK   = '3B3B3B'

def style_line(s, color, width=14000, dash=None, marker=False):
    s.graphicalProperties.line.solidFill = color
    s.graphicalProperties.line.width = width
    if dash:
        s.graphicalProperties.line.dashStyle = dash
    s.smooth = False
    if marker:
        s.marker = Marker(symbol='circle', size=3)
        s.marker.graphicalProperties.solidFill = color

def soft_title(ch, text):
    ch.title = text
    p = ch.title.tx.rich.p[0]
    p.pPr = ParagraphProperties(defRPr=CharacterProperties(sz=1000, b=False, solidFill=C_DARK))

def soft_legend(ch):
    ch.legend.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(
        defRPr=CharacterProperties(sz=800, solidFill='595959')))])

def soft_axes(ch):
    ch.y_axis.majorGridlines = ChartLines(spPr=GraphicalProperties(
        ln=LineProperties(solidFill='E9E9E9', w=6350)))
    ch.y_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill='BFBFBF', w=9525))
    ch.x_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill='BFBFBF', w=9525))
    ch.x_axis.tickLblSkip = 3
    ch.x_axis.tickMarkSkip = 3
    ch.x_axis.majorTickMark = 'none'
    ch.y_axis.majorTickMark = 'out'

def base_chart(title):
    ch = LineChart()
    soft_title(ch, title)
    ch.height, ch.width = 7.4, 11.9
    ch.legend.position = 'b'
    soft_legend(ch)
    soft_axes(ch)
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.style = 2
    return ch

cats = Reference(src, min_col=1, min_row=4, max_row=27)

# 1. Маржа
ch1 = base_chart('Маржа в % выручки — выход в плюс, тренд +5,1 п.п./мес')
s = Series(Reference(src, min_col=6, min_row=3, max_row=27), title='Маржа, %')
style_line(s, C_GREEN); ch1.append(s); ch1.set_categories(cats)
dash.add_chart(ch1, 'B9')

# 2. Выручка vs план (bar план + line факт)
ch2 = BarChart(); ch2.type = 'col'
soft_title(ch2, 'Выручка против плана, млн ₽ — план выполнен (2025: 100,9%)')
ch2.height, ch2.width = 7.4, 11.9
ch2.legend.position = 'b'; soft_legend(ch2); soft_axes(ch2); ch2.gapWidth = 100
bar = Series(Reference(src, min_col=13, min_row=3, max_row=27), title='План, млн ₽')
bar.graphicalProperties.solidFill = 'DBDBDB'
ch2.append(bar)
ln = LineChart()
ln.x_axis.delete = True; ln.y_axis.delete = True
s = Series(Reference(src, min_col=12, min_row=3, max_row=27), title='Выручка, млн ₽')
style_line(s, C_GREEN); ln.append(s)
ch2 += ln
ch2.set_categories(cats)
dash.add_chart(ch2, 'H9')

# 3. План-факт, % + цель 100
ch3 = base_chart('Выполнение плана по месяцам, % — цель 100%')
s = Series(Reference(src, min_col=14, min_row=3, max_row=27), title='План-факт, %')
style_line(s, C_BLUE); ch3.append(s)
s = Series(Reference(src, min_col=15, min_row=3, max_row=27), title='Цель 100%')
style_line(s, C_GRAY, width=12700, dash='dash'); ch3.append(s)
ch3.set_categories(cats)
dash.add_chart(ch3, 'B25')

# 4. MAU + платящие (две оси)
ch4 = base_chart('Аудитория: MAU (слева) и платящие (справа)')
s = Series(Reference(src, min_col=2, min_row=3, max_row=27), title='MAU')
style_line(s, C_BLUE); ch4.append(s)
ch4.set_categories(cats)
ch4b = LineChart()
s = Series(Reference(src, min_col=3, min_row=3, max_row=27), title='Платящие')
style_line(s, C_ORANGE); ch4b.append(s)
ch4b.x_axis.delete = True
ch4b.y_axis.axId = 200
ch4b.y_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill='D9C8B8', w=9525))
ch4.y_axis.crosses = 'autoZero'
ch4 += ch4b
dash.add_chart(ch4, 'H25')

# 5. Коммиты + деплои (две оси)
ch5 = base_chart('Разработка: коммиты (слева) и деплои в прод (справа) — живая инженерия')
s = Series(Reference(src, min_col=7, min_row=3, max_row=27), title='Коммиты')
style_line(s, C_BLUE); ch5.append(s)
ch5.set_categories(cats)
ch5b = LineChart()
s = Series(Reference(src, min_col=8, min_row=3, max_row=27), title='Деплои в прод')
style_line(s, C_ORANGE); ch5b.append(s)
ch5b.x_axis.delete = True
ch5b.y_axis.axId = 200
ch5b.y_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill='D9C8B8', w=9525))
ch5.y_axis.crosses = 'autoZero'
ch5 += ch5b
dash.add_chart(ch5, 'B41')

# 6. Retention
ch6 = base_chart('Удержание: Retention M1, % — растёт вместе с аудиторией')
s = Series(Reference(src, min_col=11, min_row=3, max_row=27), title='Retention M1, %')
style_line(s, C_PURPLE); ch6.append(s)
ch6.set_categories(cats)
dash.add_chart(ch6, 'H41')

# ---------- 4. Подвал ----------
dash.merge_cells('B57:M58')
dash['B57'] = ('Какие решения помогает принимать дашборд: 1) обосновать продолжение инвестиций и запрос ресурса на удержание '
               '(запрос владельца продукта); 2) контролировать выполнение плана ежемесячно, а не раз в год на защите бюджета; '
               '3) замечать отклонения сразу — например, декабрь-2025: 95,7% плана.')
dash['B57'].font = Font(size=9, color=GRAY)
dash['B57'].alignment = Alignment(wrap_text=True, vertical='top')

dash.page_setup.orientation = 'landscape'
dash.page_setup.fitToWidth = 1
dash.page_setup.fitToHeight = 1
dash.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
dash.print_area = 'A1:N58'

# ---------- 5. Графики Kimi на «Пульс. Графики» сохраняются openpyxl при пересохранении — не трогаем ----------

wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print('Дашборд собран, файл сохранён')
