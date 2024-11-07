import scipy
import sympy
import numpy as np
import matplotlib.pyplot as plt




x = np.linspace(0, 15, 16, endpoint=True)
y = np.vectorize(lambda x: pow(1.1, -x) + pow(1.2, x))(x)
x_new = np.linspace(0, 15, num=100, endpoint=True)
tck = scipy.interpolate.splrep(x, y, s=0)
y_new1 = scipy.interpolate.interp1d(x, y)(x_new)
y_new2 = scipy.interpolate.splev(x_new, tck, der=0)
plt.plot(
    x, y, 'b',
    x_new, y_new1, 'r',
    x_new, y_new2, 'g',
    x, y, 'x'
)
plt.legend(['Данные', "Линейная интерполяция", 'Кубический сплайн'])
plt.show()



# xk = np.arange(-5, 11)
# vals = scipy.stats.uniform(loc=-5, scale=16).rvs(20)
# pk = scipy.stats.uniform(loc=-5, scale=16).pdf(xk)
# print(vals)
# rv = scipy.stats.rv_discrete(values=(xk, pk))
# # print(rv.cdf(xk))
# # print(scipy.stats.ecdf(vals).cdf)

# print(rv.cdf(0))
# print(rv.pmf(0))

# fig = plt.figure()
# ax1 = fig.add_subplot(1, 2, 1)
# ax2 = fig.add_subplot(1, 2, 2)
# ax1.plot(xk, rv.cdf(xk))
# ax2.plot(xk, rv.pmf(xk))
# # ax2.vlines(pk, 0, scipy.stats.rv_discrete(loc=-5, scale=10).pdf(pk), colors='green', lw=1)
# ax1.set_title('Функция распределения')
# ax2.set_title('Плотность распределения')

# plt.show()

# from IPython.display import display  
# from sympy import *


# x = Symbol('x')
# display(limit(
#     (2 * x * x + x - 345)
#     / 
#     (x * x - x + 345),
# x, oo))