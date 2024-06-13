import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# save in csv file
file = open('comics.csv', 'w', newline='\n')
wr_obj = csv.writer(file)
wr_obj.writerow(['Title', 'Price', 'Status', 'Link'])

page = 1
while page <= 5:
    url = f'https://parsek1.com/collections/all-comics?page={page}'
    page += 1

    response = requests.get(url)

    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    product_section = soup.find('div', class_='collection')
    comic_spec = product_section.find_all('li', class_='grid__item')

    for comic in comic_spec:
        # title
        info = comic.find('div', class_='card__content')
        title = info.a.text.strip()

        #price
        price_info = comic.find('span', class_='price-item price-item--regular')
        price = price_info.text.strip()

        #image url
        img_addr = comic.img.attrs['src']
        image = f'https:{img_addr}'      # https-ის დამატება მომიწია, რათა კონსოლიდან შეძლებოდა ლინკზე გადასვლა

        # status
        bottom_left = comic.find('div', class_='card__badge bottom left')
        status = bottom_left.text.strip()
        if status != 'Sold out':
            status = 'In stock'

        res = 'Title: {} \nPrice: {} \nImage Link: {} \nStatus: {}\n'.format(title, price, image, status)
        print(res)

        wr_obj.writerow([title, price, status, image])
    time.sleep(random.randint(15, 20))
