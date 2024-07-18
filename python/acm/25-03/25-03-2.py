n, k = map(int, input().split())
arr = list(map(int, input().split()))
count = 0

for i in range(n):
    ma = mi = arr[i]
    temp = [arr[i]]
    for j in range(i + 1, n):
        temp.append(arr[j])

        if arr[j] > ma:
            ma = arr[j]
        if arr[j] < mi:
            mi = arr[j]

        # print(ma, mi, temp)
        if (ma - mi) > k:
            break

        if (ma - mi) == k:
            count += 1

print(count)
