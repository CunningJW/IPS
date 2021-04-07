from tinydb import TinyDB
import requests
from bs4 import BeautifulSoup

db = TinyDB('paragraphs.json')  #создаем базу данных

links = [   #составление списка сайтов, по которым требуется провести парсинг
            'https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b',
            'https://journals.sagepub.com/doi/full/10.1177/0020294020932344',
            'https://maker.pro/raspberry-pi/projects/how-to-create-a-facial-recognition-door-lock-with-raspberry-pi',
            'https://www.digikey.be/en/maker/projects/raspberry-pi-face-recognition-based-door-lock/a4c71ade7f294a62bd8cd94a803df919',
            ]

for link in links:                                          #в каждой ссылке...
    information = requests.get(link).content                #запрашиваем данные
    html = BeautifulSoup(information, 'lxml')               #преобразуем в объект BS (для удобного взаимодействия)
    paragraphs = html.find_all('p')                         #ищем все строки с параметром "р" - параграф
    for paragraph in paragraphs:                            #для каждой строки из найденных...
        if len(paragraph.get_text()) > 10:                  #проверяем на минимальный размер
            db.insert({                                     #вставляем в базу данных
                        'text':paragraph.get_text(),
                        'link':link,
                        'size':len(paragraph.get_text()),
                        })
