import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests

HOST = 'https://cian.ru/'
URL = 'https://cian.ru/'
PATH = 'database.csv'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params='')
    return r



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='_025a50318d--c-popular-block-wrap--WNSeg cg-row').find_all('div', class_='_025a50318d--c-popular-info--HRsb6')
    cards = []

    for item in items:
        cards.append(
            {
                'square': int(''.join(filter(lambda x: x.isdigit(), item.find('span', class_='_025a50318d--c-popular-tec-info--yVLGS').get_text(strip=True)))[1:-1]),
                'adress': item.find('span', class_='_025a50318d--c-popular-metro-name--tOQHQ').get_text(strip=True),
                'price': int(''.join(filter(lambda x: x.isdigit(), item.find('span', class_='_025a50318d--c-popular-price--X7UPE').get_text(strip=True))))             

            }
        )
    #print(cards)
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Адрес', 'Площадь м2', 'Стоимость'])
        for item in items:
            writer.writerow([item['adress'], item['square'], item['price']])
            

            
def calc_average(flats):
    square_sum = 0
    price_sum = 0
    for i in flats:
        square_sum += i['square']
        price_sum += i['price']

    average_price_sq2 = round(price_sum / square_sum)
    average_price_flat = round(price_sum / len(flats))
    print(f'\nPython: Средняя стоимость за квадратный метр: {average_price_sq2} руб.')
    print(f'Python: Средняя стоимость квартиры: {average_price_flat} руб.')


def calc_by_pandas():
    data = pd.read_csv('database.csv', encoding='cp1251', delimiter=';')
    print(data, '\n')
    av = round(data['Стоимость'].mean() / data['Площадь м2'].mean())
    avf = round(data['Стоимость'].mean())
    print(f'\nPandas: Средняя стоимость за квадратный метр: {av} руб.')
    print(f'Pandas: Средняя стоимость квартиры: {avf} руб.')
    


html = get_html(URL)
flats = get_content(html.text)
save_doc(flats, PATH)
calc_by_pandas()
calc_average(flats)



