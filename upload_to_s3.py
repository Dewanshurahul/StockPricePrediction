import boto3
try:
    client = boto3.client("s3")
    try:
        client.upload_file('/home/dewanshu/Desktop/DataSets/advertising.csv','stockpriceprediction','advertising.csv')
    except:
        print("Please check the input parameters")
except:
    print("connection didn't establish with AWS S3")
print("Data Uploaded...")