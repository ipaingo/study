import scipy
import matplotlib.pyplot as plt

uniform = scipy.stats.uniform(loc=-5, scale=15) # равномерное
res = uniform.rvs(20)

dens = uniform.pdf(res) # плотность
distr = uniform.cdf(range(-5, 11)) # функция распределения
print(res)
print(f"Плотность(0): {dens[0]}\nФункция распределения(0): {distr[0]}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))


ax1.plot(res, dens)
ax1.set_title("График плотности")

ax2.plot(range(-5, 11), distr)
ax2.set_title("Функция распределения")

plt.show()
