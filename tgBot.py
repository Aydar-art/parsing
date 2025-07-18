from telebot import types
from main import parse
import pandas as pd
from app.pandasApp import csv_columns
from app.set import bot, url
from app.pandasApp import get_json


#код бота телеграмма
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Вы можете запустить парсер')
    # bot.register_next_step_handler(message, menu)


@bot.message_handler(commands=['parsing'])
def start_parsing(message):
    df = pd.DataFrame([], columns=csv_columns)
    df.to_csv('data_base/new_data.csv', sep=';')

    parse(url, bot_data=[bot, message])

@bot.message_handler(commands=['archive'])
def archive(message):
    file = get_json('Архив')

    bot.send_document(message.from_user.id, file)

@bot.message_handler(commands=['new_arcihve'])
def new_archive(message):
    file = get_json('Новый архив')

    bot.send_document(message.from_user.id, file)



@bot.message_handler(commands=['new_active'])
def new_active(message):
    file = get_json('Новые')

    bot.send_document(message.from_user.id, file)



@bot.message_handler(commands=['active'])
def active(message):
    file = get_json('Активные')

    bot.send_document(message.from_user.id, file)







bot.infinity_polling(timeout=10, long_polling_timeout = 5)
