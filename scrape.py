import re
from bs4 import BeautifulSoup
import requests

# FIREBASE IMPORTS

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('uniscrape-firebase-adminsdk-6dttz-d2abb0fcac.json')
# default_app = firebase_admin.initialize_app(cred)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://uniscrape.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/prices')
print(ref.get())


class Uniqlo_Scraper:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Referer":"http://www.google.com.au","Cache-Control":"max-age=0"}
        self.baseURL = "http://www.uniqlo.com/au/"

        """Parses UNIQLO HTML to get prices"""

    def get_prices(self, filter_string):
        """Parses UNIQLO HTML to get prices"""

        result_url = "store/"+  filter_string +"/featured/sale.html"
        session = requests.session()
        response = session.get(self.baseURL + result_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.product_list = []

        product_name = soup.find_all("h2", {"class": "product-name"})
        old_price = soup.find_all("span", {"id": "old-price"})
        sale_price = soup.find_all("span", {"id": "product-price"})

        i = 0
        while i in range(0, len(product_name)):
            product_link_div = soup.find("a", {"title": product_name[i].text})
            product_url = product_link_div.attrs['href']
            p = [product_name[i].text, float(old_price[i].text[3:]), float(sale_price[i].text[3:]), product_url]
            i += 1
            self.product_list.append(p)
        return self.product_list

    def filter_prices_by_discount(self, discount,filter_string):
        """
        Takes  discount as an integer returns all products
        with a greater or equal discount
        """
        filter_list = self.get_prices(filter_string)
        new_list = []
        i = 0
        for product in filter_list:
            if (1-(product[2] / product[1])) * 100 >= discount:
                new_list.append(product)
        
        return new_list

    def get_price_dict(self,price_list):
        price_dict = {}
        for product in price_list:
            my_dict = {'old_price': product[1], 'new_price': product[2],'product_url': product[3]}
            price_dict[product[0]] = my_dict
        return price_dict



if __name__ == '__main__':
    scraper = Uniqlo_Scraper()
    # prices = scraper.get_prices()
    men_list = scraper.filter_prices_by_discount(51, 'men')
    women_list = scraper.filter_prices_by_discount(51, 'women')
    men_dict = scraper.get_price_dict(men_list)
    women_dict  = scraper.get_price_dict(women_list)
    prices_men_ref = ref.child('mens')
    prices_men_ref.set(men_dict)
    prices_women_ref = ref.child('womens')
    prices_women_ref.set(women_dict)
    print men_dict