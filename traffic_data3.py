#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:01:17 2019

@author: keyvanamini
"""

# pip install xmltodict

import requests
import json
#from xml.etree import ElementTree
#import xmltodict
#import pprint



url = 'https://traffic.api.here.com/traffic/6.3/incidents/json/8/134/86?app_id=u7vId3aGe6N0GmKuvv1s&app_code=G2byrnWbiV3VZhcX_W_pYg'
response = requests.get(url)
temp = json.loads(response.content)
#print(temp)
data1 = temp['TRAFFIC_ITEMS']
data2 = data1['TRAFFIC_ITEM']
type(data2)
ids = [d['TRAFFIC_ITEM_ID'] for d in data2]
#Count ids to get the number of traffic instances, check if there is a better indicator, such as vehicles involved in the traffic
len(ids)


