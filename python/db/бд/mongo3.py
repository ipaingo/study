import pymongo
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import scrolledtext

client = pymongo.MongoClient('192.168.112.103')
database = client['22303']

Play = database["Dan_Play"]
Team = database["Dan_Team"]
# Play.delete_many({})
# Team.delete_many({})
name = ""
city = ""
coach = ""
players = dict()
reserve = dict()
date = ""
score = ""
foul = dict()
goal = dict()
penalty = dict()
ans = ""


def clerr():
    global name, city, coach, players, reserve, date, score, foul, goal, penalty, ans
    name = ""
    city = ""
    coach = ""
    players = dict()
    reserve = dict()
    date = ""
    score = ""
    foul = dict()
    goal = dict()
    penalty = dict()
    ans = ""


def savee(entry_user):
    if entry_user.get() == 'team':
        savee1()
    else:
        savee2()


def savee1():
    global name, city, coach, players, reserve, Team
    team = {"name": name,
            "city": city,
            "coach": coach,
            "players": players,
            "reserve": reserve
            }
    Team.bios.insert_one(team)
    # print(team)
    clerr()


def savee2():
    global date, score, foul, goal, penalty, ans, Play
    team = {"date": date,
            "score": score,
            "foul": foul,
            "goal": goal,
            "penalty": penalty,
            "ans": ans
            }
    Play.bios.insert_one(team)
    # print(team)
    clerr()


def add(entry_user, combo1, txt2, combo2):
    if entry_user.get() == 'team':
        add1(combo1, txt2, combo2)
    else:
        add2(combo1, txt2, combo2)


def add1(combo1, txt2, combo2):
    global name, city, coach, players, reserve
    if combo1.get() == 'name':
        name = txt2.get()
    if combo1.get() == 'city':
        city = txt2.get()
    if combo1.get() == 'coach':
        coach = txt2.get()
    if combo1.get() == 'players':
        players[combo2.get()] = txt2.get()
    if combo1.get() == 'reserve':
        reserve[combo2.get()] = txt2.get()
    txt2.delete(0, len(txt2.get()))


def add2(combo1, txt2, combo2):
    global date, score, foul, goal, penalty, ans
    if combo1.get() == 'date':
        date = txt2.get()
    if combo1.get() == 'score':
        score = txt2.get()
    if combo1.get() == 'foul':
        foul[combo2.get()] = txt2.get()
    if combo1.get() == 'goal':
        goal[combo2.get()] = txt2.get()
    if combo1.get() == 'penalty':
        penalty[combo2.get()] = txt2.get()
    if combo1.get() == 'ans':
        ans = txt2.get()
    txt2.delete(0, len(txt2.get()))


def openn(entry_user):
    if entry_user.get() == 'team':
        openn2()
    else:
        openn1()


def openn1():
    window1 = Tk()
    window1.title("вывод")
    window1.geometry("1500x600")

    s = ""
    for qwe in Play.bios.find({}, {"_id": 0}):
        ty = str(qwe.values()) + "\n"
        ty = ty[11:]
        s += ty
    lb2 = Label(window1, text=s)
    lb2.place(x=100, y=100)
    print(s)
    window1.mainloop()


def openn2():
    window1 = Tk()
    window1.title("вывод")
    window1.geometry("1500x600")

    s = ""
    for qwe in Team.bios.find({}, {"_id": 0}):
        ty = str(qwe.values()) + "\n"
        ty = ty[11:]
        s += ty
    lb2 = Label(window1, text=s)
    lb2.place(x=10, y=10)
    print(s)
    window1.mainloop()


def callback1(combo1, combo2):
    combo2['values'] = ("", "")
    if combo1 == 'players':
        combo2['values'] = ("1", "2", "3", "4", "5", "6", "7")

    if combo1 == 'reserve':
        combo2['values'] = ("1", "2", "3", "4", "5", "6", "7")

    if combo1 == 'goal':
        combo2['values'] = ("откуда", "минута", "автор(ФИО)", "передал(ФИО)")

    if combo1 == 'foul':
        combo2['values'] = ("цвет карточки", "ФИО", "минута", "за что")

    if combo1 == 'penalty':
        combo2['values'] = ("откуда", "минута", "автор(ФИО)", "передал(ФИО)")

    combo2.current(1)


def callback(entry_user, combo1, txt2, combo2):
    if entry_user == 'team':
        combo1['values'] = ("name", "city", "coach", "players", "reserve")
    else:
        combo1['values'] = ("date", "score", "foul", "goal", "penalty", "ans")
    combo1.current(1)
    clerr()
    txt2.delete(0, len(txt2.get()))
    callback1(combo1.get(), combo2)


window = Tk()
window.title("ЛАба 3")
window.geometry("800x500")
x = 50
lb = Label(window, text="таблица")
lb.place(x=100, y=x)
entry_user = Combobox(window)
entry_user['values'] = ("Play", "team")
entry_user.current(1)
entry_user.place(x=200, y=x)
x = x + 75
combo1 = Combobox(window)
combo1['values'] = ("name", "city", "coach", "players", "reserve")
combo1.current(1)
combo1.place(x=200, y=x)
lb1 = Label(window, text="ключ")
lb1.place(x=100, y=x)
x = x + 75
combo2 = Combobox(window)
combo2['values'] = ("", "")
combo2.current(0)
combo2.place(x=175, y=x)
lb2 = Label(window, text="значение")
lb2.place(x=100, y=x)
txt2 = Entry(window, width=70)
txt2.place(x=325, y=x)
x = x + 75
my_button = Button(window, text="Добавить ключ-значение", command=lambda: add(entry_user, combo1, txt2, combo2))
my_button.place(x=100, y=x)

my_button1 = Button(window, text="Сохранить документ", command=lambda: savee(entry_user))
my_button1.place(x=300, y=x)

my_button2 = Button(window, text="Показать документы", command=lambda: openn(entry_user))
my_button2.place(x=500, y=x)

entry_user.bind("<<ComboboxSelected>>", lambda e: callback(entry_user.get(), combo1, txt2, combo2))
combo1.bind("<<ComboboxSelected>>", lambda e: callback1(combo1.get(), combo2))

window.mainloop()
