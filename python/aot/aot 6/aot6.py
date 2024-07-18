import nltk

# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
import pymorphy3
from summa import summarizer

stop_words = []


# вспомогательная функция для подсчета частот.
def calc_frequency(ref_words, text_words):
    res = 0
    for word1 in ref_words:
        if word1 in text_words:
            res += 1
    return res / len(ref_words)


# функция подсчета метрик ROUGE. все по формулкам.
def get_rouges(ref, text):
    ref = ref.lower()
    ref_unigrams = nltk.word_tokenize(ref)
    temp = []
    for word in ref_unigrams:
        if word not in stop_words:
            temp.append(word)
    ref_unigrams = temp
    reference_bigrams = list(nltk.bigrams(ref_unigrams))
    reference_trigrams = list(nltk.trigrams(ref_unigrams))

    text_unigrams = nltk.word_tokenize(text)
    temp = []
    for word in text_unigrams:
        if word not in stop_words:
            temp.append(word)
    text_unigrams = temp
    text_bigrams = list(nltk.bigrams(text_unigrams))
    text_trigrams = list(nltk.trigrams(text_unigrams))

    rouge1 = calc_frequency(ref_unigrams, text_unigrams)
    rouge2 = calc_frequency(reference_bigrams, text_bigrams)
    rouge3 = calc_frequency(reference_trigrams, text_trigrams)

    return round(rouge1, 5), round(rouge2, 5), round(rouge3, 5)


def main():
    # стоп-слова - слова, которые не вносят никакой дополнительной информации в текст: предлоги, союзы, междометия.
    global stop_words
    with open("text.txt", encoding="utf-8") as file:
        text = file.read().lower()
    stop_words = stopwords.words("russian") + "'-,./&^:;{}[]()*?!@#%+=«»–—…".split()

    # разбиваем на слова.
    sentences = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]

    morpher = pymorphy3.MorphAnalyzer()
    sentences_lemmatized = []
    dict_word_frequency = {}

    for sentence in tokens:
        current_sentence = []
        for word in sentence:
            if word not in stop_words:
                word = morpher.normal_forms(word)[0]  # записываем начальные формы,
                if word in dict_word_frequency:  # и как часто они встречаются.
                    dict_word_frequency[word] += 1
                else:
                    dict_word_frequency[word] = 1
                current_sentence.append(word)
        sentences_lemmatized.append(current_sentence)

    # будем сортировать предложения по их важности (суммарному весу их слов).
    dict_word_frequency = dict(
        sorted(dict_word_frequency.items(), key=lambda item: item[1], reverse=True)
    )

    dict_sentence_weights = {}

    for i in range(len(sentences_lemmatized)):
        weight = 0
        for word in sentences_lemmatized[i]:
            weight += dict_word_frequency[word]
        dict_sentence_weights[sentences[i]] = (weight / len(sentences_lemmatized[i]), i)

    dict_sentence_weights = dict(
        sorted(dict_sentence_weights.items(), key=lambda item: item[1][0], reverse=True)
    )

    d = float(input("Введите желаемый объем реферата (от 0 до 1): "))

    # мы оставим только желаемый процент объема, и запишем самые важные предложения в полученный реферат.
    limit = int(len(sentences) * d)
    report = ""
    count = 0
    dict_top = {}
    for k, v in dict_sentence_weights.items():
        if count == limit:
            break
        count += 1
        dict_top[k] = v

    dict_top = dict(sorted(dict_top.items(), key=lambda item: item[1][1]))

    for k in dict_top.keys():
        report += k + "\n"

    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(report)

    # сравниваем с рефератами от других библиотек.
    with open("ref_txt.txt", encoding="utf-8") as file:
        ref = file.read()
    with open("visual_world.txt", encoding="utf-8") as file:
        visual_world = file.read()
    with open("splitbrain.txt", encoding="utf-8") as file:
        splitbrain = file.read()

    summa_text = summarizer.summarize(text, ratio=0.25)

    print("Реферат:")
    for sentence in report.split("\n"):
        print(sentence)
    print()
    print("---------------------")
    print()

    print("Splitbrain:")
    for sentence in splitbrain.split("\n"):
        print(sentence)
    print()
    print("---------------------")
    print()

    print("Визуальный мир:")
    for sentence in visual_world.split("\n"):
        print(sentence)
    print()
    print("---------------------")
    print()

    print("Summa:")
    for sentence in summa_text.split("\n"):
        print(sentence)
    print()

    file = open("rouge.txt", "w", encoding="utf-8")

    print()
    rouges = f"Реферат:\n{get_rouges(ref, report)}"
    print(rouges)
    file.write(rouges + "\n")

    rouges = f"Splitbrain:\n{get_rouges(ref, splitbrain)}"
    print(rouges)
    file.write(rouges + "\n")

    rouges = f"Визуальный Мир:\n{get_rouges(ref, visual_world)}"
    print(rouges)
    file.write(rouges + "\n")

    rouges = f"Summa:\n{get_rouges(ref, summa_text)}"
    print(rouges)
    file.write(rouges)

    file.close()
    print("ROUGE-отчет сохранен как rouge.txt.")


if __name__ == "__main__":
    main()
