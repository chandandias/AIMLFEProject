import glob
import numpy as np
import os
import pandas as pd
import re
import string

def merge(category):
	path = os.getcwd()
	target = '*' + category + '.csv'
	merged_filename = os.path.join(path + '/' + category + '/' + 'merged_' + category + '_output.csv')
	all_files = glob.glob(os.path.join(path + '/' + category + '/', target))
	df_from_each_file = (pd.read_csv(f) for f in all_files)
	concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
	concatenated_df.to_csv(merged_filename, index=False, encoding='utf-8')

# To clean the numbers
def clean_numbers(number):
	number = str(number)
	final_number = re.findall('[0-9]+.[0-9]+', number)
	if len(final_number)>0 and ',' in str(final_number[0]):
		final_number = [int(final_number[0].replace(',', ''))]
	if len(final_number) == 0:
		final_number  = re.findall('[0-9]+', number)
		if len(final_number) == 0:
			final_number = '0'
	return final_number[0]

# To clean the text (Not Required)
def clean_text(text):
	word = str(text)
	text = "".join([letter for letter in word if letter not in string.punctuation])
	return text

def read_and_clean(category):
	path = os.getcwd()
	file_to_be_cleaned = os.path.join(path + '/' + category + '/' + 'merged_' + category + '_output.csv')
	filename = 'cleaned_' + category + '_data.csv'
	data = pd.read_csv(file_to_be_cleaned, delimiter = ',')
	data.columns = ['Title','SellingPrice','MRP','ProductLink','Quantity','Discount','Rating', 'Category', 'RatingCount','ReviewCount', 'Source']
	title = data['Title']
	product_link = data['ProductLink']
	sp = data['SellingPrice'].apply(lambda x: clean_numbers(x))
	mrp = data['MRP'].apply(lambda x: clean_numbers(x))
	discount = data['Discount'].apply(lambda x: clean_numbers(x))
	rating = data['Rating'].apply(lambda x: clean_numbers(x))
	rating_count = data['RatingCount'].apply(lambda x: clean_numbers(x))
	review_count = data['ReviewCount']
	category = data['Category']
	quantity = data['Quantity']
	source = data['Source']
	df = pd.DataFrame({'Title': title, 'SellingPrice': sp, 'MRP': mrp, 'ProductLink': product_link, 
		'Quantity': quantity, 'Discount': discount, 'Rating': rating, 'Category': category, 
		'RatingCount':rating_count, 'ReviewCount':review_count, 'Source':source})
	df.to_csv(filename, index=False, encoding='utf-8')
