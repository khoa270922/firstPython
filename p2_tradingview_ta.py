from tradingview_ta import *

interval = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
tesla = TA_Handler(
    symbol = 'CKA',
    screener= 'vietnam',
    exchange= 'UPCOM',
    interval= Interval.INTERVAL_1_DAY
)

td = TA_Handler(symbol= 'HCM', screener= 'vietnam', exchange= 'HOSE', interval = '1d')
'''

tesla = TA_Handler(
    symbol="AAPL",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY,
    time = '2024-10-08 11:46:33.120935'
)
#analysis = get_multiple_analysis(screener="vietnam", interval=Interval.INTERVAL_1_DAY, symbols=['HOSE:ACB', 'HOSE:SSI', 'HOSE:NAF'])
'''
print(tesla.get_analysis().summary)
if tesla.get_analysis() is not None:
    print(tesla.indicators)
else:
    print("Function returned None")
#print(tesla.get_analysis().indicators)
#print(tesla.__str__())
#print(tesla['symbol'])
#print(tesla.indicators)
#print(tesla.get_analysis().summary)
#print(tesla.get_analysis().oscillators)
#print(tesla.get_analysis().moving_averages)
#print(TradingView.search('TSLA', 'america'))