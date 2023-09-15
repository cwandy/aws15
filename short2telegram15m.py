import pandas as pd
import numpy as np
import time
from datetime import datetime
import schedule
import threading
from binance.um_futures import UMFutures
from telegram import sendme

client = UMFutures()

print(client.time())
# Binance API credentials
api_key = 'KRvir4TrHPSwXhREjT3iLWOBKK3iq3Chee5A0klzqLNLNYvDJoxqj2RUaFq5k3RF'
api_secret = 'qDCqfSG8giLxVy9AOX9Qv41pi8O7a5JHxZCPknMkz8YORfe3rRvS25rWEMqztwiA'

# Initialize the Binance client
client = UMFutures(api_key, api_secret)

# Function to fetch historical price data
interval = {'1m': '1m', '15m': '15m', '1h': '1h'}

def candle_15m(interval,symbol):
    candles_15m = client.klines(symbol=symbol, interval=interval, limit=2)
    if len(candles_15m) > 0:
        candle = candles_15m[0]
        #print(f"{interval} Candle for {symbol} - Open: {candle[1]}, Close: {candle[4]}, High: {candle[2]}, Low: {candle[3]}")
        return candle[4]
    else:
        print(f"Error fetching data for {symbol}")


def loop_15m(symbol_price_list):
    while True:
        # Bu iş parçacığı her 10 dakikada bir çalışacak işi burada yapabilir.
        now = datetime.now()
        if now.minute == 1 or now.minute == 16 or now.minute == 31 or now.minute == 46:  # Dakika sıfır olduğunda (yani tam saat başı olduğunda) çalışsın
            for item in symbol_price_list:
                item['close_15m'] = (candle_15m('15m', item['symbol']))
                close_15m[item['symbol']]=(candle_15m('15m', item['symbol']))
                time.sleep(0.1)
        else:
            tickers = client.ticker_price()
            for ticker in tickers:
                symbol = ticker['symbol']
                price = ticker['price']
                anlik[symbol] = (price)
                rate_15m=(float(anlik[symbol])/float(close_15m[symbol])-1)*100
                if rate_15m>3:
                    close_15m[symbol]=anlik[symbol]
                    print(rate_15m)
                    sendme("!!!!!!!ALERT!!!!!!\n {} PUMPED!!!!!! \nPrice: {} USD\nPrice up: {}%".format(symbol, anlik[symbol], rate_15m))
            time.sleep(50)


tickers = client.ticker_price()


symbol_price_list = []
symbols = []
anlik={}
close_15m={}
for ticker in tickers:
    symbol = ticker['symbol']
    price = ticker['price']
    anlik[symbol] =  ticker['price']
    symbols.append(symbol)
    symbol_price_list.append({'symbol': symbol, 'price': price })
for item in symbol_price_list:
    item['close_15m'] = (candle_15m('15m', item['symbol']))
    close_15m[item['symbol']] = (candle_15m('15m', item['symbol']))
    time.sleep(0.05)
symbol_price_list_15=symbol_price_list


symbol_price_list_15m=threading.Thread(target=loop_15m(symbol_price_list))
symbol_price_list_15m.start()

"""
for item in symbol_price_list:
    item['close_1h']=(fetch_candlestick_data('1h', item['symbol']))
    time.sleep(0.1)
    """
