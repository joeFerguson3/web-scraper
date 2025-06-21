import requests
from bs4 import BeautifulSoup


url = "https://www.ebay.co.uk/sch/i.html?_nkw=python&_sacat=0&_from=R40&_trksid=p2334524.m570.l1313&_odkw=abc&_osacat=0"

headers = {
    'User-Agent': 'Mozilla/5.0'
}

response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

for item in soup.select('.s-item'):
    title = item.select_one('.s-item__title')
    price = item.select_one('.s-item__price')

    if title and price:
        print(f"{title.text.strip()} - {price.text.strip()}")