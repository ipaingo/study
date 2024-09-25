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

    return(avg)



print(my_list(277))