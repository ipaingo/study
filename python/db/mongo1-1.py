from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
import json
from bson.json_util import dumps


def show_table(*params):
    for table in params:
        collection = db[table]
        print(f"@@ {table} @@")
        for i in collection.find():
            print(i)


def fill_teams():
    db[table_teams].drop()
    db.create_collection(table_teams)
    collection = db[table_teams]
    for i in [
        {
            "name": "C 3 2 pi",
            "city": "Petrozavodsk",
            "coach": "Alkin Ruslan Valerievich",
            "players": [
                {"name": "Krishtalenko Mikola", "position": "1"},
                {"name": "Leaf Anton", "position": "2"},
                {"name": "Badcoder Dan", "position": "3"},
            ],
        },
        {
            "name": "ITMO 1",
            "city": "Saint Petersburg",
            "coach": "Stankevich Andrei Sergeevich",
            "players": [
                {"name": "Korotkevich Gennadiy", "position": "1"},
                {"name": "Vasilyev Artem", "position": "2"},
                {"name": "Minaev Boris", "position": "3"},
            ],
        },
        {
            "name": "Positive Attitude",
            "city": "Petrozavodsk",
            "coach": "Alkin Ruslan Valerievich",
            "players": [
                {"name": "Onesimus Nikita", "position": "1"},
                {"name": "Supersonic Eugeny", "position": "2"},
                {"name": "Moskvich Natalia", "position": "3"},
            ],
        },
    ]:
        collection.insert_one(i)


def fill_matches():
    db[table_matches].drop()
    db.create_collection(table_matches)
    collection = db[table_matches]
    for i in [
        {
            "date": "03.12.2023",
            "team1": "C 3 2 pi",
            "team2": "Positive Attitude",
            "violations": [
                {
                    "player": "Krishtalenko Mikola",
                    "time": "10:10",
                    "type": "red",
                    "reason": "Fought with his team",
                },
                {
                    "player": "Moskvich Natalia",
                    "time": "12:50",
                    "type": "yellow",
                    "reason": "unsportsmanlike conduct",
                },
                {
                    "player": "Onesimus Nikita",
                    "time": "12:50",
                    "type": "yellow",
                    "reason": "Kicked the ball out of the field",
                },
                {
                    "player": "Supersonic Eugeny",
                    "time": "16:30",
                    "type": "red",
                    "reason": "Provoked the opposing team",
                },
            ],
            "goal approaches": [
                {
                    "hero": "Leaf Anton",
                    "pass": "Badcoder Dan",
                    "time": "1:01",
                    "scoring_team": "C 3 2 pi",
                },
                {
                    "hero": "Supersonic Eugeny",
                    "pass": "Onesimus Nikita",
                    "time": "15:21",
                    "scoring_team": "Positive Attitude",
                },
                {
                    "hero": "Krishtalenko Mikola",
                    "pass": "Leaf Anton",
                    "time": "30:12",
                    "scoring_team": "C 3 2 pi",
                },
                {
                    "hero": "Onesimus Nikita",
                    "pass": "Moskvich Natalia",
                    "time": "19:21",
                    "scoring_team": "Positive Attitude",
                },
            ],
            "goals": [
                {
                    "hero": "Leaf Anton",
                    "pass": "Badcoder Dan",
                    "time": "1:01",
                    "scoring_team": "C 3 2 pi",
                },
                {
                    "hero": "Krishtalenko Mikola",
                    "pass": "Leaf Anton",
                    "time": "30:12",
                    "scoring_team": "C 3 2 pi",
                },
                {
                    "hero": "Onesimus Nikita",
                    "pass": "Moskvich Natalia",
                    "time": "19:21",
                    "scoring_team": "Positive Attitude",
                },
            ],
            "penalties": [
                {
                    "hero": "Onesimus Nikita",
                    "pass": "Moskvich Natalia",
                    "time": "15:21",
                    "scoring_team": "Positive Attitude",
                }
            ],
        },
        {
            "date": "19.11.2023",
            "team1": {"name": "C 3 2 pi", "score": "1"},
            "team2": {"name": "ITMO 1", "score": "2"},
            "violations": [
                {
                    "player": "Krishtalenko Mikola",
                    "time": "01:49",
                    "type": "red",
                    "reason": "Was late to the competition",
                },
                {
                    "player": "Korotkevich Gennadiy",
                    "time": "12:50",
                    "type": "yellow",
                    "reason": "Obtained too many prizes",
                },
                {
                    "player": "Badcoder Dan",
                    "time": "12:50",
                    "type": "yellow",
                    "reason": "Forgot how to play",
                },
            ],
            "goal approaches": [
                {
                    "hero": "Korotkevich Gennadiy",
                    "pass": "Vasilyev Artem",
                    "time": "15:21",
                    "scoring_team": "ITMO 1",
                },
                {
                    "hero": "Minaev Boris",
                    "pass": "Korotkevich Gennadiy",
                    "time": "30:12",
                    "scoring_team": "ITMO 1",
                },
                {
                    "hero": "Leaf Anton",
                    "pass": "Krishtalenko Mikola",
                    "time": "19:21",
                    "scoring_team": "C 3 2 pi",
                },
                {
                    "hero": "Krishtalenko Mikola",
                    "pass": "Badcoder Dan",
                    "time": "19:21",
                    "scoring_team": "C 3 2 pi",
                },
            ],
            "goals": [
                {
                    "hero": "Korotkevich Gennadiy",
                    "pass": "Vasilyev Artem",
                    "time": "15:21",
                    "scoring_team": "ITMO 1",
                },
                {
                    "hero": "Minaev Boris",
                    "pass": "Korotkevich Gennadiy",
                    "time": "30:12",
                    "scoring_team": "ITMO 1",
                },
                {
                    "hero": "Krishtalenko Mikola",
                    "pass": "Badcoder Dan",
                    "time": "19:21",
                    "scoring_team": "C 3 2 pi",
                },
                {
                    "hero": "Leaf Anton",
                    "pass": "Krishtalenko Mikola",
                    "time": "19:21",
                    "scoring_team": "C 3 2 pi",
                },
            ],
            "penalties": [
                {
                    "hero": "Korotkevich Gennadiy",
                    "pass": "Vasilyev Artem",
                    "time": "19:21",
                    "scoring_team": "ITMO 1",
                }
            ],
        },
    ]:
        collection.insert_one(i)


def add_field():
    name = txt_sec_key.get()
    doc.delete("1.0", END)
    if table_var.get() == table_teams:
        d = dict_team
    else:
        d = dict_match
    key = comb_key.get()
    value = txt_value.get()
    if "." not in key:
        d[key] += value
    else:
        temp = key.split(".")
        to_where = temp[0]
        what = temp[1]
        dict_sec = d[to_where]
        if name not in dict_sec.keys():
            d[to_where][name] = {}
        d[to_where][name][what] = value
        print(d)

    doc.insert(END, json.dumps(d, indent=4))


def write_doc_to_db():
    if table_var.get() == table_teams:
        d = dict_team
    else:
        d = dict_match

    table = db[comb_table.get()]
    output_dict = {}
    for i, v in d.items():
        if type(v) == type(dict()):
            output_dict[i] = []
            for j in v.values():
                output_dict[i].append(j)

        else:
            output_dict[i] = v
    print(json.dumps(output_dict, indent=4))
    table.insert_one(output_dict)
    show_table(table_teams, table_matches)


def show_doc():
    doc_show.delete("1.0", END)
    table = db[comb_table.get()]
    text = table.find()

    doc_show.insert(END, dumps(list(text), indent=4))


def clear_doc():
    global dict_match, dict_team
    doc.delete("1.0", END)
    dict_match = def_match
    dict_team = def_team


def changed(index, value, op):
    value = table_var.get()
    if value == table_teams:
        comb_key.config(values=teams_values)
        table_var.set("")
    elif value == table_matches:
        comb_key.config(values=matches_values)


table_teams = "zimenkov-teams"
table_matches = "zimenkov-matches"
client = MongoClient("mongodb://192.168.112.103")
db = client["22305"]


dict_team = {
    "name": "",
    "city": "",
    "coach": "",
    "players": {},
}
dict_match = {
    "date": "",
    "team1": {},
    "team2": {},
    "violations": {},
    "goal approaches": {},
    "goals": {},
    "penalties": {},
}

def_team = dict_team.copy()
def_match = dict_match.copy()


root = Tk()

fill_teams()
fill_matches()

show_table(table_teams, table_matches)

root.title("MongoDB")
root.geometry("1000x700+70+0")
frame_insert = Frame(root, borderwidth=1, relief=SOLID)
frame_insert.pack(anchor=W, fill=X, padx=10, pady=10)

frame_table = Frame(frame_insert)
frame_table.pack(anchor=S, padx=5, pady=5)
Label(frame_table, text="Insertion").pack(anchor=W, fill=X, padx=5, pady=5)

tables = [table_teams, table_matches]
table_var = StringVar(value=tables[0])
table_var.trace("w", changed)
Label(frame_table, text="Table: ").pack(anchor=NE, side=LEFT, pady=5)
comb_table = ttk.Combobox(frame_table, values=tables, textvariable=table_var)
comb_table.pack(anchor=NE, side=LEFT, padx=5, pady=5)

# ghjkl
frame_values = Frame(frame_insert)
frame_values.pack(anchor=SW, padx=5, pady=5)

Label(frame_values, text="Key: ").pack(anchor=NW, side=LEFT, padx=5, pady=5)

teams_values = ["name", "city", "coach", "players.name", "players.position"]
matches_values = [
    "date",
    "team1",
    "team1.name",
    "team1.score",
    "team2",
    "team2.name",
    "team2.score",
    "violations",
    "violations.player",
    "violations.time",
    "violations.type",
    "violations.reason",
    "goal_approaches",
    "goal_approaches.id",
    "goal_approaches.hero",
    "goal_approaches.pass",
    "goal_approaches.time",
    "goal_approaches.scoring_team",
    "goals",
    "goals.hero",
    "goals.pass",
    "goals.time",
    "goals.scoring_team",
    "penalties",
    "penalties.id",
    "penalties.hero",
    "penalties.pass",
    "penalties.time",
    "penalties.scoring_team",
]
comb_key = ttk.Combobox(frame_values, values=teams_values)
comb_key.pack(anchor=NW, side=LEFT, padx=5, pady=5)

Label(frame_values, text="Seconadary key: ").pack(anchor=NW, side=LEFT, padx=5, pady=5)

txt_sec_key = Entry(frame_values)
txt_sec_key.pack(anchor=NW, side=LEFT, padx=5, pady=5)

Label(frame_values, text="Value: ").pack(anchor=NW, side=LEFT, padx=5, pady=5)

txt_value = Entry(frame_values)
txt_value.pack(anchor=NW, side=LEFT, padx=5, pady=5)

btn_add = Button(frame_values, text="Add pair", command=add_field)
btn_add.pack(anchor=NW, side=LEFT)

frame_buttons = Frame(frame_insert)
frame_buttons.pack(anchor=CENTER, side=BOTTOM, fill=X)

doc = Text(frame_insert, height=14)
doc.pack(side=BOTTOM, fill=X)

btn_write = Button(frame_buttons, text="Write document", command=write_doc_to_db)
btn_write.pack(anchor=NW, padx=5, pady=5, side=LEFT)

btn_clear = Button(frame_buttons, text="Clear document", command=clear_doc)
btn_clear.pack(anchor=NW, padx=5, pady=5, side=LEFT)

frame_show = Frame(root)
frame_show.pack(fill=X)

frame_show_btn = Frame(frame_show)
frame_show_btn.pack()
btn_show_doc = Button(frame_show_btn, text="Show document", command=show_doc)
btn_show_doc.pack(side=LEFT)

comb_table2 = ttk.Combobox(frame_show_btn, values=tables, textvariable=table_var)
comb_table2.pack(anchor=NE, side=LEFT, padx=5, pady=5)

doc_show = Text(frame_show, height=18)
doc_show.pack(side=BOTTOM, fill=X)

root.mainloop()
