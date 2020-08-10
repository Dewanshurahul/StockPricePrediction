# StockPricePrediction
This project focuses on predicting Google stock price on real time data.I used past 4 years worth of historical Google Stock Data for training and built an Machine Learning Model for predicting Stock Prices and displayed the predictions on webpage using Flask, Kafka and Highcharts. And I have deployed the project on AWS EC2 instance unsing nginx and Gunicorn3.

# Prerequisites :
  - Python3
  - Java 8
  - Kafka
  - pyspark
  - Important Python Libraries in Requirement.txt file
# Requirements for Project :
  - Create an AWS account.
  - Login after the account has been successfully created.
  - Now go to IAM in Identity and Access Management services and setup a user with programming access and give full access to the user.
  - After the setup, download as CSV file the Public Access Key and Secret Access Key.
  
# Step 1 :   
  - Install the Amazon CLI (Command Line Interface) on your local machine. (requires snap)
  ```sh
  - $ sudo snap install awscli
  ```
  - Configure AWS_CLI with AWS credentials : 
  ```sh
  - $ aws config
  ```
  - And provide both Access Keys and Security Access Key
  - Leave Other Requirement as Default
# Step 2 : 
Now, we will upload the DataSet into AWS S3 which will be used for Model Training and Testing Purpose.
  - Create a Bucket on Aws S3
  - Run the File named upload_to_s3.py (this will upload the on AWS S3 from local System)
And we will Clean our DataSet And Train our Model
  - Run python file named cleaning_training_testing.py (this will Clean, Train and Save the Model)
# Step 3 : 
  - Install Kafka
  ```sh
  $ wget "http://apachemirror.wuchna.com/kafka/2.5.0/kafka_2.12-2.5.0.tgz"
  $ tar xzf kafka_2.12-2.5.0.tgz
  ```
  -Now run Zookeeper and Kafka Server (After getting into Kafka directory) : 
  ```sh
  $ ./bin/zookeeper-server-start.sh config/zookeeper.properties
  $ ./bin/kafka-server-start.sh config/server.properties
  ```
  # Step 4 : 
    - Create producre.py
    - Create consumer.py 
    - Create app.py
    - Write index.html (for visualising the graph over the Web-Browser)
    - Create requirement.txt file with important python-libraries used in Project
    
  First run producer.py file and then run app.py file and enter the URL given by app.py on Web Browser to Visualise the Graph.
  
  # Deployment : 
  - Create an instance on AWS EC2 [FOLLOW VIDEO](https://www.youtube.com/watch?v=-Gc8CMjQZfc&list=PL5KTLzN85O4KTCYzsWZPTP0BfRj6I_yUP)
    - ssh into your instance using downloaded .pem file while creating instance
    ```sh
    $ ssh -i fileName.pem ubuntu@<IP ADDERSS>(provided by AWS instance)
    ```
    - Follow the prerequsits and Download part
    - For downloading user python-libraries
    ```sh
    $ pip3 install -r Requirements.txt
    ```
    - Clone Project on instance using git clone Command
    ```sh
    git clone "https://github.com/Dewanshurahul/StockPricePrediction.git"
    ```
    - For running the flask app on AWS, we need two additional packages: nginx and gunicorn3 (for Python3)
    - Install nginx and Gunicorn3
    ```sh
    $ sudo apt-get install nginx
    $ sudo apt-get install Gunicorn3
    ```
    - Now go in the sites-enabled folder inside nginx and do the following :
    ```sh
    $ cd /etc/nginx/sites-enabled/
    $ sudo nano flaskapp
    ```
    - Inside the flaskapp file add the following :
    ```sh
    server{
	        listen : 80;
	        server_name : your.elastic.IP;
	        location / {
		              proxy_pass http://127.0.0.1:8000;
	        }
	}
    ```
    - Save the above file and restart the nginx service.
    ```sh
    $ sudo service nginx restart
    ```
    - Download and untar Kafka same as on Done on Local System
    - Run Zookeeper and Kafka Server
    - Run producer.py
    ```sh 
    $ python3 producer.py
    ```
    - Run app.py
    ```sh
    $ gunicorn3 --threads=4 app:app
    ```
    - Enter the Provided IP Adderss to Web-Browser for Visualising Graph
    
