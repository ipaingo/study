import math
import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# генерация рандомного сида 2^24, по времени, семёрке и еще по времени.
def generate_random_seed():
    m = int(math.pow(2, 24))

    current_time = datetime.datetime.now()
    a = current_time.hour + current_time.minute + current_time.second
    if a % 4 == 0:
        a += 1
    elif a % 4 == 3:
        a += 2
    elif a % 4 == 2:
        a += 3

    a = int(a)

    b = 7 + current_time.microsecond
    if b % 2 == 0:
        b += 1

    b = int(b)

    while math.gcd(b, m) != 1:
        b = 7 + current_time.microsecond
        if b % 2 == 0:
            b += 1
        b = int(b)

    c = (
        current_time.microsecond
        + current_time.day
        + current_time.month
        + current_time.year
    )
    c = int(c)

    return [a, b, m, c]


# создаёт объект-генератор (Гугл generators или yield).
# требует сида и кол-ва требуемых значений (Желательно использовать исключительно в for'ах).
def generate_number(seed: list[int], number_count: int = 1):
    a, b, m, c0 = seed
    for _ in range(number_count):
        c = (a * c0 + b) % m
        c0 = c
        yield c


# полезная функция для получения кол-ва чисел в списке (Их частота).
# https://stackoverflow.com/a/40555781
def freq(lst):
    d = {}
    for i in lst:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    return d


def main():
    current_seed = [0, 0, 0, 0]
    while True:
        print()
        print(f"Текущий сид: {int(sum([i for i in current_seed]))}")
        print(
            """
              1 - Сгенерировать новый сид;
              2 - Сгенерировать новое псевдослучайное число / последовательность псевдослучайных чисел;
              3 - Отображение корректной работы генератора псевдослучайных чисел;
              0 - Выход.
              """
        )

        choice = input("Введите действие: ")

        if choice == "1":
            current_seed = generate_random_seed()
            print(current_seed)

        elif choice == "2":
            number_count = input("Введите желаемое количество генерируемых чисел: ")
            if not number_count.isdigit():
                print("Введённая последовательность - не число")
                input("Нажмите любую клавишу чтобы продолжить")
                continue

            if int(number_count) <= 0:
                print("Введённое количество - меньше или равно нулю")
                input("Нажмите любую клавишу чтобы продолжить")
                continue

            save_option = input("Желаете сохранить ряд в текстовый файл? (y/n): ")
            for number in generate_number(current_seed, int(number_count)):
                print(int(number))
                if save_option.lower() == "y":
                    f = open("_gen_numbers.txt", "a")
                    f.write(str(int(number)) + "\n")
                    f.close()
            input("Нажмите любую клавишу чтобы продолжить")

        elif choice == "3":
            try:
                # кол-во генерируемых чисел для проверки
                number_count = 2000

                list_of_data = []
                for number in generate_number(current_seed, number_count):
                    list_of_data.append(int(number))
                    # print(number)

                # тестирование на уникальность чисел
                print("тестирование на уникальность чисел: ", end="")
                if max(freq(list_of_data).values()) - 1 == 0:
                    print("успешно (0 повторений)")
                elif (
                    max(freq(list_of_data).values()) - 1 >= 1
                    or max(freq(list_of_data).values()) - 1 <= 3
                ):
                    print("частично успешно (от 1 до 3-х повторений)")
                else:
                    print("не успешно (более 3-х повторений)")
                print()

                start = min(list_of_data)
                end = max(list_of_data)
                last_step = start
                distribution_list = []
                # получаем кол-во чисел в каждом из диапазонов
                for new_step in range(
                    start + (end - start) // 100, end, (end - start) // 100
                ):
                    counter = 0
                    for number in list_of_data:
                        if number <= new_step and number >= last_step:
                            # print(f"число {number} между {last_step} и {new_step}")
                            counter += 1
                    distribution_list.append(counter)
                    last_step = new_step
                print(
                    f"массив кол-ва чисел в каждом из интервалов: {distribution_list}"
                )
                print(
                    f"максимальный разрыв (по шт.) между распределением чисел: {max(distribution_list) - min(distribution_list)}"
                )

                for i in range(len(distribution_list)):
                    distribution_list[i] /= number_count
                print(
                    f"массив отношения кол-ва чисел в каждом из интервалов к общему числу сгенерированных чисел: {distribution_list}"
                )
                print(
                    f"максимальный разрыв между отношениями: {max(distribution_list) - min(distribution_list)}"
                )
                print(f"среднее от относительных частот : {np.mean(distribution_list)}")

                # визуальное изображение графика распределения.
                # на графике по оси X расположены сами числа, по оси Y - их количество.
                # в процентном соотношении - число на оси Y поделить на 1000.
                # sns.displot(list_of_data, label="Распределение чисел", color="blue")
                plt.bar(range(0, 100), distribution_list)
                plt.grid(True)
                # plt.xlim(0, 2)
                # plt.ylim(0, max(list_of_data))
                # plt.autoscale(False)

                plt.show()
            except ZeroDivisionError:
                print("Сначала сгенерируйте последовательность!")
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
