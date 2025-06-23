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



# # Checks product page contains given phrase (not case-sensitive)
# def contains(url, phrase):
#     response = session.get(url)
#     response.html.render(timeout=10)

#     html = response.text

#     soup = BeautifulSoup(html, 'html.parser')
#     container = soup.select_one('div.vim.x-evo-tabs-region')

#     print(container)
#     if container.find(string=lambda t: phrase.lower() in t.lower()) is None:
#         print("false")
#         return False
#     else:
#         print("true")
#         return True