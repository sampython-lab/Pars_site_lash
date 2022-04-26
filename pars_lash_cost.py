# Run the file, specify the number of pages for parsing. After that, a file "cards.csv" with the added information will appear.

import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://parisnail.ru/'
URL = 'https://parisnail.ru/catalog/narashchivanie-resnits/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


html = get_html(URL)
print(html)


def get_content(self):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='col-xs-6 col-sm-6 col-md-4 col-lg-3 prod-elem')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='catalog-cart__title-text').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='catalog-cart__item').find('a').get('href'),
                'price': item.find('div', class_='catalog-cart__price-cont').get_text(strip=True),
                'card_img': HOST + item.find('div', class_='catalog-cart__pic').find('img').get('src')
            }
        )
    return cards


def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Ссылка на продукт', 'Цена', 'Изображение ресниц'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['price'], item['card_img']])


def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'PAGEN_1': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
    else:
        print('Error')


parser()
