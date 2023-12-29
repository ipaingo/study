n, m = map(int, input().split())
temp = list(map(int, input().split()))
b_l = temp[0]
b_r = temp[len(temp) - 1]
birds = []
for i in range(temp[len(temp) - 1] + 1):
    if i in temp:
        birds.append(1)
    else:
        birds.append(0)
birds = birds[1:]

temp = list(map(int, input().split()))
c_l = temp[0]
c_r = temp[len(temp) - 1]
cameras = []
for i in range(temp[len(temp) - 1] + 1):
    if i in temp:
        cameras.append(1)
    else:
        cameras.append(0)

max_count = 0

for i in range(b_r - c_l + c_r - b_l + 1):
    count = 0
    if i <= len(cameras) - 1:
        temp = cameras[len(cameras) - i - 1 :]
        if len(temp) <= b_r:
            temp += [0] * (b_r - len(temp))
        else:
            temp = temp[: b_r - i - 1]
    else:
        temp = [0] * (i - len(cameras) + 1) + cameras[: len(cameras) - i + b_r - 1]

    for j in range(b_r):
        if birds[j] * temp[j] == 1:
            count += 1

    if count > max_count:
        max_count = count

print(max_count)
