# test/test_load.py

import unittest
from tabeloader.load import load_restaurants, load_restaurant_details

class TestLoad(unittest.TestCase):
    def test_load_restaurants(self):
        url = 'https://award.tabelog.com/hyakumeiten/okonomiyaki'
        restaurants = load_restaurants(url)
        self.assertEqual(len(restaurants), 100)

    def test_load_restaurants_non_exist_url(self):
        url = 'https://award.tabelog.com/hyakumeiten/hirosimayaki'
        with self.assertRaises(ValueError):
            load_restaurants(url)

    def test_load_restaurant_details(self):
        url = 'https://award.tabelog.com/restaurant/12345'
        details = load_restaurant_details(url)
        self.assertIsNotNone(details)

if __name__ == '__main__':
    unittest.main()