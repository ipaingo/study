
#4 пункт

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

neutron_coord = set([(0, 0, 0)])  # начальная точка разделившегося ядра

def simulate_neutron_cascade(radius, energy, l_exponential, p1, p2, num_particles):
    total_energy = 0

    for _ in range(num_particles):
        neutron_energy = energy  # энергия нового нейтрона

        neutron_coord = set([(0, 0, 0)])  # начальная точка разделившегося ядра

        while neutron_coord:
            # Проверка вероятности захвата ядрами примесей значит успеет - поглощается
            if np.random.rand() < p1:
                neutron_coord.pop()
            else:
                # Симуляция деления ядра - если не поглощается - делится на 2 или 3
                num_sn = 2 if np.random.uniform(0, 1) < p2 else 3
                # Вычисляем новое местоположение точек
                # старт не из начальной точки, а из точки остановки
                for _ in range(num_sn):
                  try:
                    x0, y0, z0 = neutron_coord.pop()
                  except:
                    neutron_coord.add((x0, y0, z0))
                # углы наклона фи и тета
                  fi = np.arccos(1 - 2 * np.random.uniform(0, 1)) #Метод обратной функции
                  teta = np.random.uniform(0, 2 * np.pi)
                  # s - величина свободного пробега
                  s = np.random.exponential(scale=l_exponential)
                  '''
                  Параметр масштаба экспоненциального распределения.
                  Параметр масштаба определяет форму распределения, при этом большие значения приводят к более постепенному увеличению функции плотности вероятности.
                  Ожидаемое значение сгенерированных случайных чисел равно l_exponential.
                  '''
#l_exponential - проверить формулу
                  # Углы направления
                  Vx = np.sin(fi) * np.cos(teta)
                  Vy = np.sin(fi) * np.sin(teta)
                  Vz = np.cos(fi)

                  x = x0 + Vx * s
                  y = y0 + Vy * s
                  z = z0 + Vz * s
                  # Если координата попала в радиус
                  if(np.sqrt(x**2 + y**2 + z**2) <= radius):
                      neutron_coord.add((x, y, z))
                      total_energy += neutron_energy
                  # Если вышли за радиус - не рассматриваем
              # учитываем энергию от каждого нового нейтрона

                total_energy += neutron_energy * num_sn
    # усредненная энергия на один нейтрон
    return total_energy / num_particles

# Заданные параметры
radius = 15  # радиус шара в см
energy = 200  # энергия в МэВ выделяемая при делении
l_exponential = 2 #Длина пробега
#Добавить проверку на 1 величину свободного пробега
p1 = 0.4  # вероятность захвата ядрами примесей
p2 = 0.3  # вероятность получения 2-х вторичных нейтронов при делении
num_particles = 10000  # количество симулированных нейтронов

# Расчет средней энергии
average_energy = simulate_neutron_cascade(radius, energy, l_exponential, p1, p2, num_particles)

print(f"Среднее количество энергии на один нейтрон: {average_energy:.2f} МэВ")

# Визуализация результатов с добавлением электронов
x_coords = np.array([coord[0] for coord in neutron_coord])
y_coords = np.array([coord[1] for coord in neutron_coord])
z_coords = np.array([coord[2] for coord in neutron_coord])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Построение сферы
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_sphere = radius * np.outer(np.cos(u), np.sin(v))
y_sphere = radius * np.outer(np.sin(u), np.sin(v))
z_sphere = radius * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='b', alpha=0.3)

# Визуализация электронов
ax.scatter(x_coords, y_coords, z_coords, c='r', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
