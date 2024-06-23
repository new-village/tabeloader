# test/test_load.py

import unittest
from tabeloader.load import load_restaurants, load_restaurant_details, supported_categories

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
        url = 'https://tabelog.com/tokyo/A1301/A130101/13002616/'
        details = load_restaurant_details(url)
        del details[0]['update'], details[0]['rate'], details[0]['bookmark'],details[0]['comment']
        expect = {
                "name": "デリー 銀座店",
                "url": "https://tabelog.com/tokyo/A1301/A130101/13002616/",
                "address": "東京都 中央区 銀座 6-3-11 西銀座ビル 3F",
                "latitude": "35.67118233872062",
                "longitude": "139.76084268428684",
                "award": "アジア・エスニック 百名店 2023, アジア・エスニック 百名店 2022, カレー 百名店 2020, カレー 百名店 2019",
                "booking": True,
                "online_booking": False,
                "lunch_budget": '￥1,000～￥1,999',
                "dinner_budget": '￥2,000～￥2,999' 
        }
        self.assertDictEqual(details[0], expect)
    
    def test_load_restaurant_details_online_booking_available(self):
        url = 'https://tabelog.com/tokyo/A1309/A130903/13194182/'
        details = load_restaurant_details(url)
        del details[0]['update'], details[0]['rate'], details[0]['bookmark'],details[0]['comment']
        expect = {
                "name": "卯水酉",
                "url": "https://tabelog.com/tokyo/A1309/A130903/13194182/",
                "address": "東京都 新宿区 四谷 3-11-17 第二光明堂 B1F",
                "latitude": "35.68811063869665",
                "longitude": "139.71932188448693",
                "award": "居酒屋 百名店 2022",
                "booking": True,
                "online_booking": True,
                "lunch_budget": '-',
                "dinner_budget": '￥8,000～￥9,999'
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
        del details[0]['update'], details[0]['rate'], details[0]['bookmark'],details[0]['comment']
        expect = {
                "name": "吾妻橋 やぶそば",
                "url": "https://tabelog.com/tokyo/A1311/A131102/13007981/",
                "address": "東京都 墨田区 吾妻橋 1-11-2",
                "latitude": "35.70803783870925",
                "longitude": "139.79864458463263",
                "award": "そば 百名店 2024, そば 百名店 2022, そば 百名店 2021, そば 百名店 2019, そば 百名店 2018, そば 百名店 2017",
                "booking": False,
                "online_booking": False,
                "lunch_budget": '￥1,000～￥1,999',
                "dinner_budget": '￥2,000～￥2,999'
        }
        self.assertDictEqual(details[0], expect)
        self.assertEqual(len(details), 2)
    
    def test_supported_categories(self):
        categories = supported_categories()
        self.assertIsInstance(categories, dict)
        self.assertGreater(len(categories), 10)
        self.assertIn("https://award.tabelog.com/hyakumeiten/chinese_tokyo", categories)
        self.assertIn("https://award.tabelog.com/hyakumeiten/ramen_tokyo", categories)
        self.assertIn("https://award.tabelog.com/hyakumeiten/yakiniku_tokyo", categories)

if __name__ == '__main__':
    unittest.main()