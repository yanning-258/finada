import json
import os
import pandas as pd
from datetime import datetime

"""
kline columns source of information:
https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints

[
    [
        1499040000000,         // Kline open time
        "0.01634790",          // Open price
        "0.80000000",          // High price
        "0.01575800",          // Low price
        "0.01577100",          // Close price
        "148976.11427815",     // Volume
        1499644799999,         // Kline Close time
        "2434.19055334",       // Quote asset volume
        308,                   // Number of trades
        "1756.87402397",       // Taker buy base asset volume
        "28.46694368",         // Taker buy quote asset volume
        "0"                    // Unused field, ignore.
    ]
]

"""

KLINE_COLUMNS = ['open_time', 'open', 'high', 'low', 'close', 'volume',
                 'close_time', 'quote_volume', 'num_trades',
                 'taker_buy_base', 'taker_buy_quote', 'ignore']


def clean_binance_ticker(symbol, date_str):
    """Clean ticker snapshot JSON → DataFrame"""
    file_path = f"data/raw/symbol/{date_str}/{symbol}.json"
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame([{
        'symbol':           data['symbol'],
        'price':            float(data['lastPrice']),
        'volume':           float(data['volume']),
        'price_change_pct': float(data['priceChangePercent']),
        'high':             float(data['highPrice']),
        'low':              float(data['lowPrice']),
        'timestamp':        datetime.now()
    }])

    # basic checks
    assert df['price'].iloc[0] > 0,  f"{symbol}: price must be > 0"
    assert df['volume'].iloc[0] > 0, f"{symbol}: volume must be > 0"
    assert df['high'].iloc[0] >= df['low'].iloc[0], f"{symbol}: high < low"

    return df


def clean_binance_ohlcv(symbol, date_str):
    """Clean kline JSON → DataFrame"""
    file_path = f"data/raw/kline/{date_str}/{symbol}.json"

    with open(file_path, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data, columns=KLINE_COLUMNS)

    # convert types
    df['open_time']  = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    df['symbol'] = symbol

    # basic checks
    assert df.isnull().sum().sum() == 0,          f"{symbol}: nulls found"
    assert (df['high'] >= df['low']).all(),        f"{symbol}: high < low"
    assert (df['high'] >= df['open']).all(),       f"{symbol}: high < open"
    assert (df['high'] >= df['close']).all(),      f"{symbol}: high < close"
    assert (df['volume'] > 0).all(),               f"{symbol}: zero volume rows"
    assert df['open_time'].is_monotonic_increasing, f"{symbol}: timestamps not sorted"
    assert df['open_time'].duplicated().sum() == 0, f"{symbol}: duplicate timestamps"

    # drop columns you don't need
    df = df[['symbol', 'open_time', 'open', 'high', 'low', 'close', 'volume']]

    return df


if __name__ == "__main__":
    date_str = datetime.now().strftime('%Y%m%d')
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']

    for symbol in symbols:
        try:
            ticker_df = clean_binance_ticker(symbol, date_str)
            ohlcv_df  = clean_binance_ohlcv(symbol, date_str)
            print(f"✅ {symbol} — ticker rows: {len(ticker_df)}, ohlcv rows: {len(ohlcv_df)}")
            print(ohlcv_df.head(2))
        except AssertionError as e:
            print(f"❌ Validation failed: {e}")
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")