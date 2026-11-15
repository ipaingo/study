import re, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn

BASE = '/Users/szime/git/study/стратегия продукта/дз 6'
FILES = [
    '1. Стратегический контекст.md',
    '2. Анализ воронки и гипотеза.md',
    '3. Индикаторы.md',
    '4. Чувствительность и выборка.md',
    '5. Дизайн и окно наблюдения.md',
    '6. MVA и здоровье данных.md',
    '7. Правила решений.md',
    '8. Часть 2. Решение по данным.md',
]

LATEX_MAP = [
    (r'\$\\dfrac\{2973 \+ 3034\}\{2\} = 3003\.5\$', '(2973 + 3034) / 2 = 3003.5'),
    (r'\$\\chi\^2 = \\dfrac\{\{\(2973 - 3003\.5\)\}\^2\}\{3003\.5\} \+ \\dfrac\{\{\(3034 - 3003\.5\)\}\^2\}\{3003\.5\} = 0\.62\$',
     'χ² = (2973 - 3003.5)² / 3003.5 + (3034 - 3003.5)² / 3003.5 = 0.62'),
    (r'\$\\chi\^2\$ = 0\.06', 'χ² = 0.06'),
    (r'\$p_\\text\{объед\} = \\dfrac\{372 \+ 488\}\{2973 \+ 3034\} = 14\.32\\%\$',
     'p_объед = (372 + 488) / (2973 + 3034) = 14.32%'),
    (r'\$z = \\dfrac\{0\.1608 - 0\.1251\}\{\\sqrt\{0\.1432 \\cdot 0\.8568 \\cdot \\frac\{1\}\{2973\} \+ \\frac\{1\}\{3034\}\}\} = 3\.95\$',
     'z = (0.1608 - 0.1251) / √(0.1432 · 0.8568 · (1/2973 + 1/3034)) = 3.95'),
    (r'\$\\pm 1\.96 \\cdot \\sqrt\{0\.1251 \\cdot \\dfrac\{0\.8749\}\{2973\} \+ 0\.1608 \\cdot \\dfrac\{0\.8392\}\{3034\}\} = 95\\%\$',
     '± 1.96 · √(0.1251 · 0.8749/2973 + 0.1608 · 0.8392/3034) = 95%'),
    (r'\$\\alpha\$', 'α'),
]

def latex_to_text(s):
    for pat, rep in LATEX_MAP:
        s = re.sub(pat, rep, s)
    return s

def md_inline(s):
    s = latex_to_text(s)
    s = s.replace('**', '')
    s = re.sub(r'\*([^*]+)\*', r'\1', s)  # курсив -> обычный (стиль документа без выделений)
    return s

doc = Document()

# Поля страницы
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

# Базовый стиль: Arial 12, интервал 1.5
normal = doc.styles['Normal']
normal.font.name = 'Arial'
normal.font.size = Pt(12)
normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
pf = normal.paragraph_format
pf.line_spacing = 1.5
pf.space_after = Pt(6)

for hname, size in [('Heading 1', 16), ('Heading 2', 14), ('Heading 3', 12)]:
    st = doc.styles[hname]
    st.font.name = 'Arial'
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_before = Pt(10)
    st.paragraph_format.space_after = Pt(6)

# Стили списков тоже Arial 12
for lname in ['List Bullet', 'List Bullet 2', 'List Number', 'List Number 2']:
    try:
        st = doc.styles[lname]
        st.font.name = 'Arial'
        st.font.size = Pt(12)
        st.paragraph_format.line_spacing = 1.5
        st.paragraph_format.space_after = Pt(3)
    except KeyError:
        pass

def add_par(text, style=None):
    p = doc.add_paragraph(md_inline(text), style=style)
    return p

def flush_table(rows):
    # rows: list of lists of cell strings
    if not rows:
        return
    header, body = rows[0], rows[1:]
    t = doc.add_table(rows=len(body)+1, cols=len(header))
    t.style = 'Table Grid'
    for j, cell in enumerate(header):
        c = t.rows[0].cells[j]
        c.text = ''
        run = c.paragraphs[0].add_run(md_inline(cell))
        run.bold = True
    for i, row in enumerate(body):
        for j, cell in enumerate(row):
            t.rows[i+1].cells[j].text = md_inline(cell)
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(11)
    doc.add_paragraph('')

first_file = True
for fname in FILES:
    with open(os.path.join(BASE, fname), encoding='utf-8') as f:
        lines = f.read().split('\n')

    i = 0
    in_code = False
    table_rows = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            p = doc.add_paragraph()
            run = p.add_run(line.rstrip())
            run.font.name = 'Courier New'
            run.font.size = Pt(11)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            i += 1
            continue

        # таблица: накапливаем строки
        if stripped.startswith('|'):
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if all(re.fullmatch(r'[:\- ]+', c) for c in cells):
                i += 1
                continue  # разделитель
            table_rows.append(cells)
            i += 1
            continue
        elif table_rows:
            flush_table(table_rows)
            table_rows = []

        if not stripped:
            i += 1
            continue

        # картинки Obsidian
        m = re.match(r'!\[\[(.+?)\]\]', stripped)
        if m:
            img_path = os.path.join(BASE, m.group(1))
            if os.path.exists(img_path):
                doc.add_picture(img_path, width=Cm(14))
            i += 1
            continue

        if stripped.startswith('### '):
            doc.add_heading(md_inline(stripped[4:]), level=3)
        elif stripped.startswith('## '):
            doc.add_heading(md_inline(stripped[3:]), level=2)
        elif stripped.startswith('# '):
            title = md_inline(stripped[2:])
            # из файла 8 убираем номер, делаем заголовком первого уровня
            title = re.sub(r'^8\. Часть 2\. ', 'Часть 2. ', title)
            if not first_file and title.startswith('Часть 2'):
                doc.add_page_break()
            doc.add_heading(title, level=1)
        elif stripped.startswith('> '):
            p = add_par(stripped[2:])
            p.paragraph_format.left_indent = Cm(0.75)
            for run in p.runs:
                run.italic = True
        elif re.match(r'^\d+\.\s', stripped):
            indent = len(line) - len(line.lstrip())
            style = 'List Number 2' if indent > 0 else 'List Number'
            add_par(re.sub(r'^\d+\.\s', '', stripped), style=style)
        elif stripped.startswith('- '):
            indent = len(line) - len(line.lstrip())
            style = 'List Bullet 2' if indent > 0 else 'List Bullet'
            add_par(stripped[2:], style=style)
        else:
            add_par(stripped)
        i += 1
    if table_rows:
        flush_table(table_rows)
        table_rows = []
    first_file = False

out = os.path.join(BASE, 'ДЗ 6. Пакет запуска и решение по результатам AB-теста.docx')
doc.save(out)
print('saved:', out)
