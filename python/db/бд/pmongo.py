import pymongo


# Подключение
client = pymongo.MongoClient("192.168.112.103")
database = client["22306"]

# Список коллекций в базе данных
print(database.list_collection_names())


# Создание коллекции
collection_name = database["test"]

# print(client.list_database_names())
# print(client['22306'])

team = {
    "couch": {"name": "John", "s_name": "Connor", "address": "Highway 37"},
    "players": {"first": "I'm", "second": "you"},
}
collection_name.insert_one(team)
x = collection_name.find_one()
print(x)

# find находит все, можно обработать в цикле

# Выводить только некоторые атрибуты
# for x in collection_name.find({},{ "_id": 0, "name": 1, "address": 1 }): 0 - не выводим, 1 -выводим

# Фильтрация
# myquery = { "address": { "$gt": "S" } }

# Сортировка
# mydoc = collection_name.find().sort("name")
"""
Удаление одного
myquery = { "address": "Mountain 21" }
collection_name.delete_one(myquery)
x = collection_name.delete_many(myquery) удаление многих

Изменение одного документа
myquery = { "address": "Valley 345" }
newvalues = { "$set": { "address": "Canyon 123" } }

collection_name.update_one(myquery, newvalues)
"""

collection_name.drop()  # Удалить коллекцию
