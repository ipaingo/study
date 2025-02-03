#3 пункт

import numpy as np
from scipy.stats import weibull_min
from scipy.stats import norm
from scipy.stats import t

# Функция P(v) определяет вероятность в зависимости от значения v.
def P(v):
    if v < 4:
        return 0
    elif v < 15:
        return np.cos(v * np.pi / 11 + 7 * np.pi / 11) + 1
    elif v < 25:
        return 7 / 4 + v * 1 / 30 + v * v * 1 / 900
    else:
        return 0

lambda_val = 10  # Параметр масштаба для распределения Вейбулла
beta = 2         # Параметр формы для распределения Вейбулла
n = 10000        # Размер выборки

data = weibull_min.rvs(c=beta, scale=lambda_val, size=n)
data = np.vectorize(P)(data)

# Вычисление среднего значения и стандартного отклонения
mean_val = np.mean(data)
sd = np.std(data)
# Урезание методом отбора

# Значение Z для 95% доверительного интервала

Z = norm.cdf((1+0.95)/2) # критерий для двухсторонней область, квантиль нормального распределения

# Вычисление доверительного интервала
L = mean_val - Z * (sd / np.sqrt(n))
R = mean_val + Z * (sd / np.sqrt(n))

print(f"95% доверительный интервал: [{L}, {R}]")

a, b = 1, 10

data = weibull_min.rvs(c=beta, scale=lambda_val, size=n*2)
data = data[(data >= a) & (data <= b)]

new_data = data[0:n]
print(len(data))
print(len(new_data))

data = np.vectorize(P)(new_data)

# Вычисление среднего значения и стандартного отклонения
mean_val = np.mean(data)
sd = np.std(data)

# Значение Z для 95% доверительного интервала
Z = norm.cdf((1+0.95)/2)

# Вычисление доверительного интервала
L = mean_val - Z * (sd / np.sqrt(len(data))) #вместо n делить на длину массива data
R = mean_val + Z * (sd / np.sqrt(len(data)))

print(f"95% доверительный интервал: [{L}, {R}]")
print(Z)
