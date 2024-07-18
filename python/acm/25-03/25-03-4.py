n, q = map(int, input().split())

a = list(map(int, input().split()))

c = 0
for i in range(q):
    if sum(a[:i]) == 0:
        c = i
    for j in range(c, int(input())):
        if a[j] > 0:
            a[j] -= 1

print(a.count(0))
