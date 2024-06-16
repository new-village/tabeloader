import datetime
import re
import requests
from bs4 import BeautifulSoup

def load_restaurants(url) -> list:
    """
    Loads a list of restaurants from the given URL.

    Args:
        url (str): The URL of the website to load the restaurants from.

    Returns:
        list: A list of restaurants extracted from the webpage.

    Raises:
        ValueError: If the URL format is invalid.
    """
    page = _download_page(url)
    return _create_restaurants_list(page)

def load_restaurant_details(url) -> list:
    page = _download_page(url)
    extractor = RestaurantDetailsExtractor(page, url)
    return extractor.create_restaurant_details()

def _download_page(url) -> BeautifulSoup:
    """
    Downloads the HTML content of a web page and returns it as a BeautifulSoup object.

    Args:
        url (str): The URL of the web page to download.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML content of the web page.

    Raises:
        ValueError: If there is an error while retrieving the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.exceptions.RequestException as e:
        raise ValueError(f'Error: Failed to retrieve the page. {str(e)}')
    return BeautifulSoup(response.text, 'html.parser')

def _create_restaurants_list(soup) -> list:
    """
    Create a list of restaurants from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a restaurant.
              Each dictionary contains the following keys: 'name', 'url', and 'category'.
    """
    category = _remove_tabelog(soup.select_one('title').text.strip())
    restaurants = []
    for item in soup.select('div.hyakumeiten-shop__list a.hyakumeiten-shop__target'):
        restaurants.append({'name': item.select_one('div.hyakumeiten-shop__name').text.strip(), 'url': item.get('href'), 'category': category})
    return restaurants

def _remove_tabelog(text: str) -> str:
    return re.sub(r'\[?食べログ\]?', '', text).strip()

class RestaurantDetailsExtractor:
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.details = {}

    def _extract_award(self):
        badge = self.soup.select_one('div.rstinfo-table-badge-award')
        if badge:
            category = badge.select_one('span i').text.strip()
            return category.replace(" 選出店", "")
        else:
            return ''

    def _extract_address(self):
        address = self.soup.select_one('p.rstinfo-table__address').get_text(separator=" ", strip=True)
        latlong = self.soup.select_one('img.rstinfo-table__map-image').get('data-original')
        match = re.search(r'center=([-\d.]+),([-\d.]+)&', latlong)
        latitude = match.group(1) if match else 0
        longitude = match.group(2) if match else 0
        return address, latitude, longitude

    def create_restaurant_details(self):
        self.details['name'] = self.soup.select_one('h2.display-name').text.strip()
        self.details['url'] = self.url
        self.details['rate'] = self.soup.select_one('span.rdheader-rating__score-val-dtl').text.strip()
        self.details['bookmark'] = self.soup.select_one('span.rdheader-rating__hozon-target em.num').text.strip()
        self.details['comment'] = self.soup.select_one('span.rdheader-rating__review-target em.num').text.strip()
        self.details['update'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.details['address'], self.details['latitude'], self.details['longitude'] = self._extract_address()
        self.details['award'] = self._extract_award()
        return [self.details]

if __name__ == '__main__':
    # url = 'https://tabelog.com/kagoshima/A4601/A460105/46005607/'
    url = 'https://tabelog.com/kagoshima/A4601/A460105/46000828/'    
    details = load_restaurant_details(url)
    print(details)