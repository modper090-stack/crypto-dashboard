import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Binance USDT Futures Dashboard",
    layout="wide"
)

st.title("📊 Binance USDT Futures – Live Dashboard")

@st.cache_data(ttl=300)
def get_futures_data():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except:
        return pd.DataFrame()

    if "symbols" not in data:
        return pd.DataFrame()

    rows = []
    for s in data["symbols"]:
        if (
            s.get("quoteAsset") == "USDT"
            and s.get("contractType") == "PERPETUAL"
            and s.get("status") == "TRADING"
        ):
            rows.append({
                "Symbol": s["symbol"],
                "Base Asset": s["baseAsset"],
                "Status": s["status"]
            })

    return pd.DataFrame(rows)
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url, timeout=10)

    # SAFETY CHECK
    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    # If Binance returns error message
    if not isinstance(data, list):
        return pd.DataFrame()

    
