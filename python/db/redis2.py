import redis
from tkinter import *
from tkinter import ttk

db = redis.Redis(host="192.168.112.103", password="student")
sportsmen_table = "22305-zimenkov-sportsmen"
juries_table = "22305-zimenkov-jury"

window = Tk()
combobox_jury = ttk.Combobox()
combobox_sportsman = ttk.Combobox()
treeview = ttk.Treeview()
entry_result = Entry()

juries_list = []
sportsmen_list = []


def update_table():
    clear_table()
    arr = []
    for item in db.hkeys(sportsmen_table):
        val = db.hget(sportsmen_table, item)
        arr.append([item.decode("utf-8"), val.decode("utf-8")])
    for i in list(sorted(arr, key=lambda x: int(x[1]), reverse=True)):
        treeview.insert("", END, values=[i[0], i[1]])


def juries_update():
    global juries_list
    juries_list = []
    for jury in db.smembers(juries_table):
        juries_list.append(jury.decode("utf-8"))


def sportsmen_update():
    global sportsmen_list
    sportsmen_list = []
    for sportsman in db.hkeys(sportsmen_table):
        sportsmen_list.append(sportsman.decode("utf-8"))


def clear_tables():
    for i in db.hgetall(sportsmen_table):
        db.hdel(sportsmen_table, i)

    for i in db.hgetall(juries_table):
        db.hdel(juries_table, i)


def fill_tables():
    sp = [
        "Васильев Андрей",
        "Иванов Петр",
        "Соколов Роман",
        "Суконников Егор",
        "Московский Вячеслав",
    ]
    for person in sp:
        db.hset(sportsmen_table, person, "0")

    for jury in ["Зайцев Антон", "Житников Алексей", "Светлов Артемий"]:
        db.sadd(juries_table, jury)
        for s in sp:
            db.hset(jury, s, "0")


def add_line():
    current = db.hget(combobox_jury.get(), combobox_sportsman.get())
    if current is None:
        current = "0"
    current = int(current)
    db.hset(
        combobox_jury.get(),
        combobox_sportsman.get(),
        str(current + int(entry_result.get())),
    )
    score = int(db.hget(sportsmen_table, combobox_sportsman.get()))
    db.hset(
        sportsmen_table, combobox_sportsman.get(), str(score + int(entry_result.get()))
    )

    update_table()


def clear_table():
    treeview.delete(*treeview.get_children())


def main():
    global window, combobox_jury, combobox_sportsman, treeview, entry_result
    fill_tables()

    sportsmen_update()

    juries_update()

    window.title("Таблица спортсменов")
    window.geometry("1000x400")

    frame_add_points = Frame(window)
    frame_add_points.pack(pady=10)

    Label(frame_add_points, text="Судья").pack(anchor=NW, side=LEFT)
    jury_var = StringVar(value=juries_list[0])
    combobox_jury = ttk.Combobox(
        frame_add_points, values=juries_list, textvariable=jury_var, width=50
    )
    combobox_jury.pack(anchor=NE, side=LEFT, padx=5)

    Label(frame_add_points, text="Спортсмен").pack(anchor=NW, side=LEFT)
    sportsman_var = StringVar(value=sportsmen_list[0])
    combobox_sportsman = ttk.Combobox(
        frame_add_points, values=sportsmen_list, textvariable=sportsman_var, width=50
    )
    combobox_sportsman.pack(anchor=NE, side=LEFT, padx=5)

    entry_result = Entry(frame_add_points)
    entry_result.pack(anchor=NE, side=LEFT, padx=5)

    btn_send = Button(frame_add_points, text="Добавить?", command=add_line)
    btn_send.pack(anchor=NE, side=LEFT)

    treeview = ttk.Treeview(window, columns=("1", "2"), show="headings")
    treeview.heading("1", text="Спортсмен")
    treeview.column("1", width=600, anchor=N)
    treeview.heading("2", text="Баллы")
    treeview.column("2", width=300, anchor=N)

    treeview.pack(fill=Y)
    update_table()
    window.mainloop()


if __name__ == "__main__":
    main()
