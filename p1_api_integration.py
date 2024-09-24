import psycopg2
# connection info
connection = psycopg2.connect(
    host="104.199.242.171",
    database="trading-data",
    user="trading_user",
    password="123456"
)
cursor = connection.cursor()

# Example query to check connection
cursor.execute("SELECT version();")
db_version = cursor.fetchone()
print(f"Connected to: {db_version}")

cursor.close()
connection.close()

'''
import requests

# Step 1: Function to authenticate and retrieve Bearer token
def get_bearer_token():
    # Define the authentication endpoint
    auth_url = 'https://auth.fiintrade.vn/'  # Replace with your actual auth endpoint
    
    # Define the login payload (credentials)
    login_payload = {
        'username': 'StoxPlus.FiinTrade.SPA',  # Replace with your actual username
        'password': 'yfiin%**(trade'   # Replace with your actual password
    }
    
    # Make the POST request to authenticate
    response = requests.post(auth_url, json=login_payload)
    
    # Check if authentication was successful
    if response.status_code == 200:
        # Extract the token from the response (assuming it's returned as a JSON object)
        token = response.json().get('token')  # Adjust the key based on actual response
        if token:
            print("Token retrieved:", token)
            return token
        else:
            raise Exception("Token not found in the response.")
    else:
        raise Exception(f"Failed to authenticate. Status Code: {response.status_code}")

token = get_bearer_token()
print(token)
# Step 2: Function to make API request with the Bearer token
def get_data_with_token():
    # Retrieve the token using the authentication function
    token = get_bearer_token()

    # Define the data API endpoint
    api_url = 'https://core.fiintrade.vn/your-endpoint'  # Replace with your actual API endpoint
    
    # Define the headers including the Bearer token
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',  # Use the token retrieved
        'user-agent': 'Mozilla/5.0'
    }
    
    # Make the GET request to the API with the Bearer token
    response = requests.get(api_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse and return the JSON response
        data = response.json()
        print("Data:", data)
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")

# Run the data fetching function
#get_data_with_token()
'''


# API Integration for Real-Time Stock Data
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Step 1: Set up the WebDriver (Example: Chrome)
#driver_path = 'D:/python/chromedriver/chromedriver.exe'  # Update this path
driver = webdriver.Chrome()

# Step 2: Open the target website
url = 'https://fiintrade.vn/'  # Replace with the actual URL of the stock site
driver.get(url)

# Step 3: Wait for the stock prices to load (Adjust the wait condition as necessary)
try:
    # Wait until an element containing stock prices is loaded (max 10 seconds)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'price'))
    )
except Exception as e:
    print("Error loading stock prices:", e)
    driver.quit()

# Step 4: Extract stock prices
stock_prices = driver.find_elements(By.CLASS_NAME, 'price')

# Step 5: Print the scraped stock prices
for price in stock_prices:
    print(price.text)

# Step 6: Close the browser after scraping
driver.quit()
'''


'''
# Working with APIs
# Fetching Data from an API

import requests
import json

# Make an HTTP GET request to the specified URL
response = requests.get("https://technical.fiintrade.vn/TradingView/GetStockChartData?language=vi&Code=ACB&Frequency=Daily&From=2023-09-25T04%3A35%3A47.000Z&To=2024-09-19T04%3A36%3A47.000Z&Type=Stock")
#response = requests.get("https://priceonline.hsc.com.vn/stock/ACB")
# Check if the request was successful
if response.status_code == 200:
    data = response.json() # Parse the JSON data from response
    with open("data.json", "w") as file:
        json.dump(data, file)
    print(data)
else:
    print(f"Failed to fetch data: {response.status_code}")
with open("data.json", "r") as file:
    data = json.load(file)
    print(data)
'''


'''
# TradingView using tvdatafeed
from tvDatafeed import TvDatafeed, Interval

username = 'ntdkhoa@hotmail.com'
password = 'Citibank123'
tv = TvDatafeed(username, password)
data = tv.get_hist(symbol='CSTB2402', exchange='HOSE', interval=Interval.in_daily, n_bars=100)
print(data)
'''

'''
# Finnhub
import finnhub

api_key = 'crl80u1r01qhc7mk0gg0crl80u1r01qhc7mk0ggg'
# Initialize client
finnhub_client = finnhub.Client(api_key=api_key)
# Fetch stock data
quote = finnhub_client.quote(symbol='VNM', exchange='VN')
print(quote)
'''

'''
# Alpha Advantage
from alpha_vantage.timeseries import TimeSeries

api_key = 'SIMCY8EVIUP4T1ZA'
# Initialize timeseries object
ts = TimeSeries(key=api_key, output_format='pandas')
# Fetch data for a stock
data, meta_data = ts.get_daily(symbol='TSLA', outputsize='compact')
print(data)
'''

'''
# Yahoo Finance
import yfinance as yf

stock = yf.Ticker('VNM')
#print(stock.history(period='1mo'))
print(stock.info)
#print(stock.dividends)
'''