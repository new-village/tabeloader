# tabeloader
**tabeloader** is a Python library to retrieve information on Top 100 restaurants from a [Tabelog](https://tabelog.com/en/).

## Installation  
----------------------
tabeloader is available on pip installation.
```shell
$ python -m pip install tabeloader
```
  
### GitHub Install
Installing the latest version from GitHub:  
```shell
$ git clone https://github.com/new-village/tabeloader
$ cd tabeloader
$ python setup.py install
```
    
## Usage
This section describes how to use this library.  
  
### Get top 100 restaurants list
Copy the URL of the category for which you want to create a listing from the [Hyakumeiten](https://award.tabelog.com/hyakumeiten) website. The `load_restaurants` function can be executed with a URL as argument to obtain the URLs and names of the top 100 restaurants in list of dict format.
```python
>>> import tabeloader
>>> restaurants = tabeloader.load_restaurants('https://award.tabelog.com/hyakumeiten/okonomiyaki')
>>> print(restaurants)
[{'name': 'お好み焼き屋', 'url': 'https://tabelog.com/tokyo/X1234/X123456/12345678/', 'category': 'お好み焼き 百名店 2024'}, ...]
```

### Get restaurants detail list from `load_restaurants` result
The `load_restaurant_details` function can be executed with a URL as argument to obtain the URL, name, address, award etc from restaurant in list of dict format that is made by `load_restaurants`.
```python
>>> import tabeloader
>>> details = tabeloader.load_restaurant_details(restaurants)
>>> print(details)
[{"name": "お店", "url": "https://tabelog.com/tokyo/X1234/X123456/12345678/", "rate": "2.14", "bookmark": "12",  "comment": "4", "address": "東京都 千代田区 12", "latitude": "31.37949403848039", "longitude": "130.44756924746517", "award": "定食 百名店 2021"}, ...]
```

### Get restaurant detail list
The `load_restaurant_details` function supports string argument that is a specific restaurant URL of the [Tabelog](https://tabelog.com/en/) website. The function also can be executed with a URL as argument to obtain the URL, name, address, award etc.
```python
>>> import tabeloader
>>> restaurants = tabeloader.load_restaurant_details('https://tabelog.com/tokyo/X1234/X123456/12345678/')
>>> print(restaurants)
[{"name": "お店", "url": "https://tabelog.com/tokyo/X1234/X123456/12345678/", "rate": "2.14", "bookmark": "12",  "comment": "4", "address": "東京都 千代田区 12", "latitude": "31.37949403848039", "longitude": "130.44756924746517", "award": "定食 百名店 2021"}]
```

## Disclaimer
This library was created for learning Python libraries. The developer accepts no responsibility for any consequences resulting from the use of this library.  
