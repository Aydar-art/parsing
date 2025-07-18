import pandas as pd
import json

csv_columns = ['Seller', 'Address', 'Date_Item', 'Current_Price', 'Last_Price', 'Item_Link']

def add_new_elements(data):
    #получение записанных активных объявлений
    active_data = pd.read_csv('data_base/active_elements.csv', sep=';')

    #преобразование полученных данных
    new_data = pd.read_csv('data_base/new_data.csv', sep=';')

    for i in range(len(new_data)):
        el1 = new_data.iloc[i]['Item_Link']
        for j in range(i + 1, len(new_data)):
            el2 = new_data.iloc[j]['Item_Link']

            if el1 == el2:
                new_data.drop(j)
            

    #данные, которые появились сегодня
    today_active = pd.DataFrame([], columns=csv_columns)

    #поиск новых данных
    for i in range(len(new_data)):
        current = new_data.iloc[i]['Item_Link']
        was = False
        for j in range(len(active_data)):
            last = active_data.iloc[j]['Item_Link']
            if current == last:
                was = True

            else:
                pass

        if was == False:
            df = pd.DataFrame([new_data.iloc[i].tolist()], columns=csv_columns)
            today_active = pd.concat([today_active, df], join='outer')

    today_active.to_csv('data_base/new_elements.csv', index=False, sep=';')
    print('Новые объявления обнаружены...')

    #архивные объявления
    archive_data = pd.read_csv('data_base/archive.csv', sep=';')

    #массив удаленных сегодня объявлений
    today_archive = pd.DataFrame([], columns=csv_columns)

    #поиск устаревших данных
    for i in range(len(active_data)):
        last = active_data.iloc[i]['Item_Link']
        has = False
        for j in range(len(new_data)):
            current = new_data.iloc[j]['Item_Link']
            if current == last:
                has = True

        if has == False:
            df = pd.DataFrame([active_data.iloc[i].tolist()], columns=csv_columns)
            today_archive = pd.concat([today_archive, df], join='outer')

    today_archive.to_csv('data_base/new_archive_elements.csv', index=False, sep=';')
    print('Снятые публикации найдены...')


    #создание массива активных элементов
    new_active_data = pd.concat([active_data, today_active], join='outer')
    new_active_data.to_csv('data_base/active_elements.csv', index=False, sep=';')

    #создание новых архивов
    new_archive_data = pd.concat([archive_data, today_archive], join='outer')
    new_archive_data.to_csv('data_base/archive.csv', index=False, sep=';')
    print('Активные и архивированные элементы перезаписаны...')



def get_json(file_name):

    if file_name == 'Архив':
        df = pd.read_csv('data_base/archive.csv', sep=';')
    elif file_name == 'Новый архив':
        df = pd.read_csv('data_base/new_archive_elements.csv', sep=';')
    elif file_name == 'Активные':
        df = pd.read_csv('data_base/active_elements.csv', sep=';')
    else:
        df = pd.read_csv('data_base/new_elements.csv', sep=';')

    dict = []

    for i in range(len(df)):
        el = df.iloc[i]
        item = {
            'Seller': el['Seller'],
            'Address': el['Address'],
            'Date_Item': el['Date_Item'],
            'Current_Price': el['Current_Price'],
            'Last_Price': el['Last_Price'],
            'URL': el['Item_Link']
        }
        dict.append(item)

    with open('data_base/DB_json.json', 'w') as output:
        output.write(json.dumps(dict, ensure_ascii=False))
    
    return open('data_base/DB_json.json', 'rb')



def write_new_data(data):
    new_data = pd.DataFrame(data, columns=csv_columns)
    df = pd.read_csv('data_base/new_data.csv', sep=';')
    df = pd.concat([df, new_data], join='inner')

    df.to_csv('data_base/new_data.csv', sep=';', index=False)
    print('new_data was rewrited...')
    

