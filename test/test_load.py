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
        url = 'https://tabelog.com/tokyo/A1307/A130703/13229559/'
        details = load_restaurant_details(url)
        del details[0]['update'], details[0]['rate'], details[0]['bookmark'],details[0]['comment']
        expect = {
                "name": "4000 Chinese Restaurant",
                "url": "https://tabelog.com/tokyo/A1307/A130703/13229559/",
                "address": "東京都 港区 南青山 7-10-10 パークアクシス南青山7丁目 1F",
                "latitude": 35.65886103871501,
                "longitude": 139.71868198419196,
                "award": "2024年Bronze受賞店, 2023年Bronze受賞店, 2022年Bronze受賞店, 2021年Bronze受賞店, 2020年Bronze受賞店, 中国料理 百名店 2024, 中国料理 百名店 2023, 中国料理 百名店 2021",
                "booking": True,
                "online_booking": False,
                "lunch_budget": '￥15,000～￥19,999',
                "dinner_budget": '￥30,000～￥39,999' 
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
                "latitude": 35.68811063869665,
                "longitude": 139.71932188448693,
                "award": "居酒屋 百名店 2022",
                "booking": True,
                "online_booking": True,
                "lunch_budget": '-',
                "dinner_budget": '￥8,000～￥9,999'
        }
        self.assertDictEqual(details[0], expect)

    def test_none_is_available_booking(self):
        # Test that booking and online_booking are both False if the booking field is none.
        url = 'https://tabelog.com/okayama/A3305/A330501/33000402/'
        details = load_restaurant_details(url)
        self.assertFalse(details[0]['booking'])
        self.assertFalse(details[0]['online_booking'])

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
                "latitude": 35.70803783870925,
                "longitude": 139.79864458463263,
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