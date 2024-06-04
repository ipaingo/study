import pymongo
import re


email_validate_pattern = r"^\S+@\S+\.\S+$"


db_client = pymongo.MongoClient("mongodb://localhost:27017/")
current_db = db_client["foundation"]
collection_organisation = current_db["organisation"]
collection_user = current_db["user"]
collection_app = current_db["app"]


organisation_example = {
    "owner": "name",
    "name": "cool_name",
    "members": [
        {
            "name": "mem_name",
            "graduation": "Ученая степень",
            "role": "Квасогон"
        },
        {
            "name": "mem2_name",
            "graduation": "Ученая степень",
            "role": "Обама"
        }
    ]
}

user_example = {
    "name": "FIO",
    "mail": "mail@mail.mail",
    "login": "jopa",
    "password": "pwd"
}


def register(name, mail, login, pwd, repeated_pwd, grad):
    if pwd != repeated_pwd:
        return "Пароли не совпадают!"
    if collection_user.find_one({"login": login}):
        return "Данный пользователь уже существует!"
    if re.match(email_validate_pattern, mail) is None:
        return "Неверный формат почты!"
    if collection_user.find_one({"mail": mail}):
        return "Данная почта уже используется!"
    collection_user.insert_one(
        {
            "name": name,
            "mail": mail,
            "login": login,
            "password": pwd
        }
    )
    collection_organisation.insert_one({
        "owner": name,
        "name": "",
        "members": [
            {
                "name": name,
                "role": "Создатель",
                "graduation": grad
            }
        ]
    })
    return False


def save_organisation(owner, name, members):
    collection_organisation.delete_one({"owner": owner})
    collection_organisation.insert_one({
        "owner": owner,
        "name": name,
        "members": members
    })


def get_org_info(login):
    org = collection_organisation.find_one({"owner": login})
    return org


def get_list_of_org_members(login):
    org = collection_organisation.find_one({"owner": login})
    return org["members"]


def create_app(sender, name, topic, description, subject, members, date_begin, date_end, asked_sum):
    if collection_app.find_one({"name": name}):
        return "Проект с таким названием уже существует!"
    collection_app.insert_one({
        "sender": sender,
        "name": name,
        "topic": topic,
        "description": description,
        "subject": subject,
        "members": members,
        "date_begin": date_begin,
        "date_end": date_end,
        "asked_sum": asked_sum
    })
    return False


def get_apps(login):
    return list(collection_app.find({"sender": login}))



# Возвраты: 1 - неверный логин, 2 - неверный пароль. В случае успеха возвращает логин
def try_authorize(login, pwd):
    if not collection_user.find_one({"login": login}):
        return 1
    log = collection_user.find_one({"password": pwd, "login": login})
    if log:
        return log["login"]
    return 2

