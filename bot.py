# -*- coding: utf-8 -*-
import time
import telebot
import config
import re
from telebot import types
import sqlite3
import os.path

bot = telebot.TeleBot(config.token)
# img = open('rood', 'rb')
# img.close()    

sins = []
sin_actions = []
db_conn = sqlite3.connect('sins.db')
c = db_conn.cursor()
for row in c.execute('SELECT * FROM sins ORDER BY sin_id'):
    print(row)
    sins.append(row)
    sin_actions.append(str(row[2]))
db_conn.close()
print(sins)

start_pattern = r"Привет"
@bot.message_handler(regexp=start_pattern)
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я священник!')

@bot.message_handler(func=lambda message: message.text=="Хай")
def send_welcome2(message):
    bot.send_message(message.chat.id, 'хой')

@bot.message_handler(func=lambda message: message.text=="Перечисли грехи")
def list_sins(message):
    for sin in sins:
        bot.send_message(message.chat.id, sin[1])


@bot.message_handler(func=lambda message: "спасибо" in message.text.lower())
def choose_sin(message):
    bot.send_message(message.chat.id, "До новых встреч, сын мой")

@bot.message_handler(func=lambda message: "греш" in message.text.lower() or "не всё" in message.text.lower() or "ещё" in message.text.lower())
def choose_sin(message):
    markup = types.ReplyKeyboardMarkup()
    for item in sin_actions:
    	markup.add(item)
    bot.send_message(message.chat.id, "Расскажи мне, что ты совершил:", reply_markup=markup)

def determine_fee(occured_sin_action):
    for sin in sins:
        if occured_sin_action == sin[2]:
            occured_sin = sin[1]
            occured_fee = sin[3]
            occured_sin_id = sin[0]
    print(occured_sin)
    print(occured_fee)
    return(occured_sin, occured_fee, occured_sin_id)

occured_fee=100
occured_sin=''
occured_sin_id=0
charity_subject="Детский приют №13 в Сергиевом Посаде"

@bot.message_handler(func=lambda message: message.text in sin_actions)
def sin_react(message):
    # markup_hider = types.ReplyKeyboardHide()
    # bot.send_message(message.chat.id, 'Расскажи мне, что ты совершил')
    bot.send_message(message.chat.id, 'Расскажи мне, где это произошло', reply_markup=types.ReplyKeyboardHide())
    occured_sin_action = message.text
    print(occured_sin_action)
    global occured_fee
    global occured_sin
    global occured_sin_id

    occured_sin, occured_fee, occured_sin_id = determine_fee(occured_sin_action)
    # print(occured_sin)
    # print(occured_fee)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def comment_sin(message):
    if occured_sin_id in [1,2,8]:
        bot.send_message(message.chat.id, "Красавчик")
    else:
    	bot.send_message(message.chat.id, "Вот отстой!")
    time.sleep(0.3)
    bot.send_message(message.chat.id, "Кхм")
    time.sleep(1)
    bot.send_message(message.chat.id, "То есть... %s это прискорбно" %occured_sin)
    time.sleep(1)
    bot.send_message(message.chat.id, "Искупление этого греха стоит %d рублей" %occured_fee)
    time.sleep(1.3)
    bot.send_message(message.chat.id, "Мы пожертвуем эти деньги в %s" %charity_subject)
    time.sleep(0.7)
    bot.send_message(message.chat.id, "Чтобы завершить операцию поцелуйте распятие")
    img = open('rood.jpeg', 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()    

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
    bot.polling(none_stop=True)