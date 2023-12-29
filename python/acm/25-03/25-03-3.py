l = int(input())

inp = list(input())
start = -1
a = 0
for i in range(l):
    if inp[i] == "a":
        a = 1
    if (inp[i] == "b") and (a == 0):
        start = i
    # print(start, a)
    if (start < i) and (inp[i] == "b") and (a == 1):
        for j in range(start + 1, i):
            inp[j] = "a"
        a = 0
        start = i

    if (i == l - 1) and (a == 1):
        for j in range(start + 1, l):
            inp[j] = "a"

print(inp.count("a"))
