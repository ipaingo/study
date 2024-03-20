graph = [[0] * (6)] * (6)
print("Введите матрицу: ")
for j in range(6):
    graph[j] = list(map(int, input().split()))

# graph = [[0, 1, 9, 8, 8, 6],
#          [1, 0, 4, 7, 6, 7],
#          [7, 3, 0, 8, 7, 4],
#          [3, 2, 4, 0, 6, 6],
#          [1, 3, 2, 1, 0, 4],
#          [3, 4, 8, 7, 5, 0]]
paths = []
curr_index = 0
min_path = 1000000000
index = 0

# матрица всего шесть на шесть, можем себе позволить полный перебор.
# если бы нужно было писать в общем виде, пришлось бы помучиться, разумеется. :)
for i1 in range(6):
    for i2 in range(6):
        for i3 in range(6):
            for i4 in range(6):
                for i5 in range(6):
                    for i6 in range(6):
                        if ((i1 != i2) and (i1 != i3) and (i1 != i4) and (i1 != i5) and (i1 != i6)
                                and (i2 != i3) and (i2 != i4) and (i2 != i5) and (i2 != i6)
                                and (i3 != i4) and (i3 != i5) and (i3 != i6)
                                and (i4 != i5) and (i4 != i6)
                                and (i5 != i6)):
                            paths.append(str(i1 + 1) + str(i2 + 1) + str(i3 + 1) + str(i4 + 1) + str(i5 + 1) + str(i6 + 1))
                            # print(paths[curr_index])
                            curr_path = graph[i1][i2] + graph[i2][i3] + graph[i3][i4] + graph[i4][i5] + graph[i5][i6]
                            if curr_path < min_path:
                                min_path = curr_path
                                # print(min_path)
                                index = curr_index
                            curr_index += 1

print('Оптимальный маршрут: ' + paths[index] + ' (длина: ' + str(min_path) + ')')
