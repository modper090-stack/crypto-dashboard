import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Binance USDT Futures Dashboard",
    layout="wide"
)

st.title("📊 Binance USDT Futures – Live Dashboard")

@st.cache_data(ttl=60)
def get_futures_data():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url, timeout=10)

    # SAFETY CHECK
    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    # If Binance returns error message
    if not isinstance(data, list):
        return pd.DataFrame()

    rows = []
    for d in data:
        if "symbol" in d and d["symbol"].endswith("USDT"):
            rows.append({
                "Symbol": d["symbol"],
                "Last Price": float(d.get("lastPrice", 0)),
                "24h Change %": float(d.get("priceChangePercent", 0)),
                "24h High": float(d.get("highPrice", 0)),
                "24h Low": float(d.get("lowPrice", 0)),
                "Volume": float(d.get("volume", 0))
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("Volume", ascending=False)

    return df


if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

df = get_futures_data()

if df.empty:
    st.warning("⚠️ Binance API busy. Please refresh after few seconds.")
else:
    st.subheader(f"Total USDT Futures Pairs: {len(df)}")
    st.dataframe(df, use_container_width=True, height=700)
