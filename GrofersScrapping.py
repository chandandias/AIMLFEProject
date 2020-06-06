import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint


class GrofersScrapping(object):

    def __init__(self):
        self.titleX = []
        self.spX = []
        self.mrpX = []
        self.quantityX = []
        self.linkX = []
        self.discountX = []
        self.ratingX = []
        self.categoryX = []
        self.rating_countX = []
        self.review_countX = []
        self.sourceX = []

    def pulses(self, category):
        base_url = 'https://grofers.com'
        param = '/v5/search/merchants/26012/products/?lat=12.9894395055235&lon=77.7348850599167&q='
        param1 = '&suggestion_type=0&t=1&size=48&start='
        offset = 0
        total_items = 0
        stop = False
        headers = {
            'auth_key': 'd1cc0621fb608b29a85d6f243e32ef15aa7afe93012e39a9317e3ff1ecbc2846',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        while(True):
            url = base_url + param + category + param1 + str(offset)
            response = requests.get(url, headers=headers)
            json_object = json.loads(response.text)
            products = []
            if 'products' in json_object:
                products = json_object['products']

            if len(products) > 0:
                for prod in products:
                    title = prod['name']
                    mrp = prod['mrp']
                    sp = prod['price']
                    prid = prod['product_id']
                    link = base_url + '/prn/' + title.lower().replace("'", "").replace('/', '').replace(' ', '-') + '/prid/' + str(
                        prid)
                    quantity = prod['unit']
                    # discount = prod['disc_amt']
                    if float(sp) != 0.0:
                        discount = round(((float(mrp) - float(sp))/float(sp))*100, 2)
                    else:
                        discount = 0.0
                    category = prod['categories'][0]['name']
                    subcategory = prod['subcategories'][len(prod['subcategories']) - 1]['name']
                    rating = prod['rating']
                    source = 'Grofers'
                    if not (str(sp) == '0' or str(mrp) == '0'):
                        self.titleX.append(title)
                        self.spX.append(str(sp))
                        self.mrpX.append(str(mrp))
                        self.linkX.append(link)
                        self.quantityX.append(str(quantity))
                        self.discountX.append(str(discount))
                        self.categoryX.append(category)
                        self.ratingX.append(str(rating))
                        self.rating_countX.append('0')
                        self.review_countX.append('0')
                        self.sourceX.append(source)
                        print("Title: " + title)
                        print("Product Link: " + link)
                        print("Selling Price: " + str(sp))
                        print("MRP: " + str(mrp))
                        print("Quantity: " + str(quantity))
                        print("Discount: " + str(discount))
                        print("Category: " + category)
                        print("Sub Category: " + subcategory)
                        print("Rating: " + str(rating))
                        print('-' * 60)
            else:
                stop = True
            if stop == True:
                break
            else:
                offset += 48
                
        result_dict = {'Title': self.titleX, 'Selling Price': self.spX, 'MRP': self.mrpX, 'Product Link': self.linkX, 
            'Quantity': self.quantityX, 'Discount': self.discountX, 'Rating': self.ratingX, 'Category': self.categoryX, 
            'RatingCount': self.rating_countX, 'ReviewCount': self.review_countX, 'Source': self.sourceX}

        return result_dict
