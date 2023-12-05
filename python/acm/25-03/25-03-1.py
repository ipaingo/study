n = int(input())
inp = list(map(int, input().split()))
nums = {}

for i in range(len(inp)):
    no = inp[i]
    if nums.get(no) is None:
        nums[no] = 1
    else:
        nums[no] += 1


print(sum(value == 1 for value in nums.values()))
