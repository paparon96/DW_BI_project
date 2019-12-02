## I. Import libraries


import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import chart_studio as py #added newly


import pandas as pd
#from sqlalchemy import create_engine
#import psycopg2
#import matplotlib.pyplot as plt

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_marks(start, end):
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(days=1)
    #return {int(m.timestamp()): m.strftime('%Y-%m-%d %H') for m in result}
    return {int(m.timestamp()): m.strftime('%Y-%m-%d') for m in result}
    #return {m: m.strftime('%Y-%m-%d %H') for m in result}



## II. Create engine object to be able to connect to the database
#engine = create_engine('postgresql://postgres@localhost:5432/starschema_company')

## III. Extract data from the PostgreSQL tables
#table = pd.read_sql_table("order_line_fact_table", con=engine)

###################
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
'wind_speed','wind_degree','longitude','latitude']

a=my_collection['weather']


data = list(a.find())

lon_list=[]
lat_list=[]


for i in range(0,len(data)):
    temp = data[i]
    print(temp)

    values = []

    lon=temp['coord']['lon']
    lon_list.append(lon)
    lat=temp['coord']['lat']
    lat_list.append(lat)

    temp2 = temp['main']
    print(temp2)


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

    # Add coordinate values
    values.append(temp['coord']['lon'])
    values.append(temp['coord']['lat'])


    values = np.array(values)
    values = values.reshape(1,12)
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

# Save out modelling datasets
new_df.to_csv('modelling_dataset.csv')

##################
table = new_df
table = table.iloc[0:300,:]
print(table.head())

MIN_TIME = min(table['time'])
MAX_TIME = max(table['time'])

# Filter dataset for given range
table_v1 = table.copy()

app = dash.Dash('Dashboards')

app.layout = html.Div(className = 'layout', children = [
    html.H1(className = 'title', children = 'Air Pollution Dashboard'),
    html.H4('Air pollution levels in different cities', className='subtitle'),
    html.Div(className='timeline-controls', children = [
    dcc.Checklist(id = 'country-checkbox',
                  options = [ {'label': 'By City', 'value': 'by_country'}]),
    html.Div(id = 'foo'),
]),
    dcc.Graph(id='timeline3', figure={
        'data': [go.Scatter(x = table_v1.time,
                            y = table_v1.pm25,
                            ids = table_v1.city, mode = 'markers',
                            name=city)
                            for city,table_v1 in table_v1.groupby('city') ],
        'layout': {
            'title': 'PM25 levels in different cities'
        }
}),
dcc.RangeSlider(
id='time-slider',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
)
,
html.Div(className='timeline-controls2', children = [
dcc.Checklist(id = 'country-checkbox2',
              options = [ {'label': 'By City', 'value': 'by_country2'}]),
html.Div(id = 'foo2'),
]),

    dcc.Graph(id='timeline2', figure={
        'data': [go.Scatter(x = table.time,
                            y = table.o3,
                            ids = table.city,
                             mode = 'markers',
                             name=city2)
                             for city2,table in table.groupby('city')],
        'layout': {
            'title': 'Ozone levels in different cities'
        }
}),
dcc.RangeSlider(
id='time-slider2',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
),

dcc.Graph(
           id='geo',
           figure={
               'data': [go.Scattergeo(
                       lon = table['longitude'],
                       lat = table['latitude'],
                       text = table['city'],
                       #mode = 'markers'),
                       marker = dict(size=[float(i)*2 for i in table.co.values]))],
               'layout': go.Layout(geo_scope='world',
                           width=1000,
                           height=600)
               })

])


@app.callback(
    Output('foo', 'children'),
    [Input('country-checkbox', 'value')]
)
def timeline(boxes):
    print(boxes)
    if boxes and 'by_country' in boxes:
        #print('foo')
        print(table)
    #return 'foo' if boxes else 'bar'
    return 'foo' if boxes else 'bar'


@app.callback(
    Output('timeline3', 'figure'),
    [Input('country-checkbox', 'value') ,
    Input('time-slider', 'value')
    ]
)
def timeline3(boxes, time_range, table_v1 = table_v1):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df = table_v1[table_v1.time>start]
    filtered_df = filtered_df[table_v1.time<finish]

    return {
        'data': [go.Scatter(x = filtered_df.time,
                            y = filtered_df.pm25,
                            ids = filtered_df.city, mode = 'markers',
                            name=city)
                            for city,filtered_df in filtered_df.groupby('city') ],
        'layout': {
            'title': 'PM25 levels in different cities'
        }}


@app.callback(
    Output('foo2', 'children'),
    [Input('country-checkbox2', 'value')]
)
def timeline22(boxes):
    #print(boxes)
    #if boxes and 'by_country' in boxes:
        #print('foo')
        #print(table)
    #return 'foo' if boxes else 'bar'
    return 'foo' if boxes else 'bar'

@app.callback(
    Output('timeline2', 'figure'),
    [Input('country-checkbox2', 'value') ,
    Input('time-slider2', 'value')
    ]
)
def timeline2(boxes, time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df2 = table[table.time>start]
    filtered_df2 = filtered_df2[filtered_df2.time<finish]

    return {
        'data': [go.Scatter(x = filtered_df2.time,
                            y = filtered_df2.o3,
                            ids = filtered_df2.city,
                             mode = 'markers',
                             name=city)
                             for city,table in filtered_df2.groupby('city')],
        'layout': {
            'title': 'Ozone levels in different cities'
        }}


# Testing


app.run_server(host='0.0.0.0',debug=True,port=8050)
