FROM python:3.6

RUN pip3 install tweepy pymongo requests pandas
ADD . .

CMD ["python3", "./air_api_data.py" ]
