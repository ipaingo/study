def split_data(rows_to_split, interval):
    
    # началом будет первая отметка.
    count = float(rows_to_split[0].split()[0])
    
    # здесь мы будем считать отрывки.
    for i in range(1, len(rows_to_split)):
        
        # проверяем, не выйдем ли за пять минут в следующей строке.
        if ((float(rows_to_split[i].split()[0]) - count) >= interval) or (float(rows_to_split[i].split()[0]) == -1):
            
            # вставляем разделитель.
            rows_to_split.insert(i, '-1')
            
            # обновляем начало.
            count += interval
        
    return rows_to_split