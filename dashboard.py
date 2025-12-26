import streamlit as st
import pandas as pd
import requests
import time
import os

st.set_page_config(page_title="Breaker Block Dashboard", layout="wide")

API_KEY = os.getenv("BINANCE_API_KEY", "")
HEADERS = {"X-MBX-APIKEY": API_KEY}

BASE_URL = "https://fapi.binance.com"

@st.cache_data(ttl=120)
def get_symbols():
    url = f"{BASE_URL}/fapi/v1/exchangeInfo"
    r = requests.get(url, headers=HEADERS, timeout=10)
    data = r.json()
    return [s["symbol"] for s in data["symbols"] if s["quoteAsset"] == "USDT"]

def get_klines(symbol, interval, limit=50):
    url = f"{BASE_URL}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    return r.json()

def find_breaker(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if last["close"] < prev["low"]:
        return "SHORT"
    if last["close"] > prev["high"]:
        return "LONG"
    return None

st.title("📊 Binance Futures Breaker Block Screener")

symbols = get_symbols()
results = []

progress = st.progress(0)
total = min(len(symbols), 25)

for i, sym in enumerate(symbols[:25]):
    try:
        kl = get_klines(sym, "15m")
        df = pd.DataFrame(kl, columns=[
            "time","open","high","low","close","vol",
            "c1","c2","c3","c4","c5","c6"
        ])
        df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)

        direction = find_breaker(df)
        if direction:
            last = df.iloc[-1]
            entry = round((last["high"] + last["low"]) / 2, 4)
            sl = round(last["high"] if direction == "SHORT" else last["low"], 4)

            results.append({
                "PAIR": sym,
                "BIAS": direction,
                "ENTRY": entry,
                "SL": sl,
                "TF": "15m"
            })

        time.sleep(0.4)
        progress.progress((i + 1) / total)

    except:
        continue

progress.empty()

if results:
    st.success("✅ Valid Breaker Block setups found")
    st.dataframe(pd.DataFrame(results))
else:
    st.warning("❌ No valid setups right now — wait or refresh later")
