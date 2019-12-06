# Import libraries
import requests
import json
import pymongo

def get_data_pollution(city,token):
    url= "https://api.waqi.info/feed/{0}/?token={1}".format(city,token)
    res = requests.get(url)
    temp = json.loads(res.content)

    return temp


def get_data_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=bd64898a234d3ac401ec97cfd4ba3f2d'.format(city)

    res = requests.get(url)
    temp = json.loads(res.content)

    return temp

def get_data_traffic(latitude1,longitude1,latitude2,longitude2):

    url='https://traffic.api.here.com/traffic/6.3/incidents.json?app_id=u7vId3aGe6N0GmKuvv1s&app_code=G2byrnWbiV3VZhcX_W_pYg \
    &bbox={},{};{},{} \
    &criticality=minor'.format(latitude1,longitude1,latitude2,longitude2)

    response = requests.get(url)
    temp = json.loads(response.content)

    return temp

def mongo_insertion(temp, collection):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["air"]
    city = mydb[collection]

    x = city.insert_one(temp)
