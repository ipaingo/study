from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
import json


def changed(index, value, op):
    value = table_var.get()
    if value == table_teams:
        comb_key.config(values=teams_values)
        table_var.set("")
    elif value == table_matches:
        comb_key.config(values=matches_values)


def search():
    doc.delete("1.0", END)
    if table_var.get() == table_teams:
        table = table_teams
    else:
        table = table_matches

    key = comb_key.get()
    sign = dict_signs[comb_sign.get()]
    print(sign)
    value = txt_value.get()
    if sign != "equals":
        for i in db[table].find({key: {sign: value}}, {"_id": 0}):
            doc.insert(END, json.dumps(i, indent=4))
            doc.insert(END, "\n")
    else:
        for i in db[table].find({key: value}, {"_id": 0}):
            print(type(i))
            doc.insert(END, json.dumps(i, indent=4))
            doc.insert(END, "\n")


def process_command():
    if table_var2.get() == table_teams:
        table = table_teams
    else:
        table = table_matches

    a = dict()
    print(txt_query.get("1.0", END))
    aaa = json.loads(txt_query.get("1.0", END))

    print("fegh")
    count = 0
    a = [
        {
            "$unwind": "$players"
        },
        {
            "$match": {
                "players.position": {
                    "$gt": "1"
                }
            }
        },
        {
            "$count": "pass"
        }]

    a = [
        {
            "$unwind": "$goals"
        },
        {
            "$group": {
                "_id": "$goals.hero",
                "count": {"$sum": 1}
            }
        }
    ]
    doc.delete("1.0", END)
    if txt_cond.get() == "":
        command = "True"
    else:
        command = txt_cond.get()
    print(command)
    res = ""
    for item in db[table].aggregate(aaa):
        if eval(command):
            res += f"{item}\n"
        count += 1

    doc.insert(END, res)
    doc.insert(END, "\n")


table_teams = "zimenkov-teams"
table_matches = "zimenkov-matches"
client = MongoClient("mongodb://192.168.112.103")
db = client["22305"]

root = Tk()
root.title("MongoDB")
root.geometry("1000x700+70+0")

frame_jopa = ttk.Frame(root)
frame_jopa.pack()
frame_data = ttk.Frame(frame_jopa, borderwidth=2, relief="ridge")
frame_data.pack(side=LEFT, anchor=NW, padx=30)

tables = [table_teams, table_matches]
table_var = StringVar(value=tables[0])
table_var.trace("w", changed)
Label(frame_data, text="Table: ").pack(pady=5)
comb_table = ttk.Combobox(frame_data, values=tables, textvariable=table_var)
comb_table.pack(padx=5, pady=5)

teams_values = ["name", "city", "coach", "players", "players.name", "players.position"]
matches_values = ["date", "team1", "team1.name", "team1.score", "team2", "team2.name", "team2.score", "violations",
                  "violations.player",
                  "violations.time", "violations.type", "violations.reason", "goal_approaches", "goal_approaches.id",
                  "goal_approaches.hero", "goal_approaches.pass", "goal_approaches.time",
                  "goal_approaches.scoring_team", "goals",
                  "goals.hero", "goals.pass", "goals.time",
                  "goals.scoring_team",
                  "penalties", "penalties.id",
                  "penalties.hero", "penalties.pass", "penalties.time",
                  "penalties.scoring_team"]
Label(frame_data, text="Key: ").pack(padx=5, pady=5)
comb_key = ttk.Combobox(frame_data, values=teams_values)
comb_key.pack(padx=5, pady=5)

dict_signs = {
    "<": "$lt",
    ">": "$gt",
    "=": "equals",
    "<=": "$lte",
    ">=": "$gte"
}
Label(frame_data, text="Sign: ").pack(padx=5, pady=5)
comb_sign = ttk.Combobox(frame_data, values=list(dict_signs.keys()))
comb_sign.pack(padx=5, pady=5)

Label(frame_data, text="Value: ").pack(padx=5, pady=5)
txt_value = Entry(frame_data)
txt_value.pack(padx=5, pady=5)

btn_find = Button(frame_data, text="Search", command=search)
btn_find.pack(pady=5, padx=5)

frame_find2 = ttk.Frame(frame_jopa, borderwidth=2, relief="ridge")
frame_find2.pack(side=LEFT, anchor=NW, padx=30)

table_var2 = StringVar(value=tables[0])
Label(frame_find2, text="Table: ").pack( pady=5)
comb_table2 = ttk.Combobox(frame_find2, values=tables, textvariable=table_var2)
comb_table2.pack(padx=5, pady=5)

Label(frame_find2, text="Query: ").pack(pady=5, padx=5)
txt_query = Text(frame_find2, width=45, height=8)
txt_query.pack(pady=5, padx=5)

Label(frame_find2, text="Conditions: ").pack(pady=5, padx=5)
txt_cond = Entry(frame_find2, width=30)
txt_cond.pack(pady=5, padx=5)

btn_find2 = Button(frame_find2, text="Search", command=process_command)
btn_find2.pack(pady=5, padx=5)

doc = Text(root, height=20)
doc.pack(fill=X, side=BOTTOM)

root.mainloop()
