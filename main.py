from binance.client import Client
from datetime import datetime
import time

# ================= SETTINGS =================
REFRESH = 300  # 5 minutes
# ===========================================

client = Client()

def klines(symbol, interval, limit):
    return client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

def weekly_sweep(symbol):
    w = klines(symbol, Client.KLINE_INTERVAL_1WEEK, 3)

    if float(w[-1][2]) > float(w[-2][2]):
        return "HIGH"

    if float(w[-1][3]) < float(w[-2][3]):
        return "LOW"

    return None

def daily_close(symbol):
    d = klines(symbol, Client.KLINE_INTERVAL_1DAY, 2)

    if float(d[-1][4]) > float(d[-1][1]):
        return "UP"
    else:
        return "DOWN"

def m15_breaker(symbol, side):
    m = klines(symbol, Client.KLINE_INTERVAL_15MINUTE, 6)

    if side == "LONG":
        return float(m[-1][2]) > float(m[-3][2])

    if side == "SHORT":
        return float(m[-1][3]) < float(m[-3][3])

    return False

# ================= PAIRS =================

pairs = [
    s["symbol"]
    for s in client.get_exchange_info()["symbols"]
    if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
]

# ================= MAIN LOOP =================

while True:
    rows = []

    for pair in pairs:
        try:
            ws = weekly_sweep(pair)
            if not ws:
                continue

            dc = daily_close(pair)

            if ws == "LOW" and dc == "UP" and m15_breaker(pair, "LONG"):
                rows.append((pair, "LOW", "UP", "CONFIRM", "LONG"))

            if ws == "HIGH" and dc == "DOWN" and m15_breaker(pair, "SHORT"):
                rows.append((pair, "HIGH", "DOWN", "CONFIRM", "SHORT"))

        except Exception as e:
            continue

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="300">
<style>
body {{ background:#0e1117; color:white; font-family:Arial; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ border:1px solid #30363d; padding:8px; text-align:center; }}
th {{ background:#161b22; }}
tr.LONG {{ background:#0f5132; }}
tr.SHORT {{ background:#842029; }}
</style>
</head>
<body>
<h2>ðŸ“Š PRO ICT CRYPTO DASHBOARD (24Ã—7)</h2>
<p>Last update: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}</p>
<table>
<tr>
<th>PAIR</th><th>WEEKLY</th><th>DAILY</th><th>15M</th><th>SETUP</th>
</tr>
"""

    for r in rows:
        html += f"<tr class='{r[4]}'><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"

    html += "</table></body></html>"

    with open("dashboard.html", "w") as f:
        f.write(html)

    time.sleep(REFRESH)from binance.client import Client
from datetime import datetime
import time

# ================= SETTINGS =================
REFRESH = 300  # 5 minutes
# ===========================================

client = Client()

def klines(symbol, interval, limit):
    return client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

def weekly_sweep(symbol):
    w = klines(symbol, Client.KLINE_INTERVAL_1WEEK, 3)

    if float(w[-1][2]) > float(w[-2][2]):
        return "HIGH"

    if float(w[-1][3]) < float(w[-2][3]):
        return "LOW"

    return None

def daily_close(symbol):
    d = klines(symbol, Client.KLINE_INTERVAL_1DAY, 2)

    if float(d[-1][4]) > float(d[-1][1]):
        return "UP"
    else:
        return "DOWN"

def m15_breaker(symbol, side):
    m = klines(symbol, Client.KLINE_INTERVAL_15MINUTE, 6)

    if side == "LONG":
        return float(m[-1][2]) > float(m[-3][2])

    if side == "SHORT":
        return float(m[-1][3]) < float(m[-3][3])

    return False

# ================= PAIRS =================

pairs = [
    s["symbol"]
    for s in client.get_exchange_info()["symbols"]
    if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
]

# ================= MAIN LOOP =================

while True:
    rows = []

    for pair in pairs:
        try:
            ws = weekly_sweep(pair)
            if not ws:
                continue

            dc = daily_close(pair)

            if ws == "LOW" and dc == "UP" and m15_breaker(pair, "LONG"):
                rows.append((pair, "LOW", "UP", "CONFIRM", "LONG"))

            if ws == "HIGH" and dc == "DOWN" and m15_breaker(pair, "SHORT"):
                rows.append((pair, "HIGH", "DOWN", "CONFIRM", "SHORT"))

        except Exception as e:
            continue

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="300">
<style>
body {{ background:#0e1117; color:white; font-family:Arial; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ border:1px solid #30363d; padding:8px; text-align:center; }}
th {{ background:#161b22; }}
tr.LONG {{ background:#0f5132; }}
tr.SHORT {{ background:#842029; }}
</style>
</head>
<body>
<h2>ðŸ“Š PRO ICT CRYPTO DASHBOARD (24Ã—7)</h2>
<p>Last update: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}</p>
<table>
<tr>
<th>PAIR</th><th>WEEKLY</th><th>DAILY</th><th>15M</th><th>SETUP</th>
</tr>
"""

    for r in rows:
        html += f"<tr class='{r[4]}'><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"

    html += "</table></body></html>"

    with open("dashboard.html", "w") as f:
        f.write(html)

    time.sleep(REFRESH)from binance.client import Client
from datetime import datetime
import time

# ================= SETTINGS =================
REFRESH = 300  # 5 minutes
# ===========================================

client = Client()

def klines(symbol, interval, limit):
    return client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

def weekly_sweep(symbol):
    w = klines(symbol, Client.KLINE_INTERVAL_1WEEK, 3)

    if float(w[-1][2]) > float(w[-2][2]):
        return "HIGH"

    if float(w[-1][3]) < float(w[-2][3]):
        return "LOW"

    return None

def daily_close(symbol):
    d = klines(symbol, Client.KLINE_INTERVAL_1DAY, 2)

    if float(d[-1][4]) > float(d[-1][1]):
        return "UP"
    else:
        return "DOWN"

def m15_breaker(symbol, side):
    m = klines(symbol, Client.KLINE_INTERVAL_15MINUTE, 6)

    if side == "LONG":
        return float(m[-1][2]) > float(m[-3][2])

    if side == "SHORT":
        return float(m[-1][3]) < float(m[-3][3])

    return False

# ================= PAIRS =================

pairs = [
    s["symbol"]
    for s in client.get_exchange_info()["symbols"]
    if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
]

# ================= MAIN LOOP =================

while True:
    rows = []

    for pair in pairs:
        try:
            ws = weekly_sweep(pair)
            if not ws:
                continue

            dc = daily_close(pair)

            if ws == "LOW" and dc == "UP" and m15_breaker(pair, "LONG"):
                rows.append((pair, "LOW", "UP", "CONFIRM", "LONG"))

            if ws == "HIGH" and dc == "DOWN" and m15_breaker(pair, "SHORT"):
                rows.append((pair, "HIGH", "DOWN", "CONFIRM", "SHORT"))

        except Exception as e:
            continue

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="300">
<style>
body {{ background:#0e1117; color:white; font-family:Arial; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ border:1px solid #30363d; padding:8px; text-align:center; }}
th {{ background:#161b22; }}
tr.LONG {{ background:#0f5132; }}
tr.SHORT {{ background:#842029; }}
</style>
</head>
<body>
<h2>ðŸ“Š PRO ICT CRYPTO DASHBOARD (24Ã—7)</h2>
<p>Last update: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}</p>
<table>
<tr>
<th>PAIR</th><th>WEEKLY</th><th>DAILY</th><th>15M</th><th>SETUP</th>
</tr>
"""

    for r in rows:
        html += f"<tr class='{r[4]}'><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"

    html += "</table></body></html>"

    with open("dashboard.html", "w") as f:
        f.write(html)

    time.sleep(REFRESH)from binance.client import Client
from datetime import datetime
import time

# ================= SETTINGS =================
REFRESH = 300  # 5 minutes
# ===========================================

client = Client()

def klines(symbol, interval, limit):
    return client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

def weekly_sweep(symbol):
    w = klines(symbol, Client.KLINE_INTERVAL_1WEEK, 3)

    if float(w[-1][2]) > float(w[-2][2]):
        return "HIGH"

    if float(w[-1][3]) < float(w[-2][3]):
        return "LOW"

    return None

def daily_close(symbol):
    d = klines(symbol, Client.KLINE_INTERVAL_1DAY, 2)

    if float(d[-1][4]) > float(d[-1][1]):
        return "UP"
    else:
        return "DOWN"

def m15_breaker(symbol, side):
    m = klines(symbol, Client.KLINE_INTERVAL_15MINUTE, 6)

    if side == "LONG":
        return float(m[-1][2]) > float(m[-3][2])

    if side == "SHORT":
        return float(m[-1][3]) < float(m[-3][3])

    return False

# ================= PAIRS =================

pairs = [
    s["symbol"]
    for s in client.get_exchange_info()["symbols"]
    if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
]

# ================= MAIN LOOP =================

while True:
    rows = []

    for pair in pairs:
        try:
            ws = weekly_sweep(pair)
            if not ws:
                continue

            dc = daily_close(pair)

            if ws == "LOW" and dc == "UP" and m15_breaker(pair, "LONG"):
                rows.append((pair, "LOW", "UP", "CONFIRM", "LONG"))

            if ws == "HIGH" and dc == "DOWN" and m15_breaker(pair, "SHORT"):
                rows.append((pair, "HIGH", "DOWN", "CONFIRM", "SHORT"))

        except Exception as e:
            continue

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="300">
<style>
body {{ background:#0e1117; color:white; font-family:Arial; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ border:1px solid #30363d; padding:8px; text-align:center; }}
th {{ background:#161b22; }}
tr.LONG {{ background:#0f5132; }}
tr.SHORT {{ background:#842029; }}
</style>
</head>
<body>
<h2>ðŸ“Š PRO ICT CRYPTO DASHBOARD (24Ã—7)</h2>
<p>Last update: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}</p>
<table>
<tr>
<th>PAIR</th><th>WEEKLY</th><th>DAILY</th><th>15M</th><th>SETUP</th>
</tr>
"""

    for r in rows:
        html += f"<tr class='{r[4]}'><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"

    html += "</table></body></html>"

    with open("dashboard.html", "w") as f:
        f.write(html)

    time.sleep(REFRESH)