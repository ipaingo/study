# -*- coding: utf-8 -*-
"""Аналитическая база для ДЗ 4 «Анализ первых результатов» (СКЛАДИО, Q1)."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ---------- стили ----------
H1 = Font(bold=True, size=14)
H2 = Font(bold=True, size=12)
HDR = Font(bold=True, color="FFFFFF")
HDRFILL = PatternFill("solid", fgColor="1F4E79")
ASSUMFILL = PatternFill("solid", fgColor="FFF2CC")   # допущения — жёлтые
TOTFILL = PatternFill("solid", fgColor="D9E2F3")
WARNFILL = PatternFill("solid", fgColor="F8CBAD")
THIN = Border(*[Side(style="thin", color="BFBFBF")]*4)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

def style_header(ws, row, cols):
    for c in range(1, cols+1):
        cell = ws.cell(row=row, column=c)
        cell.font = HDR; cell.fill = HDRFILL; cell.border = THIN; cell.alignment = CENTER

def fmt_money(cell): cell.number_format = '# ##0'
def fmt_pct(cell):   cell.number_format = '0%'
def fmt_num1(cell):  cell.number_format = '0,0'

# =========================================================
# Лист 1. ФАКТ Q1 — расчёты по каналам
# =========================================================
ws = wb.active
ws.title = "1. Факт Q1 — расчёты"
ws["A1"] = "Факт первого квартала по данным кейса (модуль 4) — все производные показатели считаются формулами"
ws["A1"].font = H1
ws["A2"] = "ACV = 1,5 млн ₽ · валовая маржа 80% (ДЗ 3) → валовая прибыль с клиента 100 000 ₽/мес · лимит CAC payback ≤ 12 мес → потолок CAC = 1,2 млн ₽"
ws["A2"].font = Font(italic=True, size=10)

headers = ["Канал","Бюджет, ₽","MQL","CPL, ₽ (факт кейса)",
           "Конверсия MQL→SQL","SQL (расчёт)","Стоимость SQL, ₽",
           "Сделки за квартал","Стоимость закрытой сделки, ₽",
           "Пайплайн (потенц. сделки)","Вероятность закрытия пайплайна",
           "Ожидаемые сделки (закр. + пайплайн×p)","Стоимость сделки с учётом пайплайна, ₽"]
HR = 4
for j,h in enumerate(headers,1): ws.cell(row=HR, column=j, value=h)
style_header(ws, HR, len(headers))

# данные: канал, бюджет, MQL, CPL из кейса, CR MQL→SQL, сделки, пайплайн
data = [
    ("Директ",                3200000, 210, 15200, 0.34, 4, 8),
    ("Вебинары",              4500000, 620, 7260,  0.12, 1, 11),
    ("Контент",               2100000, 180, 11600, 0.41, 3, 9),
    ("Отраслевая конференция",5000000,  40, 125000,0.55, 2, 6),
    ("ABM (25 аккаунтов)",    2300000,  None, None, None, 1, 4),
    ("Email nurturing",        400000,  None, None, None, 3, 7),
]
R0 = HR+1
for i,(name,bud,mql,cpl,cr,deals,pipe) in enumerate(data):
    r = R0+i
    ws.cell(row=r, column=1, value=name).border = THIN
    ws.cell(row=r, column=2, value=bud).border = THIN; fmt_money(ws.cell(row=r,column=2))
    ws.cell(row=r, column=3, value=mql if mql is not None else "н/п*").border = THIN
    ws.cell(row=r, column=4, value=cpl if cpl is not None else "—").border = THIN
    fmt_money(ws.cell(row=r,column=4))
    ws.cell(row=r, column=5, value=cr if cr is not None else "—").border = THIN
    if cr is not None: fmt_pct(ws.cell(row=r,column=5))
    # SQL = MQL * CR
    if mql is not None:
        ws.cell(row=r, column=6, value=f"=C{r}*E{r}").border = THIN; fmt_num1(ws.cell(row=r,column=6))
        ws.cell(row=r, column=7, value=f"=B{r}/F{r}").border = THIN; fmt_money(ws.cell(row=r,column=7))
    else:
        ws.cell(row=r, column=6, value="—").border = THIN
        ws.cell(row=r, column=7, value="—").border = THIN
    ws.cell(row=r, column=8, value=deals).border = THIN
    ws.cell(row=r, column=9, value=f"=B{r}/H{r}").border = THIN; fmt_money(ws.cell(row=r,column=9))
    ws.cell(row=r, column=10, value=pipe).border = THIN
    # вероятность — ссылка на ячейку допущения
    ws.cell(row=r, column=11, value=f"=$C${R0+len(data)+2}").border = THIN; fmt_pct(ws.cell(row=r,column=11))
    ws.cell(row=r, column=12, value=f"=H{r}+J{r}*K{r}").border = THIN; fmt_num1(ws.cell(row=r,column=12))
    ws.cell(row=r, column=13, value=f"=B{r}/L{r}").border = THIN; fmt_money(ws.cell(row=r,column=13))

# строка ИТОГО
rT = R0+len(data)
ws.cell(row=rT, column=1, value="ИТОГО (6 каналов)").font = Font(bold=True)
ws.cell(row=rT, column=2, value=f"=SUM(B{R0}:B{rT-1})").font = Font(bold=True); fmt_money(ws.cell(row=rT,column=2))
ws.cell(row=rT, column=3, value=f"=SUM(C{R0}:C{R0+3})").font = Font(bold=True)  # MQL только 4 канала
ws.cell(row=rT, column=6, value=f"=SUM(F{R0}:F{R0+3})").font = Font(bold=True); fmt_num1(ws.cell(row=rT,column=6))
ws.cell(row=rT, column=7, value=f"=B{rT}/F{rT}").font = Font(bold=True); fmt_money(ws.cell(row=rT,column=7))
ws.cell(row=rT, column=8, value=f"=SUM(H{R0}:H{rT-1})").font = Font(bold=True)
ws.cell(row=rT, column=9, value=f"=B{rT}/H{rT}").font = Font(bold=True); fmt_money(ws.cell(row=rT,column=9))
ws.cell(row=rT, column=10, value=f"=SUM(J{R0}:J{rT-1})").font = Font(bold=True)
ws.cell(row=rT, column=12, value=f"=SUM(L{R0}:L{rT-1})").font = Font(bold=True); fmt_num1(ws.cell(row=rT,column=12))
ws.cell(row=rT, column=13, value=f"=B{rT}/L{rT}").font = Font(bold=True); fmt_money(ws.cell(row=rT,column=13))
for c in range(1,14): ws.cell(row=rT,column=c).fill = TOTFILL; ws.cell(row=rT,column=c).border = THIN

# допущение о вероятности
rA = rT+2
ws.cell(row=rA, column=1, value="Допущение: вероятность закрытия сделки из пайплайна p =").font = Font(bold=True)
pcell = ws.cell(row=rA, column=3, value=0.20); pcell.fill = ASSUMFILL; fmt_pct(pcell); pcell.border = THIN
ws.cell(row=rA, column=4, value="конверсия SQL→сделка ~20% из ДЗ 2 (пайплайн = сделки на стадии SQL/демо). Допущение, не факт кейса — меняя ячейку C, пересчитываются столбцы K–M.").font = Font(italic=True, size=9)
ws.cell(row=rA+1, column=1, value="* н/п — для ABM единица измерения «вовлечённые аккаунты» (12), для email — реактивация старых MQL; MQL→SQL по ним в кейсе не задана.").font = Font(italic=True, size=9)
ws.cell(row=rA+2, column=1, value="⚠ Чек сделок с конференции и ABM ВЫШЕ среднего (1,5 млн ₽) — сопоставлять «стоимость сделки» этих каналов с другими можно только с этой поправкой.").font = Font(bold=True, size=10)
ws.cell(row=rA+2, column=1).fill = WARNFILL

widths = [24,13,9,13,12,11,14,10,16,13,13,15,17]
for j,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = "B5"

# =========================================================
# Лист 2. План Q1 из ДЗ 3 + отклонения
# =========================================================
ws2 = wb.create_sheet("2. План Q1 (ДЗ 3) и отклонения")
ws2["A1"] = "План для сравнения: медиаплан ДЗ 3 (78 млн ₽/год). В кейсе модуля 4 плана нет — это ДОПУЩЕНИЕ."
ws2["A1"].font = H1
ws2["A2"] = "Два варианта плановой базы: А — по календарному плану ДЗ 3 (январь–март), Б — равные квартальные доли (год/4)."
ws2["A2"].font = Font(italic=True, size=10)

headers2 = ["Канал (кейс модуля 4)","Факт бюджет Q1, ₽",
            "План А: календарь ДЗ 3 (янв–мар), ₽","Отклонение А, ₽","Отклонение А, %",
            "План Б: год/4, ₽","Отклонение Б, ₽","Отклонение Б, %","Комментарий"]
HR2 = 4
for j,h in enumerate(headers2,1): ws2.cell(row=HR2, column=j, value=h)
style_header(ws2, HR2, len(headers2))

# (канал, факт, план_А, план_Б, комментарий)  — ₽
plan_rows = [
    ("Директ",                3200000, 2200000, 2500000, "План А = 0,6+0,7+0,9 млн (янв–март). Перерасход: +1,0 млн (+45%)."),
    ("Вебинары",              4500000, 2200000, 3000000, "План А = 0+1,0+1,2 млн (старт с февраля). Перерасход: +2,3 млн (~+105%)."),
    ("Контент",               2100000, 4900000, 3000000, "Сопоставлено с «Контент-маркетинг + SEO»: 3,0+1,9=4,9 (А) или (12+10)/4=5,5 (Б). Без SEO: 3,0 млн — тогда недобор −0,9 млн (−30%)."),
    ("Отраслевая конференция",5000000, 2000000, 3000000, "План А: конференция №1 только в марте (2,0 млн). Перерасход: +3,0 млн (+150%)."),
    ("ABM",                   2300000,  500000, 1500000, "План А: пилот 5 аккаунтов с марта. Перерасход: +1,8 млн (×4,6 к плану А)."),
    ("Email nurturing",        400000,  975000,  625000, "Сопоставлено с «Email + CRM»: 0,6+0,375=0,975 (А). Email only: 0,625 (Б). Недобор ≈ −0,2…−0,6 млн."),
]
R20 = HR2+1
for i,(name,fact,pa,pb,comm) in enumerate(plan_rows):
    r = R20+i
    ws2.cell(row=r, column=1, value=name).border = THIN
    ws2.cell(row=r, column=2, value=fact).border = THIN; fmt_money(ws2.cell(row=r,column=2))
    ws2.cell(row=r, column=3, value=pa).border = THIN; fmt_money(ws2.cell(row=r,column=3))
    ws2.cell(row=r, column=4, value=f"=B{r}-C{r}").border = THIN; fmt_money(ws2.cell(row=r,column=4))
    ws2.cell(row=r, column=5, value=f"=D{r}/C{r}").border = THIN; fmt_pct(ws2.cell(row=r,column=5))
    ws2.cell(row=r, column=6, value=pb).border = THIN; fmt_money(ws2.cell(row=r,column=6))
    ws2.cell(row=r, column=7, value=f"=B{r}-F{r}").border = THIN; fmt_money(ws2.cell(row=r,column=7))
    ws2.cell(row=r, column=8, value=f"=G{r}/F{r}").border = THIN; fmt_pct(ws2.cell(row=r,column=8))
    c = ws2.cell(row=r, column=9, value=comm); c.border = THIN; c.alignment = WRAP; c.font = Font(size=9)
    ws2.row_dimensions[r].height = 42

rT2 = R20+len(plan_rows)
ws2.cell(row=rT2, column=1, value="ИТОГО по 6 каналам").font = Font(bold=True)
for col,letter in [(2,"B"),(3,"C"),(4,"D"),(6,"F"),(7,"G")]:
    ws2.cell(row=rT2, column=col, value=f"=SUM({letter}{R20}:{letter}{rT2-1})").font = Font(bold=True)
    fmt_money(ws2.cell(row=rT2, column=col))
ws2.cell(row=rT2, column=5, value=f"=D{rT2}/C{rT2}").font = Font(bold=True); fmt_pct(ws2.cell(row=rT2, column=5))
ws2.cell(row=rT2, column=8, value=f"=G{rT2}/F{rT2}").font = Font(bold=True); fmt_pct(ws2.cell(row=rT2, column=8))
for c in range(1,10): ws2.cell(row=rT2,column=c).fill = TOTFILL; ws2.cell(row=rT2,column=c).border = THIN

rr = rT2+2
notes = [
 ("Важно: факт квартала 17,5 млн ₽ против плана А 12,8 млн (по 6 каналам) — перерасход ~+4,7 млн (+37%), при этом часть каналов недобирает по лидам.", False),
 ("Каналы плана, для которых в кейсе нет прямого факта: Ретаргетинг (0,7 млн в Q1 по плану А), Резерв (0 в Q1), SEO входит в «Контент».", False),
 ("Фактический бюджет квартала 17,5 млн ₽ в годовом темпе = 70 млн ₽/год — это 90% годового плана 78 млн; ритм расхода выше планового, сезонность ДЗ 3 предполагала пик в Q4.", False),
 ("Отклонения бюджета ≠ отклонения результата: у конференции и ABM перерасход, но выше средний чек и самая высокая конверсия MQL→SQL (55%); у вебинаров перерасход + дешёвый CPL 7 260 ₽, но конверсия всего 12% и нецелевые MQL.", True),
]
for i,(txt,warn) in enumerate(notes):
    cell = ws2.cell(row=rr+i, column=1, value=txt)
    cell.font = Font(bold=warn, size=9, color="9C0006" if warn else "000000")
    if warn: cell.fill = WARNFILL

w2 = [24,14,17,13,11,14,13,11,60]
for j,w in enumerate(w2,1): ws2.column_dimensions[get_column_letter(j)].width = w
ws2.freeze_panes = "B5"

# =========================================================
# Лист 3. Контекст для проверки ИИ
# =========================================================
ws3 = wb.create_sheet("3. Контекст для проверки ИИ")
ws3["A1"] = "Контекст кейса: факты, которые нельзя нарушать при проверке выводов Kimi K2.8"
ws3["A1"].font = H1

facts = [
 ("№","Факт / ограничение","Как использовать при верификации ИИ"),
 (1,"Цикл сделки 3,5 месяца","Лиды конца квартала физически не успели стать сделками. Вывод «канал неэффективен» только по закрытым сделкам — ошибка; обязателен анализ пайплайна. Ожидаемые сделки = закрытые + пайплайн × p (p — допущение, не факт)."),
 (2,"Чек сделок с конференции и ABM ВЫШЕ среднего (ACV 1,5 млн ₽)","Нельзя сравнивать «стоимость сделки» конференции (1,56 млн с учётом пайплайна) с контентом (0,44 млн) без поправки на чек: у конференции/ABM ROAS может быть выше при большей стоимости сделки."),
 (3,"Часть MQL с вебинаров нецелевая: склады < 1 000 м², контакт не ЛПР","Гипотеза «вебинары дают много MQL, но мало SQL» должна опираться на это, а не на абстрактное «канал холодный». CPL 7 260 ₽ дёшев, но это цена НЕцелевых лидов — сравнение CPL без учёта качества некорректно."),
 (4,"60% закрытых сделок квартала — по лидам прошлых периодов","Закрытые сделки слабо отражают текущий квартал: 60% результатов «наследованы». Корректная оценка канала = сделки + пайплайн текущего периода. Полный эффект текущих кампаний проявится через квартал-полтора."),
 (5,"ACV = 1 500 000 ₽/год, валовая маржа 80% (ДЗ 3) → валовая прибыль 100 000 ₽/мес с клиента","Потолок CAC при payback ≤ 12 мес = 1,2 млн ₽. Стоимость закрытой сделки квартала (все каналы) = 17,5/14 = 1,25 млн ₽ — на грани лимита; с учётом пайплайна (17,5/(14+45×0,2) ≈ 0,76 млн) — внутри лимита. Вывод «экономика нарушена» по одним закрытым сделкам неверен."),
 (6,"Бюджет квартала 17,5 млн ₽ (сумма по 6 каналам факта)","Контрольная сумма: 3,2+4,5+2,1+5,0+2,3+0,4 = 17,5 млн ₽. Любые расчёты «среднего CPL» и «средней стоимости сделки» должны сходиться с этой суммой."),
 (7,"Плановая база — ДОПУЩЕНИЕ из ДЗ 3 (в кейсе модуля 4 плана нет)","Отклонения «план/факт» считаются от медиаплана 78 млн ₽/год. ИИ не должен трактовать их как факты кейса; допустимы обе базы: календарный Q1 (12,8 млн по 6 каналам) и равные доли год/4 (13,4 млн)."),
 (8,"Годовой темп факта ≈ 70 млн ₽ (17,5 × 4)","При сезонности плана ДЗ 3 (пик Q4) это быстрый старт года; но перераспределение внутри квартала сильное: конференции +150%, ABM ×4,6 к плану, контент/email недобор."),
 (9,"Конверсия MQL→SQL по каналам факта: Директ 34%, вебинары 12%, контент 41%, конференция 55%","Бенчмарк из ДЗ 3 — 18% (база) / 20% (цель). Контент и конференция выше бенчмарка, Директ выше, вебинары вдвое ниже. Средневзвешенная по 4 каналам ≈ 242/1050 ≈ 23%."),
 (10,"Воронка начинается с лидов; регистрация на вебинар ≠ MQL ≠ SQL ≠ сделка","ИИ не должен складывать MQL разных каналов с разными определениями как однородную величину; ABM и email в кейсе измеряются не в MQL."),
 (11,"Сделки из пайплайна не являются закрытыми и не приносят выручку до закрытия","Нельзя приписывать каналу ARR от потенциальных сделок; можно оценивать ожидаемый ARR = ожид. сделки × ACV с явной пометкой «ожидание»."),
]
r = 3
for i,(n,f,u) in enumerate(facts):
    if i==0:
        for j,h in enumerate(facts[0],1): ws3.cell(row=r, column=j, value=h)
        style_header(ws3, r, 3); r += 1; continue
    ws3.cell(row=r, column=1, value=n).border = THIN
    c = ws3.cell(row=r, column=2, value=f); c.border = THIN; c.alignment = WRAP; c.font = Font(bold=True, size=10)
    c = ws3.cell(row=r, column=3, value=u); c.border = THIN; c.alignment = WRAP; c.font = Font(size=10)
    ws3.row_dimensions[r].height = 52
    r += 1

r += 1
ws3.cell(row=r, column=1, value="Типичные ошибки ИИ, на которые проверять в первую очередь:").font = H2
errs = [
 "• Судить вебинары только по дешевизне CPL (7 260 ₽) и объявлять их лучшим каналом, игнорируя CR 12% и нецелевые MQL.",
 "• Объявлять конференцию неэффективной из-за CPL 125 000 ₽ и всего 40 MQL, игнорируя CR 55%, 6 сделок в пайплайне и повышенный чек.",
 "• Игнорировать цикл 3,5 мес и «списывать» каналы по числу закрытых сделок за квартал (особенно ABM: 1 сделка + 4 крупных в пайплайне).",
 "• Забыть поправку 60% сделок от старых лидов — и приписать все 14 сделок текущему кварталу кампаний.",
 "• Сравнивать «стоимость сделки» каналов без поправки на разный чек (конференция/ABM > средний).",
 "• Выдумывать плановые показатели вместо пометки «допущение из ДЗ 3».",
]
for i,e in enumerate(errs):
    ws3.cell(row=r+1+i, column=1, value=e).font = Font(size=10, color="9C0006")

for j,w in [(1,4),(2,44),(3,95)]:
    ws3.column_dimensions[get_column_letter(j)].width = w

# =========================================================
# Лист 4. Сводные выводы (числа для слайдов)
# =========================================================
ws4 = wb.create_sheet("4. Сводка для слайдов")
ws4["A1"] = "Сводные показатели квартала (все значения — формулы со листа 1)"
ws4["A1"].font = H1
summary = [
 ("Показатель","Значение","Комментарий"),
 ("Бюджет квартала, все каналы", "='1. Факт Q1 — расчёты'!B11", "факт кейса, контрольная сумма 17,5 млн ₽"),
 ("MQL всего (4 канала с измеримым MQL)", "='1. Факт Q1 — расчёты'!C11", "ABM — аккаунты, email — реактивация"),
 ("SQL всего (расчёт)", "='1. Факт Q1 — расчёты'!F11", "≈242 — близко к плану ДЗ 3 ~161 SQL/кв (644/год)"),
 ("Средняя конверсия MQL→SQL", "='1. Факт Q1 — расчёты'!F11/'1. Факт Q1 — расчёты'!C11", "выше бенчмарка 18% из ДЗ 3, но расслоение по каналам огромное: 12–55%"),
 ("Стоимость SQL, средняя (4 канала)", "='1. Факт Q1 — расчёты'!G11", "диапазон по каналам: 28 тыс (контент) — 227 тыс (конференция)"),
 ("Закрытые сделки", "='1. Факт Q1 — расчёты'!H11", "60% из них — по лидам прошлых периодов"),
 ("Стоимость закрытой сделки", "='1. Факт Q1 — расчёты'!I11", "≈1,25 млн ₽ — на грани лимита CAC 1,2 млн при payback 12 мес"),
 ("Сделки в пайплайне", "='1. Факт Q1 — расчёты'!J11", "45 потенциальных сделок ждут закрытия"),
 ("Ожидаемые сделки (пайплайн × 20%)", "='1. Факт Q1 — расчёты'!L11", "ожидание, не факт"),
 ("Стоимость сделки с учётом пайплайна", "='1. Факт Q1 — расчёты'!M11", "≈0,76 млн ₽ → payback ≈ 7,6 мес — внутри лимита"),
 ("Новый ARR минимум (14 сделок × ACV)", "=14*1500000", "≥21 млн ₽; реально выше из-за чеков конференции/ABM; часть — заслуга прошлых периодов"),
 ("ROMI квартала (min)", "=14*1500000/17500000", ">100% по минимальной оценке"),
]
r = 3
for i,row in enumerate(summary):
    if i==0:
        for j,h in enumerate(row,1): ws4.cell(row=r, column=j, value=h)
        style_header(ws4, r, 3); r += 1; continue
    ws4.cell(row=r, column=1, value=row[0]).border = THIN
    c = ws4.cell(row=r, column=2, value=row[1]); c.border = THIN
    if "MQL→SQL" in row[0] or "ROMI" in row[0]: fmt_pct(c)
    else: fmt_money(c)
    c = ws4.cell(row=r, column=3, value=row[2]); c.border = THIN; c.alignment = WRAP; c.font = Font(size=9)
    ws4.row_dimensions[r].height = 28
    r += 1
for j,w in [(1,40),(2,16),(3,70)]:
    ws4.column_dimensions[get_column_letter(j)].width = w

wb.save("дз 4/аналитическая_база_Q1.xlsx")
print("OK — дз 4/аналитическая_база_Q1.xlsx")
