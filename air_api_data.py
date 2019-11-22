# Air quality API

# Import libraries
import requests
import json
import pymongo
import datetime
import pandas as pd

from utils.helper_functions import api_call, mongo_insertion


##### AIR POLLUTION DATA
# Set parameters
token = "03df9f2d4870930cf65e4acb042372759854c2a2"
cities = ["Paris","Beijing","Budapest","Barcelona","Tokyo","Dortmund","Moscow","Stockholm"]
#city = "budapest"

	
for city in cities:
	try:
		print(city)
# Get API content
		temp = api_call(city,token)

#url= "https://api.waqi.info/feed/{0}/?token={1}".format(city,token)
#res = requests.get(url)
#temp = json.loads(res.content)
#data = temp['data']
#air_data = data['iaqi']
#pm25_data = dict.get(air_data['pm25'],'v')

#print(pm25_data*2)
		temp['city']=city
		print(temp)

# Access MongoDB and instert data
		mongo_insertion(temp,"air_pollution")

##### WEATHER DATA
#city = 'Budapest'
		url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=bd64898a234d3ac401ec97cfd4ba3f2d'.format(city)

		res = requests.get(url)
		temp = json.loads(res.content)

# Get current timestamp added to the dictionary
		temp['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		temp['city']=city
		print(temp)

# Access MongoDB and instert data
		mongo_insertion(temp,"weather")


##### TRAFFIC DATA

		city_data = pd.read_csv('https://raw.githubusercontent.com/paparon96/Datasets/master/worldcities.csv')
#city = 'Zurich'
		lat = city_data[city_data['city_ascii']==city].lat
		lng = city_data[city_data['city_ascii']==city].lng

#print(city_data.head())
		print(lat)
		print(lng)

		longitude1 = str(round((lng-0.2111).values[0],3))
		longitude2 = str(round((lng+0.2111).values[0],3))
		latitude1 = str(round((lat-0.2111).values[0],3))
		latitude2 = str(round((lat+0.2111).values[0],3))
		print(longitude1)
#url='https://traffic.api.here.com/traffic/6.3/incidents.json?app_id=u7vId3aGe6N0GmKuvv1s&app_code=G2byrnWbiV3VZhcX_W_pYg \
 # &bbox=42.516,13.355;52.511,13.400 \
 #&criticality=minor'

		url='https://traffic.api.here.com/traffic/6.3/incidents.json?app_id=u7vId3aGe6N0GmKuvv1s&app_code=G2byrnWbiV3VZhcX_W_pYg \
   		&bbox={},{};{},{} \
   		&criticality=minor'.format(latitude1,longitude1,latitude2,longitude2)

#url = 'https://traffic.api.here.com/traffic/6.3/incidents/json/8/134/86?app_id=u7vId3aGe6N0GmKuvv1s&app_code=G2byrnWbiV3VZhcX_W_pYg'
		response = requests.get(url)
		temp = json.loads(response.content)
#print(temp)
#print(temp.shape)
		

		data1 = temp['TRAFFIC_ITEMS']
		data2 = data1['TRAFFIC_ITEM']
#type(data2)
		ids = [d['TRAFFIC_ITEM_ID'] for d in data2]

#Count ids to get the number of traffic instances, check if there is a better indicator, such as vehicles involved in the traffic
#print(len(ids))

		temp = {"accident_num":len(ids)}
# Get current timestamp added to the dictionary
		temp['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		temp['city']=city
		print(temp)

# Access MongoDB and instert data
		mongo_insertion(temp,"traffic")

	except:
		pass
