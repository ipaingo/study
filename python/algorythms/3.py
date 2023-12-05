with open("console.in", "r", encoding="utf-8") as file:
    arr = file.read()
    arr = arr.split("\n")

n = int(arr[0])
line = []
inp = []

for i in range(1, n+1):
    line.append(arr[i])

for i in range(n+1, len(arr)):
    inp.append(arr[i])

open("console.out", "w").close()

with open("console.out", "a", encoding="utf-8") as file:
    for i in range(len(inp)):
        for j in range(len(line)):
            if inp[i].find(line[j]) != -1:
                file.write(inp[i]+"\n")
                break
