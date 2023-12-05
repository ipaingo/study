from pymongo import MongoClient
from tkinter import *
from tkinter import ttk


def fill_items():
    db[table_items].drop()
    db.create_collection(table_items)
    collection = db[table_items]
    for i in [
        {
            "name": "Men's coat",
            "manufacturer": "H&M",
            "price": "5000",
            "features": {
                "category": "clothes",
                "weight": "1000",
                "type": "men",
                "colour": "red"
            },
            "buyers": [
                {
                    "name": "Ivan Ivanov",
                    "delivery": "Courier",
                    "review": "Great coat!",
                    "date_bought": "01-01-2023"
                },
                {
                    "name": "Petr Petrov",
                    "delivery": "Post",
                    "review": "Didn't fit.",
                    "date_bought": "02-01-2023"
                }
            ]
        },

        {
            "name": "Women's coat",
            "manufacturer": "OSTIN",
            "price": "2000",
            "features": {
                "category": "clothes",
                "weight": "1500",
                "type": "women",
                "colour": "grey"
            },
            "buyers": [
                {
                    "name": "Alina Ivanova",
                    "delivery": "Post",
                    "review": "Not bad at all.",
                    "date_bought": "04-01-2023"
                },
                {
                    "name": "Ksenia Petrova",
                    "delivery": "CDEK",
                    "review": "Cheap and looks good.",
                    "date_bought": "04-02-2023"
                }
            ]
        },

        {
            "name": "Kid's hat",
            "manufacturer": "RESERVED",
            "price": "200",
            "features": {
                "category": "clothes",
                "weight": "300",
                "type": "kids",
                "colour": "sky-blue pink"
            },
            "buyers": [
                {
                    "name": "Alina Ivanova",
                    "delivery": "Post",
                    "review": "Fits well.",
                    "date_bought": "01-01-2023"
                }
            ]
        },

        {
            "name": "Round plate",
            "manufacturer": "Kuchenland",
            "price": "1000",
            "features": {
                "category": "tableware",
                "weight": "1000",
                "type": "dishes",
                "colour": "white"
            },
            "buyers": [
                {
                    "name": "Ksenia Petrova",
                    "delivery": "CDEK",
                    "review": "Came broken.",
                    "date_bought": "01-01-2023"
                },
                {
                    "name": "Ivan Ivanov",
                    "delivery": "Courier",
                    "review": "Simple, looks nice, usable.",
                    "date_bought": "08-01-2023"
                }
            ]
        },

        {
            "name": "Set of forks",
            "manufacturer": "Prizma",
            "price": "2000",
            "features": {
                "category": "tableware",
                "weight": "500",
                "type": "cutlery",
                "colour": "metallic"
            },
            "buyers": [
                {
                    "name": "Alina Ivanova",
                    "delivery": "CDEK",
                    "review": "Fine",
                    "date_bought": "05-01-2023"
                },
                {
                    "name": "Petr Petrov",
                    "delivery": "Post",
                    "review": "Good",
                    "date_bought": "06-01-2023"
                }
            ]
        },

        {
            "name": "Set of spoons",
            "manufacturer": "Prizma",
            "price": "2000",
            "features": {
                "category": "tableware",
                "weight": "500",
                "type": "cutlery",
                "colour": "metallic"
            },
            "buyers": [
                {
                    "name": "Ivan Ivanov",
                    "delivery": "CDEK",
                    "review": "I cut my hand with it",
                    "date_bought": "05-01-2023"
                },
                {
                    "name": "Alina Ivanova",
                    "delivery": "CDEK",
                    "review": "Ordered some more after my husband threw them away in anger",
                    "date_bought": "09-01-2023"
                },
            ]
        },
        {
            "name": "Car engine",
            "manufacturer": "Toyota",
            "price": "100000",
            "features": {
                "category": "auto parts",
                "weight": "500000",
                "type": "engine",
                "colour": "no colour"
            },
            "buyers": [
                {
                    "name": "Ivan Ivanov",
                    "delivery": "Train",
                    "review": "Spent all my money on it",
                    "date_bought": "05-01-2023"
                },
            ]
        },

        {
            "name": "Car window cleaner",
            "manufacturer": "Toyota",
            "price": "1000",
            "features": {
                "category": "auto parts",
                "weight": "1500",
                "type": "additional",
                "colour": "black",
            },
            "buyers": [
                {
                    "name": "Petr Petrov",
                    "delivery": "Post",
                    "review": "Works well",
                    "date_bought": "05-07-2023"
                },
                {
                    "name": "Ivan Ivanov",
                    "delivery": "Train",
                    "review": "It's so cheap.",
                    "date_bought": "09-01-2023"
                }
            ]
        },
        {
            "name": "Car wing",
            "manufacturer": "Renault",
            "price": "10000",
            "features": {
                "category": "auto parts",
                "weight": "1000",
                "type": "car corpus",
                "colour": "red",
            },
            "buyers": [
                {
                    "name": "Ksenia Petrova",
                    "delivery": "Post",
                    "review": "Looks good as new.",
                    "date_bought": "05-07-2023"
                },
            ]
        },

        {
            "name": "iPhone",
            "manufacturer": "Apple",
            "price": "100000",
            "features": {
                "category": "mobile phones",
                "weight": "800",
                "type": "14",
                "colour": "deep purple",
                "level of pointlessness": "10/10",
            },
            "buyers": [
                {
                    "name": "Ivan Ivanov",
                    "delivery": "CDEK",
                    "review": "It's so expensive.",
                    "date_bought": "05-07-2023"
                },
                {
                    "name": "Petr Petrov",
                    "delivery": "CDEK",
                    "review": "",
                    "date_bought": "09-01-2023"
                },
                {
                    "name": "Alina Ivanova",
                    "delivery": "Post",
                    "review": "My son was very happy.",
                    "date_bought": "09-01-2023"
                }
            ]
        }
    ]:
        collection.insert_one(i)


def draw():
    global previous
    previous()
    frame = Frame(root)
    frame.pack(fill=X)
    dict_queries[comb_table.get()](frame)
    previous = lambda: frame.destroy()


def beautify(lst):
    text = "{\n"
    for i in lst:
        text += f"\t{i}\n"
    text += "}\n"
    return text


def category_do(value, doc):
    doc.delete('1.0', END)
    for i in table.find({"features.category": value}):
        doc.insert(END, f'{i["name"]}\n')


def category(frame):
    fr = Frame(frame)
    fr.pack()
    Label(fr, text="Select category: ").pack(anchor=NE, side=LEFT, padx=5, pady=5)
    arr = list_category
    var = StringVar(value=arr[0])
    comb = ttk.Combobox(fr, values=list(arr), textvariable=var)
    comb.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    doc_show = Text(frame, height=140)

    process = lambda: category_do(comb.get(), doc_show)
    Button(fr, text="Find", command=process).pack(anchor=NE, side=LEFT, padx=5, pady=5)
    doc_show.pack(side=BOTTOM, fill=X)


def characteristics_do(value, doc):
    doc.delete('1.0', END)
    i = table.find({"features.category": value})[0]
    d = dict(i["features"]).keys()
    doc.insert(END, beautify(list(d)))


def characteristics(frame):
    fr = Frame(frame)
    fr.pack()
    Label(fr, text="Select characteristic: ").pack(anchor=NE, side=LEFT, padx=5, pady=5)
    arr = list_category
    var = StringVar(value=arr[0])
    comb = ttk.Combobox(fr, values=list(arr), textvariable=var)
    comb.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    doc_show = Text(frame, height=140)

    process = lambda: characteristics_do(comb.get(), doc_show)
    Button(fr, text="Find", command=process).pack(anchor=NE, side=LEFT, padx=5, pady=5)
    doc_show.pack(side=BOTTOM, fill=X)


def users_do(value, doc):
    doc.delete('1.0', END)
    for i in table.find({"buyers.name": value}):
        doc.insert(END, f'{i["name"]}, {i["price"]}\n')


def users(frame):
    fr = Frame(frame)
    fr.pack()
    Label(fr, text="Select user: ").pack(anchor=NE, side=LEFT, padx=5, pady=5)
    arr = list_users
    var = StringVar(value=arr[0])
    comb = ttk.Combobox(fr, values=list(arr), textvariable=var)
    comb.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    doc_show = Text(frame, height=140)

    process = lambda: users_do(comb.get(), doc_show)
    Button(fr, text="Find", command=process).pack(anchor=NE, side=LEFT, padx=5, pady=5)
    doc_show.pack(side=BOTTOM, fill=X)


def colour_do(value, doc):
    doc.delete('1.0', END)
    for i in table.find({"features.colour": value}):

        doc.insert(END, f'{i["name"]}, {i["manufacturer"]} {i["price"]}\n')


def colour(frame):
    fr = Frame(frame)
    fr.pack()
    Label(fr, text="Select color: ").pack(anchor=NE, side=LEFT, padx=5, pady=5)
    arr = list_colours
    var = StringVar(value=arr[0])
    comb = ttk.Combobox(fr, values=list(arr), textvariable=var)
    comb.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    doc_show = Text(frame, height=140)

    process = lambda: colour_do(comb.get(), doc_show)
    Button(fr, text="Find", command=process).pack(anchor=NE, side=LEFT, padx=5, pady=5)
    doc_show.pack(side=BOTTOM, fill=X)


def sold(frame):
    fr = Frame(frame)
    fr.pack()
    count = 0
    for i in table.find():
        for j in i["buyers"]:
            count += 1
    Label(fr, text=f"Sold in total: {count}").pack(anchor=NE, side=LEFT, padx=5, pady=5)


def item_category(frame):
    fr = Frame(frame)
    fr.pack()
    doc_show = Text(frame, height=140)
    doc_show.pack(side=BOTTOM, fill=X)
    for category in list_category:
        count = 0
        for i in table.find({"features.category": category}):
            count += 1
        doc_show.insert(END, f"{category}: {count}\n")


def user_item_do(value, doc):
    doc.delete('1.0', END)
    t = set()
    for i in table.find({"name": value}):
        for j in i["buyers"]:
            t.add(j["name"])
    for item in t:
        doc.insert(END, f'{item}\n')


def user_item(frame):
    fr = Frame(frame)
    fr.pack()
    Label(fr, text="Select item: ").pack(anchor=NE, side=LEFT, padx=5, pady=5)
    arr = list_items
    var = StringVar(value=arr[0])
    comb = ttk.Combobox(fr, values=list(arr), textvariable=var)
    comb.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    doc_show = Text(frame, height=140)

    process = lambda: user_item_do(comb.get(), doc_show)
    Button(fr, text="Find", command=process).pack(anchor=NE, side=LEFT, padx=5, pady=5)
    doc_show.pack(side=BOTTOM, fill=X)


def delivery_item_do(value1, value2, doc):
    doc.delete('1.0', END)
    t = set()
    for i in table.find({"name": value1}):
        for j in i["buyers"]:
            if j["delivery"] == value2:
                t.add(j["name"])
    for m in t:
        doc.insert(END, f'{m}\n')


def delivery_item(frame):
    fr = Frame(frame)
    fr.pack()
    Label(fr, text="Select category: ").pack(anchor=NE, side=LEFT, padx=5, pady=5)
    arr = list_items
    var = StringVar(value=arr[0])
    comb = ttk.Combobox(fr, values=list(arr), textvariable=var)
    comb.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    var1 = StringVar(value=list_delivery[0])
    comb1 = ttk.Combobox(fr, values=list(list_delivery), textvariable=var1)
    comb1.pack(anchor=NE, side=LEFT, padx=5, pady=5)

    doc_show = Text(frame, height=140)

    process = lambda: delivery_item_do(comb.get(), comb1.get(), doc_show)
    Button(fr, text="Find", command=process).pack(anchor=NE, side=LEFT, padx=5, pady=5)
    doc_show.pack(side=BOTTOM, fill=X)


def f():
    pass


def get_categories():
    t = set()
    for i in table.find():
        t.add(i["features"]["category"])
    return list(t)


def get_manufacturers():
    t = set()
    for i in table.find():
        t.add(i["manufacturer"])
    return list(t)


def get_delivery():
    t = set()
    for i in table.find():
        for j in i["buyers"]:
            t.add(j["delivery"])
    return list(t)


def get_users():
    t = set()
    for i in table.find():
        for j in i["buyers"]:
            t.add(j["name"])
    return list(t)


def get_colours():
    t = set()
    for i in table.find():
        t.add(i["features"]["colour"])
    return list(t)


def get_items():
    t = set()
    for i in table.find():
        t.add(i["name"])
    return list(t)


previous = f

client = MongoClient("mongodb://192.168.112.103")
db = client["22305"]
table_items = "zimekov-item"
table = db[table_items]

for i in table.find({"category": "clothes"}):
    print(i)

fill_items()


list_category = get_categories()
list_manufacturers = get_manufacturers()
list_items = get_items()
list_users = get_users()
list_colours = get_colours()
list_delivery = get_delivery()


root = Tk()
root.geometry("1000x500")

frame_main = Frame(root)
frame_main.pack()


dict_queries = {
    "Products by category": category,
    "Characteristics of category": characteristics,
    "Person's purchase list": users,
    "By colour": colour,
    "Total sold": sold,
    "Total by category": item_category,
    "Buyers of an item": user_item,
    "Buyers of an item by delivery": delivery_item
}
query_var = StringVar(value="Products by category")
Label(frame_main, text="Table: ").pack(anchor=NE, side=LEFT, pady=5)
comb_table = ttk.Combobox(frame_main, width=50, values=list(dict_queries.keys()), textvariable=query_var)
comb_table.pack(anchor=NE, side=LEFT, padx=5, pady=5)

Button(frame_main, text="Choose category", command=draw).pack(anchor=NE, side=LEFT, padx=5, pady=5)
root.mainloop()