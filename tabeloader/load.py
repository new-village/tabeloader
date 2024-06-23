import datetime
import random
import re
import requests
import time
from bs4 import BeautifulSoup

def supported_categories() -> dict:
    """
    Returns a dictionary of supported categories and their URLs.

    Returns:
        dict: A dictionary containing the supported categories and their URLs.
    """
    page = _download_page('https://award.tabelog.com/hyakumeiten')
    return _create_category(page)

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

def load_restaurant_details(url_or_list) -> list:
    """
    Loads restaurant details from a given URL or a list of URLs.

    Args:
        url_or_list (str or list): The URL or list of URLs to load restaurant details from.

    Returns:
        list: A list of restaurant details extracted from the given URL(s).

    Raises:
        ValueError: If the input is not a string or a list.

    """
    if isinstance(url_or_list, str):
        page = _download_page(url_or_list)
        extractor = RestaurantDetailsExtractor(page, url_or_list)
    elif isinstance(url_or_list, list):
        extractor = BulkRestaurantDetailsExtractor(url_or_list)
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
    return BeautifulSoup(response.content.decode("utf-8", "ignore"), 'html.parser')

def _create_category(page) -> dict:
    """
    Retrieves the list of categories from the category page and returns it as a list of dictionaries.

    Returns:
        list: A list of dictionaries containing the category name and URL.
    """
    category = {}
    hyakumeiten_items = page.select('ul.hyakumeiten-nav__list li.hyakumeiten-nav__item')
    for item in hyakumeiten_items:
        title = item.select_one('p').text.strip()
        for link in item.select('a'):
            category_name = title + ' ' + link.text.strip() if title != link.text.strip() else title
            category['https://award.tabelog.com' + link.get('href')] = category_name
    del category['https://award.tabelog.com/hyakumeiten']
    return category

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
    """
    Removes the '[食べログ]' tag from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with the '[食べログ]' tag removed and stripped of leading/trailing whitespace.
    """
    return re.sub(r'\[?食べログ\]?', '', text).strip()

class RestaurantDetailsExtractor:
    """
    A class that extracts restaurant details from a given HTML soup and URL.

    Attributes:
        soup (BeautifulSoup): The HTML soup of the restaurant page.
        url (str): The URL of the restaurant page.
        details (dict): A dictionary to store the extracted restaurant details.

    Methods:
        _extract_award(): Extracts the award category of the restaurant.
        _extract_address(): Extracts the address, latitude, and longitude of the restaurant.
        create_restaurant_details(): Creates and returns a list containing the extracted restaurant details.
    """

    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.details = {}

    def _extract_award(self):
        """
        Extracts the award category of the restaurant.

        Returns:
            str: The award category of the restaurant.
        """
        badge = self.soup.select_one('td.rstinfo-badge')
        if badge:
            category = ', '.join([x.text.strip() for x in badge.select('span i')])
            return category.replace(" 選出店", "")
        else:
            return ''

    def _extract_address(self):
        """
        Extracts the address, latitude, and longitude of the restaurant.

        Returns:
            tuple: A tuple containing the address (str), latitude (str), and longitude (str) of the restaurant.
        """
        address = self.soup.select_one('p.rstinfo-table__address').get_text(separator=" ", strip=True)
        latlong = self.soup.select_one('img.rstinfo-table__map-image').get('data-original')
        match = re.search(r'center=([-\d.]+),([-\d.]+)&', latlong)
        latitude = match.group(1) if match else 0
        longitude = match.group(2) if match else 0
        return address, latitude, longitude

    def _is_available_booking(self):
        """
        Check if the restaurant is available for booking.

        Returns:
            bool: True if the restaurant is available for booking, False otherwise.
        """
        reserve_status = self.soup.select_one('p.rstinfo-table__reserve-status')
        if reserve_status and reserve_status.text.strip() == '予約可':
            return True
        else:
            return False

    def _is_available_online_booking(self):
        """
        Check if the restaurant is available for booking.

        Returns:
            bool: True if the restaurant is available for booking, False otherwise.
        """
        return bool(self.soup.select_one('div.rstdtl-side-yoyaku__booking'))

    def _extract_budget(self):
        """
        Extracts the lunch and dinner budget of the restaurant.

        Returns:
            tuple: A tuple containing the lunch budget (str) and dinner budget (str) of the restaurant.
        """
        lunch = self.soup.select_one('div.rdheader-budget i[aria-label="Lunch"]')
        lunch_budget = lunch.parent.a.text.strip() if lunch else ''
        dinner = self.soup.select_one('div.rdheader-budget i[aria-label="Dinner"]')
        dinner_budget = dinner.parent.a.text.strip() if dinner else ''
        return lunch_budget, dinner_budget

    def create_restaurant_details(self):
        """
        Creates and returns a list containing the extracted restaurant details.

        Returns:
            list: A list containing the extracted restaurant details.
        """
        self.details['name'] = self.soup.select_one('h2.display-name').text.strip()
        self.details['url'] = self.url
        self.details['rate'] = self.soup.select_one('span.rdheader-rating__score-val-dtl').text.strip()
        self.details['bookmark'] = self.soup.select_one('span.rdheader-rating__hozon-target em.num').text.strip()
        self.details['comment'] = self.soup.select_one('span.rdheader-rating__review-target em.num').text.strip()
        self.details['update'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.details['address'], self.details['latitude'], self.details['longitude'] = self._extract_address()
        self.details['award'] = self._extract_award()
        self.details['booking'] = self._is_available_booking()
        self.details['online_booking'] = self._is_available_online_booking()
        self.details['lunch_budget'], self.details['dinner_budget'] = self._extract_budget()
        return [self.details]

class BulkRestaurantDetailsExtractor(RestaurantDetailsExtractor):
    """
    A class for extracting details of multiple restaurants in bulk.

    Attributes:
        restaurants (list): A list of dictionaries representing the restaurants.
        details (list): A list to store the extracted restaurant details.
    """

    def __init__(self, restaurants):
        """
        Initializes a BulkRestaurantDetailsExtractor object.

        Args:
            restaurants (list): A list of dictionaries representing the restaurants.
        """
        self.restaurants = restaurants
        self.details = []

    def create_restaurant_details(self):
        """
        Creates restaurant details for each restaurant in the list.

        Returns:
            list: A list of dictionaries representing the restaurant details.
        """
        for resto in self.restaurants:
            # Randomly sleep for 1 to 3 seconds to avoid being blocked
            time.sleep(random.randint(1, 3))
            self.soup = _download_page(resto['url'])
            detail = {
                'name': self.soup.select_one('h2.display-name').text.strip(),
                'url': resto['url'],
                'rate': self.soup.select_one('span.rdheader-rating__score-val-dtl').text.strip(),
                'bookmark': self.soup.select_one('span.rdheader-rating__hozon-target em.num').text.strip(),
                'comment': self.soup.select_one('span.rdheader-rating__review-target em.num').text.strip(),
                'update': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'award': self._extract_award(),
                'booking': self._is_available_booking(),
                'online_booking': self._is_available_online_booking()
            }
            detail['address'], detail['latitude'], detail['longitude'] = self._extract_address()
            detail['lunch_budget'], detail['dinner_budget'] = self._extract_budget()
            self.details.append(detail)            
        return self.details
