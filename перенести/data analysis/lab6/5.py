import pandas as pd
import numpy as np

def func():
    s = pd.Series(np.random.normal(size=200))
    s = s**2
    s.index += 2

    print(s[s > 2].count())
    print(s[(s.index % 2 == 1) & (s < 2)].sum())

func()
