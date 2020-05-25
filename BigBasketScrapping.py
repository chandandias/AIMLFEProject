import requests
import json
import pandas as pd


class BigBasketScrapping(object):
    def __init__(self):
        pass

    def pulses(self):
        base_url = 'https://www.bigbasket.com'
        page = 1
        stop = False
        PRODUCTS = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        param1 = "/custompage/getsearchdata/?slug=pulse&type=deck&page=1"
        param2 = '/product/get-products/?slug=pulse&page='
        param3 = '&tab_type=[%22all%22]&sorted_on=relevance&listtype=ps'

        titleX = []
        spX = []
        mrpX = []
        discountX = []
        linkX = []
        quantityX = []
        categoryX = []
        ratingX = []
        rating_countX = []
        review_countX = []

        while (True):
            if page == 1:
                url = base_url + param1
                response = requests.get(url, headers=headers)
                json_object = json.loads(response.text)
                items = json_object['json_data']['tab_info'][0]['product_info']['products']
            else:
                url = base_url + param2 + str(page) + param3
                response = requests.get(url, headers=headers)
                json_object = json.loads(response.text)
                items = json_object['tab_info']['product_map']['all']['prods']
            print(len(items))
            if len(items) > 0:
                for item in items:
                    product = {}
                    product['title'] = item['p_desc']
                    product['mrp'] = item['mrp']
                    product['sp'] = item['sp']
                    product['link'] = base_url + item['absolute_url']
                    product['quantity'] = item['w']
                    product['category'] = item['tlc_n']
                    product['rating'] = 0
                    product['rating_count'] = 0
                    product['review_count'] = 0
                    if 'avg_rating' in item['rating_info'].keys():
                        product['rating'] = item['rating_info']['avg_rating']
                        product['rating_count'] = item['rating_info']['rating_count']
                        product['review_count'] = item['rating_info']['review_count']
                    product['id'] = item['sku']
                    product['discount'] = int(product['mrp'].split('.')[0]) - int(product['sp'].split('.')[0])
                    print("Product ID: " + str(product['id']))
                    print("Title: " + product['title'])
                    titleX.append(product['title'])
                    print("Selling Price: " + product['sp'])
                    spX.append(product['sp'])
                    print("MRP: " + product['mrp'])
                    mrpX.append(product['mrp'])
                    print("Discount: " + str(product['discount']))
                    discountX.append(str(product['discount']))
                    print("Product Link: " + product['link'])
                    linkX.append(product['link'])
                    print("Quantity: " + product['quantity'])
                    quantityX.append(product['quantity'])
                    print("Category: " + product['category'])
                    categoryX.append(product['category'])
                    print("Rating: " + str(product['rating']))
                    ratingX.append(str(product['rating']))
                    print("Rating Count: " + str(product['rating_count']))
                    rating_countX.append(str(product['rating_count']))
                    print("Review Count: " + str(product['review_count']))
                    review_countX.append(str(product['review_count']))
                    print('-' * 60)
                    if product['link'] not in PRODUCTS:
                        PRODUCTS[product.get('link', '')] = product
                    else:
                        print("Already exists")
            else:
                stop = True
            if stop == True:
                break
            else:
                page += 1

            df = pd.DataFrame(
                {'Title': titleX, 'Selling Price': spX, 'MRP': mrpX, 'Product Link': linkX, 'Quantity': quantityX,
                 'Discount': discountX, 'Rating': ratingX, 'Category': categoryX, 'Rating Count': rating_countX,
                 'Review Count': review_countX})
            output_csv = "C:\\Users\\cdiasx\\Desktop\\BITS\\FeatureEngineering\\assignment-2\\BigbasketPulses.csv"
            df.to_csv(output_csv, index=False, encoding='utf-8')

