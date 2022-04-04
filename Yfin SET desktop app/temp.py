import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.morningstar.com/stocks/xnas/fb/quote')
page = requests.get('https://www.morningstar.com/stocks/xnas/fb/quote')
text = page.text
soup = BeautifulSoup(driver.page_source)
for div in soup.findAll('div', {'class': 'dp-pair'}):
    if div.find('div', {"class": "dp-name"}).text in ('Price/Sales', 'Price/Book'):
        print(div.find('div', {"class": "dp-name"}).text.strip(), div.find('div', {"class": "dp-value"}).text.strip())

        print(div)
