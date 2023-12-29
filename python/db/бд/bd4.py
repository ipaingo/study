import pymongo
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import scrolledtext

client = pymongo.MongoClient("192.168.112.103")
database = client["22303"]

Play = database["Dan_Play"]
Team = database["Dan_Team"]
# Play.delete_many({})
# Team.delete_many({})


def openn(entry_user, combo1, txt2, combo2, txt3):
    a = ""
    if txt2.get() == "<":
        a = "$lt"
    if txt2.get() == ">":
        a = "$gt"
    if txt2.get() == "=":
        a = "-1"
    if txt2.get() == "<=":
        a = "$lte"
    if txt2.get() == ">=":
        a = "$gte"

    if entry_user.get() == "team":
        openn2(combo1, a, combo2, txt3)
    else:
        openn1(combo1, a, combo2, txt3)


def openn1(combo1, a, combo2, txt3):
    window1 = Tk()
    window1.title("вывод")
    window1.geometry("1500x600")
    s = ""
    if combo2.get() == "":
        hg = txt3.get()
        if a == "-1":
            for qwe in Play.bios.find({combo1.get(): hg}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty
        else:
            for qwe in Play.bios.find({combo1.get(): {a: hg}}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty
    else:
        vopros = txt3.get()
        firstt = combo1.get()
        secondd = combo2.get()
        print(a)
        if a == "-1":
            for qwe in Play.bios.find({firstt: {secondd: vopros}}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty
        else:
            for qwe in Play.bios.find({firstt: {secondd: {a: vopros}}}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty

    lb2 = Label(window1, text=s)
    lb2.place(x=100, y=100)
    print(s)
    window1.mainloop()


def openn2(combo1, a, combo2, txt3):
    window1 = Tk()
    window1.title("вывод")
    window1.geometry("1500x600")
    s = ""
    print(a)
    if combo2.get() == "":
        hg = txt3.get()
        if a == "-1":
            for qwe in Team.bios.find({combo1.get(): hg}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty
        else:
            for qwe in Team.bios.find({combo1.get(): {a: hg}}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty
    else:
        hg = txt3.get()
        hg1 = combo1.get()
        hg2 = combo2.get()
        if a == "-1":
            for qwe in Team.bios.find({combo1.get(): {combo2.get(): hg}}, {"_id": 0}):
                ty = str(qwe.values()) + "\n"
                ty = ty[11:]
                s += ty
        else:
            print(a)
            for qwe in Team.bios.find(
                {combo1.get(): {combo2.get(): {a: hg}}}, {"_id": 0}
            ):
                ty = str(qwe.values()) + "\n"
                print(ty)
                print("eqw")
                ty = ty[11:]
                s += ty
    lb2 = Label(window1, text=s)
    lb2.place(x=10, y=10)
    print(s)
    window1.mainloop()


def callback1(combo1, combo2):
    combo2["values"] = ("", "")
    if combo1 == "players":
        combo2["values"] = ("1", "2", "3", "4", "5", "6", "7")

    if combo1 == "reserve":
        combo2["values"] = ("1", "2", "3", "4", "5", "6", "7")

    if combo1 == "goal":
        combo2["values"] = ("откуда", "минута", "автор(ФИО)", "передал(ФИО)")

    if combo1 == "foul":
        combo2["values"] = ("цвет карточки", "ФИО", "минута", "за что")

    if combo1 == "penalty":
        combo2["values"] = ("откуда", "минута", "автор(ФИО)", "передал(ФИО)")

    combo2.current(1)


def callback(entry_user, combo1, txt2, combo2, txt3):
    if entry_user == "team":
        combo1["values"] = ("name", "city", "coach", "players", "reserve")
    else:
        combo1["values"] = ("date", "score", "foul", "goal", "penalty", "ans")
    combo1.current(1)
    clerr()
    txt2.delete(0, len(txt2.get()))
    txt3.delete(0, len(txt3.get()))
    callback1(combo1.get(), combo2)


window = Tk()
window.title("ЛАба 4.1")
window.geometry("800x500")
x = 50
lb = Label(window, text="таблица")
lb.place(x=100, y=x)
entry_user = Combobox(window)
entry_user["values"] = ("Play", "team")
entry_user.current(1)
entry_user.place(x=200, y=x)
x = x + 75
combo1 = Combobox(window)
combo1["values"] = ("name", "city", "coach", "players", "reserve")
combo1.current(1)
combo1.place(x=200, y=x)
lb1 = Label(window, text="ключ")
lb1.place(x=100, y=x)
x = x + 75
combo2 = Combobox(window)
combo2["values"] = ("", "")
combo2.current(0)
combo2.place(x=400, y=x - 75)
lb2 = Label(window, text="знак")
lb2.place(x=100, y=x)
txt2 = Entry(window, width=70)
txt2.place(x=325, y=x)
x = x + 75

lb3 = Label(window, text="число")
lb3.place(x=100, y=x)
txt3 = Entry(window, width=70)
txt3.place(x=325, y=x)
x = x + 75

my_button2 = Button(
    window,
    text="результат",
    command=lambda: openn(entry_user, combo1, txt2, combo2, txt3),
)
my_button2.place(x=500, y=x)

entry_user.bind(
    "<<ComboboxSelected>>",
    lambda e: callback(entry_user.get(), combo1, txt2, combo2, txt3),
)
combo1.bind("<<ComboboxSelected>>", lambda e: callback1(combo1.get(), combo2))

window.mainloop()
