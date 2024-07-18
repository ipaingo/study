def build(a, v, tl, tr):
    if tl == tr:
        if a[tl] == ">":
            t[v] = 1
        else:
            t[v] = -1
    else:
        tm = (tl + tr) // 2
        build(a, v * 2, tl, tm)
        build(a, v * 2 + 1, tm + 1, tr)
        t[v] = t[v * 2] + t[v * 2 + 1]


def s(v, tl, tr, l, r):
    if l > r:
        return 0
    if (l == tl) and (r == tr):
        return t[v]
    tm = (tl + tr) // 2
    return s(v * 2, tl, tm, l, min(r, tm)) + s(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r)


n = int(input())
symb = list(input().split())

# n = 2
# symb = ['<', '>']

t = 4 * n * [0]

build(symb, 1, 0, n - 1)

stuff = [0] * (n + 1)

v = set()
stuff[0] = s(1, 0, n - 1, 0, n - 1)
stuff[n] = -s(1, 0, n - 1, 0, n - 1)
v.add(stuff[0])
v.add(stuff[n])

for i in range(1, n):
    stuff[i] = -s(1, 0, n - 1, 0, i - 1) + s(1, 0, n - 1, i, n - 1)
    v.add(stuff[i])

cnt = 1
ans = [0] * (n + 1)
for i in sorted(v):
    for j in range(0, len(stuff)):
        if stuff[j] == i:
            ans[j] = cnt
            cnt += 1

print(" ".join(map(str, ans)))
