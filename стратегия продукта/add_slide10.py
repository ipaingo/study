# -*- coding: utf-8 -*-
import zipfile, re, os
from xml.sax.saxutils import escape

SRC = 'Стратегия_Wildberries 1.pptx'
z = zipfile.ZipFile(SRC)
entries = {i.filename: z.read(i.filename) for i in z.infolist()}
infos = {i.filename: i for i in z.infolist()}
head = entries['ppt/slides/slide9.xml'].decode('utf-8')
ROOT = head[head.index('<p:sld'):head.index('<p:cSld>')]

ID = [400]
def shape(x, y, cx, cy, paras):
    ID[0] += 1
    ps = []
    for txt, sz, bold, color, spc_aft in paras:
        b = ' b="1"' if bold else ''
        aft = f'<a:spcAft><a:spcPts val="{spc_aft}"/></a:spcAft>' if spc_aft else '<a:spcAft><a:spcPts val="0"/></a:spcAft>'
        ps.append(
            f'<a:p><a:pPr indent="0" lvl="0" marL="0" marR="0" rtl="0" algn="l">'
            f'<a:lnSpc><a:spcPct val="120000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>{aft}'
            f'<a:buClr><a:srgbClr val="000000"/></a:buClr><a:buSzPts val="1200"/><a:buFont typeface="Arial"/><a:buNone/></a:pPr>'
            f'<a:r><a:rPr{b} lang="en-US" sz="{sz}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>'
            f'<a:t>{escape(txt)}</a:t></a:r>'
            f'<a:endParaRPr{b} sz="{sz}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:endParaRPr></a:p>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ID[0]}" name="Shape{ID[0]}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="0" lIns="0" spcFirstLastPara="1" rIns="0" wrap="square" tIns="0"><a:noAutofit/></a:bodyPr>'
            f'<a:lstStyle/>{"".join(ps)}</p:txBody></p:sp>')

def line(x, y, cx):
    ID[0] += 1
    return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{ID[0]}" name="Line{ID[0]}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="0"/></a:xfrm>'
            f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="9525"><a:solidFill><a:srgbClr val="DDD0E6"/></a:solidFill></a:ln></p:spPr>'
            f'<p:style><a:lnRef idx="2"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="0"><a:schemeClr val="accent1"/></a:fillRef>'
            f'<a:effectRef idx="1"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="tx1"/></a:fontRef></p:style></p:cxnSp>')

COLS = [
 ("Поведение", "Покупатель рассказывает задачу, а не ищет товар",
  [("«Одеть ребёнка в школу за 5 тысяч» — привычный сценарий покупки", 600),
   ("Повторный визит начинается с консультанта, который помнит размеры и бюджет семьи", 600),
   ("«Примерочные» заказы исчезли: выкуп выше, очередей на возвраты меньше", 0)]),
 ("Продукт", "Поисковая строка стала диалогом",
  [("Разговор, 3–5 подходящих вариантов и честный срок «завтра в ПВЗ у дома»", 600),
   ("Реклама отделена от совета: пометка, не больше одной из пяти позиций", 600),
   ("Продавец видит, почему товар не попал в ответ", 0)]),
 ("Бизнес", "Доход сверх комиссии вырос",
  [("Спонсорские рекомендации и рассрочка банка работают внутри совета", 600),
   ("Диалог окупается с запасом, свои GPU на всю аудиторию, включая пики распродаж", 600),
   ("Главная метрика компании и инвесторов — GMV без возвратов на покупателя", 0)]),
 ("Позиция", "№1 удержан: дверь не отнимается",
  [("Знание покупателя не переносится конкурентам и не сгорает со складами", 600),
   ("Ассистенты Ozon и Яндекса вторые: догоняют годы накопленных диалогов", 600),
   ("Перенос карточек, как хотел Минэк, почти не ударил по WB", 0)]),
]

M = 711403
CW = 2554000
GAP = 290000
shapes = []
shapes.append(shape(M, 405994, 6350400, 241500, [("2029 · три года спустя", 1200, True, "A80E8E", 0)]))
shapes.append(shape(M, 797357, 10769700, 711300, [("Wildberries 2029: покупка начинается с разговора, а не с поиска", 2300, True, "241036", 0)]))
xs = [M + i*(CW+GAP) for i in range(4)]
for (label, head, lines), x in zip(COLS, xs):
    shapes.append(shape(x, 1827252, CW, 241500, [(label, 1200, True, "A80E8E", 0)]))
shapes.append(line(M, 2080541, 11087100))
for (label, head, lines), x in zip(COLS, xs):
    shapes.append(shape(x, 2180000, CW, 700000, [(head, 1300, True, "241036", 0)]))
    paras = [(t, 1200, False, "3D2A4F", a) for t, a in lines]
    shapes.append(shape(x, 2920000, CW, 2100000, paras))
shapes.append(line(M, 5150000, 11087100))
footer = [("Каждое изменение заработано развилкой, а не спрогнозировано: ", 1400, True, "241036", 0),
          ("июль 2027, январь и декабрь 2028. Если к декабрю 2028-го картина иная — срабатывает слайд 7: ставка закрывается, GPU уходят в общий ИИ-пул.", 1400, False, "241036", 0)]
shapes.append(shape(M, 5257167, 11087100, 1000000, footer))

slide10 = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r' + ROOT +
           '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
           '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
           + ''.join(shapes) +
           '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>').encode('utf-8')

NOTES = [
 "Это рисунок 2029 года — три года после старта ставки. Это не прогноз, а контракт с самими собой: каждая строка привязана к развилкам роадмапа. Пройдём по четырём измерениям.",
 "Поведение. Покупатель перестал искать товар — он рассказывает задачу. «Одеть ребёнка в школу за пять тысяч» — привычный сценарий, и это то, что конкурент не скопирует баннером. Повторный визит начинается с консультанта, который помнит размеры, бюджет и состав семьи. Сегодняшняя боль — заказы «три размера на примерку»: при выкупе одежды 42% каждый исчезнувший примерочный заказ — это и оставшаяся выручка, и сэкономленная обратная логистика. К 2029-му очередей на возвраты в ПВЗ меньше, а покупатель приходит за советом, а не за скидкой — это важно, потому что рычаг скидки за карту банка слабеет с 1 октября 2026 года по 289-ФЗ.",
 "Продукт. Поисковая строка стала диалогом: разговор, три-пять подходящих вариантов и честный срок «завтра в ПВЗ у дома» — за это нам прощают то, что мы не привозим за час. Реклама отделена от совета: спонсорские места помечены и занимают не больше одной из пяти позиций, поэтому совет без пометки воспринимается как мнение, а не баннер. Продавец видит, почему товар не попал в ответ — конфликт с законом о платформах закрыт прозрачностью по статье 5.",
 "Бизнес. Доход сверх комиссии вырос там, где обещали: спонсорские рекомендации внутри ответа и рассрочка WB Банка внутри совета. Диалог окупается с запасом — по порогу окупаемости не ниже 2, зафиксированному на январской развилке 2028 года. Свои GPU, заказанные в 4 квартале 2026-го с поставкой 36–52 недели, работают на всю аудиторию, включая пики распродаж. Валовой GMV растёт медленнее, чем мог бы — это известная жертва трейд-оффа 2, — зато выкуп выше и склады разгружены. Главная метрика компании и инвесторов — GMV без возвратов на покупателя.",
 "Позиция. WB удержал статус крупнейшего маркетплейса: знание покупателя, накопленное в миллиардах диалогов, не переносится конкурентам и не пострадало ни в одной атаке на склады. Ozon и Яндекс остались быстрее в срочной доставке и сильнее в финтехе, но их ассистенты вторые: они догоняют не функцию, а годы накопленных разговоров. И главное — случился тот сценарий, против которого строилась ставка: карточку разрешили переносить между площадками, как хотел Минэк, — и это почти не ударило по WB, потому что главной дверью оказалось доверие, а не карточка.",
 "Если спросят, откуда уверенность в сроках: ниоткуда, и это честно. Каждый уровень этого слайда нужно заработать пройденным порогом — плюс 2% GMV без возвратов на покупателя и окупаемость не ниже 1 к июлю 2027-го, окупаемость не ниже 2 к январю 2028-го. Если к декабрю 2028 года картина не похожа на эту, срабатывает слайд 7: ставка закрывается, консультант остаётся в том виде, в котором окупается, GPU уходят в общий ИИ-пул, ресурсы — на пересмотр отложенных альтернатив. Этот слайд работает в обе стороны.",
]
n9 = entries['ppt/notesSlides/notesSlide9.xml'].decode('utf-8')
m = re.search(r'(<p:txBody>.*?<a:lstStyle/>)(.*?)(</p:txBody>)', n9, re.S)
assert m, 'notes txBody not found'
paras = ''.join(f'<a:p><a:r><a:t>{escape(t)}</a:t></a:r></a:p>' for t in NOTES)
notes10 = (n9[:m.start()] + m.group(1) + paras + m.group(3) + n9[m.end():]).encode('utf-8')

new = {
 'ppt/slides/slide10.xml': slide10,
 'ppt/slides/_rels/slide10.xml.rels': ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r'
   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout3.xml"/>'
   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide10.xml"/>'
   '</Relationships>').encode('utf-8'),
 'ppt/notesSlides/notesSlide10.xml': notes10,
 'ppt/notesSlides/_rels/notesSlide10.xml.rels': entries['ppt/notesSlides/_rels/notesSlide9.xml.rels'],
}
ct = entries['[Content_Types].xml'].decode('utf-8')
adds = ('<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" PartName="/ppt/slides/slide10.xml"/>'
        '<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml" PartName="/ppt/notesSlides/notesSlide10.xml"/>')
entries['[Content_Types].xml'] = ct.replace('</Types>', adds + '</Types>').encode('utf-8')
rels = entries['ppt/_rels/presentation.xml.rels'].decode('utf-8')
assert 'rId19"' not in rels
entries['ppt/_rels/presentation.xml.rels'] = rels.replace('</Relationships>',
    '<Relationship Id="rId19" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide10.xml"/></Relationships>').encode('utf-8')
pres = entries['ppt/presentation.xml'].decode('utf-8')
entries['ppt/presentation.xml'] = pres.replace('</p:sldIdLst>',
    '<p:sldId id="265" r:id="rId19"/></p:sldIdLst>').encode('utf-8')

out = 'SW1_new.pptx'
zo = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
for name, info in infos.items():
    ni = zipfile.ZipInfo(name, date_time=info.date_time)
    ni.compress_type = info.compress_type
    ni.external_attr = info.external_attr
    zo.writestr(ni, entries[name])
for name, data in new.items():
    zo.writestr(name, data, zipfile.ZIP_DEFLATED)
zo.close()
os.replace(out, SRC)
print('slide 10 added')
