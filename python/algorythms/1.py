def power(a, n, m):
    if n == 0:
        return 1

    p = power(a, n // 2, m)
    p = (p * p) % m
    if n % 2:
        p = (p * a) % m
    return p


with open("input.txt", "r", encoding="utf-8") as file:
    arr = file.read()
    inp = list(map(int, arr.split()))

out = int(power(inp[0], inp[1], inp[2]))

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(str(out))
