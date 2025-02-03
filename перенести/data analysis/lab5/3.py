import numpy as np
import scipy
import matplotlib.pyplot as plt


x = np.linspace(0, 15, 16, endpoint=True)
y = np.vectorize(lambda x: 1.1**(-x) + 1.2**x)(x)

# print(x, y)

x_new = np.linspace(0, 15, num=100, endpoint=True)
tck = scipy.interpolate.splrep(x, y, s=0)
y_new1 = scipy.interpolate.interp1d(x, y)(x_new)
y_new2 = scipy.interpolate.splev(x_new, tck, der=0)
plt.plot(x, y, 'b', x_new, y_new1, 'r', x_new, y_new2, 'g', x, y, 'x')
plt.legend(['Данные', "Линейная интерполяция", 'Кубический сплайн'])
plt.show()