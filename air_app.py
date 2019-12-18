## I. Import libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import chart_studio as py
import pickle
from dash_utils import add_row, lag_creators
import xgboost
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_marks(start, end):
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(days=2)
    return {int(m.timestamp()): m.strftime('%Y-%m-%d') for m in result}

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
my_collection = mydb['air']

# AIR POLLUTION COLLECTION
a=my_collection['air_pollution']
data = list(a.find())
colnames = ['city','time','co', 'no2', 'o3', 'pm10', 'pm25', 'so2','w','p','t']

for i in range(0,len(data)):
    print("START")
    print(i)
    values = []
    data2 = data[i]
    print(data2)

    temp = data2['data']

    # City data
    values.append(data2['city'])

    # Time data
    time = temp['time']
    values.append(time['s'])

    # Air quality data
    air_data = temp['iaqi']
    keys = colnames[2:]
    for key in keys:
        if key in list(air_data.keys()):
            values.append(dict.get(air_data[key],'v'))
        else:
            values.append(0)

    values = np.array(values)
    values = values.reshape(1,11)

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
    temperature_keys = ['temp','pressure','humidity','temp_min','temp_max']

    for key in temperature_keys:
            values.append(temp2[key])

    # Get clouds
    values.append(dict.get(temp['clouds'],'all'))

    # Get wind
    keys = ['speed','deg']
    temp3 = temp['wind']
    for key in keys:
        if key in list(temp3.keys()):
            values.append(temp3[key])
        else:
            values.append(0)

    # Add coordinate values
    values.append(temp['coord']['lon'])
    values.append(temp['coord']['lat'])


    values = np.array(values)
    print(values)
    values = values.reshape(1,12)
    if i==0:
        weather_df = pd.DataFrame(values)
    else:
        temper = pd.DataFrame(values)
        weather_df = weather_df.append(temper)

weather_df.columns = colnames
print("PANDAS")

# Optimize time zones
weather_df['time'] = pd.to_datetime(weather_df['time'], format = "%Y-%m-%d %H:%M:%S").dt.round('60min')

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

for i in range(0,len(data)):
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

    if i==0:
        traffic_df = pd.DataFrame(values)
    else:
        temper = pd.DataFrame(values)
        traffic_df = traffic_df.append(temper)

traffic_df.columns = colnames

print(traffic_df)

# Datetime converted to closest hour
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

# Import old data
old_data = pd.read_csv('./modelling_dataset.csv',index_col=0)
print(old_data.head())

# Merge with new data
new_df = old_data.append(new_df)
print(new_df.head())

# Save out modelling datasets
#new_df.to_csv('modelling_dataset.csv')

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
    if forecast_col.iloc[i]==1:
        pred_table3.iloc[i,2]=y_forecast[j]
        j = j+1

# Non-forecast DataFrame
table_non_forecast = new_df.copy()
# Convert columns to numeric!
table_non_forecast['co'] = pd.to_numeric(table_non_forecast['co'],errors='coerce')
table_non_forecast['pm25'] = pd.to_numeric(table_non_forecast['pm25'],errors='coerce')
table_non_forecast['time'] =  pd.to_datetime(table_non_forecast['time'], format='%Y-%m-%d %H:%M:%S')


##################
table = pred_table3.copy()
print(table.head())

MIN_TIME = min(table['time'])
MAX_TIME = max(table['time'])

# Filter dataset for given range
table_v1 = table.copy()

# Convert columns to numeric!
table_v1['co'] = pd.to_numeric(table_v1['co'],errors='coerce')
table_v1['pm25'] = pd.to_numeric(table_v1['pm25'],errors='coerce')

# Support table for world map
print("Grouped table")
temped_group_table = table_non_forecast.groupby(by='city').last()
print(temped_group_table)

app = dash.Dash('Dashboards')

app.layout = html.Div(className = 'layout', children = [
    html.H1(className = 'title', children = 'Air Pollution Dashboard'),
    html.H4('Air pollution levels in different cities', className='subtitle'),
    dcc.Graph(id='timeline3', figure={
        'data': [go.Scatter(x = table_v11.time,
                            y = table_v11.co,
                            name=city, marker=dict(size=12,
        color=np.where(table_v11['forecast']==1, 'red', 'green'),
    ))
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

    dcc.Graph(id='timeline2', figure={
        'data': [go.Scatter(x = table12.time,
                            y = table12.o3,
                             name=city2)
                             for city2,table12 in table_non_forecast.groupby('city')],
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
                         name=city2)
                         for city2,table12 in table_non_forecast.groupby('city')],
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
                         name=city2)
                         for city2,table12 in table_non_forecast.groupby('city')],
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
                         name=city2)
                         for city2,table12 in table_non_forecast.groupby('city')],
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
                       lon = temped_group_table['longitude'],
                       lat = temped_group_table['latitude'],
                       text = temped_group_table.index,
                       marker = dict(size=[float(i)/5 + 10 for i in table_non_forecast.groupby(by='city')['pm25'].mean()],
                       color=  np.where(table_non_forecast.groupby(by='city')['pm25'].mean() > 150, 'red', 'green')),
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
               }),

dcc.Graph(id='accidents', figure = {
'data' : [go.Bar(ids = table12.index,
               x = table12.time,
               y = table12.accident_num,
               orientation='v',
               name = city2)
        for city2,table12 in table_non_forecast.groupby('city')],
        'layout': {
            'title': 'Hourly traffic accidents in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
            }
}),
dcc.RangeSlider(
id='time-slider7',
min=MIN_TIME.timestamp(),
max=MAX_TIME.timestamp(),
value=[MIN_TIME.timestamp(), MAX_TIME.timestamp()],
marks = get_marks(MIN_TIME, MAX_TIME)
)

])


@app.callback(
    Output('timeline3', 'figure'),
    [
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
                            name=city,
                            marker=dict(size=12,
        color=np.where(filtered_df11['forecast']==1, 'green', 'red'),
    )) for city,filtered_df11 in filtered_df.groupby('city') ],
        'layout': {
            'title': 'CO levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}


@app.callback(
    Output('timeline2', 'figure'),
    [
    Input('time-slider2', 'value')
    ]
)
def timeline2(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df2 = table_non_forecast[table_non_forecast.time>start]
    filtered_df2 = filtered_df2[filtered_df2.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.o3,
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
    Input('time-slider4', 'value')
    ]
)
def timeline4(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df3 = table_non_forecast[table_non_forecast.time>start]
    filtered_df3 = filtered_df3[filtered_df3.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.pm25,
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
    Input('time-slider5', 'value')
    ]
)
def timeline5(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df4 = table_non_forecast[table_non_forecast.time>start]
    filtered_df4 = filtered_df4[filtered_df4.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.pm10,
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
    Input('time-slider6', 'value')
    ]
)
def timeline6(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df4 = table_non_forecast[table_non_forecast.time>start]
    filtered_df4 = filtered_df4[filtered_df4.time<finish]

    return {
        'data': [go.Scatter(x = table12.time,
                            y = table12.pm10,
                             name=city)
                             for city,table12 in filtered_df4.groupby('city')],
        'layout': {
            'title': 'NO2 levels in different cities',
            'plot_bgcolor': '#DCDCDC',
                    'paper_bgcolor': '#DCDCDC'
        }}

@app.callback(
    Output('accidents', 'figure'),
    [
    Input('time-slider7', 'value')
    ]
)
def accidents(time_range, table = table):
    start, finish = [datetime.fromtimestamp(t) for t in time_range]
    filtered_df5 = table_non_forecast[table_non_forecast.time>start]
    filtered_df5 = filtered_df5[filtered_df5.time<finish]

    return {
    'data' : [go.Bar(ids = table12.index,
                   x = table12.time,
                   y = table12.accident_num,
                   orientation='v',
                   name = city2)
            for city2,table12 in filtered_df5.groupby('city')],
            'layout': {
                'title': 'Hourly traffic accidents in different cities',
                'plot_bgcolor': '#DCDCDC',
                        'paper_bgcolor': '#DCDCDC'
                }
    }
