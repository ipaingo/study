import re
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

def create_dict():
    dict_capacitive_devices = dict()
    with open("n_log1.txt", "r", encoding="utf-8") as file:
        text = file.readlines()

    for line in text:

        search_result = re.search(r'(^[0-9:]+,[0-9]+).+A00000000001.+KEEP.+capacitive_devices=\[([B0-9,]+)].+link_power_arr=\[(.+)]', line)
        if not search_result:
            continue

        line_time = search_result.group(1)
        link_power = list(map(int, search_result.group(3).split(",")))
        capacitive_devices = search_result.group(2).split(",")

        for index in range(len(capacitive_devices)):
            current_cap = capacitive_devices[index]
            current_pwr = link_power[index]
            if current_cap not in dict_capacitive_devices:
                dict_capacitive_devices[current_cap] = dict()
            dict_capacitive_devices[current_cap][line_time] = current_pwr
    return dict_capacitive_devices


def create_time(begin, end):
    arr = []
    for i in range(begin, end+1):
        arr.append("14:"+'{:02d}'.format(i)+":00,000")
    return arr


def time_to_int(time, begin):
    time = list(map(int, re.split(r'[:,]', time)))
    begin = list(map(int, re.split(r'[:,]', begin)))
    return time[3] - begin[3] + (time[2] - begin[2])*1000 + (time[1] - begin[1])*1000*60


def main():
    minute = 60000
    dict_cap = create_dict()
    dict_b3 = {k: v for k, v in dict_cap["B00000000003"].items() if k < "14:10:00,000" }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    ax1.set_title("link_power за 10 минут")
    ax2.set_title("link_power за 5 минут")

    ax1.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax1.plot(dict_b3.keys(), dict_b3.values(), label="B00000000003")
    ax1.legend(loc='upper left')

    ax2.set_yticks(range(50, 82, 2))
    ax2.set_ylim(50, 82)
    ax2.set_xticks(range(0, minute*6, minute), create_time(5, 10))

    for name_cap, time_cap in sorted(dict_cap.items(), key=lambda tup: tup[0]):
        temp = dict()
        for time, value in time_cap.items():
            if "14:05:00,000" <= time < "14:10:00,000":
                temp[time_to_int(time, "14:05:00,000")] = value


        ax2.plot(temp.keys(), temp.values(), label=name_cap, marker=",")
    ax2.legend(loc='upper right')

    plt.show()


if __name__ == "__main__":
    main()





