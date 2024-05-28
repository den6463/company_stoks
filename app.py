from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

app = Flask(__name__)

def save_data_to_excel(symbol, filename="stock_data.xlsx"):
    end = datetime.now()
    start = datetime(end.year - 1, end.month, end.day)
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    
    path = os.path.join(os.getcwd(), filename)
    if os.path.exists(path):
        old_data = pd.read_excel(path)
        combined_data = pd.concat([old_data, data], ignore_index=True)
        combined_data.drop_duplicates(subset='Date', keep='last', inplace=True)
    else:
        combined_data = data

    combined_data.to_excel(path, index=False)

def prepare_data(symbol):
    data = pd.read_excel('stock_data.xlsx')
    data.set_index('Date', inplace=True)
    data = data[['Close']]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    X_test = []
    for i in range(60, len(scaled_data)):
        X_test.append(scaled_data[i-60:i, 0])
    X_test = np.array(X_test)
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    
    return X_test, scaler

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symbol = request.form.get('symbol')
    save_data_to_excel(symbol)
    X_test, scaler = prepare_data(symbol)
    model = load_model('trained_model.h5')
    prediction = model.predict(X_test)
    last_prediction = scaler.inverse_transform(prediction)[-1][0]
    
    data = pd.read_excel('stock_data.xlsx')
    # Remove rows where 'Date' is NaT
    data.dropna(subset=['Date'], inplace=True)
    dates = data['Date'].dt.strftime('%Y-%m-%d').tolist()
    prices = data['Close'].tolist()
    table_data = data.head(10)

    return render_template('result.html', company_name=symbol, prediction=last_prediction, dates=dates, prices=prices, table_data=table_data)


if __name__ == "__main__":
    app.run(debug=True)
