import math
import datetime
from time import perf_counter

MAX_ASCII = 1114111


# генерация рандомного сида из третьей лабораторной.
def generate_random_seed():
    m = 5000

    # для генерации будем использовать текущий момент времени.
    current_time = datetime.datetime.now()
    a = current_time.hour + current_time.minute + current_time.second
    if a % 4 == 0:
        a += 1
    elif a % 4 == 2:
        a += 3
    elif a % 4 == 3:
        a += 2

    a = int(a)

    b = 7 + current_time.microsecond
    if b % 2 == 0:
        b += 1  # b должно быть нечетным.

    b = int(b)

    # проверка на то, что b и m взаимно простые.
    while math.gcd(b, m) != 1:
        # просто увеличиваем b, сохраняя нечетность, пока они не станут взаимно простыми.
        b += 2
        b = int(b)

    c = current_time.microsecond + current_time.day + current_time.month + current_time.year
    c = int(c)

    return [a, b, c, m]


# создает объект-генератор. 
def generate_number(a, b, c, m):
    return (a * c + b) % m


# чтение ключа из файла.
def read_key(f):
    try:
        with open(f, "r", encoding="utf-8") as file:
            arr = file.read()
            arr = arr.split()
            if len(arr) != 4:
                print("Файл составлен неверно.")
                return None
            return list(map(int, arr))
    except FileNotFoundError:
        print("Файл не найден.")
        return None


# гаммирование.
def gamma():
    # получаем файл с ключом.
    save_option = input("Введите название файла с ключом (например, file.key): ")
    # save_option = "file.key"
    if save_option.endswith(".key") == 0:
        print("Неверное расширение файла.")
        return
    if read_key(save_option) is None:
        return
    a, b, c, m = read_key(save_option)

    # получаем файл с текстом.
    f = input("Введите название файла с данными (например, data.txt): ")
    # f = "data.txt"
    try:
        with open(f, "r", encoding="utf-8") as file:
            data = file.read()
    except UnicodeDecodeError:
        print("Ошибка кодировки файла. Используйте файл с кодировкой UTF-8.")
        return
    except FileNotFoundError:
        print("Файл не найден.")
        return

    change = "gammed_"
    if f.startswith("gammed_"):
        change = "degammed_"
        f = f.lstrip("gammed_")

    # для подсчета времени, которое ушло на шифрование.
    start_time = perf_counter()

    # получаем первое псевдослучайное число с помощью генератора.
    n = generate_number(a, b, c, m)

    length = len(data)

    new_string = ""

    for i in range(length):
        # каждый следующий символ представляем в виде числа,
        # xor-им с псевдослучайным числом,
        # и снова записываем в виде символа.
        new_string += chr(n ^ ord(data[i]))

        # получаем следующее псевдослучайное число.
        n = generate_number(a, b, n, m)

    # закончили с циклом, записываем конец.
    end_time = perf_counter()

    print(f"Затраченное время: {(end_time - start_time):0.4f} секунд")

    # записываем результат в новый файл.
    with open(f'{change}{f}', "w", encoding="utf-8") as file:
        file.write(new_string)


def main():
    current_seed = [0, 0, 0, 0]
    while True:
        # небольшой интерфейс.
        print()
        print(f"Текущий сид: {int(sum([i for i in current_seed]))}")
        print("""
              1 - Сгенерировать новый сид;
              2 - Выполнить шифрование;
              0 - Выход.
              """)

        choice = input("Введите действие: ")

        # генерация нового кода.
        if choice == "1":
            current_seed = generate_random_seed()
            save_option = input("Сохранить сид в файл (например, file.key): ")
            save_option.strip()
            if save_option == "":
                print("Отмена записи.")
                continue

            a, b, c, m = current_seed

            f = open(save_option, "w", encoding="utf-8")
            f.write(str(a) + "\n" + str(b) + "\n" + str(c) + "\n" + str(m))
            f.close()
            print("Сид успешно записан в файл.")

        # шифрование.
        elif choice == "2":
            gamma()

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
