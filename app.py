from flask import Flask, render_template, make_response
import json
import consumer
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    predicted_price, real_price, date = consumer.stock_price_prediction()
    date = int(datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%s')) * 1000
    data = [date, predicted_price, real_price]
    response = make_response(json.dumps(data))
    response.content_type = "application/json"
    time.sleep(2)
    return response

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, passthrough_errors=True)
