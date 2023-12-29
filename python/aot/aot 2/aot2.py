path_to_dict = ""


def check_dictionary(word, dictionary):
    if word in dictionary:
        print(word, end="")


# находит немного измененные верные варианты в словаре.
def find_correct(word, dictionary):
    word_length = len(word)

    # проверяем, на каком языке слово.
    if word.isascii():
        range_ascii = range(97, 123)  # латиница.
    else:
        range_ascii = range(1072, 1104)  # кириллица.

    # замена каждой буквы.
    for i in range(word_length):
        for j in range_ascii:
            new_s = word[0:i] + chr(j) + word[i + 1 : word_length]
            check_dictionary(new_s, dictionary)

    # вставка новой буквы.
    for i in range(word_length):
        for j in range_ascii:
            new_s = word[0:i] + chr(j) + word[i:word_length]
            check_dictionary(new_s, dictionary)

    # удаление буквы.
    for i in range(word_length):
        new_s = word[0:i] + word[i + 1 : word_length]
        check_dictionary(new_s, dictionary)

    # перемещение соседних букв.
    for i in range(word_length - 1):
        new_s = word[0:i] + word[i + 1] + word[i] + word[i + 2 : word_length]
        check_dictionary(new_s, dictionary)


# открывает словарь из файла, проверяет, верно ли написано слово, выводит соответствующий результат.
def check_dict(user_input):
    with open(path_to_dict, "r", encoding="utf-8") as file:
        dict_words = file.readlines()

    if user_input + "\n" in dict_words:
        print("Слово написано верно!")
    else:
        print("Слово написано неверно.\nПравильные варианты: ")
        find_correct(user_input + "\n", dict_words)


def main():
    global path_to_dict
    path_to_dict = str(input("Файл словаря: "))

    inp = "0==0"
    while inp != "":
        inp = str(input("Слово для проверки: "))
        check_dict(inp)


if __name__ == "__main__":
    main()
