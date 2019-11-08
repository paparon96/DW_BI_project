docker run --name some-mongo -d -p 27017:27017 mongo:bionic

docker exec -it some-mongo bash

mongo

use weather

show collections

db.paris.find().pretty()
