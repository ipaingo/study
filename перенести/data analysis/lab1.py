def my_list(n):
    numbers = []
    n += 1
    if n % 724 != 0:
        n += (724 - (n % 724))
    else:
        n += 1

    while n < 100000:
        numbers.append(n)
        n += 724

    less_numbers = numbers[49:70]

    less_numbers.pop(10)

    avg = sum(less_numbers) / len(less_numbers)
    avg = round(avg)

    return avg


def work(n):
    set_1 = set(range(2, n + 1, 2))
    set_2 = set(range(5, 101, 5))

    union = set_1.union(set_2)
    sum_1 = sum(union)

    inter = set_1.intersection(set_2)
    sum_2 = sum(inter)

    return sum_1 + sum_2


def farm(animal):
    farm1 = {
        'корова': [11, 250],
        'курица': [5, 2],
        'свинья': [12, 100],
        'гусь': [8, 5],
        'лошадь': [18, 400]
    }

    farm2 = {
        'корова': [13, 230],
        'курица': [5, 3],
        'свинья': [11, 90],
        'гусь': [9, 5],
        'индюк': [10, 8]
    }

    if (animal in farm1) and (animal in farm2):
        age1 = farm1[animal][0]
        mass1 = farm1[animal][1]

        age2 = farm2[animal][0]
        mass2 = farm2[animal][1]

        if age1 == age2:
            return (mass1 + mass2) / 2
        elif age1 < age2:
            return mass1
        else:
            return mass2
    elif animal in farm1:
        return farm1[animal][1]
    elif animal in farm2:
        return farm2[animal][1]


from sys import getsizeof


def check_generator():
    mas_gen = [i for i in range(1000000) if i % 7 == 0]
    mem1 = getsizeof(mas_gen)

    def gen():
        for i in range(1000000):
            if i % 7 == 0:
                yield i

    gen = gen()
    elem1 = next(gen)
    elem2 = next(gen)
    mem2 = getsizeof(elem2)

    return mem1 - mem2


from math import sqrt


def function(n):
    numbers = [10 * i for i in range(1, 10**(n-1) + 1)]  # прикольно, понравилось

    def div8(x):
        return x % 8 == 0

    list_1 = list(filter(div8, numbers))
    list_2 = list(map(sqrt, list_1))
    list_3 = list(zip(list_1, list_2))

    total_sum = 0
    for num, sq in list_3:
        total_sum += num + sq

    total_sum = round(total_sum)

    return total_sum


# Примеры использования:
print(function(5))  # 125577203
print(function(6))  # 12517167165

