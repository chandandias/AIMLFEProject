from bs4 import BeautifulSoup
import requests
import pandas as pd

class AmazonScrapping(object):

    def __init__(self):
        pass

    def pulses(self):
        base_url = 'https://www.amazon.in'
        param = '/s?k=pulses&qid=1590299046&ref=sr_pg_1&page='
        page = 1
        stop = False
        total_items = 0
        last_page = 0
        PRODUCTS = {}
        titleX = []
        linkX = []
        ratingsX = []
        offer_pricesX = []
        old_pricesX = []
        discountX = []
        ratingcountX = []
        quantityX = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        while (True):
            url = base_url + param + str(page)
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                break
            soup = BeautifulSoup(response.text, 'lxml')
            lis = soup.find_all('li', {'class': 'a-disabled'})
            if page == 1:
                last_page = int(lis[len(lis) - 1].text)
            items = soup.find_all('div', {'data-component-type': 's-search-result'})
            print(len(items))
            if (len(items) > 0):
                for item in items:
                    product = {}
                    intermidiate = item.find('span', {'data-component-type': 's-product-image'})
                    anchor = intermidiate.find('a')
                    product['title'] = item.find('h2').text.strip()
                    details = item.find('div', {'class': 'a-section a-spacing-none a-spacing-top-micro'})
                    try:
                        item_detail = details.find_all('a')
                        product['star'] = item_detail[0].text
                    except:
                        product['star'] = "No Stars"

                    product['link'] = base_url + anchor['href']
                    item_resp = requests.get(product['link'], headers=headers)
                    item_soup = BeautifulSoup(item_resp.text, 'lxml')
                    try:
                        table = item_soup.find('table', {'class': "a-lineitem"})
                        try:
                            product['offer_price'] = table.find('span', {'id': 'priceblock_ourprice'}).text.strip()
                        except:
                            try:
                                product['offer_price'] = table.find('span', {'id': 'priceblock_saleprice'}).text.strip()
                            except:
                                product['offer_price'] = '0'
                        try:
                            product['old_price'] = table.find('span', {
                                'class': 'priceBlockStrikePriceString a-text-strike'}).text.strip()
                        except:
                            product['old_price'] = '0'
                        try:
                            product['save'] = table.find('td', {
                                'class': 'a-span12 a-color-price a-size-base priceBlockSavingsString'}).text.strip()
                        except:
                            product['save'] = '0'
                    except:
                        print("No Price details")
                    try:
                        product['reviews'] = item_soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()
                    except:
                        product['reviews'] = 'No Reviews'
                    try:
                        quant = item_soup.find('div', {'id': "variation_size_name"})
                        product['quantity'] = quant.find_all('span')[0].text.strip()
                    except:
                        try:
                            quant_list = product['title'].lower().split(' ')
                            quant = quant_list[len(quant_list) - 1]
                            if quant[len(quant) - 1] == 'g':
                                product['quantity'] = quant
                            else:
                                product['quantity'] = "No Quantity"
                        except:
                            product['quantity'] = "No Quantity"
                    total_items += 1
                    if product['link'] not in PRODUCTS:
                        PRODUCTS[product.get('link', '')] = product
                    print("Title: " + product['title'])
                    titleX.append(product['title'])
                    print("Product Link: " + product['link'])
                    linkX.append(product['link'])
                    print("Rating: " + product['star'])
                    ratingsX.append(product['star'])
                    print("Selling Price: " + product['offer_price'])
                    offer_pricesX.append(product['offer_price'])
                    print("Actual Price: " + product['old_price'])
                    old_pricesX.append(product['old_price'])
                    print("Discount: " + product['save'])
                    discountX.append(product['save'])
                    print("Rating Count: " + product['reviews'])
                    ratingcountX.append(product['reviews'])
                    print("Quantity: " + product['quantity'])
                    quantityX.append(product['quantity'])
                    print('-' * 60)
            else:
                stop = True
            if stop == True:
                break
            else:
                if page < 2:
                    page += 1
                else:
                    break

        df = pd.DataFrame(
            {'Title': titleX, 'Selling Price': offer_pricesX, 'MRP': old_pricesX, 'Product Link': linkX, 'Quantity': quantityX,
             'Discount': discountX, 'Rating': ratingsX, 'Rating count': ratingcountX})
        output_csv = "C:\\Users\\cdiasx\\Desktop\\BITS\\FeatureEngineering\\assignment-2\\AmazonPulses.csv"
        df.to_csv(output_csv, index=False, encoding='utf-8')
