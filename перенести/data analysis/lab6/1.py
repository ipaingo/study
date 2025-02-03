import pandas as pd

def series_data(name, index):
    nums = []
    for p in range(1, 10000):
        if p % 17 == 0:
            nums.append(p)
    
    s = pd.Series(nums)
    s.name = name
    s.index += 1
    s[s.index % 2 == 1] *= 2
    s[s.index % 2 == 0] += 555

    return round((s[index] + s[index + 1] + s[index + 15]) / 3)

print(series_data('Название серии', 52))
print(series_data('Название серии', 72))