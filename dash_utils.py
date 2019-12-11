def lag_creators(num_lags,target_var,dataset):

    for i in range(5,num_lags+1):
        temp = 'lag_hour_{}_{}'.format(i,target_var)
        temp_series = dataset.groupby('city')[target_var]
        dataset[temp] = temp_series.shift(periods = i)

    return dataset


# Always the last 3 (number of lags) for each city is the prediction!
def add_row(x,lags):
    for i in range(0,lags):
        last_row = x.iloc[-1]
        last_time = last_row.time
        last_row['time'] = last_time + pd.DateOffset(hours=1)
        x = x.append(last_row)
        x.iloc[-1,-1] = 1
    return x
