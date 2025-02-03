import pandas as pd

def frame_data(values, indices):
    df = pd.DataFrame(values, indices)
    df.sort_index(ascending=False, inplace=True)
    return df.iloc[1, -1]

print(frame_data([[1,11,21],[1,2,3],[-1,-2,-3]], ['V','E','F']))
print(frame_data([[111,111,31,41,51,116],[141,15,61,6,717,160],[77,82,91,324,314,10]], ['Z','E','F']))