
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
            # print(f"{title.text.strip()} - {price.text.strip()} - {seller}")
           
            if  seller not in sellers:
                sellers.append(seller)
    # print(pending_searches)

            

# Gets products for a paricular seller
def seller_search(seller):
    url = "https://www.ebay.co.uk/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=" + seller
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    for item in soup.select('.s-item')[2:]:
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        
        sales(item)

        # Creates new product
        if title and price:
            pending_searches.append(title.text)

pending_searches.append("Electric Toothbrush Drip tray stand")

# Converts text to seller profile link format
def profile_link(text):
    text = text.replace(' ', '+')
    text = text.replace('/', '%2F')
    text = text.replace(',', '%2C')
    text = 'https://www.ebay.co.uk/sch/i.html?_nkw=' + text
    print(text)
    return text


# Detects key phrase in a product listing and returns num of sales
def sales(item):
    link = item.select_one('.s-item__link')
    url = link['href']

    response = requests.get(url, headers=headers)
    html = response.text
    print("running")
    soup = BeautifulSoup(html, 'html.parser')


# Searches sellers for first 10 products
def run():
    for i in range(2):
        if len(pending_searches) == 0:
            seller_search(sellers.pop(0))
        print("searching " + pending_searches[0])
        search(profile_link(pending_searches.pop(0)))
   
    print(sellers)

run()
    