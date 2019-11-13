docker run --name some-mongo -d -p 27017:27017 mongo:bionic

docker exec -it some-mongo bash

mongo

use weather

show collections

db.air_pollution.find().pretty()
db.weather.find().pretty()
db.traffic.find().pretty()
