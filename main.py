import random
import datetime
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from app.set import headers
from app.pandasApp import add_new_elements, write_new_data, csv_columns



#получение страницы в объявлениями
def get_html(url, params=None, bot_data=None):
    bot, message = bot_data
    bot.send_message(message.from_user.id, 'Попытка подключения...')
    html = requests.get(url, headers=headers, params=params, timeout=3)

    if int(html.status_code) != 200:
        bot.send_message(message.from_user.id, 'Ошибка при подключении ❌ |' + str(html.status_code) + '\nПовторная попытка через 10 минут')
        time.sleep(600)
        return get_html(url, bot_data=bot_data)
    
    else:
        bot.send_message(message.from_user.id, 'Успешное подключение ✅')
        return BeautifulSoup(html.content, 'lxml')
    


#получение объявлений
def get_items(html):
    items = html.find_all('div', attrs={'data-marker': 'item'})
    return items


#получение ссылки на объявление
def get_itemLink(item):
    itemLink = url_head + item.find('div', {'class': re.compile(r'iva-item-title')}).find('a')['href']
    return itemLink


#получение имени продавца
def get_name(item):
    try:
        name = item.find('div', attrs={'class': re.compile('iva-item-sellerInfo')}).find('div').find('div').find('a').find('p').contents[0]
    except:
        name = '\'Без имени\''
    return name

#получение даты объявления
def get_date():
    now_date = datetime.datetime.now()
    item_time = f'{now_date.day}.{now_date.month}.{now_date.year}'
    return item_time

#получение адреса
def get_address(item):
    try:
        address = item.find('div', attrs={'class': re.compile('iva-item-content')}).find('div', attrs={'class': re.compile('geo-root')}).find('p').find('span').contents[-1]
    except:
        address = '\'Без адреса\''
    return address

#получение цены товара
def get_price(item):
    try:
        item_price = item.find('p', attrs={'data-marker': 'item-price'}).find('span').contents[0]
    except:
        item_price = '0'
    item_price = item_price.replace('\\', '')
    item_price = item_price.replace('xa', '')
    return item_price



url_head = 'http://avito.ru'

def parse(url, bot_data):
    data = []
    bot, message = bot_data
    bot.send_message(message.from_user.id, 'Адрес подключения: ' + f'[{url}]({url})', parse_mode='Markdown')
    html = get_html(url, bot_data=bot_data)
    catalog_item = get_items(html)

    #перебор всех объявлений на странице
    for item in catalog_item:
        itemLink = get_itemLink(item)

        seller_name = get_name(item)
        seller_address = get_address(item)
        seller_date = get_date()
        item_price = get_price(item)

        data.append([seller_name, seller_address, seller_date, item_price, item_price, itemLink])



    

    try:
        haveNextPage = True
        nextPageLink = url_head + html.find('a', attrs={'data-marker': 'pagination-button/nextPage'})['href']
        bot.send_message(message.from_user.id, 'Переход на следующую страницу =>')
    except:
        haveNextPage = False


    if haveNextPage:
        write_new_data(data)
        sleep = random.randint(300, 360)
        bot.send_message(message.from_user.id, f'Переход на страницу через {sleep} сек')
        time.sleep(sleep)
        parse(nextPageLink, bot_data=bot_data)
    else:
        bot.send_message(message.from_user.id, 'Данные собраны\nОбрабатываю данные...')
        add_new_elements(data)
        bot.send_message(message.from_user.id, 'Данные успешно обработаны ✅')