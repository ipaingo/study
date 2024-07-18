def build1(a, v, tl, tr):
    if tl == tr:
        if a[tl] == 1:
            t1[v] = 1
        else:
            t1[v] = 0
    else:
        tm = (tl + tr) // 2
        build1(a, v * 2, tl, tm)
        build1(a, v * 2 + 1, tm + 1, tr)
        t1[v] = t1[v * 2] + t1[v * 2 + 1]


def build2(a, v, tl, tr):
    if tl == tr:
        if a[tl] == 0:
            t2[v] = 1
        else:
            t2[v] = 0
    else:
        tm = (tl + tr) // 2
        build2(a, v * 2, tl, tm)
        build2(a, v * 2 + 1, tm + 1, tr)
        t2[v] = t2[v * 2] + t2[v * 2 + 1]


def s(t, v, tl, tr, l, r):
    if l > r:
        return 0
    if (l == tl) and (r == tr):
        return t[v]
    tm = (tl + tr) // 2
    return s(t, v * 2, tl, tm, l, min(r, tm)) + s(
        t, v * 2 + 1, tm + 1, tr, max(l, tm + 1), r
    )


n = 5
t1 = 4 * n * [0]
t2 = 4 * n * [0]

hm = [1, 0, 0, 1, 1]
build1(hm, 1, 0, 4)
build2(hm, 1, 0, 4)

print(s(t1, 1, 0, n - 1, 0, 1))
