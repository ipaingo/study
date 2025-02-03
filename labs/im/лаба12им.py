import numpy as np
from scipy import stats

# Определение параметров
num_experiments = 100 # Количество экспериментов
sample_size = 10 # Размер каждой выборки
means = [2.000000002, 2, 2.000005] # Заданные математические ожидания для каждой выборки
significance_level = 0.1 # Уровень значимости для критерия

# Инициализация счетчика отвержения нулевой гипотезы
null_hypothesis_rejections = 0

# Использование метода Монте-Карло для оценки мощности критерия
for _ in range(num_experiments):
    # Генерация выборок для каждого заданного математического ожидания
    samples = [np.random.normal(mean, 0.1, sample_size) for mean in means]

    # Проведение однофакторного дисперсионного анализа и проверка нулевой гипотезы
    f_stat, p_value = stats.f_oneway(*samples)
    if p_value < significance_level:
        null_hypothesis_rejections += 1

# Оценка мощности критерия
power = null_hypothesis_rejections / num_experiments
print("Мощность критерия:", power)