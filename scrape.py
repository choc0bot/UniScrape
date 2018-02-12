import re
from bs4 import BeautifulSoup
import requests


class Uniqlo_Scraper:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Referer":"http://www.google.com.au","Cache-Control":"max-age=0"}
        self.baseURL = "http://www.uniqlo.com/au/"

        """Parses UNIQLO HTML to get prices"""

    def get_prices(self):
        """Parses UNIQLO HTML to get prices"""

        result_url = "store/men/featured/sale.html"
        session = requests.session()
        response = session.get(self.baseURL + result_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.product_list = []

        product_name = soup.find_all("h2", {"class": "product-name"})
        old_price = soup.find_all("span", {"id": "old-price"})
        sale_price = soup.find_all("span", {"id": "product-price"})

        i = 0
        while i in range(0, len(product_name)):
            product_link_div = soup.find("a", {"title": product_name[i].text })
            product_url = product_link_div.attrs['href']
            p = [product_name[i].text, float(old_price[i].text[3:]), float(sale_price[i].text[3:]), product_url]
            i += 1
            self.product_list.append(p)
        
        return self.product_list
            

        
    def filter_prices_by_discount(self, discount):
        filter_list =  self.get_prices()
        new_list = []
        i = 0
        for product in filter_list:
            if (1-(product[2] / product[1])) * 100 >= discount :
                new_list.append(product)


        for product in new_list:        
            print product[0]
            print product[1]
            print product[2]
            print product[3]


if __name__ == '__main__':
    scraper = Uniqlo_Scraper()
    # prices = scraper.get_prices()
    scraper.filter_prices_by_discount(51)
    # print prices
