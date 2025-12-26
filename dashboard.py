import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Binance USDT Futures Dashboard", layout="wide")

st.title("📊 Binance USDT Futures – Live Dashboard")

@st.cache_data(ttl=60)
def get_futures_data():
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    data = requests.get(url, timeout=10).json()

    rows = []
    for d in data:
        if d["symbol"].endswith("USDT"):
            rows.append({
                "Symbol": d["symbol"],
                "Last Price": float(d["lastPrice"]),
                "24h Change %": float(d["priceChangePercent"]),
                "24h High": float(d["highPrice"]),
                "24h Low": float(d["lowPrice"]),
                "Volume": float(d["volume"])
            })

    df = pd.DataFrame(rows)
    df = df.sort_values("Volume", ascending=False)
    return df

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

df = get_futures_data()

st.subheader(f"Total USDT Futures Pairs: {len(df)}")

st.dataframe(
    df,
    use_container_width=True,
    height=700
)
