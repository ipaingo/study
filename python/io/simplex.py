import sys
from numpy import *

N = 102
M = 102
global f
f_new = 0
c = zeros(N)
a = zeros((M, N))
b = zeros(M)
u = zeros(M, dtype=int)
z = zeros(N)
a_new = zeros((M, N))
b_new = zeros(M)
z_new = zeros(N)


def make_table(n, m):
    # костыли мои костыли...
    global f
    f_new = 0
    for i in range(m):
        f_new += c[u[i]] * b[i]
    f = f_new
    for i in range(n):
        for j in range(m):
            z[i] += c[u[j]] * a[j][i]
        z[i] -= c[i]


def show_table(n, m):
    global f
    print("+-------+-------+" + "-------+" * n)

    print("| Basis |  BSD  |", end="")
    for i in range(n):
        spaces = 6 - len(str(i + 1))
        print(" " * spaces + "x" + str(i + 1) + "|", end="")
    print()

    print("+-------+-------+" + "-------+" * n)

    for i in range(m):
        spaces = 6 - len(str(i + 1))

        print("|" + " " * spaces + "x" + str(u[i] + 1) + "|", end="")

        b_form = '{:.2f}'.format(b[i])
        spaces_b = 7 - len(b_form)
        print(spaces_b * " " + b_form + "|", end="")
        for j in range(n):
            a_form = '{:.2f}'.format(a[i][j])
            spaces_a = 7 - len(a_form)
            print(spaces_a * " " + a_form + "|", end="")
        print()

    print("+-------+-------+" + "-------+" * n)
    print("|   z   |", end="")

    f_form = '{:.2f}'.format(f)
    spaces_f = 7 - len(f_form)
    print(" " * spaces_f + f_form + "|", end="")
    for i in range(n):
        z_form = '{:.2f}'.format(z[i])
        spaces_z = 7 - len(z_form)
        print(" " * spaces_z + z_form + "|", end="")
    print("\n" + "+-------+-------+" + "-------+" * n)


def calculate_table(n, m):
    global f
    mx = 0
    s = r = -1
    for i in range(n):
        if z[i] > mx:
            mx = z[i]
            s = i

    if mx == 0:
        return 1

    mn = 1000000000
    for i in range(m):
        if a[i][s] > 0 and b[i] / a[i][s] < mn:
            mn = b[i] / a[i][s]
            r = i

    if mn == 1000000000:
        return 2

    u[r] = s
    print(r+1, s+1)

    for i in range(n):
        a_new[r][i] = a[r][i] / a[r][s]

    b_new[r] = b[r] / a[r][s]

    # прямоугольники мои прямоугольники...
    for i in range(m):
        if i != r:
            for j in range(n):
                a_new[i][j] = (a[i][j] * a[r][s] - a[r][j] * a[i][s]) / a[r][s]

    for i in range(m):
        if i != r:
            b_new[i] = (b[i] * a[r][s] - a[i][s] * b[r]) / a[r][s]

    for i in range(n):
        z_new[i] = (z[i] * a[r][s] - a[r][i] * z[s]) / a[r][s]
    f_new = (f * a[r][s] - z[s] * b[r]) / a[r][s]

    for i in range(m):
        for j in range(n):
            a[i][j] = a_new[i][j]
    for i in range(m):
        b[i] = b_new[i]
    for i in range(n):
        z[i] = z_new[i]
    f = f_new
    return 0


def show_answer(n, m):
    global f
    print("Найдено решение:")
    print("z* =", -f)
    x = zeros(n)
    for i in range(m):
        x[u[i]] = b[i]
    x = x[:n - m]
    print("x* = (", end="")
    for i in range(len(x) - 1):
        print(str('{:.2f}'.format(x[i])) + ", ", end="")
    print(str('{:.2f}'.format(x[len(x) - 1])) + ")")


n = int(input("Enter n: "))
m = int(input("Enter m: "))
# n = 6
# m = 3
print("Enter ci(i=1..n)")
c = [0] * (n)
c = list(map(int, input().split()))
# c = [6, 3, 6, 5, 2, 3]
# print(c)

for i in range(n):
    c[i] = -c[i]
# print(c)

a = [[0] * (n) for _ in range(m)]
print("Enter aji(i=1..n, j=1..m)")
for j in range(m):
    a[j] = list(map(int, input().split()))
# a = [[5, -1, 2, -1, 5, 0], [4, 0, 6, 2, 0, 4], [0, 5, 4, 5, 3, 1]]
# print(a)

b = [0] * (m)
print("Enter bj(j=1..m)")
b = list(map(int, input().split()))
# b = [4, 5, 8]
# print(b)

tru_n = n

Q = 0
# u = [0] * (m)
for i in range(m):
    c.append(Q)
    u[i] = i + n
    # print(u[i])
    for j in range(m):
        if j == i:
            a[i].append(1)
        else:
            a[i].append(0)

n += m

make_table(n, m)

while True:
    show_table(n, m)
    res = calculate_table(n, m)
    if res == 1:
        for i in range(m):
            if u[i] > tru_n and b[i]:
                print("Нет решений")
                exit()
        show_answer(n, m)
        break
    elif res == 2:
        print("Бесконечность")
        break
