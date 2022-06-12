from pymongo import MongoClient
import requests                    # for "get" request to API
import json                        # parse json into a list
import pandas as pd                # working with data frames
import datetime as dt
from binance import Client
apikey = ''
secret = ''
client = Client(apikey, secret)


client_mongo = MongoClient('mongodb+srv://root:lm7bo6csfi7Lp5le@cluster0.gzaqw.mongodb.net/root?retryWrites=true&w=majority')
db = client_mongo.get_database('klines')

def data_spot(symbol,date):
    historical = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, date)
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open Time', 'open', 'high', 'low', 'close', 'volume', 'Close Time', 'Quote Asset Volume',
                       'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
    hist_df['datetime'] = pd.to_datetime(hist_df['Close Time'] / 1000, unit='s')
    df = hist_df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    if (len(df.index) == 0):
        return None
    df.open = df.open.astype("float")
    df.high = df.high.astype("float")
    df.low = df.low.astype("float")
    df.close = df.close.astype("float")
    df.volume = df.volume.astype("float")
    return df


def get_data_1h(n):
    records=db.klines_records
    df= pd.DataFrame(list(records.find()))
    df=df.head(n).reset_index()
    return df

def get_data_1d():
    records = db.klines_records_day
    df = pd.DataFrame(list(records.find()))
    return df

def get_Future_price(symbol, interval, startTime, endTime):
    url = "https://fapi.binance.com//fapi/v1/klines"
    #startTime = str(int(startTime.timestamp() * 1000))
    #endTime = str(int(endTime.timestamp() * 1000))
    limit = '1500' 
    req_params = {"symbol" : symbol, 'interval' : interval, 'startTime' : startTime, 'endTime' : endTime, 'limit' : limit}
    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))
    if (len(df.index) == 0):
        return None
    df = df.iloc[:, 0:6]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    df['datetime'] = pd.to_datetime(df['datetime']/1000, unit='s')
    df.open = df.open.astype("float")
    df.high = df.high.astype("float")
    df.low = df.low.astype("float")
    df.close = df.close.astype("float")
    df.volume = df.volume.astype("float")
    return df
