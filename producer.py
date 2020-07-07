from time import sleep
from kafka import KafkaProducer
from alpha_vantage.timeseries import TimeSeries
import random
import json

#Function to get the data from alphavantage
def get_data():
    ticker = 'GOOGL'
    lines = open('/home/dewanshu/Desktop/keys').read().splitlines()
    keys = random.choice(lines)
    time = TimeSeries(key=keys, output_format='json')
    data, metadata = time.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    return data

#Function to publish a message
def publish_data(producerkey,key):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        producerkey.send("stock_price", json.dumps(data[key]).encode('utf-8'), key_bytes)
        print("Data Published")
    except:
        print("Data not Published")

#Function to declear connection to producer
def kafka_producer_connection():
    try:
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        return producer
    except:
        print("Connection not Established")

#Declearing main function
if __name__=="__main__":
    try:
        data = get_data()
    except:
        print("Data didn't get fetched")
    if len(data) > 0:
        try:
            kafka_producer = kafka_producer_connection()
        except:
            print("Connection not Established")
        for key in sorted(data):
            publish_data(kafka_producer,key)
            sleep(2)