from AmazonScrapping import AmazonScrapping
from BigBasketScrapping import BigBasketScrapping
from GrofersScrapping import GrofersScrapping
import pandas as pd
import os
from merge_csv import merge, read_and_clean

class Main(object):
    def __init__(self):
        self._amazonscrapping = AmazonScrapping()
        self._grofersscrapping = GrofersScrapping()
        self._bisbasketscrapping = BigBasketScrapping()

    def create_csv(self, dict, filename):
        df = pd.DataFrame(dict)
        output_csv = filename + ".csv"
        df.to_csv(output_csv, index=False, encoding='utf-8')

    def get_data(self, category):
        path = os.getcwd()
        self.OUT = os.path.abspath(os.path.join(path + '/' + category))
        if (not os.path.exists(self.OUT)):
            os.mkdir(self.OUT)
        grofers = self._grofersscrapping.pulses(category)
        self.create_csv(grofers, self.OUT + '/Grofers_' + category)
        big_basket = self._bisbasketscrapping.pulses(category)
        self.create_csv(big_basket, self.OUT +  '/BigBasket_' + category)
        amazon = self._amazonscrapping.pulses(category)
        self.create_csv(amazon, self.OUT +  '/Amazon_' + category)
        merge(category)

        
if __name__ == "__main__":
    categories = ['nestle', 'pulses', 'chocolates']
    #categories = ['chocolates']
    [(lambda category:  Main().get_data(category)) (category) for category in categories]
    [(lambda category:  read_and_clean(category)) (category) for category in categories]
    

