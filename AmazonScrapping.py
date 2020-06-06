from bs4 import BeautifulSoup
import requests

class AmazonScrapping(object):

    def __init__(self):
        self.titleX = []
        self.linkX = []
        self.ratingX = []
        self.spX = []
        self.mrpX = []
        self.discountX = []
        self.rating_countX = []
        self.quantityX = []
        self.review_countX = []
        self.categoryX = []
        self.sourceX = []

    def pulses(self, category):
        base_url = 'https://www.amazon.in'
        param = '/s?k='
        param1 = '&qid=1590299046&ref=sr_pg_1&page='
        page = 1
        stop = False
        total_items = 0
        last_page = 0

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        while (True):
            url = base_url + param + category + param1 + str(page)
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
                for item in items[:21]:
                    intermidiate = item.find('span', {'data-component-type': 's-product-image'})
                    anchor = intermidiate.find('a')
                    title = item.find('h2').text.strip()
                    details = item.find('div', {'class': 'a-section a-spacing-none a-spacing-top-micro'})
                    try:
                        item_detail = details.find_all('a')
                        star = item_detail[0].text
                    except:
                        star = "No Stars"

                    link = base_url + anchor['href']
                    item_resp = requests.get(link, headers=headers)
                    item_soup = BeautifulSoup(item_resp.text, 'lxml')
                    try:
                        table = item_soup.find('table', {'class': "a-lineitem"})
                        try:
                            offer_price = table.find('span', {'id': 'priceblock_ourprice'}).text.strip()
                            # print(offer_price)
                        except:
                            try:
                                offer_price = table.find('span', {'id': 'priceblock_saleprice'}).text.strip()
                            except:
                                offer_price = '0'
                        try:
                            old_price = table.find('span', {
                                'class': 'priceBlockStrikePriceString a-text-strike'}).text.strip()
                        except:
                            old_price = '0'
                        # try:
                        #     save = table.find('td', {
                        #         'class': 'a-span12 a-color-price a-size-base priceBlockSavingsString'}).text.strip()
                        # except:
                        #     save = '0'
                    except:
                        print("No Price details")
                    # save = '0'
                  #  print(old_price)
                    mrp = float(old_price.replace('₹ ', ''))
                    sp = float(offer_price.replace('₹ ', ''))
                  #  print(mrp)
                  #  print(sp)
                    try:
                        save = round(((mrp - sp)/mrp)*100, 2)
                    except:
                        save = 0
                   # print(save)
                    try:
                        reviews = item_soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()
                    except:
                        reviews = 'No Reviews'
                    try:
                        quant = item_soup.find('div', {'id': "variation_size_name"})
                        quantity = quant.find_all('span')[0].text.strip()
                    except:
                        try:
                            quant_list = title.lower().split(' ')
                            quant = quant_list[len(quant_list) - 1]
                            if quant[len(quant) - 1] == 'g':
                                quantity = quant
                            else:
                                quantity = "No Quantity"
                        except:
                            quantity = "No Quantity"
                    total_items += 1
                    if not (offer_price == '0' or old_price == '0'):
                        self.titleX.append(title)
                        self.linkX.append(link)
                        self.ratingX.append(star)
                        self.spX.append(offer_price)
                        self.mrpX.append(old_price)
                        self.discountX.append(save)
                        self.rating_countX.append(reviews)
                        self.quantityX.append(quantity)
                        self.categoryX.append('None')
                        self.review_countX.append('0')
                        self.sourceX.append("Amazon")
                        print("Title: " + title)
                        print("Product Link: " + link)
                        print("Rating: " + star)
                        print("Selling Price: " + offer_price)
                        print("Actual Price: " + old_price)
                        print("Discount: " + str(save))
                        print("Rating Count: " + reviews)
                        print("Quantity: " + quantity)
                        print('-' * 60)
            else:
                stop = True
            if stop == True:
                break
            else:
                if page < int(2):
                    page += 1;break
                else:
                    break

        result_dict = {'Title': self.titleX, 'Selling Price': self.spX, 'MRP': self.mrpX, 'Product Link': self.linkX, 
                    'Quantity': self.quantityX, 'Discount': self.discountX, 'Rating': self.ratingX, 'Category': self.categoryX, 
                    'RatingCount': self.rating_countX, 'ReviewCount': self.review_countX, 'Source': self.sourceX}
        return result_dict
