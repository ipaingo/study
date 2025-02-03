import pandas as pd


transaction = [120, -31, '20.1', 12.3, 'bank', 12, -4, -7, 150, 'mr.', 23, 32, 21]

t = pd.Series(transaction, index=range(10, 23))
print(t)

t = t[t.apply(lambda x: type(x) == int)]
print('-------------')
print(t)

print(t.var(ddof=1)) # дисперсия несмещенная: ddof вычитается из N при вычислении
print(t.mean())