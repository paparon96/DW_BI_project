# Data Warehousing & Business Intelligence

## Air pollution monitoring and prediction project

Keyvan Amini <br>
Aron Pap

### TO-DO
  * (P1) Check why recent points are not displayed on the graph!!
  * (P1) Check why map has so many circles!
  * (P1) Add new graphs
  * (P1) Adding the prediction points
  * (P3) Use snake-case for variable names everywhere!!
  * (P2) Put tokens and keys into environmental variables
  * (P4) Use spaces instead of tabs in Python!
  * (P1) Handle errors, exceptions --> Added logging to the Python file (example below)
    * ERROR:root:
    * Traceback (most recent call last):
    * File "air_api_data.py", line 88, in <module>
    * data1 = temp['TRAFFIC_ITEMS']
    * KeyError: 'TRAFFIC_ITEMS'
  * (P3) Remove commented out code! (Repeat in final iteration!!)


### Introduction
In this project we aim to collect and store data about air pollution in different cities throughout the world. Driven by the final goal of building an "Early Warning System" for unhealthy air pollution levels we collect data from 3 main sources via API:

* Basic air pollution data (main pollutants PM25, PM10, CO, CO2 etc., source: The World Air Quality Project)
  (https://aqicn.org/api/)
* Basic weather data (temperature, wind, humidity etc.)
  (https://openweathermap.org/api)
* Traffic data (number of traffic incidents as a proxy for emission of pollutants)
  (https://developer.here.com/documentation/traffic/dev_guide/topics/what-is.html)

This collection is also inspired by scientific results related to potential predictors/causes of air pollution (https://www.economist.com/graphic-detail/2019/11/09/indias-toxic-smog-is-a-common-affliction-in-middle-income-countries)

We store the collected datasets in MongoDB on an AWS machine. We will build a predictive model once we have enough historical data. Subsequentially we set up an ETL process that gets the data from our MongoDB (later capable of running the predictions) and transforms it into a new dataframe which is the input for our dashboard. The dashboard will be implemented via Dash.

### PART 1

All the files we used to implement this project are available in our GitHub repository. To replicate the results please use the following steps:

1. Set up MongoDB on your computer via Docker (*mongoDB_creator.sh*)
2. Create a Python file which calls the API-s and insert the collected data into our database (*air_api_data.py*)
  * Use the API keys provided in the *air_api_data.py* script
  * Optionally some of the function definitions can be defined in separate **utils** files (*utils* folder)
3. Create a Docker image from this file (*Dockerfile*)
4. Set up a cron job to schedule running this Docker image every hour, consisting of:
  * A shell file with the commands (*cron.sh*)
  * A cron file which calls the above mentioned shell file (*cron*)
  * Add this cron file to crontab (*cron*)
5. Set up ETL process through a Python file:
  * Extract collections from our mongoDB database (E)
  * Turn collections into Pandas dataframes (T)
  * Merge dataframes on **time** and **city** (T)
  * Pass the dataframes to the dashboard application file (L)
 





### PART 2

All the files we used to implement this part of the project are also available in our GitHub repository. To replicate the results please use the following steps:

1. Set up ETL process through a Python file: (first part of *air_app.py*)
  * Extract collections from our mongoDB database (E)
  * Turn collections into Pandas dataframes (T)
  * Merge dataframes on **time** and **city** (T)
  * Pass the dataframes to the dashboard application file (L)
2. Train an XGBoost regressor for the forecast of CO pollution levels 3 hours in advance, using lagged variables (*Pollution_prediction.ipynb*)
  * Use the historical data (*modelling_dataset.csv*) as a training dataset
  * Train the model
  * Save the model as a pickle object
3. Also read in historical data from csv file in *air_app.py* and merge with the data from the MongoDB (*modelling_dataset.csv* and *air_app.py*)
4. Run the prediction on the dataframes, incorporate the forecast into the final dataframe used for the Dashboards.
5. Create the code for the dashboards as in the second part of the *air_app.py* file
6. Create a separate script for running the dashboard (*server.py*)

