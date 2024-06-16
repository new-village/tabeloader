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
        url = 'https://tabelog.com/kagoshima/A4601/A460105/46000828/'
        details = load_restaurant_details(url)
        details[0].pop('update')
        expect = {
                "name": "高城庵",
                "url": "https://tabelog.com/kagoshima/A4601/A460105/46000828/",
                "rate": "3.66",
                "bookmark": "5496",
                "comment": "152",
                "address": "鹿児島県 南九州市 知覧町郡 6329",
                "latitude": "31.37949403848039",
                "longitude": "130.44756924746517",
                "award": "定食 百名店 2021"
        }
        self.assertDictEqual(details[0], expect)

    def test_load_restaurant_details_non_exist_url(self):
        url = 'https://tabelog.com/tokyo/A1234/A123456/12345678/'
        with self.assertRaises(ValueError):
            load_restaurant_details(url)
    
    def test_bulkload_restaurant_details(self):
        url1 = 'https://tabelog.com/tokyo/A1311/A131102/13007981/'
        url2 = 'https://tabelog.com/tokyo/A1311/A131102/13003755/'
        restaurants = [{'name': '吾妻橋', 'url': url1},{'name': '佐久良', 'url': url2}]
        details = load_restaurant_details(restaurants)
        details[0].pop('update')
        expect = {
                "name": "吾妻橋 やぶそば",
                "url": "https://tabelog.com/tokyo/A1311/A131102/13007981/",
                "rate": "3.72",
                "bookmark": "43671",
                "comment": "608",
                "address": "東京都 墨田区 吾妻橋 1-11-2",
                "latitude": "35.70803783870925",
                "longitude": "139.79864458463263",
                "award": "そば 百名店 2024"
        }
        self.assertDictEqual(details[0], expect)
        self.assertEqual(len(details), 2)

if __name__ == '__main__':
    unittest.main()