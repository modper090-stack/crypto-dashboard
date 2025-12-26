import streamlit as st
import pandas as pd
import time
from binance.client import Client

st.set_page_config(page_title="Breaker Block Dashboard", layout="wide")

client = Client()

@st.cache_data(ttl=60)
def get_symbols():
    info = client.futures_exchange_info()
    return [s['symbol'] for s in info['symbols'] if s['quoteAsset'] == 'USDT']

def get_klines(symbol, interval, limit=100):
    return client.futures_klines(symbol=symbol, interval=interval, limit=limit)

def find_breaker(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last['close'] < prev['low']:
        return "BEARISH"
    if last['close'] > prev['high']:
        return "BULLISH"
    return None

st.title("📊 Binance USDT Futures – Breaker Block Dashboard")

symbols = get_symbols()
results = []

for sym in symbols[:30]:  # limit for API safety
    try:
        klines_15m = get_klines(sym, Client.KLINE_INTERVAL_15MINUTE, 50)
        df = pd.DataFrame(klines_15m, columns=[
            'time','open','high','low','close','vol',
            'c1','c2','c3','c4','c5','c6'
        ])
        df[['open','high','low','close']] = df[['open','high','low','close']].astype(float)

        breaker = find_breaker(df)

        if breaker:
            last = df.iloc[-1]
            entry = (last['high'] + last['low']) / 2

            results.append({
                "PAIR": sym,
                "BIAS": breaker,
                "ENTRY": round(entry, 4),
                "SL": round(last['high'] if breaker=="BEARISH" else last['low'], 4),
                "TF": "15m"
            })

        time.sleep(0.3)

    except:
        continue

if results:
    st.success("Breaker Block setups found")
    st.dataframe(pd.DataFrame(results))
else:
    st.warning("No active Breaker Block setups right now")
