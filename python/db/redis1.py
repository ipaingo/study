import redis
from tkinter import *
from tkinter import ttk
from tkinter import font

db = redis.Redis(host="192.168.112.103", password="student")

# все таблицы в таком формате.
users_table = "22305-zimenkov-users"

# в этих переменных хранятся значения применяемых шрифтов для пользователей.
tuple_font = ("arial", 10, "normal")
font_colour = "black"

# элементы tkinter.
window = Tk()
entry_username = Entry()
entry_fontsize = Entry()
combobox_colour = ttk.Combobox()
combobox_font = ttk.Combobox()
combobox_user = ttk.Combobox()
combobox_weight = ttk.Combobox()
label_result = Label()
entry_result = Entry()
label_sample = Label()
# список имен пользователей в базе данных.
users = []


# штука для отладки, удаляет все записи в базе данных.
def delete_all():
    for key in db.hgetall(users_table):
        db.hdel(users_table, key)


# добавляет новую запись в базу данных.
def add_line():
    username = entry_username.get()
    font_name = combobox_font.get()
    font_colour = combobox_colour.get()
    font_size = entry_fontsize.get()
    font_weight = combobox_weight.get()
    print(" ".join([font_name, font_size, font_weight, font_colour]))
    db.hset(
        users_table,
        username,
        ";".join([font_name, font_size, font_weight, font_colour]),
    )
    update_list_of_users()


# noinspection PyUnresolvedReferences
def show_user_info():
    # находит параметры шрифта выбранного пользователя.
    global tuple_font, font_colour
    user = combobox_user.get()
    text = db.hget(users_table, user)
    label_result.config(text=text)
    p = str(text.decode("utf-8")).split(";")
    tuple_font = (p[0], p[1], p[2])
    font_colour = p[3]
    label_sample.config(text=entry_result.get(), font=tuple_font, fg=font_colour)


# обновляет список пользователей (список list_of_users).
def update_list_of_users():
    global users
    users = []
    for i in db.hkeys(users_table):
        users.append(i.decode("utf-8"))
    combobox_user.config(values=users)


def main():
    # delete_all()
    update_list_of_users()
    global entry_username, entry_fontsize, combobox_colour, combobox_font, combobox_weight, window, combobox_user, combobox_weight, entry_result, label_sample, label_result
    window.title("RedisDB")
    window.geometry("1000x320")
    fnt = ("Montserrat", 12)
    Label(window, text="Имя пользователя", font=fnt).grid(row=0, column=0)

    entry_username = Entry(window, width=35)
    entry_username.grid(row=0, column=1)

    fonts = font.families()
    fonts_var = StringVar(value=fonts[0])
    Label(window, text="Шрифт", font=fnt).grid(row=0, column=2)
    combobox_font = ttk.Combobox(window, values=fonts, textvariable=fonts_var)
    combobox_font.grid(row=0, column=3)

    colours = ["black", "purple", "orange", "yellow", "red", "green", "blue"]
    colour_var = StringVar(value=colours[0])
    Label(window, text="Цвет", font=fnt).grid(row=1, column=0)
    combobox_colour = ttk.Combobox(window, values=colours, textvariable=colour_var)
    combobox_colour.grid(row=1, column=1)

    weights = ["normal", "bold", "italic"]
    weight_var = StringVar(value=weights[0])
    Label(window, text="Написание", font=fnt).grid(row=1, column=2)
    combobox_weight = ttk.Combobox(window, values=weights, textvariable=weight_var)
    combobox_weight.grid(row=1, column=3)

    Label(window, text="Размер", font=fnt).grid(row=1, column=4)
    entry_fontsize = Entry(window)
    entry_fontsize.insert(0, "10")
    entry_fontsize.grid(row=1, column=5)

    btn_add_line = Button(window, text="Добавить!", command=add_line, font=fnt)
    btn_add_line.grid(row=2, column=2, pady=10)

    Label(window, text="Пользователь", font=fnt).grid(row=3, column=0)
    combobox_user = ttk.Combobox(window, values=users)
    combobox_user.grid(row=3, column=1)

    btn_search_user_info = Button(
        window, text="Применить", command=show_user_info, font=fnt
    )
    btn_search_user_info.grid(row=3, column=2)

    label_result = Label(window, font=("Arial", 12))
    label_result.grid(row=3, column=3)

    entry_result = Entry(window, width=100)
    entry_result.insert(0, "Предпросмотр сообщения / Message preview")
    entry_result.grid(row=4, column=0, columnspan=6)

    label_sample = Label(window)
    label_sample.grid(row=5, column=0, columnspan=6)
    label_sample.config(text="Предпросмотр сообщения / Message preview")

    window.mainloop()


if __name__ == "__main__":
    main()
