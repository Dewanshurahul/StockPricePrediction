# import boto3
# import pandas as pd
# from pyspark import SparkContext
# from pyspark.sql import SQLContext
# client = boto3.client("s3")
# path = "s3://stockpriceprediction/HistoricalQuotes.csv"
# df = pd.read_csv(path)
# # print(df.head(20))
# sc = SparkContext()
# sqlContext = SQLContext(sc)
# sparkdf = sqlContext.createDataFrame(df)
# # print(sparkdf.head(5))
# x = sparkdf.head(5)
# print(x)
# sc.stop()

import boto3
from pyspark import SparkContext
from pyspark.sql import SQLContext
client = boto3.client('s3')
sc = SparkContext()
sqlContext = SQLContext(sc)
path="s3://stockpriceprediction/HistoricalQuotes.csv"

df = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load(path)
print(df.head(20))
