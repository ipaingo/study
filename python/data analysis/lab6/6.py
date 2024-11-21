import pandas as pd
import numpy as np

def func():
    df = pd.read_csv("CreditCardTransaction.csv")
    
    np.random.seed(12)
    dfs = df.sample(10000)

    departs = dfs["Department"].value_counts()
    departs = departs.nlargest(3)

    trnx = dfs[(dfs["Year"] == 2022) & ((dfs["Month"] == 1) | (dfs["Month"] == 2))]["TrnxAmount"]
    sum_trnx = trnx.sum()
    med_trnx = trnx.median()

    dfs["TrnxDifference"] = abs(med_trnx) - abs(dfs["TrnxAmount"])

    print("departs\n", departs)
    print("sum", sum_trnx)
    print("median", med_trnx)
    print(dfs)


func()
