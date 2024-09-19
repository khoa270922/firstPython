import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('daily_index.csv')

df = df[::-1]
# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Sort by date (if not sorted already)
df = df.sort_index()

# Ensure 'Price' is numeric, forcing invalid parsing to NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

'''
# Bollinger Bands 
# are a volatility indicator in technical analysis, composed of a moving average (typically the 20-day SMA) 
# and two standard deviations above and below this average.
# BB consist of three lines: 
# Middle Band: A simple moving average (SMA) of the stock price.
# Upper/Lower Band: The middle band plus/minus two times the standard deviation of the price.
# These bands expand and contract based on market volatility, helping to identify potential breakout points.
# 
# Formula: Upper/Lower Band = MA(TP) +/- (k x ơ)
# MA is the moving average of the typical price (TP)
# TP = (High+Low+Close)/3, ơ is the standard deviation of the closing prices over the past 20 periods, k is a constant (typically 2)
# Calculate the typical price (TP)
# Breakout Indicator: When prices touch the upper or lower bands, it may signal that the stock is overbought (upper band) or oversold (lower band).
# Volatility Indicator: The wider the bands, the more volatile the stock. When the bands contract, volatility is low.
# 
# How to Use Bollinger Bands in Trading:
# Overbought Condition: When the stock price touches or exceeds the upper band, 
# it may signal overbought conditions, potentially leading to a sell.
# Oversold Condition: When the stock price touches or falls below the lower band, 
# it may indicate oversold conditions, signaling a potential buy.

df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3

# Calculate the 20-day moving average of the typical price
df['SMA_20'] = df['TP'].rolling(window=20).mean()

# Calculate the standard deviation of the typical price over the 20-day period
df['STD'] = df['TP'].rolling(window=20).std()

# Calculate the upper and lower Bollinger Bands
df['Upper Band'] = df['SMA_20'] + (2 * df['STD'])
df['Lower Band'] = df['SMA_20'] - (2 * df['STD'])

# Display the DataFrame
print(df[['Close', 'MA', 'Upper Band', 'Lower Band']])
'''


'''
# RSI (0-100)
# measures the speed and change of price movements.
# Overbought: RSI>70, meaning the stock may be overvalued and a pullback could happen.
# Oversold: RSI<30, indicating the stock may be undervalued and a rebound might occur.

def rsi(group, len):
    # Calculate the daily price change
    group['Change'] = group['Price'].diff()
    # Separate gains and losses
    group['Gain'] = group['Change'].apply(lambda x: x if x > 0 else 0)
    group['Loss'] = group['Change'].apply(lambda x: -x if x <0 else 0)
    # Calculate the average gain and average loss over a len-day period
    group['avg_gain'] = group['Gain'].rolling(window=len).mean() # window length is len of days
    group['avg_loss'] = group['Loss'].rolling(window=len).mean()
    # Calculate the relative strenth (RS)
    group['RS'] = group['avg_gain'] / group['avg_loss']
    # Calculate the RSI
    group['RSI'] = 100 - (100 / (1 + group['RS']))
    return group

vn30 = rsi(df[df['Stock'] == 'VN30'], 14)
print(vn30)
# acb['RSI'].plot(title='RSI')
# acb['RSI'].plot(x = 'Date', y = 'RSI', kind = 'line', title = 'RSI')
# acb['RSI'].plot(kind='line', title='Average Stock Price')
# plt.ylabel('RSI')
# plt.show() # Draw the chart
'''

# When to Use SMA vs EMA:
# EMA reacts faster to price changes compared to SMA, 
# as it assigns more weight to recent data points.
# SMA: Useful for long-term trend analysis. 
# It's less sensitive to short-term fluctuations and provides a smoother line.
# EMA: Better for short-term analysis. It reacts quicker to price changes, 
# making it more useful for spotting potential trend reversals.

'''
# Exponential Moving Average (EMA) gives more weight to recent prices, 
# making it more responsive to recent changes in stock prices.
# Formula: EMA_today = (P_today x a) + (EMA_yesterday x (1 - a))
# a = 2/ (n+1) is the smoothing factor, n is the number of periods 

def ema(group, len):
    group[f'ema{len}'] = group['Price'].ewm(span=len, adjust=False).mean()
    return group

df = df.groupby('Stock').apply(ema, len=3, include_groups=False)
print(df)
'''

'''
# Simple Moving Averate (SMA)
# the arithmetic mean of a set of prices over a specified period.
# Moving averages help smooth out price fluctuations to identify trends.
def sma(group, len):
    group[f'sma{len}'] = group['Price'].rolling(window=len).mean()
    return group

#acb = df[df['Stock'] == 'ACB']
#acb = sma(acb, 3)
#df = df.groupby('Stock').apply(lambda x: sma(x, len=3, include_groups=False))
df = df.groupby('Stock').apply(sma, len=3, include_groups=False)
print(df)
'''

'''
# Logarithmic Returns with NumPy
def cal_log_return(group):
    group['log_return'] = np.log(group['Price'] / group['Price'].shift(1))
    return group

df = df.groupby('Stock').apply(cal_log_return)
print(df)
'''

'''
# Calculate Cumulative Returns
# the total change in the price of an asset (such as a stock) 
# over a specific period, expressed as a percentage of the initial price.

def cal_cum_re(group):
    init_price = group['Price'].iloc[0] # Get the initial price (P_0)
    # Calculate the cumulative return: (P_t - P_0) / P_0
    group['Cumulative Return'] = (group['Price'] - init_price) / init_price
    # If you want the return as a percentage, multiply by 100
    group['Cumulative Return (%)'] = group['Cumulative Return'] * 100
    return group

# Applies the function calculate_cumulative_return() to each group (i.e., stock) separately.
df = df.groupby('Stock').apply(cal_cum_re)
print(df)
'''

'''
# Calculating Daily Returns
# the percentage change in stock prices from one day to the next.

df['Daily_return'] =df[df['Stock'] == 'ACB']['Price'].pct_change()
print(df[df['Stock'] == 'ACB'])
'''

'''
# Filter the data for specific stock
acb = df[df['Stock'] == 'VN30']
try:
    # need to use .groupby('Stock') before resampling to avoid issues, 
    # especially when dealing with multiple categories.
    acb_wap = acb.groupby('Stock').resample('W').mean()
    print(acb_wap)
except Exception as e:
    print("Error:", e)
'''

'''
#  Resampling Time Series Data
weekly_avg_prices = df.groupby('Stock').resample('W').mean()
print(weekly_avg_prices)
'''

'''
df.groupby(['Stock' == 'ACB']).plot(x = 'Date', y = 'Price', kind = 'line', title = ' Prices Over Time')
plt.show()
'''

'''
vn30 = df.loc[(df['Stock'] == 'VN30')]
vn30 = vn30[::-1] # Reverse the date
vn30.plot(x = 'Date', y = 'Price', kind = 'line', title = ' Prices Over Time')
plt.show() # Draw the chart
'''

'''
df = pd.read_csv('daily_index.csv')
# Get all VN30 daily indices
vn30 = df.loc[(df['Stock'] == 'VN30')]
# Reverse the date
vn30 = vn30[::-1]
# Draw the chart
vn30.plot(x = 'Date', y = 'Price', kind = 'line', title = ' Prices Over Time')
plt.show()
'''

'''
# Grouping and plotting the average price for each stock
grouped = df.groupby('Stock')['Price'].mean()
grouped.plot(kind='bar', title='Average Stock Price')
plt.ylabel('Price')
plt.show()
'''

'''
df.groupby('Stock') == ''
df.plot(x = 'Date', y = 'Price', kind = 'line', title = 'Stock Prices Over Time')
plt.show()
'''

'''
print(df.loc[(df['Stock'] == 'VN30')])
mean_group = df.groupby('Stock')['Price'].mean()
max_group = df.groupby('Stock')['Price'].max()
min_group = df.groupby('Stock')['Price'].min()
print(mean_group)
print(max_group)
print(min_group)
'''

'''
import csv
with open('VN30.csv', 'r') as file:
    csv_reader = csv.reader(file)
    head = []
    lp_test = []
    with open('daily_index.csv', 'w', newline='') as file:
       csvwriter = csv.writer(file)
       csvwriter.writerow(['Date', 'Stock', 'Price'])
       for index, row in enumerate(csv_reader):
        if index == 0:
            head = row
        else:
            for i in range(1, len(row)):
               csvwriter.writerow([row[0], head[i], row[i]])
'''
    
#prices = df['Price']
#print(prices)
#high_price_stocks = df[df['Price']> 100]
#print(high_price_stocks)
#df['SMA5'] = df['Price'].rolling(window=5).mean()
#print(df[['Price', 'SMA5']])
#print(df.head())

'''
# Creating a dummy DataFrame with stock data
data = {
    'Stock': ['AAPL', 'GOOG', 'AMZN', 'TSLA', 'MSFT', 'NFLX', 'FB', 'NVDA', 'BABA', 'ORCL'],
    'Date': ['2024-01-01', '2024-01-01', '2024-01-01', '2024-01-01', '2024-01-01',
             '2024-01-02', '2024-01-02', '2024-01-02', '2024-01-02', '2024-01-02'],
    'Price': [150, 2800, 3400, 1100, 300, 600, 330, 220, 240, 280]
}

# Creating the DataFrame
df = pd.DataFrame(data)

# Saving the DataFrame to a CSV file
df.to_csv('dummy_stock_data.csv', index=False)
'''

# Create a stock_data.csv file with sample stock data (e.g., stock name, price, date).
# Write a Python program to read and print this CSV file.
'''
import csv

with open('vib_20240911', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)

    print(header)
    for line in csvreader:
        print(line)

with open('trade_log.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(['Stock', 'Action', 'Price', 'Quantity'])
    csvwriter.writerow(['XYZ', 'Buy', 50, 100])
    csvwriter.writerow(['ABC', 'Sell', 45, 200])


with open('trade_log.csv', 'r') as file:
    csvreader = csv.reader(file)
    #header = next(csvreader)    
    for line in csvreader:
        print(line)
'''

# Write a program that writes a list of numbers to a file. 
# Then, read the numbers from the file and print them.
'''
# List of numbers to write to the file
list_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Open a file for writing (creates the file if it doesn't exist)
with open("list_num.txt", "w") as f:
    # Write each number to the file, each on a new line
    for number in list_num:
        f.write(f"{number}\n")

# Step 2: Reading numbers from the file
with open("list_num.txt", "r") as f:
    lines = f.readlines()
    numbers_from_file = [int(line.strip()) for line in lines]
    print(numbers_from_file)
'''