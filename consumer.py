import os
os.environ["PYSPARK_PYTHON"]='/usr/bin/python3'
from kafka import KafkaConsumer
import pandas as pd
import json

#Importing pyspark modules
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel

#Declearing spark context
sc= SparkContext()
sqlContext = SQLContext(sc)

#Declearing the model path
try:
    Path = "stockModel"
    load_trained_model = LinearRegressionModel.load(Path)
except:
    print("Plese check path of trained model")

#Declearing consumer connection
try:
    consumer = KafkaConsumer('stock_price',bootstrap_servers=['localhost:9092'])
except:
    print('connection error')

#getting data and predicting result using the model
def stock_price_prediction(load_model):
        for msg in consumer:
            res = json.loads(msg.value.decode('utf-8'))
            datalist = list(res.values())
            df = pd.DataFrame([datalist], columns=['Open', 'Close', 'Volume', 'High', 'Low'])
            df = df.astype(float)
            spark_df = sqlContext.createDataFrame(df)
            vectorAssembler = VectorAssembler(inputCols=['Open', 'High', 'Low'], outputCol='Independent Columns')
            df_vect = vectorAssembler.transform(spark_df)
            df_vect_features = df_vect.select(['Independent Columns', 'Close'])
            predictions = load_trained_model.transform(df_vect_features)
            predictions.select("prediction", "Close", "Independent Columns").show()
            predicted_value = predictions.select('prediction').collect()[0].__getitem__("prediction")
            closed_value = predictions.select('Close').collect()[0].__getitem__('Close')
            print(msg.key)
            date_time = msg.key.decode('utf-8')
            return predicted_value, closed_value, date_time

stock_price_prediction(load_trained_model)
try:
    consumer.close()
except:
    print("Close Consumer Manually")