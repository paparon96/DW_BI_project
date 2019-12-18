# Air quality API

# Import libraries
import requests
import json
import pymongo
import datetime
import pandas as pd
import logging
from dotenv import load_dotenv, find_dotenv
import os

# Importing environmental variables
env_path = './api_keys.env'
load_dotenv(dotenv_path=env_path)

from utils.helper_functions import get_data_pollution, get_data_weather, get_data_traffic, mongo_insertion

##### Global parameters
cities = ["Paris","Beijing","Budapest","Barcelona","Tokyo","Dortmund","Moscow","Stockholm"]

for city in cities:
	try:
		print(city)

##### AIR POLLUTION DATA

# Get API content
		POLLUTION_TOKEN = os.getenv("POLLUTION_TOKEN")
		temp = get_data_pollution(city,POLLUTION_TOKEN)
		temp['city']=city
		print(temp)
# Access MongoDB and instert data
		mongo_insertion(temp,"air_pollution")


##### WEATHER DATA
		WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
		temp_weather = get_data_weather(city,WEATHER_TOKEN)
# Get current timestamp added to the dictionary
		temp_weather['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		temp_weather['city']=city
# Access MongoDB and instert data
		mongo_insertion(temp_weather,"weather")



##### TRAFFIC DATA
		city_data = pd.read_csv('https://raw.githubusercontent.com/paparon96/Datasets/master/worldcities-2.csv')
		lat = city_data[city_data['city_ascii']==city].lat
		lng = city_data[city_data['city_ascii']==city].lng
		print(lat)
		print(lng)
		longitude1 = str(round((lng-0.2111).values[0],3))
		longitude2 = str(round((lng+0.2111).values[0],3))
		latitude1 = str(round((lat-0.2111).values[0],3))
		latitude2 = str(round((lat+0.2111).values[0],3))

		TRAFFIC_ID = os.getenv("TRAFFIC_ID")
		TRAFFIC_CODE = os.getenv("TRAFFIC_CODE")
		temp_traffic = get_data_traffic(TRAFFIC_ID,TRAFFIC_CODE,latitude1,longitude1,latitude2,longitude2)
		data1 = temp_traffic['TRAFFIC_ITEMS']
		data2 = data1['TRAFFIC_ITEM']
		ids = [d['TRAFFIC_ITEM_ID'] for d in data2]
		print(len(ids))

#Count ids to get the number of traffic instances
		temp_traffic = {"accident_num":len(ids)}
		
# Get current timestamp added to the dictionary
		temp_traffic['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		temp_traffic['city']=city

# Access MongoDB and instert data
		mongo_insertion(temp_traffic,"traffic")

	except:
		logging.exception('')
