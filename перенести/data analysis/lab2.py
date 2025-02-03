import re
import os

def function1(string):
    return len(re.findall(r"\b[оОэЭ]\w*\b", string))

def function2(string):
    return len(re.findall(r"\b[\w-]+\b", string))

def function3(string):
    return len(re.findall(r"\b[А-ЯA-Z]{2,}\b", string))

def repl(str):
    return "_" + str.group(0).lower()

def function4(string):
    return re.sub(r"([A-Z])([a-z]*)", repl, string)

def task5():
    with open('out1.txt', "w", encoding="utf-8") as write_file:
        with open('n_log1.txt', "r", encoding="utf-8") as read_file:
            for line in read_file:
                if re.search(r".*KEEP.*volume=.*", line) != None:
                    write_file.write(line)

        with open('n_log2.txt', encoding="utf-8") as read_file:
            for line in read_file:
                if re.search(r".*KEEP.*volume=.*", line) != None:
                    write_file.write(line)

    mx = 0
    mn = 999999999
    sum = 0
    col = 0
    with open('out1.txt', encoding="utf-8") as read_file:
        for line in read_file:
            num = int(re.search(r"volume=(\d*)", line).group(1))
            mx = max(mx, num)
            mn = min(mn, num)
            sum += num
            col += 1

    sum_mma = mx + mn + int(sum / col)

    print(sum_mma)



n_file_before = 0
n_file_after = 0
 
for root, dirs, files in os.walk("folder_main"):
    for file in files:
        n_file_before += 1
        if not file.endswith('.csv') and not file.endswith('.doc'):
            n_file_after += 1

print(n_file_before)
print(n_file_after)
print(n_file_before + n_file_after)