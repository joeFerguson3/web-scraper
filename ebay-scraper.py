
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re

url = "https://www.ebay.co.uk/sch/i.html?_nkw=keyboard"

headers = {
    'User-Agent': 'Mozilla/5.0'
}
sellers = []

# sellers which have been searched
complete_sellers = []

pending_searches = []

# Products which have been searched
complete_searches = {}
session = HTMLSession()

# Gets sellers for a specific search
def search(search):
    print("searching for: " + search)
    complete_searches[search] = 0
    url = search
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    
    for item in soup.select('.s-item')[2:]:
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        seller = item.select_one('.s-item__seller-info-text')
        product_link = item.select_one('.s-item__link')
        product_url = product_link['href']

        # Checks listing exists
        if title and price and seller and contains(product_url, "3d printed"):
           
            # complete_searches[search] += sales(product_url)

            complete_searches[search] += 1
            seller = seller.text.split(' ')[0]
            # print(f"{title.text.strip()} - {price.text.strip()} - {seller}")
           
            if seller not in sellers:
                sellers.append(seller)
    print(str(complete_searches[search]) + " sellers found")


            

# Gets products for a paricular seller
def seller_search(seller):
    print("Finding new listings from " + seller)
    url = "https://www.ebay.co.uk/sch/ai.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=" + seller
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    for item in soup.select('.s-item')[2:]:
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        product_link = item.select_one('.s-item__link')
        product_url = product_link['href']
        
        # Creates new product
        if title and price and contains(product_url, "3d printed"):
            pending_searches.append(title.text)
    print(str(len(pending_searches)) + " listings found")



# Converts text to seller profile link format
def profile_link(text):
    text = text.replace(' ', '+')
    text = text.replace('/', '%2F')
    text = text.replace(',', '%2C')
    text = 'https://www.ebay.co.uk/sch/i.html?_nkw=' + text
    return text


# Returns num of sales for a listing
def sales(url):
    try:
        response = session.get(url)
        response.html.render(timeout=10)

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        availability = soup.select_one('#qtyAvailability')

        spans = availability.select('.ux-textspans.ux-textspans--SECONDARY')
        number = (spans[1].text).split(" ")[0]
        number = int(number.replace(",", ""))

        print(number)
        return number
    except IndexError:
        return 0
 
# Checks product description contains given phrase (not case-sensitive)
def contains(url, phrase):
    id = get_product_id(url)

    # Link to product description
    desc = "https://itm.ebaydesc.com/itmdesc/" + id

    response = requests.get(desc, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Gets visible text
    text = soup.get_text(separator=' ', strip=True)

    # Checks for phrase in text
    if phrase.lower() in text.lower():
        return True
    else:
        return False
    
# Returns product id, extracted from given URL
def get_product_id(url):
   match = re.search(r"/itm/(\d+)", url)
   product_id = match.group(1) 
   return product_id


pending_searches.append("oral b toothbrush stand")
# Searches sellers for first 10 products
def run():
    for i in range(100):
        while len(pending_searches) == 0:
            complete_sellers.append(sellers[0])
            seller_search(sellers.pop(0))
  
        search(profile_link(pending_searches.pop(0)))
   
    print(complete_sellers)
    print(sellers)
    print(complete_searches)

run()
    