# webscraping

# Bavarian Beer Price Web Scraper

This script extracts the 12 cheapest beers from Bavaria listed on "www.biermarket.de" and saves them in a CSV file.

## Overview

The `WebScraper` class, implemented in the script, uses the BeautifulSoup library to navigate through the website's pages, extract relevant beer data, and calculate the price per liter for each beer. The results are then sorted to identify the cheapest 12 beers based on price per liter, and this data is written to a CSV file.

## Dependencies

- Python 3.x
- requests
- BeautifulSoup4

You can install these packages using pip:

```bash
pip install requests beautifulsoup4
