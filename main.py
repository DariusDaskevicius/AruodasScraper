import requests
import json
from bs4 import BeautifulSoup

HOST = 'https://en.aruodas.lt'
URL = 'https://m.en.aruodas.lt/butai/vilniuje/?FRoomNumMin=2&FRoomNumMax=2'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
}

def get_html(url, params=''):
    request = requests.get(url, headers=HEADERS, params=params)
    return request

def save_json(items):
    with open('flats.json', 'w', encoding='utf-8') as json_file:
        json.dump(items, json_file, indent=4, ensure_ascii=False)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='result-item-v3')
    flats = []

    for item in items:
        flats.append({
           'Adress': item.find('span', class_='result-item-info-v3').find('span', class_='item-address-v3').get_text(strip=True),
           'Description': item.find('span', class_='result-item-info-v3').find('span', class_='item-description-v3').get_text(strip=True),
           'Price': item.find('span', class_='result-item-info-v3').find('span', class_='item-price-main-v3').get_text(strip=True),
           'Image': item.find('a', class_='object-image-link').find('img').get('src')
        })
    return flats

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        flats = []
        flats.extend(get_content(html.text))
        save_json(flats)
    else:
        print('Error')

parser()