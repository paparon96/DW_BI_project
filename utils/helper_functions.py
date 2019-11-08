# Import libraries
import requests
import json
import pymongo

def api_call(city,token):
    token = "03df9f2d4870930cf65e4acb042372759854c2a2"
    #city = "beijing"
    url= "https://api.waqi.info/feed/{0}/?token={1}".format(city,token)
    res = requests.get(url)
    temp = json.loads(res.content)

    return temp

def mongo_insertion(temp):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["weather"]
    city = mydb["city"]

    x = city.insert_one(temp)
