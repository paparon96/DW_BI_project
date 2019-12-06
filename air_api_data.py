# Air quality API

# Import libraries
import requests
import json
import pymongo
import datetime
import pandas as pd
import logging

from utils.helper_functions import get_data_pollution, get_data_weather, get_data_traffic, mongo_insertion

##### Global parameters
cities = ["Paris","Beijing","Budapest","Barcelona","Tokyo","Dortmund","Moscow","Stockholm"]

for city in cities:
	try:
		print(city)

##### AIR POLLUTION DATA
# Set parameters
		token = "03df9f2d4870930cf65e4acb042372759854c2a2"

# Get API content
		temp = get_data_pollution(city,token)
		temp['city']=city
		print(temp)
# Access MongoDB and instert data
		mongo_insertion(temp,"air_pollution")



##### WEATHER DATA
		temp_weather = get_data_weather(city)
# Get current timestamp added to the dictionary
		temp_weather['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		temp_weather['city']=city
# Access MongoDB and instert data
		mongo_insertion(temp_weather,"weather")



##### TRAFFIC DATA
		city_data = pd.read_csv('https://raw.githubusercontent.com/paparon96/Datasets/master/worldcities.csv')
		lat = city_data[city_data['city_ascii']==city].lat
		lng = city_data[city_data['city_ascii']==city].lng

		longitude1 = str(round((lng-0.2111).values[0],3))
		longitude2 = str(round((lng+0.2111).values[0],3))
		latitude1 = str(round((lat-0.2111).values[0],3))
		latitude2 = str(round((lat+0.2111).values[0],3))

		temp_traffic = get_data_traffic(latitude1,longitude1,latitude2,longitude2)

		data1 = temp_traffic['TRAFFIC_ITEMS']
		data2 = data1['TRAFFIC_ITEM']
		ids = [d['TRAFFIC_ITEM_ID'] for d in data2]

#Count ids to get the number of traffic instances
		temp_traffic = {"accident_num":len(ids)}
# Get current timestamp added to the dictionary
		temp_traffic['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		temp_traffic['city']=city

# Access MongoDB and instert data
		mongo_insertion(temp_traffic,"traffic")



	except:
		logging.exception('')
		#pass
