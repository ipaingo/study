# Вставка кэшированных значений <v> в ячейки с формулами,
# чтобы любой просмотрщик видел вычисленные числа.
import zipfile, shutil, re, os

PATH = "/Users/szime/git/study/стратегия продукта/дз 5/ДЗ5_Приоритизация_Зименкова_М08-502_Таблица.xlsx"
TMP = "/tmp/dz5_patched.xlsx"

values = {}

# --- Исходные данные: I18..I35 (чел-нед) ---
effort = [16, 48, 42, 12, 32, 40, 4, 12, 48, 64, 12, 4, 24, 12, 30, 3, 15, 3]
for i, v in enumerate(effort):
    values[("Исходные данные", f"I{18+i}")] = v

# --- RICE: J20..J37, K20..K37, L20..L37 ---
rice_k = [468.75, 937.5, 2142.857142857143, 131.25, 281.25, 87.5, 11250, 67.5,
          312.5, 0, 2083.333333333333, 337.5, 208.3333333333333, 729.1666666666667,
          0, 375, 1666.666666666667, 375]
rice_l = [7, 5, 2, 14, 12, 15, 1, 16, 11, 17, 3, 10, 13, 6, 17, 8, 4, 8]
for i in range(18):
    r = 20 + i
    values[("RICE", f"J{r}")] = effort[i]
    values[("RICE", f"K{r}")] = rice_k[i]
    values[("RICE", f"L{r}")] = rice_l[i]

# --- Искажения RICE ---
values[("Искажения RICE", "D5")] = 312.5
values[("Искажения RICE", "D6")] = 0
values[("Искажения RICE", "D7")] = 0
values[("Искажения RICE", "D8")] = 1666.666666666667
values[("Искажения RICE", "D9")] = 729.1666666666667
values[("Искажения RICE", "D10")] = 937.5
values[("Искажения RICE", "E5")] = 31.25
values[("Искажения RICE", "E7")] = 1666.666666666667
values[("Искажения RICE", "E9")] = 2.1

# --- План квартала: смета ---
values[("План квартала", "E61")] = 61.1
values[("План квартала", "E62")] = 18.9
values[("План квартала", "E63")] = 2.9

# --- RICE: мини-таблица F5..F16 ---
for coord, v in [("F5", 100000), ("F6", 120000), ("F7", 10800), ("F8", 7000),
                 ("F11", 0.15), ("F12", 0.25), ("F13", 0.35), ("F14", 0.45),
                 ("F15", 0.6), ("F16", 0.8)]:
    values[("RICE", coord)] = v

# --- RICE: D-формулы (=$F$5 / =$F$7 / =$F$8) ---
d_formulas = {"D20": 100000, "D21": 100000, "D22": 100000, "D23": 7000,
              "D26": 100000, "D27": 10800, "D30": 100000, "D31": 10800,
              "D34": 100000, "D36": 100000}
for coord, v in d_formulas.items():
    values[("RICE", coord)] = v

# --- RICE: H20..H37 (множители Confidence) ---
h_vals = [0.15, 0.15, 0.45, 0.45, 0.15, 0.35, 0.45, 0.15, 0.15, 0.15,
          0.25, 0.25, 0.25, 0.35, 0.25, 0.15, 0.25, 0.15]
for i, v in enumerate(h_vals):
    values[("RICE", f"H{20+i}")] = v

# карта: имя листа -> xml-файл
zin = zipfile.ZipFile(PATH)
wbxml = zin.read("xl/workbook.xml").decode("utf-8")
rels = zin.read("xl/_rels/workbook.xml.rels").decode("utf-8")
sheet_rid = dict(re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wbxml))
rid_target = {}
for tag in re.findall(r'<Relationship [^>]+/>', rels):
    m_id = re.search(r'Id="(rId\d+)"', tag)
    m_t = re.search(r'Target="([^"]+)"', tag)
    if m_id and m_t:
        rid_target[m_id.group(1)] = m_t.group(1)
def norm_target(t):
    t = t.lstrip("/")
    return t if t.startswith("xl/") else "xl/" + t
sheet_file = {name: norm_target(rid_target[rid]) for name, rid in sheet_rid.items()}

# группируем правки по файлам
by_file = {}
for (sheet, coord), val in values.items():
    by_file.setdefault(sheet_file[sheet], {})[coord] = val

def fmt(v):
    if isinstance(v, int) or (isinstance(v, float) and v == int(v)):
        return str(int(v))
    return repr(round(v, 10))

new_contents = {}
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename in by_file:
        xml = data.decode("utf-8")
        for coord, val in by_file[item.filename].items():
            # ячейка с формулой: <c r="K20" ...><f>...</f></c> -> добавить <v>
            pat = re.compile(r'(<c r="%s"[^>]*>)(<f>.*?</f>)(?:<v>.*?</v>)?(</c>)' % coord)
            m = pat.search(xml)
            if not m:
                print("!! не найдена формула:", item.filename, coord)
                continue
            xml = xml[:m.start()] + m.group(1) + m.group(2) + "<v>%s</v>" % fmt(val) + m.group(3) + xml[m.end():]
        data = xml.encode("utf-8")
    new_contents[item.filename] = (item, data)
zin.close()

with zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED) as zout:
    for fname, (item, data) in new_contents.items():
        zout.writestr(item, data)

shutil.move(TMP, PATH)
print("patched OK")
