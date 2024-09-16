import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('daily_index.csv')
df['Date'] = pd.to_datetime(df['Date'])
print(df)

vn30 = df.loc[(df['Stock'] == 'VN30')]
# Reverse the date
vn30 = vn30[::-1]
# Draw the chart
vn30.plot(x = 'Date', y = 'Price', kind = 'line', title = ' Prices Over Time')
plt.show()


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