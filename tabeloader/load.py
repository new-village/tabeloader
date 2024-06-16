import requests
import re
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
    return 'load_restaurants'

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

# url = 'https://award.tabelog.com'

# def load():
#     # Retrieve the category page
#     page = get_page(url + '/hyakumeiten')
#     category_list = create_category_list(page)
#     # Retrieve restaurant name and URL for each category
#     restaurant_list = create_restaurant_list(category_list)

#     # for category in category_list:
#     #     page = get_page(category['url'])
#     #     category['restaurants'] = create_restaurant_list(page)
#     return category_list

# def create_restaurant_list(category_list) -> list:
#     """
#     Retrieves the list of restaurants from the category page and returns it as a list of dictionaries.

#     Parameters:
#         category_list (list): A list of dictionaries containing the category name and URL.

#     Returns:
#         list: A list of dictionaries containing the restaurant name and URL.
#     """
#     restaurant_list = []
#     for category in category_list:
#         page = get_page(category['url'])
#         restaurant_items = page.select('ul.hyakumeiten-list__list li.hyakumeiten-list__item')
#         for item in restaurant_items:
#             restaurant_list.append({'category': category['category'], 'restaurant': item.select_one('a').text.strip(), 'url': url + item.select_one('a').get('href')})
#     return restaurant_list


# def create_category_list(page) -> list:
#     """
#     Retrieves the list of categories from the category page and returns it as a list of dictionaries.

#     Returns:
#         list: A list of dictionaries containing the category name and URL.
#     """
#     category_list = []
#     hyakumeiten_items = page.select('ul.hyakumeiten-nav__list li.hyakumeiten-nav__item')
#     for item in hyakumeiten_items:
#         title = item.select_one('p').text.strip()
#         for link in item.select('a'):
#             category_name = title + ' ' + link.text.strip() if title != link.text.strip() else title
#             category_list.append({'category': category_name, 'url': url + link.get('href')})
#     return category_list

# Usage
if __name__ == '__main__':
    print(load_restaurants('https://award.tabelog.com/hyakumeiten/okonomiyaki'))