import re
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

def create_dict():
    with open("n_log2.txt", "r", encoding="utf-8") as file:
        text = file.readlines()

    dict_volumes = dict()

    for line in text:

        search_result = re.search(r'(^[0-9:]+,[0-9]+).+A00000000002 <--->.+KEEP.+volume=([0-9]+)', line)
        if not search_result:
            continue

        line_time = search_result.group(1)
        volume = search_result.group(2)
        dict_volumes[line_time] = volume
    return dict_volumes

def sort_dict(d):
    time = range(10, 70, 10)
    
    times = list(map(lambda x: f"15:{'{:02}'.format(x)}:00,000", time))
    # print(times)
    ans = dict()
    index = 0

    curr = list()
    for time, v in d.items():
        # print(time, index)
        curr.append(int(v))
        if time >= times[index]:
            # print(current)
            ans[index] = sum(curr)/len(curr)
            index += 1
            curr = list()
        if index > len(times):
            break
    ans[index] = sum(curr)/len(curr)
    return ans
    

dict_volumes = create_dict()
dict_10min = {k: v for k, v in dict_volumes.items() if k < "15:10:00,000"}


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))

ax1.set_title("График1. Volume")
ax2.set_title("График2. Volume по 10 минут")

ax1.xaxis.set_major_locator(MaxNLocator(nbins=10))
ax1.plot(dict_10min.keys(),dict_10min.values(), label="A00000000002")
ax1.legend(loc="upper left")


sorted_dict = sort_dict(dict_volumes)
# print(sorted_dict)
ax2.plot(sorted_dict.keys(), sorted_dict.values(), label="A00000000002")
ax2.legend(loc="upper left")
ax2.set_xticks(range(0, 6))
plt.show()