n, m = map(int, input().split())

a = [[] * m for i in range(n)]
b = [[] * m for j in range(n)]

for i in range(n):
    a[i] = list(map(int, input().split()))

for i in range(n):
    b[i] = list(map(int, input().split()))

temp = ""

for i in range(n):
    for j in range(m):
        temp += str(a[i][j] + b[i][j]) + " "
    print(temp[: len(temp) - 1])
    temp = ""
