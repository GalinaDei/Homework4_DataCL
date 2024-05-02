'''Урок 4. Парсинг HTML. XPath
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса 
на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные 
из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:
Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер 
и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.'''

'//*[@id="content"]/div/div/div/div[3]'
'//*[@id="content"]/div/div/div/div[3]/div'
'//*[@id="content"]/div/div/div/div[3]/div/table/tbody/tr'

import requests
from lxml import html
import pandas as pd
import csv

url = "https://cbr.ru/currency_base/daily/"

response = requests.get(url, headers = {
   'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'})

tree = html.fromstring(response.content)

table_rows_all = tree.xpath("/html/body/main/div/div/div/div[3]/div/table/tbody")
table_rows = table_rows_all[0]
print(len(table_rows))

data = []
for i in range(1,len(table_rows)):
    columns = table_rows[i].xpath(".//td/text()")
    record = {}  
    record['Цифровой код'] = int(columns[0].strip())
    record['Буквенный код'] = columns[1].strip()
    record['Единиц'] = int(columns[2].strip())
    record['Валюта'] = columns[3].strip()
    record['Курс'] = float('.'.join(columns[4].strip().split(',')))

    data.append(record)

print(data[:10])
df = pd.DataFrame(data)
df.to_csv('currency.csv', sep = ',', encoding = 'utf-8')
print(df.head())