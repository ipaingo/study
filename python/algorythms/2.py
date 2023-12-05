with open("input.txt", "r", encoding="utf-8") as file:
    arr = file.read()
    inp = list(map(int, arr.split()))

out = ((inp[0] + 1) // 2) * ((inp[1] + 1) // 2)

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(str(out))
