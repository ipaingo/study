from scipy.integrate import odeint
import numpy as np


def f(y, x):
	return x*x + 2*x

y0 = 1

step = 200
x_output = np.linspace(0, 4, step)
    
y_result = odeint(f, y0, x_output)
y_result = y_result[:, 0]

print(y_result[-1])



x_output1 = np.linspace(0, 4, step//100)
    
y_result1 = odeint(f, y0, x_output1)
y_result1 = y_result1[:, 0]

print(y_result1[-1])