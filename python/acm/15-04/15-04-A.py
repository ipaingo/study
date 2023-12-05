a = int(input())
b = int(input())
n = int(input())

for i in range(b, a-1, -1):
    temp = n
    cnt = temp // i
    temp = temp - cnt*i
    if a <= temp <= b:
        print('aaa')

