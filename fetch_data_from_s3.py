import boto3
import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
try:
    client = boto3.client("s3")
    path = "s3://stockpriceprediction/HistoricalQuotes.csv"
    df = pd.read_csv(path)
    # print(df.head(20))
except:
    print("Please Check path for given file")

try:
    sc = SparkContext()
    sqlContext = SQLContext(sc)
    sparkdf = sqlContext.createDataFrame(df)
    print(sparkdf.head(5))
except:
    print("Check for pandas DataFrame")
sc.stop()