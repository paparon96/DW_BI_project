# Air quality API

# Import libraries
import requests
import json
import pymongo
from utils.helper_functions import api_call, mongo_insertion

# Set parameters
token = "03df9f2d4870930cf65e4acb042372759854c2a2"
city = "beijing"

# Get API content
temp = api_call(city,token)

#url= "https://api.waqi.info/feed/{0}/?token={1}".format(city,token)
#res = requests.get(url)
#temp = json.loads(res.content)
#data = temp['data']
#air_data = data['iaqi']
#pm25_data = dict.get(air_data['pm25'],'v')

#print(pm25_data*2)
print(temp)

# Access MongoDB and instert data
mongo_insertion(temp)
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["weather"]
#city = mydb["city"]

#x = city.insert_one(temp)
