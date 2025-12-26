
import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Weekly vs Daily Screener", layout="wide")

BASE_URL = "https://fapi.binance.com"

@st.cache_data(ttl=300)
def get_usdt_futures_symbols():
    url = f"{BASE_URL}/fapi/v1/exchangeInfo"
    data = requests.get(url, timeout=10).json()
    symbols = []
    for s in data["symbols"]:
        if s["quoteAsset"] == "USDT" and s["contractType"] == "PERPETUAL":
            symbols.append(s["symbol"])
    return symbols

def get_klines(symbol, interval, limit):
    url = f"{BASE_URL}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    return requests.get(url, params=params, timeout=10).json()

st.title("📊 Binance Futures Weekly vs Daily Screener")

auto = st.checkbox("🔄 Auto Refresh (5 min)", value=True)

symbols = get_usdt_futures_symbols()

results = []

with st.spinner("Scanning coins..."):
    for sym in symbols:
        try:
            w = get_klines(sym, "1w", 2)
            d = get_klines(sym, "1d", 2)

            weekly = w[-2]
            daily = d[-2]

            w_high = float(weekly[2])
            w_low = float(weekly[3])
            d_close = float(daily[4])

            if d_close > w_high:
                signal = "⬆ ABOVE WEEKLY HIGH"
            elif d_close < w_low:
                signal = "⬇ BELOW WEEKLY LOW"
            else:
                continue

            results.append({
                "Symbol": sym,
                "Weekly High": round(w_high, 4),
                "Weekly Low": round(w_low, 4),
                "Daily Close": round(d_close, 4),
                "Signal": signal
            })

        except:
            continue

df = pd.DataFrame(results)

st.subheader("📌 Signals Found")
st.dataframe(df, use_container_width=True)

st.caption(f"Total signals: {len(df)}")

if auto:
    time.sleep(300)
    st.rerun()
