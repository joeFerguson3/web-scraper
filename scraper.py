import requests
from bs4 import BeautifulSoup


url = "https://www.ebay.co.uk/sch/i.html?item=256582607134&rt=nc&_trksid=p4429486.m3561.l161211&_ssn=peripheral_centre"

headers = {
    'User-Agent': 'Mozilla/5.0'
}

response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

for item in soup.select('.s-item'):
    title = item.select_one('.s-item__title')
    price = item.select_one('.s-item__price')
    link = item.select_one('.s-item__link')
    url = link['href']

    if title and price:
        print(f"{title.text.strip()} - {price.text.strip()}")
        print(url)