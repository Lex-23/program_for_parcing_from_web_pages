import requests
from bs4 import BeautifulSoup

DOLLAR_BIN = 'https://www.rbc.ru/crypto/currency/btcusd'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}

full_page = requests.get(DOLLAR_BIN, headers=headers)

soup = BeautifulSoup(full_page.content, 'html.parser')

convert = soup.find_all('div', {'class': 'chart__subtitle js-chart-value'})
print(convert[0].text)
