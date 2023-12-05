import csv
from re import match, sub

dict_texts = dict()


# проверяет, является ли входная строка line новой главой, сопоставляя её с регулярными выражениями.
# у рассказа! главы! ужас.
def is_chapter_name(line):
    return match('Глава.*[IV]', line) \
        or match('[IV].*', line) \
        or match('Случай [^ ]*$', line) \
        or match('Действие [^ ]*$', line) \
        or match('Пролог.*', line) \
        or match('Эпилог.*', line)


def is_empty_line(line):
    return line.strip() == ""


# проверка на таб (4 пробела) в начале строки.
def starts_with_tab(line):
    return line[0:4] == "    "


# проверяет, является ли text пустым.
def is_empty_text(text):
    for line in text:
        if not is_empty_line(line):
            return False
    return True


# выделяет заголовок и добавляет текст в словарь dict_texts.
def add_to_dict(text):
    index = 0
    header = ""
    # записываем название, пока не дойдем до начала текста.
    while not starts_with_tab(text[index]):
        header += text[index]
        index += 1
        if index >= len(text):
            return
    index += 1
    # если текст начинается с * * *, то у него нет названия.
    # в таком случае названием будет первое предложение в рассказе.
    if header == "* * *\n":
        header = ""
        h = text[index]
        for i in h:
            if i not in "!?.\n":
                header += i
            else:
                header += i
                break

    header = header.strip()
    text_no_header = text[index:]
    if is_empty_text(text_no_header):
        return
    dict_texts[header] = text_no_header


def main():
    path_to_file = str(input("Путь до текста: "))
    # path_to_file = "Чехов - рассказы.txt"
    with open(path_to_file, "r", encoding="utf-8") as file:
        text = file.readlines()
    option = -1
    while option not in [1, 2, 3]:
        option = int(input("Что вы хотите сделать с файлом?\n"
                           "1. Создать csv файл заголовков;\n"
                           "2. Создать файл заголовков и разделить рассказы по файлам;\n"
                           "3. Выйти из программы.\n"
                           "Ввод: "))
        if option not in [1, 2, 3]:
            print("Неверная опция!")

    if option == 3:
        exit()

    current_text = []
    is_new_text = True
    for line in text:
        if not starts_with_tab(line) and not is_chapter_name(line) and len(current_text) != 0 and not is_new_text:
            add_to_dict(current_text)
            current_text = []
            is_new_text = True
        else:
            if is_new_text:
                is_new_text = False
        current_text.append(line)

    # запись в csv файл.
    while True:
        filename = str(input("Адрес csv файла для сохранения: "))
        if filename[-4:] == ".csv":
            break
        print("Неверное расширение файла.")

    # csv выпендривается.
    arr = [[i] for i in sorted(dict_texts.keys())]
    if filename != "":
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Названия рассказов"])
            writer.writerows(arr)

    if option == 2:
        directory = str(input("Адрес папки для сохранения файла: "))
        for i in arr:
            header = i[0].split("\n")[0]
            if len(header) > 100:
                header = f"{header[:100]}"
            path = directory + "\\" + sub(r'[^\w«»_. -]', '', header.strip()) + ".txt"
            print(path)
            with open(path, "w", encoding="utf-8") as f:
                for j in dict_texts[i[0]]:
                    f.write(j)
    print("Файлы созданы успешно. Выход из программы.")


if __name__ == "__main__":
    main()
