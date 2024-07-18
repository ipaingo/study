import math


def get_err_codes(seq):
    checksums = []

    for i in range(4):
        p = 2**i
        tmp = [(j // p) % 2 for j in range(len(seq))]
        checksums.append(tmp)

    # получаем вектор кода по формуле.
    parity_bits = [0] * 4
    for i in range(4):
        parity_bits[i] = sum([seq[j] * checksums[i][j] for j in range(len(seq))]) % 2

    return parity_bits


# создание матрицы контрольной суммы.
def matrix_sum(str_length):
    control_byte = [1, 2, 4, 8, 16]  # массив позиций контрольных битов.
    str_line = ["", "", "", "", "", ""]
    for i in range(1, 5):
        j = 1
        # расставляем нули и единицы.
        while j < str_length:
            if j % control_byte[i - 1] == 0:
                for k in range(control_byte[i - 1]):
                    if j >= str_length:
                        break
                    str_line[i] += "1"
                    j += 1
                for k in range(control_byte[i - 1]):
                    if j >= str_length:
                        break
                    str_line[i] += "0"
                    j += 1
            else:
                str_line[i] += "0"
                j += 1
    return str_line


def gen_code(seq):
    # выделяем место для контрольных битов.
    # всего их (изначальная длина + log_2 контрольных битов + бит четности).
    final_len = len(seq) + math.ceil(math.log2(len(seq))) + 1
    initial_vector = [0]
    cnt = 0
    # ставим нули туда, где должны быть контрольные биты.
    for i in range(1, final_len + 1):
        if int(math.log2(i)) == math.log2(i):
            initial_vector.append(0)
        else:
            print(cnt)
            initial_vector.append(seq[cnt])
            cnt += 1
    print("iv", initial_vector)
    # получаем значения контрольных битов.
    bits = get_err_codes(initial_vector)
    print("b", bits)

    # расставляем контрольные биты.
    for i in range(len(bits)):
        p = 2**i
        try:
            initial_vector[p] = bits[i]
        except IndexError:  # для вводимых строк меньше чем 2^len(bits) длины.
            initial_vector.append(bits[i])

    # бит чётности.
    initial_vector[0] = sum(initial_vector) % 2

    return initial_vector


# функция проверки на наличие ошибок по методу.
def check_code(seq):
    bits = get_err_codes(seq)
    bits = [str(bits[-1 - i]) for i in range(4)]
    idx = int("".join(bits), 2)
    global_parity = sum(seq) % 2
    if idx != 0 and global_parity != 0:  # 1 ошибка.
        return idx  # возвращаем индекс позиции с ошибкой.
    if idx != 0 and global_parity == 0:  # 2 ошибки.
        return -2
    if idx == 0 and global_parity != 0:  # 0 бит неверный.
        return -1
    return 0  # нет ошибок.


def main():
    exit_flag = False
    while not exit_flag:
        # ввод действия.
        while True:
            print(
                "Выберите действие:\n1 - сгенерировать последовательность,\n2 - проверить последовательность,"
                "\n3 - выход."
            )
            try:
                optype = int(input())
            except ValueError:
                print("Неправильный ввод.")
                continue
            else:
                if optype == 1 or optype == 2 or optype == 3:
                    break
                else:
                    print("Неправильный ввод.")
                    continue

        if optype == 3:
            exit_flag = True
            break

        # ввод длины кода (изначальный / на проверку).
        while True:
            print("Введите длину кода:")
            try:
                length = int(input())
            except ValueError:
                print("Не число.")
                continue
            else:
                if optype == 1:
                    if 4 <= length <= 8:
                        break
                    else:
                        print("Неправильный ввод длины кода.")
                        continue
                if optype == 2:
                    if 9 <= length <= 13:
                        break
                    else:
                        print("Неправильный ввод длины кода.")
                        continue

        # ввод кода (изначальный / на проверку).
        while True:
            print("Введите код: (вводите биты через пробел)")
            rawseq = input()
            seq = list(map(int, rawseq.split(" ")))
            if len(seq) != length:
                print("Введённый код не соответствует заданной длине.")
                continue
            for i in seq:
                if i != 0 and i != 1:
                    print("В коде присутствуют символы помимо 0 и 1.")
                    break
            else:
                break

        # генерация нового кода.
        if optype == 1:
            code = gen_code(seq)
            matrices = matrix_sum(len(code))
            new = ""
            for i in range(len(code)):
                new += "="
            print(new)
            for line in matrices:
                print(line)
            print(new)

            print(f"Сгенерированный код имеет длину {len(code)} символов:")
            print_res = ""
            for i in range(len(code)):
                print_res += str(code[i]) + " "
            print(print_res)
        # проверка существующего кода.
        elif optype == 2:
            code = check_code(seq)
            if code == -1:
                print("Нулевой бит чётности может быть инвертирован.")
            elif code == -2:
                print("В коде 2 (или другое четное число) ошибок.")
            elif code == 0:
                print("Ошибок не найдено.")
            else:
                print(f"Возможно, ошибка в позиции {code} (отсчёт начинается с 0).")
        # выход из программы.
        elif optype == 3:
            exit_flag = True
            break


if __name__ == "__main__":
    main()
