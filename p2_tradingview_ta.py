
from tradingview_ta import *
import requests

interval = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
tesla = TA_Handler(
    symbol = 'CKA',
    screener= 'vietnam',
    exchange= 'UPCOM',
    interval= Interval.INTERVAL_1_DAY
)

td = TA_Handler(symbol= 'vn30f2410', screener= 'vietnam', exchange= 'hnx', interval = '1d')


tesla = TA_Handler(
    symbol="AAPL",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY,
)

#analysis = get_multiple_analysis(screener="vietnam", interval=Interval.INTERVAL_1_DAY, symbols=['HOSE:ACB', 'HOSE:SSI', 'HOSE:NAF'])

'''
def get_stock_list():
        response = requests.get(
            'https://scanner.tradingview.com/vietnam/scan',
            headers= {'user-agent': 'Mozilla/5.0'}
        )
        if response.status_code == 200:
            data = response.json()
            stock_list = []
            
            if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                for record in data['data']:
                    stock_list.append(record.get('s').split(':'))
                return stock_list    
            logging.warning("Exright API returned no data.")
            return []
        else:
            logging.error(f"Exright Failed to fetch data. Status Code: {response.status_code}")
            return []
'''
#print(get_stock_list())
'''        
print(tesla.get_analysis().summary)
if tesla.get_analysis() is not None:
    print(tesla.indicators)
else:
    print("Function returned None")
'''
#print(tesla.get_analysis().indicators)
#print(tesla.__str__())
#print(tesla['symbol'])
#print(tesla.indicators)
#print(tesla.get_analysis().summary)
#print(tesla.get_analysis().oscillators)
#print(tesla.get_analysis().moving_averages)
#print(TradingView.search('TSLA', 'america'))
#id = td.get_analysis().indicators
#mv = td.get_analysis().moving_averages

#if td.get_indicators():
#    r = td.get_indicators()
#    print(r)
#print(td.get_analysis().summary)
#print(td.get_analysis().oscillators)
#print(td.get_analysis().moving_averages)
#print(td.get_indicators())
#print(td.indicators)

#print(type(mv['COMPUTE']['EMA30']))
#print(mv)
#print(id)

#clean_record = {}
    #print(f"{field}:{record.get(field)}")
#print(type(mv['COMPUTE']))
#print(mv['COMPUTE'].setdefault('Ichimoku', None))

url = "https://iboard-query.ssi.com.vn/exchange-index/multiple"
headers = {
    #"Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"}

# The payload you found
payload = {
    "indexIds": ["VNINDEX", "VN30", "HNX30", "VNXALL", "HNXIndex", "HNXUpcomIndex"]
}

# Sending the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the response status and content
if response.status_code == 200:
    print("Success!")
    print(response.json())  # Print the returned data (if any)
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print any error message returned
