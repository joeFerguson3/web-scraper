
import requests
from bs4 import BeautifulSoup


url = "https://www.ebay.co.uk/sch/i.html?_nkw=keyboard"

headers = {
    'User-Agent': 'Mozilla/5.0'
}
sellers = []
pending_searches = []


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

        # Checks listing exists
        if title and price and seller:
            seller = seller.text.split(' ')[0]
            print(f"{title.text.strip()} - {price.text.strip()} - {seller}")
           
            if  seller not in sellers:
                sellers.append(seller)
                seller_search(seller)
    print(pending_searches)

            


def seller_search(seller):
    url = "https://www.ebay.co.uk/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=" + seller
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    for item in soup.select('.s-item')[2:]:
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        link = item.select_one('.s-item__link')
        url = link['href']

        if title and price and link:
            pending_searches.append(title.text)


search("https://www.ebay.co.uk/sch/i.html?_nkw=keyboard")