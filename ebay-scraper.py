
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
        seller_info = item.select_one('.s-item__seller-info-text')
        product_link = item.select_one('.s-item__link')
        product_url = product_link['href']

        if seller_info is not None:
            rating = seller_info.text.split(' ')[1]
            rating = rating.replace("(", "").replace(")", "").replace(",", "")
            rating = int(rating)
        else:
            rating = 0

        # Checks listing exists
        if title and price and seller_info and rating > 1000 and contains(product_url, "3d printed"):

            complete_searches[search] += 1
            seller = seller_info.text.split(' ')[0]
           
            if seller not in sellers and seller not in complete_sellers:
                sellers.append(seller)
    print(str(complete_searches[search]) + " sellers found")


            

# Gets products for a paricular seller
def seller_search(seller):
    print("Finding new listings from " + seller)

    #Link to seller page
    url = "https://www.ebay.co.uk/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=" + seller
    
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

 
    for item in soup.select('.s-item')[2:]:
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        product_link = item.select_one('.s-item__link')
        product_url = product_link['href']

        # Creates new product, if contains key word and above given sale count
        sold = sales(product_url)
        if title and price and sold >= 250:
            pending_searches.append(title.text)

        with open("data.txt", "a") as f:
            f.write(" | " + str(len(pending_searches)) + " | " + str(sold) + " | " + product_url + "\n")
    
    print(str(len(pending_searches)) + " listings found")



# Gets the link for a particular search
def search_link(text):
    text = text.replace(' ', '+')
    text = text.replace('/', '%2F')
    text = text.replace(',', '%2C')
    text = 'https://www.ebay.co.uk/sch/i.html?_nkw=' + text
    return text


# Returns num of sales for a listing
def sales(url):
    try:
        response = session.get(url)
        print(response.html.html[:3000])
        try:
            response.html.render(timeout=20)
        except Exception as e:
            print("Render error:", e)
            return 0

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        text = soup.get_text().lower()
        if "sold" in text:
            print("Sold info found")

        availability = soup.select_one('#qtyAvailability')
        if not availability:
            print("no availability")
            return 0

        spans = availability.select('.ux-textspans.ux-textspans--SECONDARY')
        print(spans)
        if len(spans) < 2:
            print("len < 2")
            return 0

        number = (spans[1].text).split(" ")[0]
        number = int(number.replace(",", ""))

        return number
    except (IndexError, ValueError, AttributeError):
        print("other error")
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


pending_searches.append("BT Smart Hub 2 Wall mount bracket smarthub homehub Slim Custom - Internet Router")
# Searches sellers for first 10 products
def run():
    for i in range(30):
        while len(pending_searches) == 0:
            complete_sellers.append(sellers[0])
            with open("data.txt", "a") as f:
                f.write("\n" + sellers[0] + "\n")
            
            with open("sellers.txt", "a") as f:
                f.write(sellers[0] + "\n")


            # Finds sellers products
            seller_search(sellers.pop(0))

        # Searches for new sellers
        search(search_link(pending_searches.pop(0)))
        
        print(complete_searches)

    print(complete_sellers)
    print(sellers)
    print(complete_searches)


run()
    