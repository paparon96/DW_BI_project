## I. Import libraries


import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import chart_studio as py #added newly
import pickle
from dash_utils import add_row, lag_creators
import xgboost


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
#### MODELLING

new_df = new_df.drop_duplicates(subset=['city', 'time'], keep='last')

# Copy current dataset to be used for prediction later
pred_table = new_df.copy()

# Import model
filename = './xgb_model.sav'
xgb1 = pickle.load(open(filename, 'rb'))

# Import columns for modelling
filename = './model_cols.sav'
lag_cols = pickle.load(open(filename, 'rb'))


pred_table2 = pred_table.copy()
print(pred_table2.shape)

pred_table2['time'] =  pd.to_datetime(pred_table2['time'], format='%Y-%m-%d %H:%M:%S')
#print(pred_table2.dtypes)
pred_table2 = pred_table2.reset_index(drop=True)

unique_city_names = pred_table2.city.nunique()
lags = 8

# Dummy, indicator column
pred_table2['forecast'] = 0

# Always the last 3 (number of lags) for each city is the prediction!
def add_row(x,lags):
    for i in range(0,lags):
        last_row = x.iloc[-1]
        last_time = last_row.time
        last_row['time'] = last_time + pd.DateOffset(hours=1)
        x = x.append(last_row)
        x.iloc[-1,-1] = 1
    return x


pred_table2 = pred_table2.groupby('city').apply(add_row, lags=5).reset_index(drop=True)
print(pred_table2.shape)

pred_table3 = pred_table2.copy()
pred_table3 = lag_creators(8,'co',pred_table3)
pred_table3 = lag_creators(8,'accident_num',pred_table3)
pred_table3 = lag_creators(8,'wind_speed',pred_table3)

pred_table3 = pred_table3.dropna()

pred_table4 = pred_table3[pred_table3.forecast==1]
print(pred_table4)
#pred_table4 = pred_table4.dropna()

pred_features = pred_table4[lag_cols]


# Convert columns to numeric!
def num_convert(x):
    temp = pd.to_numeric(x,errors='coerce')

    return temp

pred_features = pred_features.apply(num_convert)

print("Prediction table")
print(pred_features)

y_forecast = xgb1.predict(pred_features)
print(len(y_forecast))
print(y_forecast)


j=0
forecast_col = pred_table3['forecast']
print(type(forecast_col))
for i in range(0,pred_table3.shape[0]):

    #if pred_table2.iloc[i,-1]==1:
    if forecast_col.iloc[i]==1:
        pred_table3.iloc[i,2]=y_forecast[j]
        #print(pred_table2.iloc[i,:])
        j = j+1

    #print("i {}".format(i))
    #print("j {}".format(j))



##################
#table = new_df
#table = table.iloc[0:300,:]
table = pred_table3.copy()
print(table.head())

MIN_TIME = min(table['time'])
MAX_TIME = max(table['time'])

# Filter dataset for given range
table_v1 = table.copy()

# Convert columns to numeric!
table_v1['co'] = pd.to_numeric(table_v1['co'],errors='coerce')
table_v1['pm25'] = pd.to_numeric(table_v1['pm25'],errors='coerce')
#print(table_v1.dtypes)


app = dash.Dash('Dashboards')

app.layout = html.Div(className = 'layout', children = [
    html.H1(className = 'title', children = 'Air Pollution Dashboard'),
    html.H4('Air pollution levels in different cities', className='subtitle'),
    #html.Div(className='timeline-controls', children = [
    #dcc.Checklist(id = 'country-checkbox',
    #              options = [ {'label': 'By City', 'value': 'by_country'}]),
    #html.Div(id = 'foo'),
#]),
    dcc.Graph(id='timeline3', figure={
        'data': [go.Scatter(x = table_v11.time,
                            y = table_v11.co,
                            # ids = table_v1.city,
                            # mode = 'markers',
                            name=city, marker=dict(size=12,
        #color=np.where(np.logical_and(table_v11['forecast']==1,True), 'green', 'red'),
        color=np.where(table_v11['forecast']==1, 'red', 'green'),
    )) # Change color to forecast later!!
        for city,table_v11 in table_v1.groupby('city') ],
        'layout': {
        'title': 'CO levels in different cities',
        'plot_bgcolor': '#DCDCDC',
                'paper_bgcolor': '#DCDCDC'
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
#html.Div(className='timeline-controls2', children = [
#dcc.Checklist(id = 'country-checkbox2',
#              options = [ {'label': 'By City', 'value': 'by_country2'}]),
#html.Div(id = 'foo2'),
#]),

    dcc.Graph(id='timeline2', figure={
        'data': [go.Scatter(x = table12.time,
                            y = table12.o3,
                            #ids = table12.city,
                             #mode = 'markers',
                             name=city2)
                             for city2,table12 in table.groupby('city')],
        'layout': {
            'title': 'Ozone levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
            }
}),
dcc.RangeSlider(
id='time-slider2',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
),

dcc.Graph(id='timeline4', figure={
    'data': [go.Scatter(x = table12.time,
                        y = table12.pm25,
                        #ids = table12.city,
                         #mode = 'markers',
                         name=city2)
                         for city2,table12 in table.groupby('city')],
    'layout': {
        'title': 'PM25 levels in different cities',
        'plot_bgcolor': '#DCDCDC',
                'paper_bgcolor': '#DCDCDC'
        }
}),
dcc.RangeSlider(
id='time-slider4',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
),

dcc.Graph(id='timeline5', figure={
    'data': [go.Scatter(x = table12.time,
                        y = table12.pm10,
                        #ids = table12.city,
                         #mode = 'markers',
                         name=city2)
                         for city2,table12 in table.groupby('city')],
    'layout': {
        'title': 'PM10 levels in different cities',
        'plot_bgcolor': '#DCDCDC',
                'paper_bgcolor': '#DCDCDC'
        }
}),
dcc.RangeSlider(
id='time-slider5',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
),

dcc.Graph(id='timeline6', figure={
    'data': [go.Scatter(x = table12.time,
                        y = table12.pm10,
                        #ids = table12.city,
                         #mode = 'markers',
                         name=city2)
                         for city2,table12 in table.groupby('city')],
    'layout': {
        'title': 'NO2 levels in different cities',
        'plot_bgcolor': '#DCDCDC',
                'paper_bgcolor': '#DCDCDC'
        }
}),
dcc.RangeSlider(
id='time-slider6',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
),

dcc.Graph(
           id='geo',
           figure={
               'data': [go.Scattergeo(
                       lon = table_v1['longitude'],
                       lat = table_v1['latitude'],
                       text = table_v1['city'],
                       #mode = 'markers'),
                       marker = dict(size=[float(i)/5 + 10 for i in table_v1.pm25.values],
                       color=  np.where(table_v1.pm25.values > 150, 'red', 'green')),
                       opacity = 0.9)],
               'layout': go.Layout(geo_scope='world',
                           width=1000,
                           height=600,
                           title="Average PM25 pollution levels",
                           plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                            geo = go.layout.Geo(
                                bgcolor = '#DCDCDC',
                                framecolor='#DCDCDC'
                                ))
               })
])


#@app.callback(
#    Output('foo', 'children'),
#    [Input('country-checkbox', 'value')]
#)
#def timeline(boxes):
#    print(boxes)
#    if boxes and 'by_country' in boxes:
#        #print('foo')
#        print(table)
    #return 'foo' if boxes else 'bar'
#    return 'foo' if boxes else 'bar'


@app.callback(
    Output('timeline3', 'figure'),
    [
    #Input('country-checkbox', 'value') ,
    Input('time-slider', 'value')
    ]
)
def timeline3(time_range, table_v1 = table_v1):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df = table_v1[table_v1.time>start]
    filtered_df = filtered_df[table_v1.time<finish]

    return {
        'data': [go.Scatter(x = filtered_df11.time,
                            y = filtered_df11.co,
                            #ids = filtered_df.city,
                            #mode = 'markers',
                            name=city,
                            marker=dict(size=12,
        #color=np.where(np.logical_and(table_v11['forecast']==1,True), 'green', 'red'),
        color=np.where(filtered_df11['forecast']==1, 'green', 'red'),
    )) for city,filtered_df11 in filtered_df.groupby('city') ],
        'layout': {
            'title': 'CO levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}


#@app.callback(
#    Output('foo2', 'children'),
#    [Input('country-checkbox2', 'value')]
#)
#def timeline22(boxes):
    #print(boxes)
    #if boxes and 'by_country' in boxes:
        #print('foo')
        #print(table)
    #return 'foo' if boxes else 'bar'
#    return 'foo' if boxes else 'bar'

@app.callback(
    Output('timeline2', 'figure'),
    [
    #Input('country-checkbox2', 'value') ,
    Input('time-slider2', 'value')
    ]
)
def timeline2(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df2 = table[table.time>start]
    filtered_df2 = filtered_df2[filtered_df2.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.o3,
                            #ids = table12.city,
                             #mode = 'markers',
                             name=city)
                             for city,table12 in filtered_df2.groupby('city')],
        'layout': {
            'title': 'Ozone levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}

@app.callback(
    Output('timeline4', 'figure'),
    [
    #Input('country-checkbox2', 'value') ,
    Input('time-slider4', 'value')
    ]
)
def timeline4(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df3 = table[table.time>start]
    filtered_df3 = filtered_df3[filtered_df3.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.pm25,
                            #ids = table12.city,
                             #mode = 'markers',
                             name=city)
                             for city,table12 in filtered_df3.groupby('city')],
        'layout': {
            'title': 'PM25 levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}

@app.callback(
    Output('timeline5', 'figure'),
    [
    #Input('country-checkbox2', 'value') ,
    Input('time-slider5', 'value')
    ]
)
def timeline5(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df4 = table[table.time>start]
    filtered_df4 = filtered_df4[filtered_df4.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.pm10,
                            #ids = table12.city,
                             #mode = 'markers',
                             name=city)
                             for city,table12 in filtered_df4.groupby('city')],
        'layout': {
            'title': 'PM10 levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}

@app.callback(
    Output('timeline6', 'figure'),
    [
    #Input('country-checkbox2', 'value') ,
    Input('time-slider6', 'value')
    ]
)
def timeline6(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df4 = table[table.time>start]
    filtered_df4 = filtered_df4[filtered_df4.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.pm10,
                            #ids = table12.city,
                             #mode = 'markers',
                             name=city)
                             for city,table12 in filtered_df4.groupby('city')],
        'layout': {
            'title': 'NO2 levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}

# Testing


#app.run_server(host='0.0.0.0',debug=True,port=8050)
