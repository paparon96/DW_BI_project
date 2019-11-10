#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 20:13:13 2019

@author: keyvanamini
"""

import requests
import json
import pymongo

# Get API content
#key = "XFCf7fzUZ9Pf9BuwRtQQfc92IJJzmSPZ"
# Import the library to make the request to the TomTom API
r = requests.get("https://api.tomtom.com/routing/1/calculateRoute/&key=XFCf7fzUZ9Pf9BuwRtQQfc92IJJzmSPZ")# Print out the response to make sure it went through
print(r)