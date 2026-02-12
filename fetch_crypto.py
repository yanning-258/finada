import requests
import json
from datetime import datetime
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
import pandas as pd

#fetch bitcoin price from Binance

#Assets
URL_SUF = "https://api.binance.com/api/v3/ticker/24hr?symbol="
SYMBOLS =  ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']

"""
BINANCE:
# Get current price for one coin
url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"

# Get historical data (klines/candlesticks)
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=7"
"""


#fetch price info for symbols
data_list = []
for symbol in SYMBOLS:
    url = URL_SUF + symbol
    response = requests.get(url)
    data = response.json()

    data_list.append({
        'symbol': symbol,
        'price': float(data['lastPrice']),
        'volume': float(data['volume']),
        'price_change_pct': float(data['priceChangePercent']),
        'timestamp': datetime.now()
    })
    
df = pd.DataFrame(data_list)
print(df)

#save to csv
csv_name = 'crypto_prices.csv'
df.to_csv(csv_name, index=False)
print(f"Data saved to {csv_name}")