import pandas as pd

def sellers(n):
    df = pd.read_csv("tranzaktions.csv", delimiter="\t")
    group = df.groupby('Продавец').get_group("seller_" + str(n))
    sum_n, avg_n = group["Цена (млн)"].agg(["sum", "mean"])
    # avg_n = round(group["Цена (млн)"].agg(["mean"]))
    avg2_n = round((group.where(group["Цена (млн)"] >= 2))["Цена (млн)"].mean())
    return sum_n + round(avg_n) + avg2_n

print(sellers(2))
