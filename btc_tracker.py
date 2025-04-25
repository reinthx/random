import requests
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv("btc_tracker.env")
btc_tracker_api_key = os.environ.get('BTC_TRACKER_API_KEY')

if not btc_tracker_api_key:
    raise ValueError("API key not found in environment!")

url = f"https://api.twelvedata.com/time_series/cross?base=BTC&quote=USD&interval=1day&apikey={btc_tracker_api_key}"
response = requests.get(url)
data = response.json()
print(data)
price = data['values'][0]['close']
timestamp = data['values'][0]['datetime']


conn = sqlite3.connect("btc_prices.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT UNIQUE,
        usd REALos
    )
""")

count = 0
for entry in data['values']:
    timestamp = entry['datetime']
    price = entry['close']

    c.execute("SELECT 1 FROM prices WHERE timestamp = ?", (timestamp,))
    if not c.fetchone():  # Only insert if timestamp not found
        c.execute("INSERT INTO prices (timestamp, usd) VALUES (?, ?)", (timestamp, price))
        count += 1

conn.commit()
conn.close()

print(f"{count} entries inserted.")