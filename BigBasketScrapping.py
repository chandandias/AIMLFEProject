import requests
import json


class BigBasketScrapping(object):

    def __init__(self):
        self.titleX = []
        self.spX = []
        self.mrpX = []
        self.discountX = []
        self.linkX = []
        self.quantityX = []
        self.categoryX = []
        self.ratingX = []
        self.rating_countX = []
        self.review_countX = []
        self.sourceX = []

    def pulses(self, category):
        base_url = 'https://www.bigbasket.com'
        page = 1
        stop = False
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        param1 = "/custompage/getsearchdata/?slug="
        param2 = "&type=deck&page=1"
        param3 = '/product/get-products/?slug='
        param4 = '&page='
        param5 = '&tab_type=[%22all%22]&sorted_on=relevance&listtype=ps'

        while (True):
            if page == 1:
                url = base_url + param1 + category + param2
                response = requests.get(url, headers=headers)
                json_object = json.loads(response.text)
                items = json_object['json_data']['tab_info'][0]['product_info']['products']
            else:
                url = base_url + param3 + category + param4 + str(page) + param5
                response = requests.get(url, headers=headers)
                json_object = json.loads(response.text)
                items = json_object['tab_info']['product_map']['all']['prods']
            print(len(items))
            if len(items) > 0:
                for item in items:
                    title = item['p_desc']
                    mrp = item['mrp']
                    sp = item['sp']
                    link = base_url + item['absolute_url']
                    quantity = item['w']
                    category = item['tlc_n']
                    rating = 0
                    rating_count = 0
                    review_count = 0
                    if str(item['rating_info']) != 'None':
                        if 'rating_info' in item:
                            if 'avg_rating' in item['rating_info']:
                                rating = item['rating_info']['avg_rating']
                                rating_count = item['rating_info']['rating_count']
                                review_count = item['rating_info']['review_count']
                    else:
                        rating = '0'
                        rating_count = '0'
                        review_count = '0'
                    _id = item['sku']
                    source = 'BigBasket'
                    if float(sp.split('.')[0]) != 0.0:
                        discount = round(((int(mrp.split('.')[0]) - int(sp.split('.')[0]))/int(sp.split('.')[0]))*100, 2)
                    else:
                        discount = 0.0
                    if not (str(sp) == '0' or str(mrp) == '0'):
                        self.titleX.append(title)
                        self.spX.append(sp)
                        self.mrpX.append(mrp)
                        self.discountX.append(str(discount))
                        self.linkX.append(link)
                        self.quantityX.append(quantity)
                        self.categoryX.append(category)
                        self.ratingX.append(str(rating))
                        self.rating_countX.append(str(rating_count))
                        self.review_countX.append(str(review_count))
                        self.sourceX.append(source)
                        print("Title: " + title)
                        print("Selling Price: " + sp)
                        print("MRP: " + mrp)
                        print("Discount: " + str(discount))
                        print("Product Link: " + link)
                        print("Quantity: " + quantity)
                        print("Category: " + category)
                        print("Rating: " + str(rating))
                        print("Rating Count: " + str(rating_count))
                        print("Review Count: " + str(review_count))
                        print('-' * 60)
            else:
                stop = True
            if stop == True:
                break
            else:
                page += 1

        result_dict = {'Title': self.titleX, 'Selling Price': self.spX, 'MRP': self.mrpX, 'Product Link': self.linkX, 
                    'Quantity': self.quantityX, 'Discount': self.discountX, 'Rating': self.ratingX, 'Category': self.categoryX, 
                    'RatingCount': self.rating_countX, 'ReviewCount': self.review_countX, 'Source': self.sourceX}
        return result_dict
