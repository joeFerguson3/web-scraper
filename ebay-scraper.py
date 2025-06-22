import requests
from bs4 import BeautifulSoup


url = "https://www.ebay.co.uk/sch/i.html?_nkw=keyboard"

headers = {
    'User-Agent': 'Mozilla/5.0'
}


# Gets sellers for a specific search
def search(title):
    url = title
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    
    for item in soup.select('.s-item'):
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        seller = item.select_one('.s-item__seller-info-text')

        if title and price and seller:
            print(f"{title.text.strip()} - {price.text.strip()} - {seller.text.split(' ')[0]}")


search("https://www.ebay.co.uk/sch/i.html?_nkw=keyboard")