#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:01:17 2019

@author: keyvanamini
"""

# pip install xmltodict

import requests
import json
import pandas as pd
import datetime

#from xml.etree import ElementTree
#import xmltodict
#import pprint


#In the link below we can change the parameter bbox, which is the latitude and longitude
city_data = pd.read_csv('https://raw.githubusercontent.com/paparon96/DW_BI_project/master/worldcities.csv?token=ALIWHUNL5MZMADFACKDM4U252VVBO')
city = 'Zurich'
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

print(temp)
