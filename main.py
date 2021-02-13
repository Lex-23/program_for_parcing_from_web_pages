import requests
from bs4 import BeautifulSoup
import time
import smtplib


dif = int(input('tracked difference course:'))
# сюда вписывается отклонение курса, которое будет для критичным
time_out = int(input('tracking interval: '))
# задается время для проверки курса, в секундах


class Currency:

    BTC_USD = 'https://ru.investing.com/crypto/bitcoin/btc-usd'
    # адрес сайта, который будет парсится на предмет курса битка
    headers = {'User-Agent': 'your_user_agent'}
    # юзер-агент устройства, с которого запускается программа
    current_converted_price = 0
    difference = dif

    def __init__(self):
        self.current_converted_price = float(self.
                                             get_currency_price().
                                             replace(',', '.'))

    # функция для получения текущего курса биткоина в виде строки
    def get_currency_price(self):
        full_page = requests.get(self.BTC_USD, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.find_all('span', {'id': 'last_last'})
        res = convert[0].text.replace('.', '')
        return res

    # функция для проверки отклонения курса
    def check_currency(self):
        currency = float(self.get_currency_price().replace(',', '.'))
        if currency >= self.current_converted_price + self.difference:
            print('The rate has drown a lot')
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print('the rate has fallen sharply')
            self.send_mail()
        print(f'1 bitcoin = {str(currency)} USD now')
        time.sleep(time_out)
        self.check_currency()

    # функция отправки сообщения на почту о критическом изменении курса
    @staticmethod
    def send_mail():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        # адрес и пароль почты отправителя
        server.login('mail_address_from', 'password')

        # данные для письма
        subject = 'Rate btc'
        body = 'Rate btc was changing'
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            'mail_address_from',  # почта отправления
            'maik_address_to',    # почта получения
            message
        )
        server.quit()


cur = Currency()
cur.check_currency()
