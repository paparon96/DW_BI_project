# Docker token
import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta


client = MongoClient('mongodb://localhost:27017/')
mydb=client

#Accessing a collection
#my_collection = mydb['weather']
my_collection = mydb['air']

# AIR POLLUTION COLLECTION
a=my_collection['air_pollution']
data = list(a.find())
#print(data)

colnames = ['city','time','co', 'no2', 'o3', 'pm10', 'pm25', 'so2','w','p','t']
#colnames = ['city','time','pm25']
#values = []

for i in range(0,len(data)):
    print("START")
    print(i)
    values = []
    data2 = data[i]
    #print(type(data2))
    #print(len(data2))
    print(data2)

    temp = data2['data']


    # City data
    #city_name = temp['city']
    values.append(data2['city'])
    #values.append(city_name['name'])

    # Time data
    time = temp['time']
    #print(time['s'])
    values.append(time['s'])

    # Air quality data
    air_data = temp['iaqi']
    #values.append(dict.get(air_data['pm25'],'v'))
    keys = colnames[2:]
    for key in keys:
        if key in list(air_data.keys()):
            values.append(dict.get(air_data[key],'v'))
        else:
            values.append(0)


    #pm25_data = dict.get(air_data['pm25'],'v')
    #print(pm25_data)

    values = np.array(values)
    values = values.reshape(1,11)
    #values = values.reshape(1,3)

    if i==0:
        air_pollution_df = pd.DataFrame(values)
    else:
        temper = pd.DataFrame(values)
        air_pollution_df = air_pollution_df.append(temper)

air_pollution_df.columns = colnames
print("PANDAS")
print(air_pollution_df)
air_pollution_df['time'] = pd.to_datetime(air_pollution_df['time'], format = "%Y-%m-%d %H:%M:%S")
print(type(air_pollution_df.time.iloc[0]))


# WEATHER COLLECTION
colnames = ['city', 'time','temperature','pressure',
'humidity', 'temp_min', 'temp_max', 'cloud',
'wind_speed','wind_degree']

a=my_collection['weather']
data = list(a.find())
for i in range(0,len(data)):
    temp = data[i]
    print(temp)

    temp2 = temp['main']
    print(temp2)

    values = []

    # Get city

    values.append(temp['name'])

    # Get timestamp
    values.append(temp['time'])

    # Get basic weather data
    for key in temp2:

            values.append(temp2[key])


    # Get rain
    #temp4 = temp['rain']
    #for key in temp4:

    #        values.append(temp4[key])

    # Get clouds
    values.append(dict.get(temp['clouds'],'all'))

    # Get wind
    keys = ['speed','deg']
    temp3 = temp['wind']
    for key in keys:
        if key in list(temp3.keys()):
            #print(key)
            values.append(temp3[key])
            #print(temp3[key])
        else:
            values.append(0)

    values = np.array(values)
    values = values.reshape(1,10)
    if i==0:
        weather_df = pd.DataFrame(values)
    else:
        temper = pd.DataFrame(values)
        weather_df = weather_df.append(temper)

#print(values)
weather_df.columns = colnames
print("PANDAS")

# Optimize time zones
weather_df['time'] = pd.to_datetime(weather_df['time'], format = "%Y-%m-%d %H:%M:%S").dt.round('60min')

# ["Paris","Beijing","Paris","Tokyo","Dortmund","Moscow","Stockholm"]
weather_df.loc[weather_df.city=='Moscow','time'] = weather_df.loc[weather_df.city=='Moscow','time']  + timedelta(hours=2)
weather_df.loc[weather_df.city=='Beijing','time'] = weather_df.loc[weather_df.city=='Beijing','time']  + timedelta(hours=7)
weather_df.loc[weather_df.city=='Tokyo','time'] = weather_df.loc[weather_df.city=='Tokyo','time']  + timedelta(hours=8)
weather_df['time'] = weather_df['time']  - timedelta(hours=1) # To make it UTC+0 timezone

print(type(weather_df.time.iloc[0]))
print(weather_df)
print(weather_df.shape)


# TRAFFIC COLLECTION
colnames = ['city', 'time','accidents']

a=my_collection['traffic']
data = list(a.find())
print(data)

colnames = ['city','time','accident_num']

for i in range(0,len(data)): # CHANGE THIS IN THE NEW VERSION!!
    values = []

    temp = data[i]


    # Get city
    values.append(temp['city'])

    # Get time
    values.append(temp['time'])

    # Get number of accidents
    values.append(temp['accident_num'])

    values = np.array(values)
    values = values.reshape(1,3)

    if i==0: # CHANGE THIS IN THE NEW VERSION!!
        traffic_df = pd.DataFrame(values)
    else:
        temper = pd.DataFrame(values)
        traffic_df = traffic_df.append(temper)

traffic_df.columns = colnames

print(traffic_df)

# Datetime converted to closest hour
#traffic_df['time_new'] = pd.to_datetime(traffic_df['time'], format = "%Y-%m-%d %H:%M:%S").dt.round('60min')
traffic_df['time'] = pd.to_datetime(traffic_df['time'], format = "%Y-%m-%d %H:%M:%S").dt.round('60min')
traffic_df.loc[traffic_df.city=='Moscow','time'] = traffic_df.loc[traffic_df.city=='Moscow','time']  + timedelta(hours=2)
traffic_df.loc[traffic_df.city=='Beijing','time'] = traffic_df.loc[traffic_df.city=='Beijing','time']  + timedelta(hours=7)
traffic_df.loc[traffic_df.city=='Tokyo','time'] = traffic_df.loc[traffic_df.city=='Tokyo','time']  + timedelta(hours=8)
traffic_df['time'] = traffic_df['time']  - timedelta(hours=1) # To make it UTC+0 timezone

print(type(traffic_df.time.iloc[0]))
print(traffic_df)

## Merge Datasets
new_df = pd.merge(air_pollution_df, weather_df,  how='left', left_on=['city','time'], right_on = ['city','time'])
new_df = pd.merge(new_df, traffic_df,  how='left', left_on=['city','time'], right_on = ['city','time'])
print(new_df)