# -*- coding: utf-8 -*-
import time
import telebot
import config
import re
from telebot import types
import sqlite3

bot = telebot.TeleBot(config.token)


start_pattern = r"Привет"
@bot.message_handler(regexp=start_pattern)
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я священник!')

@bot.message_handler(func=lambda message: message.text=="Хай")
def send_welcome2(message):
    bot.send_message(message.chat.id, 'хой')

@bot.message_handler(func=lambda message: message.text=="Перечисли грехи")
def list_sins(message):
    # bot.send_message(message.chat.id, 'блин')
    db_conn = sqlite3.connect('sins.db')
    c = db_conn.cursor()
    for row in c.execute('SELECT sin_name FROM sins ORDER BY sin_id'):
    	bot.send_message(message.chat.id, row)
    db_conn.close()

# db_conn = sqlite3.connect('sins.db')
# db_conn.close()

# sins = ['Обожрался', 'Распустился', 'Алчнулся', 'Опечалился', 'Погневился', 'Приуныл', 'Тщеславнулся', 'Возгордился']
@bot.message_handler(func=lambda message: "греш" in message.text.lower())
def choose_sin(message):
    # bot.send_message(message.chat.id, 'Расскажи мне, что ты совершил')
    markup = types.ReplyKeyboardMarkup()
    for item in sins:
    	markup.add(item)
    bot.send_message(message.chat.id, "Расскажи мне, что ты совершил:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in sins)
def sin_react(message):
    # bot.send_message(message.chat.id, 'Расскажи мне, что ты совершил')
    bot.send_message(message.chat.id, 'Расскажи мне, где это произошло', reply_markup=types.ReplyKeyboardHide())

# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, 'Привет! Я твой персональный священник!')

# @bot.message_handler(commands=['auth'])
# def send_auth(message):
#     pass 

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_msg(message):
#     bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    sins = ['Обожрался', 'Распустился', 'Алчнулся', 'Опечалился', 'Погневился', 'Приуныл', 'Тщеславнулся', 'Возгордился']
    bot.polling(none_stop=True)