import telebot
from telebot import types

api = "8069908727:AAHNfe5mIyrCWldz07kAGWkzM5I_tI09CCY"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет-привет")
    
    
    
    
    
bot.infinity_polling()