from bs4 import BeautifulSoup
import requests

base_url = 'https://www.amazon.in'
param = '/s?k=pulses&qid=1590299046&ref=sr_pg_1&page='
page = 1
stop = False
total_items = 0
last_page = 0
PRODUCTS = {}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
while(True):
	url = base_url + param + str(page)
	response = requests.get(url, headers=headers, verify=False)
	if response.status_code != 200:
		break
	soup = BeautifulSoup(response.text, 'lxml')
	lis = soup.find_all('li', {'class':'a-disabled'})
	if page == 1:
		last_page = int(lis[len(lis)-1].text)
	items = soup.find_all('div', {'data-component-type':'s-search-result'})
	print(len(items))
	if (len(items) > 0):
		for item in items:
			product = {}
			anchor = item.find('a')
			product['title'] = item.find('h2').text.strip()
			product['link'] = base_url + anchor['href']
			details = item.find('div', {'class':'a-section a-spacing-none a-spacing-top-micro'})
			try:
				item_detail = details.find_all('a')
				product['star'] = item_detail[0].text
			except:
				product['star'] = "No Stars"
			try:
				product['offer_price'] = int(item.find('span', {'data-a-color':'price'}).text.split('â‚¹')[1])
			except:
				product['offer_price'] = 0
			try:
				product['old_price'] = int(soup.find('span', {'data-a-color':'secondary'}).text.split('â‚¹')[1])
			except:
				product['old_price'] = 0
			total_items += 1
			if product['link'] not in PRODUCTS:
				PRODUCTS[product.get('link', '')] = product
			print(product['title'])
			print(product['link'])
			print(product['star'])
			print(product['offer_price'])
			print(product['old_price'])
			print('-' * 60)
	else:
		stop = True
	if stop == True:
		break
	else:
		if page <= last_page:
			page += 1
		else:
			break
