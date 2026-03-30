import requests, json, os
from datetime import datetime
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
#import yfinance as yf
import pandas as pd
from typing import List, Dict

#fetch bitcoin price from Binance

#Assets
URL_SUF_binance = "https://api.binance.com/api/v3/ticker/24hr?symbol="
URL_SUF_bin_kline = "https://api.binance.com/api/v3/klines?symbol="
URL_SUF_yf = ""
CRYPTO_SYMBOLS =  ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
STOCK_SYMBOLS = ['NVDA', 'TSM', 'GOOG']
ASSETS_SYMBOLS = ['GLD', '^VIX']

"""
BINANCE:
# Get current price for one coin
url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"

# Get historical data (klines/candlesticks)
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=7"
"""


#fetch price info for symbols
def fetch_binance(url_suf, symbols):
    
    #for each symbol in the binance symbol list
    for symbol in symbols:
        try: 
            now = datetime.now()
            folder_path = f"data/raw/symbol/{now.strftime('%Y%m%d')}"
            file_path = f"{folder_path}/{symbol}.json"

            #skip if already dowloaded today
            if os.path.exists(file_path):
                print(f"Skipping {symbol} - already exist")
                continue
            
            url = url_suf + symbol
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            os.makedirs(folder_path, exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {symbol} to {file_path}")

        except Exception as e:
            print(f"Failed: {e}")
            continue
        # data_list.append({
        #     'symbol': symbol,
        #     'price': float(data['lastPrice']),
        #     'volume': float(data['volume']),
        #     'price_change_pct': float(data['priceChangePercent']),
        #     'timestamp': datetime.now()
        # })
    
        # df = pd.DataFrame(data_list)

        # #save to csv
        # csv_name = f"crypto_prices_{symbol}.csv"
        # df.to_csv(csv_name, index=False)
        # print(f"Data saved to {csv_name}")

def fetch_binance_ohlcv(url_suf, symbols):
    """Fetch OHLC + Volume for each symbol, for candlestick chart"""
    for symbol in symbols:
        try: 
            now = datetime.now()
            folder_path = f"data/raw/kline/{now.strftime('%Y%m%d')}"
            file_path = f"{folder_path}/{symbol}.json"

            #skip if already dowloaded today
            if os.path.exists(file_path):
                print(f"Skipping kline {symbol} - already exist")
                continue
            
            url = url_suf + symbol + "&interval=1d&limit=365"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            os.makedirs(folder_path, exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {symbol} to {file_path}")

        except Exception as e:
            print(f"Failed: {e}")
            continue


"""
main flow
- call load
- call clean
- call store
"""

#clean..clean what clean...they set api so beautiful, necessary meh



if __name__== "__main__":
    fetch_binance(URL_SUF_binance, CRYPTO_SYMBOLS)
    fetch_binance_ohlcv(URL_SUF_bin_kline, CRYPTO_SYMBOLS)
