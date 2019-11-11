# weather API

# Import libraries
import requests
import json
import pymongo

#url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=bd64898a234d3ac401ec97cfd4ba3f2d'
city = 'Budapest'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=bd64898a234d3ac401ec97cfd4ba3f2d'.format(city)

res = requests.get(url)
temp = json.loads(res.content)

print(temp)
