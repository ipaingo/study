# если заменить маленькие массивы, на которых тестируются функции,
# на результат верной обработки example.csv, ничего не поменяется,
# но быстрее, проще и нагляднее просто посчитать значения для маленького массива,
# чем для всего example.csv.

import statistics
import pytest
from main import *  # сами функции, собственно.
from split_lib import split_data


def test_read_data_from_file():  # 1. проверка на отсутствие файла.
    try:
        read_data_from_file("exampl.csv")
    except FileNotFoundError:
        pytest.fail("Файл не найден.")


def test_roots():  # 2. проверка на отсутствие доступа к файлу.
    try:
        read_data_from_file("err.csv")
    except PermissionError:
        pytest.fail("Файл недоступен для чтения.")


def test_csv():  # 3. ex1.csv там же, где err.csv. просто испорченный example.csv.
    x = read_data_from_file("ex1.csv")
    for i in range(len(x)):
        if len(x[i].split()) != 2:
            pytest.fail("Формат файла не удовлетворяет шаблону csv.")


def test_data():  # 4. проверка на количество колонок. выявляет ошибку, если колонка только одна.
    try:
        calculate_statistics(["1", "2 354", "-1", "5 54"])
    except IndexError:
        pytest.fail("В файле присутствует строка с одной колонкой.")


def test_type():  # 5. проверка на то, что данные являются числами.
    x = read_data_from_file("ex1.csv")
    try:
        calculate_statistics(x)
    except ValueError:
        pytest.fail("Неверный тип данных.")


def test_time():  # 6. проверка на верное деление на интервалы.
    if split_data(["1 200", "3 2345", "5 200", "7 100"], 5) != [
        "1 200",
        "3 2345",
        "5 200",
        "-1",
        "7 100",
    ]:
        pytest.fail("Неверные временные интервалы.")
        # маленький массив можно заменить на пример верно разделенного example.csv.


def test_amount():  # 7. проверка на количество интервалов.
    count = 0
    x = split_data(["1 200", "3 2345", "5 200", "7 100"], 5)
    for i in range(
        len(x)
    ):  # маленькие массивы, опять же, можно заменить. это просто пример для демонстрации работы теста.
        if x[i] == "-1":
            count += 1
    if count != 1:
        pytest.fail("Неверное количество интервалов.")


def test_stat():  # 8. проверка на верный подсчет статистики.
    x = read_data_from_file("ex2.csv")
    x.append("-1")
    if calculate_statistics(split_data(x, 5)) != ["1.0,5,3,915,200", "7.0,7,1,100,100"]:
        pytest.fail(
            "Статистика подсчитана неверно."
        )  # справа просто результат работы программы на ex2.csv.


def test_max():  # 9. проверка на... "maxint"?... слишком большое число, короче.
    x = read_data_from_file("example.csv")
    try:
        calculate_statistics(split_data(x, 999999))
    except statistics.StatisticsError:
        pytest.fail("Временной промежуток должен быть меньше общей длины эксперимента!")


def test_min():  # 10. проверка на отрицательное число.
    x = read_data_from_file("ex2.csv")
    try:
        calculate_statistics(split_data(x, -999999))
    except statistics.StatisticsError:
        pytest.fail("Временной промежуток должен быть положительным!")


def test_zero():  # 11. проверка на ноль.
    x = read_data_from_file("ex2.csv")
    try:
        calculate_statistics(split_data(x, 0))
    except statistics.StatisticsError:
        pytest.fail("Временной промежуток должен быть положительным!")
