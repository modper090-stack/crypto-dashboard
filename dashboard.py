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


if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

df = get_futures_data()

if df.empty:
    st.warning("⚠️ Binance API busy. Please refresh after few seconds.")
else:
    st.subheader(f"Total USDT Futures Pairs: {len(df)}")
    st.dataframe(df, use_container_width=True, height=700)
