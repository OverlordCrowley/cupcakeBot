import datetime
from datetime import datetime
import telebot
import sqlite3
import os
from aiogram import types
import emoji
import base64
# from pathlib import Path
# import pathlib
# from aiogram.types import user
# from telethon.sync import TelegramClient
# from telethon import connection
from telebot import types


class BotDB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


bot = telebot.TeleBot('')
db = BotDB('database.db')


login = ""
password = ""
id = -1
person = -1
addData = []
deskr = []
order = []
status = []

markup2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
item1 = types.KeyboardButton(emoji.emojize('принят'))
item2 = types.KeyboardButton(emoji.emojize('готов'))
item3 = types.KeyboardButton(emoji.emojize('в доставке'))
item4 = types.KeyboardButton(emoji.emojize('завершен'))
item5 = types.KeyboardButton(emoji.emojize('отменен'))
markup2.row(item1, item2, item3)
markup2.row(item4, item5)

markup0 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)

markup = telebot.types.InlineKeyboardMarkup(row_width=3)
markup.add(types.InlineKeyboardButton(text="Изменить логин", callback_data='login'))
markup.add(types.InlineKeyboardButton(text="Изменить пароль", callback_data='pass'))
markup.add(types.InlineKeyboardButton(text="Посмотреть заказы", callback_data='orders'))
markup.add(types.InlineKeyboardButton(text="Купить товар", callback_data='buy'))
markup.add(types.InlineKeyboardButton(text="Посмотреть количество бонусов", callback_data='bonus'))

adminMarkup = telebot.types.InlineKeyboardMarkup(row_width=5)
adminMarkup.add(types.InlineKeyboardButton(text="Все заказы", callback_data='many'))
adminMarkup.add(types.InlineKeyboardButton(text="Посмотреть заказ", callback_data='several'))
adminMarkup.add(types.InlineKeyboardButton(text="Поменять статус заказа", callback_data='editStatus'))
adminMarkup.add(types.InlineKeyboardButton(text="Добавить товар", callback_data='add'))
adminMarkup.add(types.InlineKeyboardButton(text="Редактировать товар", callback_data='edit'))
adminMarkup.add(types.InlineKeyboardButton(text="Удалить товар", callback_data='delete'))


@bot.message_handler(commands=['start'])
def start(message):
    first_text = "! Здесь <b>Вы</b> откроете для себя необычные сочетания вкусов и возможность радовать себя и своих близких вкуснейшими десертами! Чтобы просмотреть наш товар, введите в строку слово, (например: /items), либо нажмите подходящую кнопку меню. Бот покажет вам разные дисерты и наши данные! Всего вам наилучшего"
    bot.send_message(message.chat.id, "Здравствуй, " + str(message.from_user.first_name) + first_text,
                     parse_mode="html",
                     )
    bot.send_message(message.chat.id,
                     "<b>Вот все команды </b>\n /sign_up - команда, чтобы создать новый аккаунт\n /sign_in - команда, чтобы войти в аккаунт\n /items - команда, чтобы посмотреть наш ассортимент\n /contact - команда, чтобы посмотреть наши контакты и адрес\n /help посмотреть все команды\n /menu - открыть меню с кнопками",
                     parse_mode="html")


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id,
                     "<b>Вот все команды </b>\n /sign_up - команда, чтобы создать новый аккаунт\n /sign_in - команда, чтобы войти в аккаунт\n /items - команда, чтобы посмотреть наш ассортимент\n /contact - команда, чтобы посмотреть наши контакты и адрес\n /help посмотреть все команды\n /menu - открыть меню с кнопками",
                     parse_mode="html")


@bot.message_handler(commands=['sign_up'])
def new_handler(message):
    msg = bot.send_message(message.chat.id, "Отправьте сперва логин, затем пароль через пробел")
    bot.register_next_step_handler(msg, reg)


def reg(message):
    global login
    global password
    global id
    global person
    login = ""
    password = ""
    id = -1
    person = -1
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    connect.commit()

    mes = message.text.split(' ')

    try:
        people_login = mes[0]
        people_pass = mes[1]
        if (people_login is not None) and (people_pass is not None):
            # connect = sqlite3.connect('database.db')
            # cursor = connect.cursor()
            # connect.commit()

            cursor.execute(f"SELECT * FROM 'Users'")
            data = cursor.fetchall()
            b = 0
            for i in range(len(data)):
                if data[i][1] == people_login:
                    b = 1

                else:
                    b = 0

            if b == 0:
                cursor.execute(f"INSERT INTO 'Users' (Login, Pass) VALUES ('{people_login}', '{people_pass}')")
                connect.commit()
                bot.send_message(message.chat.id, "Вы успешно зарегистрировались")
                cursor.execute(f"SELECT * FROM 'Users' Where Login = '{people_login}'")
                data = cursor.fetchone()
                cursor.execute(f"INSERT INTO 'Bonus' ( Person_id, Bonus ) VALUES ( '{data[0]}', '{0}' )")
                connect.commit()
            else:
                bot.send_message(message.chat.id, "Пользователь с таким логином уже существует")
        else:
            bot.send_message(message.chat.id, "Вы ввели лишний пробел повторите попытку")

    except:
        bot.send_message(message.chat.id, "Данный пользователь уже существуйте")


@bot.message_handler(commands=['sign_in'])
def start_handler(message):
    msg = bot.send_message(message.chat.id, "Отправь логин и пароль через пробел")
    bot.register_next_step_handler(msg, auth)


def auth(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    connect.commit()

    mes = message.text.split()
    try:
        people_login = mes[0]
        people_pass = mes[1]
        cursor.execute(f"SELECT * FROM 'Users' WHERE Login = '{people_login}' AND Pass = '{people_pass}'")
        data = cursor.fetchone()
        # data = cursor.fetchall()
        if (data != ""):
            global login
            global id
            global password
            global person
            id = data[0]
            login = people_login
            password = people_pass
            person = data[3]
            bot.send_message(message.chat.id, "Вы успешно вошли")

            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            if person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)

        else:
            msg = bot.send_message(message.chat.id, "Ошибка в логине или пароле, повторите попытку")

    except:
        msg = bot.send_message(message.chat.id, "Ошибка в логине или пароле, повторите попытку")


@bot.message_handler(commands=['menu'])
def start_handler(message):
    if (person == 0):
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
    elif (person == 1):
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
    else:
        bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


@bot.message_handler(commands=['order'])
def start_handler(message):
    msg = bot.send_message(message.chat.id, "Отправьте id заказа")
    bot.register_next_step_handler(msg, orderGet)


@bot.message_handler(commands=['contact'])
def start_handler(message):
    msg = bot.send_message(message.chat.id,
                           "Мы находимся по адресу: улица Мухтара Ауэзова, 46/1 Сарыарка район, Астана\nНомер чтобы с нами связаться: +77014139436",
                           parse_mode="html")
    if person == 0:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
    elif person == 1:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
    else:
        bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def orderGet(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM 'Orders' WHERE Id = '{message.text}';")
    data = cursor.fetchone()
    if data != None:
        bot.send_message(message.chat.id, f"Id заказа: {data[0]}\nСтатус: {data[10]}\n")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    else:
        bot.send_message(message.chat.id, "Вы ввели неправильный id товара")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


@bot.message_handler(commands=['items'])
def start_handler(message):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM 'Menu';")

        pork_result = cursor.execute(f"SELECT * FROM Menu")
        data = pork_result.fetchall()
        for i in range(len(data)):
            file_base64 = data[i][6]
            image_64_decode = base64.decodebytes(file_base64)
            image_result = open('image.jpg', 'wb')
            image_result.write(image_64_decode)
            photo = open(f'C:/Users/Crowley/Downloads/telebot/image.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
            txt = "Id: " + str(data[i][0]) + " " + data[i][1] + " (" + data[i][2] + " - " + str(
                data[i][3]) + "гр) " + "- " + str(data[i][4]) + "тг"
            bot.send_message(message.chat.id, txt)

        msg = bot.send_message(message.chat.id, 'Введите id десерта, который вы хотите посмотреть')
        bot.register_next_step_handler(msg, itemsNext)
    except:
        bot.send_message(message.chat.id, "Повторите попытку позже")


def itemsNext(message):
    if (message.text != None):
        try:
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            pork_result = cursor.execute(f"SELECT * FROM Menu Where id = '{int(message.text)}'")
            data = pork_result.fetchone()
            file_base64 = data[6]
            image_64_decode = base64.decodebytes(file_base64)
            image_result = open('image.jpg', 'wb')
            image_result.write(image_64_decode)
            photo = open(f'C:/Users/Crowley/Downloads/telebot/image.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
            txt = "Id: " + str(data[0]) + " " + data[1] + " (" + data[2] + " - " + str(data[3]) + "гр) " + "- " + str(
                data[4]) + "тг"
            bot.send_message(message.chat.id, txt)
            bot.send_message(message.chat.id, data[5])
            bot.send_message(message.chat.id, data[7])
            if (person == 0):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif (person == 1):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        except:
            bot.send_message(message.chat.id, "Повторите попытку позже")
    else:
        bot.send_message(message.chat.id, "Повторите попытку позже")


def orderGet(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM 'Orders' WHERE Id = '{message.text}';")
    data = cursor.fetchone()
    if data != None:
        bot.send_message(message.chat.id, f"Id заказа: {data[0]}\nСтатус: {data[10]}\n")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    else:
        bot.send_message(message.chat.id, "Вы ввели неправильный id товара")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


@bot.callback_query_handler(func=lambda callback: callback.data)

def chek_callback_data(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'login':

        msg = bot.send_message(callback.message.chat.id, 'Отправьте логин на который хотите использовать')
        bot.register_next_step_handler(msg, loginEx)
    elif callback.data == 'pass':
        msg = bot.send_message(callback.message.chat.id,
                               'Отправьте пароль который хотите использовать')
        bot.register_next_step_handler(msg, passEx)
    elif callback.data == 'several':
        msg = bot.send_message(callback.message.chat.id,
                               'Отправьте id заказа')
        bot.register_next_step_handler(msg, orderMostAdmin)
    elif callback.data == 'orders':
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM 'Orders' WHERE Person_Id = '{id}';")
        data = cursor.fetchall()
        if not data:
            bot.send_message(callback.message.chat.id, 'У вас на данный момент нет заказов')
            if person == 0:
                bot.send_message(callback.message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(callback.message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(callback.message.chat.id,
                                 "Для полного функционала зарегистрируйтесь/зайдите в профиль")
        elif data != "":
            for number in range(len(data)):
                bot.send_message(callback.message.chat.id,
                                 f"Id: {data[number][0]}\nТовар: {data[number][1]}\nСтатус: {data[number][10]}")
            msg = bot.send_message(callback.message.chat.id,
                                   'Отправьте id заказа, чтобы посмотреть его подробнее')
            bot.register_next_step_handler(msg, orderMost)
    elif callback.data == 'many':
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM 'Orders';")
        data = cursor.fetchall()
        if (data != ""):
            for number in range(len(data)):
                bot.send_message(callback.message.chat.id,
                                 f"Id: {data[number][0]}\nТовар: {data[number][1]}\nСтатус: {data[number][10]}")
            msg = bot.send_message(callback.message.chat.id,
                                   'Отправьте id заказа, чтобы посмотреть его подробнее')
            bot.register_next_step_handler(msg, orderMostAdmin)
        else:
            bot.send_message(callback.message.chat.id,
                             "Заказов на данный момент нет")
    elif callback.data == 'add':
        global addData
        addData = []
        msg = bot.send_message(callback.message.chat.id,
                               'Отправьте название десерта')
        bot.register_next_step_handler(msg, addName)
    elif callback.data == 'edit':
        global deskr
        deskr = []
        msg = bot.send_message(callback.message.chat.id,
                               'Отправьте название десерта')
        bot.register_next_step_handler(msg, editItem)
    elif callback.data == 'delete':
        deskr = []
        msg = bot.send_message(callback.message.chat.id,
                               'Отправьте название десерта')
        bot.register_next_step_handler(msg, delItem)
    elif callback.data == 'buy':
        msg = bot.send_message(callback.message.chat.id,
                               'Отправьте название десерта')
        bot.register_next_step_handler(msg, buyStepOne)
    elif callback.data == 'bonus':
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM 'Bonus' WHERE Person_id = '{id}'")
        data = cursor.fetchone()
        txt = 'У вас ' + str(data[1]) + " бонусов"
        bot.send_message(callback.message.chat.id, txt, parse_mode="html")
        if person == 0:
            bot.send_message(callback.message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(callback.message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(callback.message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    elif callback.data == 'editStatus':
        global status
        status = []
        msg = bot.send_message(callback.message.chat.id, 'Отправьте id заказа', parse_mode="html")
        bot.register_next_step_handler(msg, editStatus)

def editStatus(message):
    text = message.text.split(' ');
    if text != "":
        status.append(text[0])
        msg = bot.send_message(message.chat.id, 'выберите статус заказа с помощью клавиатуры', parse_mode="html", reply_markup=markup2)

        bot.register_next_step_handler(msg, editStatusTwo)
    else:
        bot.send_message(message.chat.id, 'Вы не ввели id', parse_mode="html")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

def editStatusTwo(message):
    text = message.text;
    if text != "":
        status.append(text)
        try:
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            cursor.execute(f"Update Orders set Status = '{status[1]}' Where Id = '{status[0]}'")
            connect.commit()
            bot.send_message(message.chat.id, "Статус обновлен")

            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
        except:
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    else:
        bot.send_message(message.chat.id, 'Вы не ввели id', parse_mode="html")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")



def orderMostAdmin(message):
    msg = message.text.split(' ')
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM 'Orders' WHERE Id = '{msg[0]}';")
    data = cursor.fetchone()
    if data != "":
        try:
            bot.send_message(message.chat.id,
                             f"Id: {data[0]}\nТовар: {data[1]}\nТип торта: {data[2]}\nКоличество: {data[3]}\nЦена: "
                             f"{data[4]}\nПолная цена: {data[5]}\nДата покупки: {data[6]}\nАдрес доставки: {data[7]}\nТелефон: {data[8]}" +
                             f"\nСтатус: {data[10]}")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        except:
            bot.send_message(message.chat.id, "Не правильно введен id заказа ")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

    else:
        bot.send_message(message.chat.id, "У вас на даный момент нет заказов")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def buyStepOne(message):
    global order
    order = []
    if message.text is not None:
        order.append(message.text)
        msg = bot.send_message(message.chat.id,
                               'Отправьте тип десерта')
        bot.register_next_step_handler(msg, buyStepTwo)
    else:
        bot.send_message(message.chat.id,
                         'Попробуйте заново')


def buyStepTwo(message):
    if message.text is not None:
        order.append(message.text.lower())
        msg = bot.send_message(message.chat.id,
                               'Отправьте количество тортов')
        bot.register_next_step_handler(msg, buyStepThree)
    else:
        bot.send_message(message.chat.id,
                         'Попробуйте заново')


def buyStepThree(message):
    if message.text is not None:
        order.append(message.text)
        msg = bot.send_message(message.chat.id,
                               'Отправьте адрес доставки')
        bot.register_next_step_handler(msg, buyStepFour)
    else:
        bot.send_message(message.chat.id,
                         'Попробуйте заново')


def buyStepFour(message):
    if message.text is not None:
        order.append(message.text)
        msg = bot.send_message(message.chat.id,
                               'Отправьте ваш номер телефона')
        bot.register_next_step_handler(msg, buyStepFive)
    else:
        bot.send_message(message.chat.id,
                         'Попробуйте заново')


def buyStepFive(message):
    try:
        if message.text is not None:
            order.append(message.text)
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            cursor.execute(f"SELECT * FROM 'Menu' WHERE Name = '{order[0]}' AND Type = '{order[1]}';")
            data = cursor.fetchone()
            cursor1 = connect.cursor()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor1.execute(
                f'INSERT INTO Orders(Item_name, Type, Number, Price, FullPrice, Date, Address, Phone, Person_Id, Status)'
                f'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                    order[0], order[1], order[2], data[4], int(data[4] * int(order[2])), str(dt_string), order[3],
                    order[4],
                    id, 'ожидается'))
            connect.commit()
            addbonus = int(data[4] * int(order[2]))
            cursor.execute(f"SELECT * FROM 'Bonus' WHERE Person_id = '{id}'")
            data = cursor.fetchone()

            bot.send_message(message.chat.id, "Ваш заказ отправлен на рассмотрение")
            addbonus = addbonus * 0.05 + data[1]
            cursor.execute(f"Update Bonus set Bonus = '{addbonus}' Where Person_id = '{id}';")
            connect.commit()
            if (person == 0):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif (person == 1):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

        else:
            bot.send_message(message.chat.id,
                             'Попробуйте заново')
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    except:
        bot.send_message(message.chat.id,
                         'Вы ввели некорректные данные, попробуйте заново')
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def delItem(message):

    if message.text != None:
        deskr.append(message.text)
        msg = bot.send_message(message.chat.id,
                               'Отправьте тип десерта')
        bot.register_next_step_handler(msg, DelNext)
    else:
        bot.send_message(message.chat.id,
                         'Попробуйте заново')
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def DelNext(message):
    if message.text is not None:
        msg = message.text.split(' ')
        txt = msg[0].lower()
        try:
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()


            cursor.execute(
                f"SELECT * FROM Menu WHERE Name = '{deskr[0]}' AND Type = '{txt}'")
            data = cursor.fetchone()
            if data[0] > -1:
                cursor.execute(
                    f"DELETE FROM Menu WHERE Name = '{deskr[0]}' AND Type = '{txt}'")
                connect.commit()
                bot.send_message(message.chat.id, "Десерт успешно удален")
                if (person == 0):
                    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
                elif (person == 1):
                    bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
                else:
                    bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
            else:
                bot.send_message(message.chat.id,
                                 'Данного десерта нет в ассортименте')
                if person == 0:
                    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
                elif person == 1:
                    bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
                else:
                    bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
        except:
            bot.send_message(message.chat.id,
                             'Попробуйте заново')
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    else:
        bot.send_message(message.chat.id,
                         'Попробуйте заново')
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def editItem(message):

    try:
        if message.text != None:
            deskr.append(message.text)
            msg = bot.send_message(message.chat.id,
                                   'Отправьте тип десерта и характеристику для изминения')
            bot.register_next_step_handler(msg, neditItem)
        else:
            bot.send_message(message.chat.id, "Попробуйте заново")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    except:
        bot.send_message(message.chat.id, "Попробуйте заново")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def neditItem(message):
    try:
        msg = message.text.split(' ')
        deskr.append(msg[0].lower())

        if msg[1].lower() == "вес":
            deskr.append("Weight")
            msg1 = bot.send_message(message.chat.id, "Отправьте желаемый вес")
            bot.register_next_step_handler(msg1, Editable)
        elif msg[1].lower() == "цена":
            deskr.append("Price")
            msg1 = bot.send_message(message.chat.id, "Отправьте желаемeю цену")
            bot.register_next_step_handler(msg1, Editable)
        elif msg[1].lower() == "подзаголовок":
            deskr.append("Subtitle")
            msg1 = bot.send_message(message.chat.id, "Отправьте желаемый подзаголовок")
            bot.register_next_step_handler(msg1, Editable)
        elif msg[1].lower() == "описание":
            deskr.append("Descripton")
            msg1 = bot.send_message(message.chat.id, "Отправьте желаемое описание")
            bot.register_next_step_handler(msg1, Editable)
        elif msg[1].lower() == "фото":
            bot.send_message(message.chat.id, "Изменение фото невозможно, пересоздайте товар")
        else:
            bot.send_message(message.chat.id, "Попробуйте заново")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    except:
        bot.send_message(message.chat.id, "Попробуйте заново")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

def Editable(message):

    # try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(
            f"Update Menu set '{deskr[2]}' = '{message.text}' WHERE Name = '{deskr[0]}' AND  Type = '{deskr[1]}'")
        connect.commit()
        bot.send_message(message.chat.id, "Десерт успешно изменен")
        if (person == 0):
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif (person == 1):
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    # except:
    #     bot.send_message(message.chat.id, "Повториите попытку")
    #     if person == 0:
    #         bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
    #     elif person == 1:
    #         bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
    #     else:
    #         bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def addName(message):
    # global addData

    try:
        name = message.text
        if (name != None):
            markup1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            item1 = types.KeyboardButton(emoji.emojize('стандартный :shortcake:'))
            item2 = types.KeyboardButton(emoji.emojize('увеличенный :birthday_cake:'))
            markup1.row(item1, item2)

            name = message.text.strip()
            addData.append(name)

            msg1 = bot.send_message(message.chat.id, "Отправьте тип десерта", reply_markup=markup1)

            bot.register_next_step_handler(msg1, addType)

        else:
            bot.send_message(message.chat.id, "Вы не заполнили название десерта, поробуйте заново")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

    except:
        msg1 = bot.send_message(message.chat.id, "Попробуйте заново")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

def addType(message):
    try:
        txt = message.text
        if (txt != None):
            if (txt == emoji.emojize('стандартный :shortcake:') or txt.strip() == "стандартный" or txt.lower() == 'стандартный'):
                txt = "стандартный"
                addData.append(txt.lower)
                msg = bot.send_message(message.chat.id, "Отправьте вес блюда")
                bot.register_next_step_handler(msg, addWeight)
            elif (txt == emoji.emojize('увеличенный :birthday_cake:') or txt.strip() == "увеличенный" or txt.lower() == 'увеличенный'):
                txt = "увеличенный"
                addData.append(txt)
                msg = bot.send_message(message.chat.id, "Отправьте вес блюда")
                bot.register_next_step_handler(msg, addWeight)
        else:
            msg1 = bot.send_message(message.chat.id, "Вы не заполнили имя десерта, попробуйте еще раз")
            bot.register_next_step_handler(msg1, addType)

    except:
        msg1 = bot.send_message(message.chat.id, "Вы не заполнили имя десерта, попробуйте еще раз")
        bot.register_next_step_handler(msg1, addName)


def addWeight(message):
    try:
        Weight = message.text
        if Weight != None:
            addData.append(Weight)
            msg1 = bot.send_message(message.chat.id, "Отправьте цену десерта", )
            bot.register_next_step_handler(msg1, addPrice)
        else:
            msg1 = bot.send_message(message.chat.id, "Вы не заполнили тип десерта, попробуйте еще раз")
            bot.register_next_step_handler(msg1, addWeight)
    except:
        msg1 = bot.send_message(message.chat.id, "Вы не заполнили тип десерта, попробуйте еще раз")
        bot.register_next_step_handler(msg1, addWeight)


def addPrice(message):
    try:
        price = message.text
        if price != None:
            addData.append(price)
            msg1 = bot.send_message(message.chat.id, "Отправьте подзаголовок десерта", )
            bot.register_next_step_handler(msg1, addSubtitle)
        else:
            msg1 = bot.send_message(message.chat.id, "Вы не заполнили цену десерта, попробуйте еще раз")
            bot.register_next_step_handler(msg1, addPrice)
    except:
        msg1 = bot.send_message(message.chat.id, "Вы не заполнили цену десерта, попробуйте еще раз")
        bot.register_next_step_handler(msg1, addPrice)


def addSubtitle(message):
    try:
        Subtitle = message.text
        if (Subtitle != None):
            addData.append(Subtitle)
            msg1 = bot.send_message(message.chat.id, "Отправьте фото", )
            bot.register_next_step_handler(msg1, addPhoto)
        else:
            msg1 = bot.send_message(message.chat.id, "Вы не заполнили подзаголовок десерта, попробуйте еще раз")
            bot.register_next_step_handler(msg1, addPrice)
    except:
        msg1 = bot.send_message(message.chat.id, "Вы не заполнили подзаголовок десерта, попробуйте еще раз")
        bot.register_next_step_handler(msg1, addPrice)


def addPhoto(message):
    try:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        image = open("image.jpg", 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        addData.append(image_64_encode)
        msg = bot.send_message(message.chat.id, "Отправьте описание блюда")
        bot.register_next_step_handler(msg, addDesciption)
    except:
        msg = bot.send_message(message.chat.id, "Отправьте фото еще раз")
        bot.register_next_step_handler(msg, addPhoto)


def addDesciption(message):
    text = message.text
    addData.append(text)
    # try:
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    try:
        cursor.execute(
            f'SELECT * FROM Menu Where Name = {addData[0]} AND Type = {addData[1]}')
        data = cursor.fetchone()
        bot.send_message(message.chat.id, "Данный десерт уже добавлен")
    except:
        # if not data:

        cursor.execute(
            f'INSERT INTO Menu (Name, Type, Weight, Price, Subtitle, Photo, Description) VALUES(?, ?, ?, ?, ?, ?, ?)',
            (addData[0], addData[1], addData[2], addData[3], addData[4], addData[5], addData[6]))
        connect.commit()
        addData
        bot.send_message(message.chat.id, "Ваш десерт успешно добавлен")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")



        # else:
        #     bot.send_message(message.chat.id, "Данный десерт уже существует")
        #     if person == 0:
        #         bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        #     elif person == 1:
        #         bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        #     else:
        #         bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")
    # except:
    #     bot.send_message(message.chat.id, "Повторите все действия заново")
    #     if person == 0:
    #         bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
    #     elif person == 1:
    #         bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
    #     else:
    #         bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def orderMost(message):
    msg = message.text.split(' ')
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM 'Orders' WHERE Id = '{msg[0]}' AND Person_Id = {id};")
    data = cursor.fetchone()
    if data != "":
        try:
            bot.send_message(message.chat.id,
                             f"Id: {data[0]}\nТовар: {data[1]}\nТип торта: {data[2]}\nКоличество: {data[3]}\nЦена: "
                             f"{data[4]}\nПолная цена: {data[5]}\nДата покупки: {data[6]}\nАдрес доставки: {data[7]}\nТелефон: {data[8]}" +
                             f"\nСтатус: {data[10]}")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        except:
            bot.send_message(message.chat.id, "Не правильно введен id заказа ")
            if person == 0:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif person == 1:
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
            else:
                bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")

    else:
        bot.send_message(message.chat.id, "У вас на даный момент нет заказов")
        if person == 0:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif person == 1:
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        else:
            bot.send_message(message.chat.id, "Для полного функционала зарегистрируйтесь/зайдите в профиль")


def loginEx(message):
    mes = message.text.split(' ')
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM 'Users' WHERE Login = '{login}'")
    data = cursor.fetchall()
    if len(data) < 2:
        try:
            cursor.execute(
                f"Update Users set Login = '{mes[0]}' WHERE Id = '{id}'")
            connect.commit()
            bot.send_message(message.chat.id, "Логин успешно изменен")
            if (person == 0):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif (person == 1):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        except:
            bot.send_message(message.chat.id, "Ошибка не удалось обновить данные, повторите попытку")

    else:
        bot.send_message(message.chat.id, "Пользователь с таким логином уже существует")


def passEx(message):
    mes = message.text.split(' ')
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM 'Users' WHERE Login = '{login}'")
    data = cursor.fetchall()
    if len(data) < 2:
        try:
            cursor.execute(
                f"Update Users set Pass = '{mes[0]}' WHERE Id = '{id}'")
            connect.commit()
            bot.send_message(message.chat.id, "Пароль успешно изменен")
            if (person == 0):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
            elif (person == 1):
                bot.send_message(message.chat.id, "Выберите действие", reply_markup=adminMarkup)
        except:
            bot.send_message(message.chat.id, "Ошибка не удалось обновить данные, повторите попытку")

    else:
        bot.send_message(message.chat.id, "Попробуйте позже")


bot.polling(none_stop=True)
