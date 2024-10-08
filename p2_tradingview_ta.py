from tradingview_ta import TradingView, TA_Handler, Interval, Exchange
'''
interval = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
tesla = TA_Handler(
    symbol = 'ACB',
    screener= 'vietnam',
    exchange= 'HOSE',
    interval= Interval.INTERVAL_1_MONTH
)
'''

tesla = TA_Handler(
    symbol="AAPL",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)

#print(tesla.get_analysis().indicators)
print(tesla.get_analysis().summary)
#print(tesla.get_analysis().oscillators)
#print(tesla.get_analysis().moving_averages)
#print(TradingView.search('TSLA', 'america'))