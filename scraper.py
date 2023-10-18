# Extract the 12 cheapest beers from Bavaria from "www.biermarket.de" and save them in a csv file.
import csv
import heapq
import time
from abc import ABC, abstractmethod
from time import sleep

import requests
from bs4 import BeautifulSoup


class WebScraper:
    '''
      Extracting data using beautifulsoup
        1. Get the last available page
        2. Fetches beer infomation for page
        3. updating next page number and product_names, values in dictionary

    '''

    def __init__(self, base_url, state):
        self.base_url = base_url
        self.url = f"{self.base_url}/bier/deutsches-bier"
        self.state = state
        self.current_page = 1
        self.last_page = self._get_last_page()
        self.lowest_values = {}

    def _get_last_page(self):
        req = requests.get(f'{self.url}/{self.state}/')
        soup = BeautifulSoup(req.content, 'html.parser')
        last_page_item = soup.find('li', {'class': 'page-item page-last'})
        last_page_num = int(last_page_item.find(
            'input', {'id': 'p-last'})['value'])
        return last_page_num

    def get_product_detail(self, product_name):
        product_name = product_name.lower().replace(
            ' ', '-').replace('ö', 'oe').replace('ä', 'ae').replace('ü', 'ue')
        req = requests.get(f"{self.base_url}/{product_name}")
        print(f"{self.base_url}/{product_name}")
        soup = BeautifulSoup(req.content, 'html.parser')
        product_price = soup.find('meta', {'itemprop': 'price'})
        detail_product_unit = soup.find(
            'div', class_='product-detail-price-unit')
        detail_product_quantity = detail_product_unit.find(
            'span', {'class': 'price-unit-content'}).text.strip().replace(' Liter', '')
        quantity_value = float(
            product_price['content'])/float(detail_product_quantity)
        return quantity_value

    def fetch_next(self):
        if self.current_page <= self.last_page:
            page_url = f"{self.url}/{self.state}/?order=lagerbestand&p={self.current_page}"
            request_data = requests.get(page_url)
            soup_data = BeautifulSoup(request_data.content, 'html.parser')
            products = soup_data.find_all('div', class_='product-info')
            for product in products:
                try:
                    product_name = product.find(
                        'a', {'class': 'product-name'}).text.strip()
                    price_unit_ref = product.find(
                        'span', {'class': 'price-unit-reference'}).text.strip().split()[0]
                    val = price_unit_ref.replace('(', '').replace(",", ".")
                    self.lowest_values[product_name] = float(val)
                    if product_name == 'Kuchlbauer Alkoholfreie Weisse':
                        print(self.current_page)
                except AttributeError:
                    val = self.get_product_detail(product_name)
                    self.lowest_values[product_name] = val
            self.current_page += 1


if __name__ == '__main__':
    g_url = 'https://www.biermarket.de'
    state = 'bayern'.replace('ö', 'oe').replace('ä', 'ae').replace('ü', 'ue')
    try:
        scraper = WebScraper(g_url, state)
        while scraper.current_page <= scraper.last_page:
            scraper.fetch_next()
            time.sleep(2)
        cheapest_12 = heapq.nsmallest(
            12, scraper.lowest_values.items(), key=lambda x: x[1])

    except AttributeError:
        cheapest_12 = {}

    with open('cheapest_12_{}.csv'.format(state), 'w', newline='') as file:
        fields = ["Product_Name", "Price (Euro/L)"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for name, price in cheapest_12:
            writer.writerow({'Product_Name': name, 'Price (Euro/L)': price})
