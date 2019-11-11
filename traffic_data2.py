#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 20:47:22 2019

@author: keyvanamini
"""

import configparser
import requests
import json
import sys
import time
import datetime

from urllib.request import urlopen

# URL to the tomtom api
apiURL      = "https://api.tomtom.com/routing/1/calculateRoute/"
# apiKey
apiKey      = "XFCf7fzUZ9Pf9BuwRtQQfc92IJJzmSPZ"

#[coordinates]
sourceLat   = 51.5560241
sourceLon   = -0.2817075
destLat     = 53.4630621
destLon     = -2.2935288

tomtomURL = "%s/%s,%s:%s,%s/json?key=%s" % (apiURL,sourceLat,sourceLon,destLat,destLon,apiKey)

getData = urlopen(tomtomURL).read()
jsonTomTomString = json.loads(getData)

totalTime = jsonTomTomString['routes'][0]['summary']['travelTimeInSeconds']

print ("time to destination is: ", totalTime)