# Импорт необходимых библиотек
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.matplotlib.use('TkAgg')

# Определение функции для получения угла theta
def get_theta(theta, r, s):
    # Первый случай: текущий угол находится между theta_bar и 2*pi - theta_bar
    if theta_bar < theta < 2 * np.pi - theta_bar:
        return (theta + s) % (2 * np.pi)
    # Второй случай: угол находится вне этого диапазона
    else:
        return (theta + (s / (r + s_bar))) % (2 * np.pi)

# Функция для получения z1
def get_z1(theta, w, r):
    # Первый случай: текущий угол находится между theta_bar и 2*pi - theta_bar
    if theta_bar < theta < 2 * np.pi - theta_bar:
        return L - r * np.cos(theta) + w
    # Второй случай: угол находится вне этого диапазона
    else:
        return L - r * np.cos(theta_bar) + w

# Функция для получения z2
def get_z2(theta):
    # Первый случай: текущий угол меньше pi
    if 0 <= theta < np.pi:
        return 1
    # Второй случай: текущий угол больше или равно pi и меньше 2*pi
    elif np.pi <= theta < 2 * np.pi:
        return -1

# Функция для визуализации результатов
def visualization(true_thetas, predict_thetas):
    indexes_x = [i for i in range(1, 201)]
    plt.plot(indexes_x, predict_thetas, label='Предсказанные значения')
    plt.plot(indexes_x, true_thetas, 'r', label='Истинные значения')
    plt.xlabel('Время')
    plt.ylabel('Позиция')
    plt.title('Предсказанные и истинные значения')
    plt.legend()
    plt.show()

# Функция для определения веса
def tri_f(x):
    a, b, c = -w_bar, w_bar, 0
    if a <= x < c:
        return (2 * (x - a)) / ((b - a) * (c - a))
    elif x == c:
        return 2/(b-a)
    elif c < x <= b:
        return (2 * (b - x)) / ((b - a) * (b - c))
    else:
        return 0.0

# Функция для обновления весов
def new_weight(z_1, z_2, true_z_1, true_z_2):
    w1 = tri_f(true_z_1 - z_1)
    if np.isnan(true_z_2):
        return w1
    elif true_z_2 == z_2:
        return w1
    else:
        return 0.0

# Основная часть программы
if __name__ == '__main__':
    # Векторизация функций
    vectorized_get_theta = np.vectorize(get_theta)
    vectorized_get_z1 = np.vectorize(get_z1)
    vectorized_get_z2 = np.vectorize(get_z2)
    vectorized_new_weight = np.vectorize(new_weight)

    # Параметры
    N = 3000  # Количество частиц
    L = 2     # Заданный параметр
    w_bar = 0.1  # Среднее значение шума
    theta_bar = np.pi/3  # Заданный угол
    s_bar = 0.3  # Среднее значение сдвига

    # Загрузка данных
    data = pd.read_csv("C:\\Users\\regst\\Desktop\\учёба\\им\\PF_data.txt", sep=",")

    # Генерация начальных условий
    R = np.random.uniform(0, 2 * L, N)
    particles = np.random.uniform(0, 2 * np.pi, N)
    weights = np.ones(N) / N

    # Массив для хранения оцененных позиций
    estimated_positions = np.zeros(200)

    # Цикл по времени
    for k in range(200):
        # Получение истинных значений
        true_z1 = data['distSensor'][k]
        true_z2 = data['halfPlaneSensor'][k]

        # Генерация случайного значения s
        S = np.random.uniform(-s_bar, s_bar, N)

        # Обновление углов
        particles = vectorized_get_theta(particles, R, S)

        # Вычисление z1
        z1 = vectorized_get_z1(particles, weights, R)

        # Вычисление z2
        z2 = vectorized_get_z2(particles)

        # Обновление весов
        weights = vectorized_new_weight(z_1=z1, z_2=z2, true_z_1=true_z1, true_z_2=true_z2)

        # Нормализация весов
        weights /= np.sum(weights)

        # Оценка позиции
        estimated_positions[k] = np.sum(particles * weights)

        # Индексация частиц
        indices = np.random.choice(np.arange(N), size=N, p=weights)
        particles = particles[indices]
        weights = weights[indices]
        R = R[indices]

    # Визуализация результатов
    visualization(data['GroundTruth'], estimated_positions)