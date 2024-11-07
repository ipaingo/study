import scipy.integrate as integrate
import numpy as np

result1 = integrate.quad(
	lambda x: np.cos(x) + np.sin(x) - 1,
	np.pi,
	2*np.pi
)

result2 = integrate.dblquad(
	lambda x, y: 2*x - y,
	1,
	2,
	lambda x: x,
	lambda x: x*x
)

print(result1[0]) # второй элемент кортежа - допустимая погрешность
print(result2[0])