import time
import datetime
import requests
import json
import pandas as pd

today = datetime.date.today()
#today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
from_date = round(time.mktime((today.year - 1, today.month, today.day, 0, 0, 0, 0, 0, 0)))
to_date = round(time.mktime((today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)))
#print(from_date, to_date)

LIST_STOCK = ('ACB', 'VNM')
INTERVAL = '1D'
ssi_url = 'https://iboard-api.ssi.com.vn/statistics/charts/history?resolution=' + INTERVAL + '&symbol=' + LIST_STOCK[0] + '&from=' + str(from_date) + '&to=' + str(to_date)
vietstock_url = 'https://api.vietstock.vn/ta/history?symbol=' + LIST_STOCK[0] + '&resolution=D&from=' + str(from_date) + '&to=' + str(to_date)

vietstock_headers = {
    'Referer': 'https://ta.vietstock.vn',
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Host': 'api.vietstock.vn',
    'Accept-Encoding': 'gzip,deflate, br',
    'Connection': 'keep-alive',
}

#print(ssi_url)
print(vietstock_url)
response = requests.get(vietstock_url, headers = vietstock_headers)
if response.status_code == 200:
    data = response.json()
    body = json.loads(data)
    day = body['t']
    high = body['h']
    low = body['l']
    open = body['o']
    close = body['c']
    volume = body['v']
    # Create data frame
    df = pd.DataFrame({'Time': day, 'High': high, 'Low': low, 'Open': open, 'Close': close, 'Volume': volume})
    df['Date'] = pd.to_datetime(df['Time'],unit='s')
    df['Stock'] = LIST_STOCK[0]
    print(df)
else:
    print(f"fail: {response.status_code} {response.text}")