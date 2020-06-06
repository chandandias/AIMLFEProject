import pandas as pd
import os

def compute_recommendations(category):
	path = os.getcwd()
	input_file = os.path.join(path + '/cleaned_' + category + '_data.csv')
	data = pd.read_csv(input_file, delimiter = ',')
	compute_result = data.sort_values(by=['Discount', 'Rating', 'RatingCount'], ascending=False)
	print(compute_result.head(5))
compute_recommendations('pulses')
