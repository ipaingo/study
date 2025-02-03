import numpy as np
# Инициализация переменных
center = np.array([1, 1, 2])  # центр шара M
R = 0.5                        # радиус шара M
alpha = 0.5                    # некоторый положительный параметр для функции f(omega)
n = 100                        # количество экспериментов
count = 1000                   # количество векторов в эксперименте

# Функция микрофасетной BRDF
def f(theta):
    return (alpha**2 * np.cos(theta)) / (np.pi * (np.cos(theta)**2 * (alpha**2 - 1) + 1)**2)

# Вспомогательная функция q1
def q1(theta):
    return 1/np.pi * np.cos(theta)

# Вспомогательная функция q2
def q2(theta):
    return f(theta)

# Функция видимости V(omega)
def V(omega):
# Константы из уравнения, полученного в результате объединения уравнений прямой и шара
    a = np.sum(omega**2)
    b = -2 * np.dot(omega, center) #скалярное произведение векторов и матриц
    c = np.sum(center**2) - R**2
# Если дискриминант > 0, то пересекает шар, если = 0, то касается шара,
#   иначе не пересекает и не касается шара
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        return 0
    return 1

# Функция для генерации случайных точек на полусфере
def generate_points(count_points, gen="stand"):
    # Угол theta
    theta = np.arccos(1 - np.random.uniform(0, 1, count_points))  # равномерное распределение
    if gen == "q1":
        theta = np.arccos(1 - 2 * np.random.uniform(0, 1, count_points)) / 2  # распределение q1
    elif gen == "q2":
        v = np.random.uniform(0, 1, count_points)
        theta = np.arccos(np.sqrt((1-v) / (v * (alpha**2 - 1) + 1)))  # распределение q2

    # Угол phi
    phi = np.random.uniform(0, 2 * np.pi, count_points)

    # Высчитывание новых координат
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    return np.column_stack((x, y, z))

def integral_q1():
   points = generate_points(count, "q1")
   integrand = np.apply_along_axis(lambda omega: f(np.arccos(omega[2])) * V(omega) * np.cos(np.arccos(omega[2])) / q1(np.arccos(omega[2])), 1, points)
   return np.mean(integrand)

def integral_q2():
   points = generate_points(count, "q2")
   integrand = np.apply_along_axis(lambda omega: f(np.arccos(omega[2])) * V(omega) * np.cos(np.arccos(omega[2])) / q2(np.arccos(omega[2])), 1, points)
   return np.mean(integrand)

def integral_standard():
   points = generate_points(count)
   integrand = np.apply_along_axis(lambda omega: f(np.arccos(omega[2])) * V(omega) * np.cos(np.arccos(omega[2])) * 2 * np.pi, 1, points)
   return np.mean(integrand)

var_q1 = np.var([integral_q1() for _ in range(n)])

var_q2 = np.var([integral_q2() for _ in range(n)])
var_standard = np.var([integral_standard() for _ in range(n)])


np.set_printoptions(suppress=True)

print(integral_q1())
print(integral_q2())
print(integral_standard())
print("Дисперсия оценки интеграла с использованием вспомогательного распределения q1:", var_q1)
print("Дисперсия оценки интеграла с использованием вспомогательного распределения q2:", var_q2)
print("Дисперсия оценки интеграла с использованием стандартного метода Монте-Карло:", var_standard)
