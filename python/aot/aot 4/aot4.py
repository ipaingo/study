import pymorphy3
import matplotlib.pyplot as plt

import razdel

morph = pymorphy3.MorphAnalyzer()


def draw_graph(frequency, default_name):
    x_axis = range(1, len(frequency) + 1)
    plt.title("закон Зипфа для " + str(default_name))
    plt.xlabel("ранг")
    plt.ylabel("частота")
    plt.plot(x_axis, frequency)
    plt.show()


def create_dict(default_name, text):
    filename = str(input("введите путь до файла словаря: "))
    dict_lemmas = {}
    word_count = 0

    for w in razdel.tokenize(text):
        word = w.text

        p = morph.parse(word)[0]
        lemma = str(p.normal_form)
        if lemma[0] not in "'-,./&^:;{}[]()*?!@#%+=«»–—…":
            word_count += 1
            if lemma in dict_lemmas:
                dict_lemmas[lemma] += 1
            else:
                dict_lemmas[lemma] = 1

    dict_lemmas = list(reversed(sorted(dict_lemmas.items(), key=lambda x: x[1])))

    values = [None for _ in range(len(dict_lemmas))]
    c_sum = 0
    for i, v in enumerate(dict_lemmas):
        value = v[1] / word_count
        c_sum += value * (i + 1)
        values[i] = value

    s = "значение постоянной Зипфа: " + str(c_sum / len(dict_lemmas))
    print(s)
    if filename != "":
        with open(filename, "w", encoding="utf-8") as file:
            file.write(s + "\n")
            file.write("Всего лемм: " + str(word_count) + "\n")
            for char in dict_lemmas:
                file.write(str(char[0]) + " " + str(char[1]) + "\n")
    draw_graph(values, default_name)


def main():
    filepath = str(input("введите путь до файла: "))
    if filepath != "":
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()

    create_dict(filepath, text)


if __name__ == "__main__":
    main()
