#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import pickle

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# # Data preprocessing

# ## Read in data

# In[ ]:


dataset = pd.read_csv("./modelling_dataset.csv")

# Some data cleaning
dataset = dataset.drop(columns = ["Unnamed: 0"])
dataset = dataset.drop_duplicates(subset=['city', 'time'], keep='last')

print(dataset.shape)
print(dataset.columns)
print(dataset.head())


# ## Handle missing values

# In[ ]:


dataset.isna().sum() # We see that the big problem is with accident_num we will handle that


# In[ ]:


# Number of accidents
dataset['accident_num'].fillna(dataset.groupby('city')['accident_num'].transform("median"), inplace=True)


# In[ ]:


# After the imputation we drop the observations with missing data
dataset = dataset.dropna()
print(dataset.shape)
print(dataset.isna().sum())


# In[ ]:


# Sort dataset by city and time
dataset = dataset.sort_values(by=['city', 'time'])
print(dataset.head())


# In[ ]:


# Copy current dataset to be used for prediction later
pred_table = dataset.copy()


# ## Lag creators

# In[ ]:


def lag_creators(num_lags,target_var,dataset):

    for i in range(5,num_lags+1):
        temp = 'lag_hour_{}_{}'.format(i,target_var)
        temp_series = dataset.groupby('city')[target_var]
        dataset[temp] = temp_series.shift(periods = i)

    return dataset


# In[ ]:


dataset = lag_creators(8,'co',dataset)
print(dataset.head())


# In[ ]:


# Other lags
dataset = lag_creators(8,'accident_num',dataset)
#print(dataset.head())


# In[ ]:


# Other lags
dataset = lag_creators(8,'wind_speed',dataset)
#print(dataset.head())


# In[ ]:


lag_cols = [i for i in dataset.columns if 'lag' in i]
print(lag_cols)


# # Modelling

# In[ ]:


# Burn NaN-s from lag-generation
dataset = dataset.dropna()

print(dataset.shape)


# ## CO model

# In[ ]:


# Features
modelling_table = dataset[lag_cols]
print(modelling_table.head())


# In[ ]:


# Target variable
y = dataset['co']
X = modelling_table.copy()


# In[ ]:


pred_model = LinearRegression().fit(X, y)


# In[ ]:


y_pred = pred_model.predict(X)


# In[ ]:


# Save model
filename = './pred_model.sav'
pickle.dump(pred_model, open(filename, 'wb'))

# Save columns for modelling
filename = './model_cols.sav'
pickle.dump(lag_cols, open(filename, 'wb'))


# # Predicting

# In[ ]:


print(pred_table.shape)
pred_table.head()


# In[ ]:


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


# ## Data preprocessing for prediction points

# In[ ]:


pred_table3 = pred_table2.copy()
pred_table3 = lag_creators(8,'co',pred_table3)
pred_table3 = lag_creators(8,'accident_num',pred_table3)
pred_table3 = lag_creators(8,'wind_speed',pred_table3)

pred_table4 = pred_table3[pred_table3.forecast==1]
pred_table4 = pred_table4.dropna()

pred_features = pred_table4[lag_cols]


# ## Running the model on the prediction points

# In[ ]:


y_forecast = pred_model.predict(pred_features)


# ## Inserting prediction values back to the dashboard table

# In[ ]:


j=0
for i in range(0,pred_table2.shape[0]):

    if pred_table2.iloc[i,-1]==1:
        pred_table2.iloc[i,2]=y_forecast[j]
        j = j+1


# In[ ]:


temp = pred_table2[pred_table2.forecast==1]
print(temp)


# # Support (Work in Progress)

# In[ ]:
