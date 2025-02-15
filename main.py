import telebot
from telebot import types
import sqlite3

api = "8069908727:AAHNfe5mIyrCWldz07kAGWkzM5I_tI09CCY"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=["start"])
def start(message):
    
    connection = sqlite3.connect('test_db.sql')
    cursor = connection.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS test (id varchar(100) primary key, first_name varchar(50), last_name varchar(50), city varchar(50))')
    
    connection.commit()
    cursor.close()
    connection.close()
    
    
    bot.send_message(message.chat.id, "Привет, ты новый пользователь, давай я тебя зарегистрирую. Введи своё имя.")
    bot.register_next_step_handler(message, id_and_user_first_name, id)
    
def id_and_user_first_name(message, id):
    id = message.from_user.username
    first_name = message.text.strip()
    bot.send_message(message.chat.id, "Введи свою фамилию.")
    bot.register_next_step_handler(message, user_last_name, first_name, id)
    
def user_last_name(message, first_name, id):
    last_name = message.text.strip()
    bot.send_message(message.chat.id, "Введи свой город.")
    bot.register_next_step_handler(message, user_city, first_name, last_name, id)
    
def user_city(message, first_name, last_name, id):
    city = message.text.strip()
    
    connection = sqlite3.connect('test_db.sql')
    cursor = connection.cursor()
    
    cursor.execute("INSERT OR REPLACE INTO test (id, first_name, last_name, city) VALUES ('%s', '%s', '%s', '%s')" %(id, first_name, last_name, city))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    markup = types.InlineKeyboardMarkup()
    list_btn = types.InlineKeyboardButton("Список пользователей", callback_data="list")
    markup.add(list_btn)
    
    bot.send_message(message.chat.id, "Вы успешно зарегестрировались", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "list":
        connection = sqlite3.connect('test_db.sql')
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM test")
        
        list = cursor.fetchall()
        
        info = ''
        for el in list:
            info += f'id: @{el[0]}, имя:{el[1]}, фамилия:{el[2]}, город пользователя:{el[3]}\n'
        
        cursor.close()
        connection.close()
        
        bot.send_message(call.message.chat.id, info)

    
bot.infinity_polling()