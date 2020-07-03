import boto3
import pandas as pd

try:
    client = boto3.client("s3")
    path = "s3://stockpriceprediction/HistoricalQuotes.csv"
    df = pd.read_csv(path)
#     print(df.head())
except:
    print("Please Check path for given file")

df['Date'] = pd.to_datetime(df.Date)
df['Date'] = df ["Date"].dt.strftime('%m/%d/%y')
# print(df['Date'])

# print(df.columns.tolist())
df = df.rename(columns={df.columns[1] : 'Close'})
df = df.rename(columns={df.columns[2] : 'Volume'})
df = df.rename(columns={df.columns[3] : 'Open'})
df = df.rename(columns={df.columns[4] : 'High'})
df = df.rename(columns={df.columns[5] : 'Low'})
# print(df.columns.tolist())

# Convered datatype of columns into float
# and removed "$" sign from the dataframe
try:
    df[df.columns[1:]] = df[df.columns[1:]].replace('[\$,]', '', regex=True).astype(float)
except ValueError:
    print("Could not convert datatype to an Float.")

# print(df)

""" Checking datatype of each column """
# print('Close ',df['Close'].dtype)
# print('Volume ',df['Volume'].dtype)
# print('Low ',df['Low'].dtype)
# print('Open ',df['Open'].dtype)
# print('High ',df['High'].dtype)

from pyspark import SparkContext
from pyspark.sql import SparkSession

sc = SparkContext()
sparkSession = SparkSession(sc)
stockData = sparkSession.createDataFrame(df)

# print(stock_price_data)
# print(stock_price_data.printSchema())
# print(stock_price_data.describe().toPandas().transpose())

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

print("Seperating the Open, High and Low:")
featureAssembler = VectorAssembler(inputCols=["Open", "High", "Low"], outputCol="Independent Columns")
output = featureAssembler.transform(stockData)
# print(output.show())

# Checking the Vectorized Feature
# print(output.select("Independent Columns").show())

# Listing Columns
# print(output.columns)

# Getting Column Sorted
finalData = output.select("Independent Columns", "Close")
print(finalData.show())

# Dividing Data for Training and Testing
trainData, testData = finalData.randomSplit([0.70, 0.3])

# Training the Model
reg = LinearRegression(featuresCol='Independent Columns', labelCol='Close')
reg = reg.fit(trainData)
LR = LinearRegression(featuresCol='Independent Columns', labelCol='Close', maxIter=10, regParam=0.3, elasticNetParam=0.8)
lr_Model = LR.fit(trainData)
print("Coefficients: " + str(lr_Model.coefficients))
print("Intercept: " + str(lr_Model.intercept))

# Testing the Model
LRPredictions = lr_Model.transform(testData)
print(LRPredictions.select("Close", "Independent Columns", "Prediction").show(5))


LREvaluator = RegressionEvaluator(predictionCol="prediction", labelCol="Close", metricName="r2")
print(f"R Squared (R2) on test data = {LREvaluator.evaluate(LRPredictions)}")

lr_Model.save("stockModel")
print("Model saved Succesfully")