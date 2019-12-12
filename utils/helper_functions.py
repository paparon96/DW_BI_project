# Import libraries
import requests
import json
import pymongo

def get_data_pollution(city,token):
    url= "https://api.waqi.info/feed/{0}/?token={1}".format(city,token)
    res = requests.get(url)
    temp = json.loads(res.content)

    return temp


def get_data_weather(city,token):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(city,token)

    res = requests.get(url)
    temp = json.loads(res.content)

    return temp

def get_data_traffic(app_id,app_code,latitude1,longitude1,latitude2,longitude2):

    url='https://traffic.api.here.com/traffic/6.3/incidents.json?app_id={}&app_code={} \
    &bbox={},{};{},{} \
    &criticality=minor'.format(app_id,app_code,latitude1,longitude1,latitude2,longitude2)

    response = requests.get(url)
    temp = json.loads(response.content)

    return temp

def mongo_insertion(temp, collection):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["air"]
    city = mydb[collection]

    x = city.insert_one(temp)
