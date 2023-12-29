from msvcrt import getch

global texts


# загружает текст из файла в глобальный массив.
def add_text():
    global texts
    filepath = str(input("путь до файла текста: "))
    if filepath != "":
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            texts.append(text)
    else:
        return


# создает словарь всех встречающихся в тексте символов.
def create_char_dict(filename):
    dict_char = set()  # уникальность символов достигается с помощью множества!
    for text in texts:
        for char in text:
            dict_char.add(char.lower())
    if filename != "":
        with open(filename, "w", encoding="utf-8") as f:
            f.write("всего уникальных символов: " + str(len(dict_char)) + "\n")
            for char in dict_char:
                if char != "\n":
                    f.write(char + "\n")
                else:
                    f.write("(перенос строки)" + "\n")


# вычисляет частоту встречаемых символов.
def get_chars_frequency(filename):
    dict_chars = {}  # гениальные названия, конечно.
    count = 0
    for text in texts:
        for char in text:
            count += 1
            if char in dict_chars.keys():
                dict_chars[char] += 1
            else:
                dict_chars[char] = 1
    if filename != "":
        with open(filename, "w", encoding="utf-8") as f:
            f.write("всего символов: " + str(count) + "\n")
            for char in dict(
                sorted(dict_chars.items(), key=lambda item: item[1])
            ).__reversed__():
                f.write(str(char) + " " + str(dict_chars[char]) + "\n")


# функция для наведения красоты в словах.
# убирает лишние пробелы и дефисы.
def process_word(word):
    word = word.replace(" ", "")

    if word == "":
        return ""

    if word[len(word) - 1] == "-":
        word = word[0 : len(word) - 1]

    if word == "":
        return ""

    if word[0] == "-":
        word = word[1 : len(word)]

    if len(word) == 0:
        return ""

    return word


# создает словарь всех встречающихся слов.
def create_word_dict(filename):
    set_words = set()
    for text in texts:
        truncated_text = text
        for char in "',./&^:;{}[]()*?!@#%+=«»–—\"":
            truncated_text = truncated_text.replace(char, "")
        truncated_text = truncated_text.replace("\n", " ").lower()

        for word in truncated_text.split(" "):
            word = process_word(word)
            if word not in [" ", "", "-"]:
                set_words.add(word.lower())

    if filename != "":
        with open(filename, "w", encoding="utf-8") as f:
            f.write("всего уникальных слов: " + str(len(set_words)) + "\n")
            for word in set_words:
                f.write(word + "\n")


def get_words_frequency(filename):
    dict_words = {}
    count = 0
    for text in texts:
        truncated_text = text
        for word in "',./&^:;{}[]()*?!@#%+=«»–—":
            truncated_text = truncated_text.replace(word, "")
        truncated_text = truncated_text.replace("\n", " ").lower()
        for word in truncated_text.split(" "):
            word = process_word(word)
            if word not in ["", " ", "-"]:
                count += 1
                if word in dict_words.keys():
                    dict_words[word] += 1
                else:
                    dict_words[word] = 1

    if filename != "":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"всего слов: {count}\n")
            for word in dict(
                sorted(dict_words.items(), key=lambda item: item[1])
            ).__reversed__():
                f.write(str(word) + " " + str(dict_words[word]) + "\n")


def main():
    global texts
    texts = []
    text_loaded = False

    while True:
        print(
            "нажмите кнопку действия:\n"
            "1. добавить текст;\n"
            "2. словарь символов;\n"
            "3. частотный словарь символов;\n"
            "4. словарь слов;\n"
            "5. частотный словарь слов;\n"
            "6. выход."
        )

        x = int(input("ввод: "))

        if x in [1, 2, 3, 4, 5, 6]:
            if x == 6:
                exit()
            if x == 1:
                add_text()
                text_loaded = True
            else:
                if text_loaded:
                    filename = str(
                        input("введите путь до файла сохраняемого словаря: ")
                    )
                    if x == 2:
                        create_char_dict(filename)
                    elif x == 3:
                        get_chars_frequency(filename)
                    elif x == 4:
                        create_word_dict(filename)
                    elif x == 5:
                        get_words_frequency(filename)
                else:
                    print("не загружен текст для обработки.")
            _ = input("нажмите Enter, чтобы продолжить.")


if __name__ == "__main__":
    main()
