# извините... она возможно не запустится без своей venv... но venv весит 300 мегабайт :(
# я для такого случая оставила картинки и сохранила вывод из консоли в файлик.

import spacy
import pymorphy3
import matplotlib.pyplot as plt
import networkx as nx

# загрузка модели.
nlp = spacy.load("ru_core_news_sm")
morph = pymorphy3.MorphAnalyzer(lang='ru')

# парсим самодельные грамматические основы.
gr_basis = []
with open('basis.txt', 'r', encoding="utf-8") as go:
    for line in go:
        bases = line.rstrip().split(",")
        subject_list = []
        predicate_list = []
        for base in bases:
            subject = base.split("-")[0].split()
            predicate = base.split("-")[1].split()
            for p in subject:
                subject_list.append(p)
            for s in predicate:
                predicate_list.append(s)
        subject_sort = sorted(subject_list)
        predicate_sort = sorted(predicate_list)
        gr_basis.append([subject_sort, predicate_sort])

f = open("cottage.txt", "r", encoding="utf-8")
text = f.read()

# парсим текст с помощью модели.
doc = nlp(text)
sentences = [sent.text for sent in doc.sents]

# находим подлежащее и сказуемое.
lib_gr_basis = []
# дательный, творительный, родительный, предложный.
wrong_case = ['datv', 'ablt', 'gent', 'loct']

for sentence in doc.sents:
    subject = []
    predicate = []
    for token in sentence:
        case = morph.parse(token.text)[0].tag.case
        # ROOT - корень.
        # nsubj - подлежащее глагола.
        if (token.dep_ == "nsubj" or token.dep_ == "nsubj:pass") and (case not in wrong_case or case == 'loct') and case != None:
            subject.append(token.text)
        if token.dep_ == "conj" and token.pos_ == "NOUN" and case != None and case not in wrong_case:
            subject.append(token.text)
        if token.dep_ == "nmod" and token.pos_ == "ADJ" and case == "nomn" and case not in wrong_case:
            subject.append(token.text)
        if token.dep_ == "ROOT" and case not in wrong_case and token.pos_ == "NOUN":
            subject.append(token.text)
        if token.dep_ == "obj" and case not in wrong_case and token.pos_ == "PROPN":
            subject.append(token.text)

        if token.dep_ == "ROOT" and case not in wrong_case and token.pos_ != "NOUN" and token.text[-2:] != "сь":
            predicate.append(token.text)
        if token.dep_ == "conj" and token.pos_ in ["VERB", "ADJ"] and case not in wrong_case and token.text[-2:] != "сь"\
                and token.text[-2:] not in ["ый", "ий", "ая", "яя", "ое", "ее"]:
            predicate.append(token.text)
        if token.dep_ == "cop" and token.pos_ == "AUX" and case not in wrong_case and token.text[-2:] != "сь":
            predicate.append(token.text)
        if token.dep_ == "ccomp" and token.pos_ == "VERB" and case not in wrong_case and token.text[-2:] != "сь":
            predicate.append(token.text)
        if token.dep_ == "parataxis" and token.pos_ == "VERB" and case not in wrong_case and token.text[-2:] != "сь":
            predicate.append(token.text)
        # сказуемое в первом лице.
        if token.dep_ == "obj" and token.pos_ == "VERB" and case == None and token.text[-2:] != "сь":
            predicate.append(token.text)

        # инфинитив.
        if token.dep_ == "xcomp" and case not in wrong_case:
            predicate.append(token.text)
    subj_sort = sorted(subject)
    pred_sort = sorted(predicate)
    lib_gr_basis.append([subj_sort, pred_sort])

count = 0
for i in range(len(lib_gr_basis)):
    if lib_gr_basis[i] == gr_basis[i]:
        # совпадает с самодельным разбором.
        print("O: ", lib_gr_basis[i], " ------- ", gr_basis[i])
        count += 1
    else:
        # есть расхождения.
        print("X: ", lib_gr_basis[i], " ------- ", gr_basis[i])

print("---------------------")
print(count)
print("Точность работы: ", str(round(count/58, 2)))
print("---------------------")

# вывод предложений, по которым будем строить графы.
for sentence in doc.sents:
    print(sentence)
    for token in sentence:
        print(token.text, token.dep_, token.tag_, token.pos_, morph.parse(token.text)[0].tag.case)
    print()

# собственно, рисуем сами графы.
i = 0
for sentence in sentences[:4]:
    sent = nlp(sentence)
    tok = []
    deps = []
    for token in sent:
            tok.append([token.text, token.head.text])
            deps.append(token.dep_)

    G = nx.Graph()
    G.add_edges_from(tok)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 6))
    nx.draw(G, pos, edge_color='black',
            width=1,
            linewidths=1,
            node_size=400,
            node_color='#5390fe',
            alpha=0.9,
            labels={node:node for node in G.nodes()})
    k = 0
    for d in deps:
        nx.draw_networkx_edge_labels(G, pos, edge_labels={tuple(tok[k]) :d}, font_color='#14145b')
        k += 1
    plt.axis('off')
    plt.savefig('sentence {}.png'.format(i+1))
    plt.show()
    i += 1

