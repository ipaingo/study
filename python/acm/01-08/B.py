n = int(input())
s = list(map(int, input().split()))
c = list(map(int, input().split()))
q = int(input())
x = list(map(int, input().split()))

for j in range(q):
    temp = s.copy()
    ans = 0
    for i in range(n):
        if (temp[i] < x[j]) and (temp[i] > -1):
            x[j] -= temp[i]
            ans += c[i]
            temp[i] = -1
    print(ans)
