import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pandas as pd


class GrofersScrapping(object):

        def init(self):
                pass

        def pulses(self):
        
                # headers = {
                #     "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
                base_url = 'https://grofers.com'
                param = '/v5/search/merchants/26012/products/?lat=12.9894395055235&lon=77.7348850599167&q=pulses&suggestion_type=0&t=1&size=48&start='
                offset = 0
                total_items = 0
                stop = False
                headers = {
                    'auth_key': 'd1cc0621fb608b29a85d6f243e32ef15aa7afe93012e39a9317e3ff1ecbc2846',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
                }

                url = base_url + param + str(offset)
                response = requests.get(url, headers=headers)
                json_object = json.loads(response.text)
                products = json_object['products']
                print(len(products))
                titleX = []
                spX = []
                mrpX = []
                quantityX = []
                linkX = []
                discountX = []
                ratingX = []

                if len(products) > 0:
                    for prod in products:
                        title = prod['name']
                        mrp = prod['mrp']
                        sp = prod['price']
                        prid = prod['product_id']
                        link = base_url + '/prn/' + title.lower().replace("'", "").replace('/', '').replace(' ', '-') + '/prid/' + str(
                            prid)
                        quantity = prod['unit']
                        discount = prod['disc_amt']
                        category = prod['categories'][0]['name']
                        subcategory = prod['subcategories'][len(prod['subcategories']) - 1]['name']
                        rating = prod['rating']
                        print("Product ID: " + str(prid))
                        print("Title: " + title)
                        titleX.append(title)
                        print("Selling Price: " + str(sp))
                        spX.append(str(sp))
                        print("MRP: " + str(mrp))
                        mrpX.append(str(mrp))
                        print("Product Link: " + link)
                        linkX.append(link)
                        print("Quantity: " + str(quantity))
                        quantityX.append(str(quantity))
                        print("Discount: " + str(discount))
                        discountX.append(str(discount))
                        print("Category: " + category)
                        print("Sub Category: " + subcategory)
                        print("Rating: " + str(rating))
                        ratingX.append(str(rating))
                        print('-' * 60)


                df = pd.DataFrame({'Title': titleX, 'Selling Price': spX, 'MRP': mrpX, 'Product Link': linkX, 'Quantity': quantityX, 'Discount': discountX, 'Rating': ratingX})
                output_csv = "C:\\Users\\cdiasx\\Desktop\\BITS\\FeatureEngineering\\assignment-2\\GrofersPulses.csv"
                df.to_csv(output_csv, index=False, encoding='utf-8')



