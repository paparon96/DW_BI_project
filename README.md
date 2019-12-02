# Data Warehousing & Business Intelligence

## Air pollution monitoring and prediction project

Keyvan Amini <br>
Aron Pap

### Introduction
In this project we aim to collect and store data about air pollution in different cities throughout the world. Driven by the final goal of building an Early Warning System for unhealthy air pollution levels we collect data from 3 primary sources via API:

* Basic air pollution data (The World Air Quality Project, https://aqicn.org/api/)
* Basic weather data (Temperature, wind, humidity etc.) (https://openweathermap.org/api)
* Traffic data (https://developer.here.com/documentation/traffic/dev_guide/topics/what-is.html)

This collection is also driven by "expert knowledge" related to potential predictors/causes of air pollution (https://www.economist.com/graphic-detail/2019/11/09/indias-toxic-smog-is-a-common-affliction-in-middle-income-countries)

We store the collected datasets in MongoDB on an AWS machine. We will build a predictive model once we have enough historical data. Then we have already set up an ETL process that gets the data from our MongoDB (later capable of running the predictions) and transforms it into a new dataframe which is the input for our dashboard. The dashboard will be implemented via Dash.

### PART 1

All the files we used to implement this project are available in our GitHub repository. To replicate the results please use the following steps:

1. Set up MongoDB on your computer via Docker (*mongoDB_creator.sh*)
2. Create a Python file which calls the API-s and insert the collected data into our database (*air_api_data.py*)
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
