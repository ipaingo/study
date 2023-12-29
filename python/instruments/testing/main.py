import csv
import sys
import statistics
from split_lib import split_data


# запись данных из файла.
def read_data_from_file(filename):
    # это вернем.
    rows_csv = []
    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile)

        # для удобства при выполнении split будем разделять данные в строчках пробелом.
        for row in read_csv:
            rows_csv.append(" ".join(row))

    rows_csv.pop(0)
    return rows_csv


# статистика и вывод в формате 'начало,конец,количество,среднее,медиана'.
def calculate_statistics(data_stat):
    # отметка начала отрывка. поместим в нее первое значение.

    start = float(data_stat[0].split()[0])

    # массив значений в пятиминутном отрывке, который надо будет обработать статистике.
    # началом является первая отметка, поэтому поместим в массив соответствующее ей значение.
    data = [int(data_stat[0].split()[1])]

    # этот массив мы вернем для вывода.
    result = []

    for i in range(1, len(data_stat)):

        # проверяем, является ли следующий элемент разделителем.
        if float(data_stat[i].split()[0]) == -1:

            # если так, запишем длинную строку из нужных нам значений, разделенных запятой. мода не работает в линуксе, поэтому пришлось ее убрать.
            result.append(
                ",".join(
                    [
                        str(start),
                        data_stat[i - 1].split()[0],
                        str(len(data)),
                        str(statistics.mean(data)),
                        str(statistics.median(data)),
                    ]
                )
            )

            # обновим массив данных для статистики.
            data = []

        elif not data:

            # костыль. обновим начало.
            start = float(data_stat[i].split()[0])
            data.append(int(data_stat[i].split()[1]))

        else:
            # если мы не вышли за пять минут, прибавим к массиву для статистики новый элемент.
            data.append(int(data_stat[i].split()[1]))

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Неправильное количество аргументов")
    else:
        raw_data = read_data_from_file(sys.argv[1])

        # в конец добавляем -1, потому что это число будет разделителем между промежутками в N секунд.
        raw_data.append("-1")

        # вывод.
        divided_data = split_data(raw_data, int(sys.argv[2]))

        # print(calculate_statistics(divided_data))

        for i in range(len(calculate_statistics(divided_data))):
            print(calculate_statistics(divided_data)[i])
