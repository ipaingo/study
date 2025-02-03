import numpy as np

# Функция для вычисления оценки вероятности P(N <= k) с помощью метода контрольных случайных величин
def estimate_prob(p, k):
    count = np.sum(np.random.uniform(0, 1, len(p)) <= p) # создаём равномерное распределение, сравниваем каждый элемент и считаем количество вер, меньше или равно неисправ
    return count

p = np.array([0.9, 0.5, 0.3, 0.4])  # вероятности неисправности элементов
k = 2 # заданный порог
iterations = 10000

prob_estimate = np.array([estimate_prob(p, k) for _ in range(iterations)]) # массив, содержащий оценку вероятности, рассчитанную с использованием функции estimate_prob для каждой итерации цикла.

I = prob_estimate <= k

c = -np.cov(np.array([I, prob_estimate]), bias=True)[0, 1] / np.sum(p * (1 - p))
Z = I + c * (prob_estimate - np.sum(p))

print("КСВ:", np.mean(Z))

# Стандартный метод Монте-Карло для проверки
cnt_broken = 0
n = len(p)
M = 10000
for i in range(M):
    x_p = np.random.uniform(0, 1, n)

    if np.sum(x_p < p) > k:
        cnt_broken += 1

print(f"Вероятность работающей системы (Метод Монте-Карло): {(1 - (cnt_broken / M)) * 100}%")