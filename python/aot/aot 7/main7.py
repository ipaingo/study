import graphviz
import stanza
import time

nlp = stanza.Pipeline('ru', download_method=False, warnings=False)

dict_transition = dict()

dict_upos = dict()

dict_translate = {
    "ADP": "Предлог",
    "ADJ": "Прилагательное",
    "NOUN": "Существительное",
    "VERB": "Глагол",
    "NUM": "Число",
    "CCONJ": "Союз",
    "PRON": "Местоимение",
    "ADV": "Наречие",
}


def uposify(upos):
    if upos == "PROPN":
        return "NOUN"
    if upos == "DET":
        return "PRON"
    if upos == "SCONJ":
        return "CCONJ"
    if upos == "AUX":
        return "VERB"
    return upos


# filename = str(input("Путь до файла: "))
filename = "text_short.txt"
with open(filename, "r", encoding="utf-8") as file:
    text = file.read()

time_start = time.time()
doc = nlp(text)
print("\nDone processing!")
print(f"Time spent: {time.time() - time_start}")
count = 0
for sentence in doc.sentences:
    words = sentence.words
    for word in sentence.words:
        upos1 = uposify(word.upos)
        if upos1 not in ["PUNCT", "SYM", "PART"]:
            if upos1 not in dict_transition:
                dict_transition[upos1] = dict()
            if word.head != 0 and words[word.head - 1].upos not in ["PUNCT", "SYM", "PART"]:
                word2 = words[word.head - 1]

                upos2 = uposify(word2.upos)

                if upos2 not in dict_transition[upos1]:
                    dict_transition[upos1][upos2] = 1
                else:
                    dict_transition[upos1][upos2] += 1
                count += 1


for k, v in dict_transition.items():
    for k1, v1 in v.items():
        dict_transition[k][k1] = v1 / count

for k, v in dict_transition.items():
    for k1, v1 in v.items():
        if f"{k}|{k1}" not in dict_upos:
            dict_upos[f"{k}|{k1}"] = v1
        else:
            dict_upos[f"{k}|{k1}"] += v1

dict_upos = list(reversed(sorted(dict_upos.items(), key=lambda x: x[1])))

count = 0
for i in dict_upos:
    a, b = i[0].split("|")

    print(f"{dict_translate[a]} -> {dict_translate[b]}: {i[1]}")
    count += 1
    if count == 5:
        break

dot = graphviz.Digraph(comment="Uposes", strict=True, engine="circo")
for k, v in dict_transition.items():
    dot.node(dict_translate[k])
    for k1, v1 in v.items():
        dot.node(dict_translate[k1])
        dot.edge(dict_translate[k], dict_translate[k1], label="{:.5f}".format(v1))

dot.render('doctest-output/upos.png').replace('\\', '/')
