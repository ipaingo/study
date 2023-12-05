def solve(l, a, c):
    # l - длина стержня, a - длины деталей,
    # c - стоимость деталей.
    n = len(a)
    rec = 0
    for i in range(n):
        if (a[i] <= l) and (rec < solve(l - a[i], a, c) + c[i]):
            rec = solve(l - a[i], a, c) + c[i]

    return rec


l = 20
a = [5, 6, 8, 7]
c = [2, 1, 3, 4]

print(solve(l, a, c))
