import tkinter as tk   # библиотека tkinter используется для создания окна,
from tkinter import *  # с которым взаимодействует пользователь.
import math

# эта функция нужна для создания независимых списков.
def unshared_copy(inList):
    if isinstance(inList, list):
        return list(map(unshared_copy, inList))
    return inList

# эта функция создает окно, в котором выводится результат.
def show_result(result):
    window2 = tk.Toplevel()
    window2.geometry("555x400")
    window2.title("Результат работы")

    frame1 = tk.Frame(master=window2, height=400)
    frame1.pack(fill=tk.X)

    answer_label = tk.Label(window2, text="Обработанное сообщение:")
    answer_label.place(x=0, y=2)

    result_text = tk.Text(frame1)
    result_text.place(x=0, y=25)

    result_text.insert("1.0", result)

    result_text = tk.Text(window2)
    result_text.pack()

    window2.mainloop()

# эта функция вызывается, когда пользователь нажимает кнопку "Зашифровать".
def encrypt_text():
    # сохраняет зашифрованное сообщение, чтобы потом можно было его расшифровать.
    global memory
    memory = []
    text = enter_text.get("1.0", tk.END) # получает текст из поля ввода.

    # выводит сообщение об ошибке, если пользователь ничего не ввел.
    if text == "" or text == "\n":
        correct_text_label = tk.Entry(background="#F0F0F0", borderwidth=0, width=100)
        correct_text_label.delete(0, tk.END)
        correct_text_label.insert(0, "Введите сообщение!")
        correct_text_label.place(x=5, y=435)
        return -1

    # получение ключей, создание переменных.
    column_key = enter_key2.get()
    row_key = enter_key1.get()
    row_key_list = ""

    # сообщение об ошибке или об успешной проверке.
    correct_text_label = tk.Entry(background="#F0F0F0", borderwidth=0, width=100)
    correct_text_label.delete(0, tk.END)
    correct_text_label.insert(0, check_keys(column_key, row_key))
    correct_text_label.place(x=5, y=435)

    # выполняется, если ошибок нет.
    if check_keys(column_key, row_key) == "Все хорошо!":
        # создание вспомогательной строчки, состоящей из ключей строк по порядку, как в табличке.
        line_count = math.ceil(len(text) / len(column_key))
        for i in range(line_count):
            row_key_list += row_key[i % len(row_key)]

        # записываем работу алгоритма в список.
        encrypted_text = encrypt(text, row_key_list, column_key, row_key)

        # преобразовываем двумерный массив в строку, чтобы вывести результат шифровки пользователю.
        # квадратные скобки используются для обозначения начала и конца блока, т. к. в сообщении могут быть
        # символы переноса строки, которые становятся реальными переносами строки при выводе на экран.
        result = ""
        for i in range(len(encrypted_text)):
            result+="["
            for j in range(len(encrypted_text[i])):
                result += encrypted_text[i][j]
            result += "]\n"

        # результат хранится в глобальной переменной, которая не должна изменяться при работе других функций.
        # поэтому создаем несвязанную копию с помощью маленькой вспомогательной функции.
        memory = unshared_copy(encrypted_text)

        # создаем окно и показываем результат пользователю.
        show_result(result)

# сам алгоритм шифрования.
def encrypt(text, row_key_list, column_key, row_key):
    # вспомогательные переменные для сокращения формулы.
    columns = len(column_key)
    rows = len(row_key)
    # двумерный список блоков.
    encrypted_text = [[] for i in range(columns * rows)]
    # с помощью цикла пройдем по всем символам.
    for i in range(len(text)):
        ri = i // columns
        sj = i % columns
        # считаем положение символа по формуле с помощью введенных ключей.
        k = columns * (int(row_key_list[ri]) - 1) + int(column_key[sj]) - 1
        # добавляем символ в блок.
        encrypted_text[k].append(text[i])
    return encrypted_text


# эта функция вызывается, когда пользователь нажимает кнопку "Расшифровать".
def decrypt_text():
    try:
        # если memory не существует, эта операция выдаст ошибку. это означает, что программе нечего расшифровывать.
        encrypted_text = unshared_copy(memory)
    except:
        # сообщение об ошибке.
        correct_text_label = tk.Entry(background="#F0F0F0", borderwidth=0, width=100)
        correct_text_label.delete(0, tk.END)
        correct_text_label.insert(0, "Сначала зашифруйте сообщение!")
        correct_text_label.place(x=5, y=435)
        return -1

    # то же самое, если memory была создана, но осталась пустой.
    if not memory:
        correct_text_label = tk.Entry(background="#F0F0F0", borderwidth=0, width=100)
        correct_text_label.delete(0, tk.END)
        correct_text_label.insert(0, "Сначала зашифруйте сообщение!")
        correct_text_label.place(x=5, y=435)
        return -1

    # немножко вычислений для определения количества символов.
    symbol_count = 0
    for i in range(len(encrypted_text)):
        if len(encrypted_text[i]) != 0:
            symbol_count += len(encrypted_text[i])

    # получение ключей, создание переменных.
    column_key = enter_key2.get()
    row_key = enter_key1.get()
    row_key_list = ""

    # выполняется, если ключи введены верно.
    if check_keys(column_key, row_key) == "Все хорошо!":
        # как и для шифрующей функции, создаем вспомогательню переменную ключей для строк.
        line_count = math.ceil(symbol_count / len(column_key))
        for i in range(line_count):
            row_key_list += row_key[i % len(row_key)]
        # так как эта функция возвращает строку, можно сразу отдать результат выполнения на вывод.
        show_result(decrypt(encrypted_text, symbol_count, column_key, row_key_list))

# расшифровывающая функция.
def decrypt(encrypted_text, symbol_count, column_key, row_key_list):
    # вспомогательное.
    text = ""
    columns = len(column_key)
    try:
        # с помощью цикла пройдем по всем символам.
        for i in range(symbol_count):
            ri = i // columns
            sj = i % columns
            # считаем положение символа по формуле с помощью введенных ключей.
            k = columns * (int(row_key_list[ri]) - 1) + int(column_key[sj]) - 1
            # записываем первый символ из полученного блока в строку для вывода.
            text += encrypted_text[k][0]
            # удаляем этот символ.
            encrypted_text[k].pop(0)
        return text
    except:
        # в некоторых случаях неверно подобранный ключ может вызывать
        # выход за пределы массива. в таком случае программа сообщает
        # пользователю об ошибке вместо того, чтобы просто сломаться.
        return "Ошибка расшифровки. Ключ подобран неверно."

# функция проверки правильности введенных ключей.
def check_keys(key1, key2):
    # ключ должен быть введен.
    if (key1 == "") or (key2 == ""):
        return "Введите оба ключа!"

    # ключ должен состоять из цифр.
    try:
        key1_int = int(key1)
        key2_int = int(key2)
    except:
        return "Ключ должен содержать только цифры без пробелов!"

    # исключает введение минусов, нулей и неправильных комбинаций.
    if len(key2) != 3:
        return "Ключ строк введен неверно!"
    for i in range(1, 4):
        if (key2.find(str(i)) == -1) or (key2[i - 1] == "0"):
            return "Ключ строк введен неверно!"

    if len(key1) != 5:
        return "Ключ столбцов введен неверно!"
    for i in range(1, 6):
        if (key1.find(str(i)) == -1) or (key1[i - 1] == "0"):
            return "Ключ столбцов введен неверно!"

    # ободряюще сообщает пользователю об успехе, если не обнаруживает ошибок.
    return "Все хорошо!"

# выводит в текстовое поле подсказку, если нажать на соответствующую кнопку.
def hint():
    enter_text.delete("1.0", tk.END)
    enter_text.insert("1.0",
                      "Введите в это поле сообщение, которое хотите зашифровать.\nВведите два ключа (например, 123 и 12345).\nНажмите кнопку \"Зашифровать\", чтобы получить зашифрованное сообщение.\nПоследнее зашифрованное сообщение сохранится в памяти.\nВведите ключи и нажмите кнопку \"Расшифровать\",\nчтобы показать исходное сообщение.\nP.S. Комбинации клавиш работают только на английской раскладке.")


if __name__ == "__main__":
    # создание окна, с которым работает пользователь.
    window1 = tk.Tk()
    window1.title("Метод рассечения-разнесения")
    window1.geometry("555x460")

    frame = tk.Frame(master=window1, height=400)
    frame.pack(fill=tk.X)

    enter_key1_label = tk.Label(text="Ключ строк:")
    enter_key1_label.place(x=5, y=5)

    enter_key1 = tk.Entry()
    enter_key1.place(x=85, y=5)
    enter_key1.insert(0, "123")

    enter_key2_label = tk.Label(text="Ключ столбцов:")
    enter_key2_label.place(x=240, y=5)

    enter_key2 = tk.Entry()
    enter_key2.place(x=340, y=5)
    enter_key2.insert(0, "12345")

    enter_text_label = tk.Label(text="Введите текст для обработки:")
    enter_text_label.place(x=5, y=30)

    enter_text = tk.Text(frame)
    enter_text.place(x=0, y=55)

    # небольшой текст, который можно использовать для проверки программы.
    enter_text.insert("1.0",
                      "А судьи кто? – За древностию лет\nК свободной жизни их вражда непримирима,\nСужденья черпают из забытых газет\nВремен Очаковских и покоренья Крыма.")

    encrypt_button = tk.Button(text="Зашифровать", command=encrypt_text)
    encrypt_button.place(x=5, y=405)
    decrypt_button = tk.Button(text="Расшифровать", command=decrypt_text)
    decrypt_button.place(x=100, y=405)
    hint_button = tk.Button(text="Показать подсказку", command=hint)
    hint_button.place(x=202, y=405)

    window1.mainloop()
