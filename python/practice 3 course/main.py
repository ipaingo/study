from initialize_db import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

root = Tk()
global_login = StringVar()
graduations = (
    "Бакалавр",
    "Магистр",
    "Кандидат наук",
    "Доктор наук",
    "Нет"
)


def to_register():
    frame_authorization.pack_forget()
    frame_registration.pack()


def to_organisation():
    subframe_all_apps.pack_forget()
    subframe_create_app.pack_forget()
    subframe_organisation.pack()
    clear_table_members()
    root.geometry("")
    org = get_org_info(global_login.get())
    ent_name_org.config(text=org["name"])
    for member in org["members"]:
        tbl_members.insert("", END, values=(member["name"], member["graduation"], member["role"]))
    root.geometry("")


def to_all_apps():
    subframe_create_app.pack_forget()
    subframe_organisation.pack_forget()
    subframe_all_apps.pack()

    all_apps = get_apps(global_login.get())
    print(all_apps)

    frames = []
    for child in subframe_all_apps.winfo_children():
        child.destroy()
    if len(all_apps) == 0:
        ttk.Label(subframe_all_apps, text="Заявки отсутствуют!").pack(pady=10)
    for i in range(len(all_apps)):
        frames.append(Frame(subframe_all_apps, borderwidth=1, relief=SOLID))
        ttk.Label(frames[i], text=all_apps[i]["name"]).pack()
        ttk.Label(frames[i], text=f"{all_apps[i]['date_begin']}-{all_apps[i]['date_end']}").pack()
        ttk.Label(frames[i], text=f"Сумма: {all_apps[i]['asked_sum']}").pack()
        ttk.Label(frames[i], text="Статус: Ожидание").pack()
        frames[i].pack(pady=5)

    root.geometry("")


def to_create_app():
    global checkbuttons_members, rows_members, roles_inputs, names_members

    checkbuttons_members = []
    rows_members = []
    roles_inputs = []
    names_members = []

    subframe_organisation.pack_forget()
    subframe_all_apps.pack_forget()
    subframe_create_app.pack()

    for child in subframe_members.winfo_children():
        child.destroy()

    mems = get_list_of_org_members(global_login.get())
    for i in range(len(mems)):
        rows_members.append(Frame(subframe_members))

        checkbuttons_members.append(BooleanVar())

        Checkbutton(rows_members[i], variable=checkbuttons_members[i]).pack(anchor=NE, side=LEFT, pady=5)
        roles_inputs.append(StringVar())

        names_members.append(mems[i]["name"])
        ttk.Label(rows_members[i], text=names_members[i]).pack(anchor=NE, side=LEFT, pady=5)
        ttk.Entry(rows_members[i], textvariable=roles_inputs[i]).pack(anchor=NE, side=LEFT, pady=5)
        rows_members[i].pack(fill=BOTH, expand=1)
    root.geometry("")


def clear_table_members():
    tbl_members.delete(*tbl_members.get_children())


def org_save_to_db():
    mems = []
    for i in tbl_members.get_children():
        usr = tbl_members.item(i)["values"]
        mems.append({
            "name": usr[0],
            "graduation": usr[1],
            "role": usr[2]
        })

    save_organisation(global_login.get(), ent_name_org.get(), mems)
    messagebox.showinfo("Успех!", "Данные об организации изменены.")
    to_organisation()


def app_save_to_db():
    participants = []
    for i in range(len(roles_inputs)):
        part = checkbuttons_members[i].get()
        name = names_members[i]
        role = roles_inputs[i].get()
        if part:
            participants.append({
                "name": name,
                "role": role
            })
        print(checkbuttons_members[i].get(), names_members[i], roles_inputs[i].get())
    name = ent_app_name.get()
    topic = ent_app_topic.get()
    descr = ent_app_description.get("1.0", END)[0:-1]
    subj = subject.get()
    begin = ent_date_begin.get()
    end = ent_date_end.get()
    asked = ent_app_sum.get()
    if name == "" or topic == "" or subj == "" or asked == "":
        lbl_error.config(text="Заполните все поля!")
        return
    attempt = create_app(global_login.get(), name, topic, descr, subj, participants, begin, end, asked)

    if attempt:
        lbl_error.config(text=attempt)
    else:
        to_all_apps()
        messagebox.showinfo("Успех!", "Заявка отправлена.")


def add_user():
    tbl_members.insert("", END, values=(ent_new_user_name.get(), graduation_new_user.get(), ent_new_user_role.get()))


def delete_selected_user():
    selected_item = tbl_members.selection()[0]
    tbl_members.delete(selected_item)


def process_signup():
    login = ent_login_auth.get()
    pwd = ent_password_auth.get()
    attempt = try_authorize(login, pwd)
    print(attempt)
    if attempt == 1:
        lbl_error_auth.config(text="Пользователя с таким именем не существует!")
    elif attempt == 2:
        lbl_error_auth.config(text="Неверный пароль!")
    else:
        global_login.set(attempt)
        frame_authorization.pack_forget()
        frame_main.pack()
        to_organisation()


def process_register():
    fio = ent_fio_registration.get()
    login = ent_login_registration.get()
    mail = ent_mail_registration.get()
    password = ent_password_registration.get()
    password_repeat = ent_password_repeat_registration.get()

    if fio == "" or login == "" or mail == "" or password == "" or password_repeat == "":
        lbl_error_register.config(text="Заполните все поля!")
        return

    try_reg = register(fio, mail, login, password, password_repeat, graduation.get())
    if try_reg:
        lbl_error_register.config(text=try_reg)
    else:
        frame_registration.pack_forget()
        frame_authorization.pack()
        messagebox.showinfo("Успех!", "Учетная запись создана")


root.geometry("500x500")
root.title("Грантовый фонд")

# Окно авторизации
frame_authorization = Frame(root)

subframe_auth_login = Frame(frame_authorization)
subframe_auth_login.pack()
ttk.Label(subframe_auth_login, text="Логин: ").pack(anchor=NE, side=LEFT, pady=5)
ent_login_auth = ttk.Entry(subframe_auth_login)
ent_login_auth.pack(anchor=NW, side=LEFT, padx=5, pady=5)

subframe_auth_password = Frame(frame_authorization)
subframe_auth_password.pack()
ttk.Label(subframe_auth_password, text="Пароль: ").pack(anchor=NE, side=LEFT, pady=5)
ent_password_auth = ttk.Entry(subframe_auth_password, show="*")
ent_password_auth.pack(anchor=NW, side=LEFT, padx=5, pady=5)

lbl_error_auth = ttk.Label(frame_authorization)
lbl_error_auth.pack()

btn_login = ttk.Button(frame_authorization, text="Войти", command=process_signup)
btn_login.pack()
btn_to_register = ttk.Button(frame_authorization, text="Создать новую учетную запись", command=to_register)
btn_to_register.pack()
# КОНЕЦ Окно авторизации

# Окно регистрации
frame_registration = Frame(root)

subframe_register_fio = Frame(frame_registration)
subframe_register_fio.pack()
ttk.Label(subframe_register_fio, text="ФИО: ").pack(anchor=NE, side=LEFT, pady=5)
ent_fio_registration = ttk.Entry(subframe_register_fio)
ent_fio_registration.pack(anchor=NW, side=LEFT, padx=5, pady=5)

subframe_register_login = Frame(frame_registration)
subframe_register_login.pack()
ttk.Label(subframe_register_login, text="Логин: ").pack(anchor=NE, side=LEFT, pady=5)
ent_login_registration = ttk.Entry(subframe_register_login)
ent_login_registration.pack(anchor=NW, side=LEFT, padx=5, pady=5)

subframe_register_mail = Frame(frame_registration)
subframe_register_mail.pack()
ttk.Label(subframe_register_mail, text="Почта: ").pack(anchor=NE, side=LEFT, pady=5)
ent_mail_registration = ttk.Entry(subframe_register_mail)
ent_mail_registration.pack(anchor=NW, side=LEFT, padx=5, pady=5)

subframe_graduation = Frame(frame_registration)
subframe_graduation.pack()
graduation = StringVar(value=graduations[0])
comb_graduation = ttk.Combobox(subframe_graduation, values=graduations, textvariable=graduation)
ttk.Label(subframe_graduation, text="Образование: ").pack(anchor=NE, side=LEFT, pady=5)
comb_graduation.pack(anchor=NW, side=LEFT, padx=5, pady=5)

subframe_register_password = Frame(frame_registration)
subframe_register_password.pack()
ttk.Label(subframe_register_password, text="Пароль: ").pack(anchor=NE, side=LEFT, pady=5)
ent_password_registration = ttk.Entry(subframe_register_password, show="*")
ent_password_registration.pack(anchor=NW, side=LEFT, padx=5, pady=5)

subframe_register_password_repeat = Frame(frame_registration)
subframe_register_password_repeat.pack()
ttk.Label(subframe_register_password_repeat, text="Повторите пароль: ").pack(anchor=NE, side=LEFT, pady=5)
ent_password_repeat_registration = ttk.Entry(subframe_register_password_repeat, show="*")
ent_password_repeat_registration.pack(anchor=NW, side=LEFT, padx=5, pady=5)

lbl_error_register = ttk.Label(frame_registration)
lbl_error_register.pack()

btn = ttk.Button(frame_registration, text="Зарегистрироваться", command=process_register)
btn.pack()
# КОНЕЦ Окно регистрации

# Главное окно меню
frame_main = Frame(root)

subframe_nav_buttons = Frame(frame_main)
subframe_nav_buttons.pack()

btn_organisation = ttk.Button(subframe_nav_buttons, text="Организация", command=to_organisation)
btn_organisation.pack(anchor=NW, side=LEFT, padx=5, pady=5)
btn_all_apps = ttk.Button(subframe_nav_buttons, text="Заявки", command=to_all_apps)
btn_all_apps.pack(anchor=NW, side=LEFT, padx=5, pady=5)
btn_create_app = ttk.Button(subframe_nav_buttons, text="Создать заявку", command=to_create_app)
btn_create_app.pack(anchor=NW, side=LEFT, padx=5, pady=5)
# КОНЕЦ Главное окно меню

# Изменение организации
subframe_organisation = Frame(frame_main)

subframe_org_name = Frame(subframe_organisation)
subframe_org_name.pack()
ttk.Label(subframe_org_name, text="Организация").pack(anchor=NE, side=LEFT, pady=5)
ent_name_org = ttk.Entry(subframe_org_name)
ent_name_org.pack(anchor=NW, side=LEFT, padx=5, pady=5)

header_members = ("name", "graduation", "role")
tbl_members = ttk.Treeview(subframe_organisation, columns=header_members, show="headings")
tbl_members.heading("name", text="Имя")
tbl_members.heading("graduation", text="Образование")
tbl_members.heading("role", text="Роль")
tbl_members.pack(fill=BOTH, expand=1)

btn_delete_user = ttk.Button(subframe_organisation, text="Удалить выделенного пользователя", command=delete_selected_user)
btn_delete_user.pack(pady=5)

subframe_new_user = Frame(subframe_organisation, borderwidth=1, relief=SOLID)
subframe_new_user.pack()

ttk.Label(subframe_new_user, text="Имя нового пользователя: ").pack(anchor=NE, side=LEFT, pady=5, padx=10)
ent_new_user_name = ttk.Entry(subframe_new_user)
ent_new_user_name.pack(anchor=NW, side=LEFT, padx=5, pady=5)

ttk.Label(subframe_new_user, text="Роль: ").pack(anchor=NE, side=LEFT, pady=5)
ent_new_user_role = ttk.Entry(subframe_new_user)
ent_new_user_role.pack(anchor=NW, side=LEFT, padx=5, pady=5)

graduation_new_user = StringVar(value=graduations[0])
comb_graduation_new_user = ttk.Combobox(subframe_new_user, values=graduations, textvariable=graduation_new_user)
ttk.Label(subframe_new_user, text="Образование: ").pack(anchor=NE, side=LEFT, pady=5)
comb_graduation_new_user.pack(anchor=NW, side=LEFT, padx=5, pady=5)

btn_add_user = ttk.Button(subframe_organisation, text="Добавить пользователя", command=add_user)
btn_add_user.pack()
btn_save_users = ttk.Button(subframe_organisation, text="Сохранить", command=org_save_to_db)
btn_save_users.pack()
# КОНЕЦ изменение организации


# Создать заявку
subframe_create_app = Frame(frame_main)

ttk.Label(subframe_create_app, text="Название проекта").pack(pady=5)
ent_app_name = ttk.Entry(subframe_create_app)
ent_app_name.pack()

ttk.Label(subframe_create_app, text="Тема").pack(pady=5)
ent_app_topic = ttk.Entry(subframe_create_app)
ent_app_topic.pack()

ttk.Label(subframe_create_app, text="Описание").pack(pady=5)
ent_app_description = Text(subframe_create_app, height=3)
ent_app_description.pack()

# Соня, сделай
subjects = [
    "То",
    "Сё",
    "Пятое",
    "Десятое"
]
subject = StringVar(value=subjects[0])
comb_subject = ttk.Combobox(subframe_create_app, values=subjects, textvariable=subject)
ttk.Label(subframe_create_app, text="Предметная область").pack()
comb_subject.pack()

ttk.Label(subframe_create_app, text="Сотрудники").pack(pady=5)
subframe_members = Frame(subframe_create_app)
subframe_members.pack()
rows_members = []
checkbuttons_members = []
roles_inputs = []
names_members = []

ttk.Label(subframe_create_app, text="Сроки выполнения исследований").pack(pady=5)
subframe_app_dates = Frame(subframe_create_app)
subframe_app_dates.pack()

subframe_date_begin = Frame(subframe_app_dates)
subframe_date_begin.pack(anchor=NW, side=LEFT, padx=5, pady=5)

ent_date_begin = DateEntry(subframe_date_begin, selectmode="day")
ttk.Label(subframe_date_begin, text="Начало").pack()
ent_date_begin.pack()

subframe_date_end = Frame(subframe_app_dates)
subframe_date_end.pack(anchor=NW, side=LEFT, padx=5, pady=5)

ent_date_end = DateEntry(subframe_date_end, selectmode="day")
ttk.Label(subframe_date_end, text="Конец").pack()
ent_date_end.pack()

ttk.Label(subframe_create_app, text="Запрашиваемая сумма финансирования").pack(pady=5)
ent_app_sum = ttk.Entry(subframe_create_app)
ent_app_sum.pack()

lbl_error = ttk.Label(subframe_create_app)
lbl_error.pack()

btn_process_app_creation = ttk.Button(subframe_create_app, text="Создать", command=app_save_to_db)
btn_process_app_creation.pack()

# КОНЕЦ Создать заявку


# Список заявок

subframe_all_apps = Frame(frame_main)

# КОНЕЦ список заявок

frame_authorization.pack()
root.mainloop()
