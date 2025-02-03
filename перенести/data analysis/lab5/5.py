from sympy import *
from IPython.display import display
init_printing()


x = Symbol("x")
expr = (2*x**2 + x - 345)/(x**2 - x + 345)
print(limit(expr, x, oo))

