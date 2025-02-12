import telebot
from telebot import types

api = ""
bot = telebot.TeleBot(api)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет-привет")
    
    
    
    
    
bot.infinity_polling()
