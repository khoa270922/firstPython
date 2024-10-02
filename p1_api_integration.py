import datetime as dt
#from datetime import datetime
import requests
import json
import pandas as pd
import logging
import psycopg2
#import string
import decimal
'''
def get_ExRight_list():      
    params = {
        'fromDate': (datetime.datetime.today() - datetime.timedelta(1)).strftime('%d/%m/%Y'),
        'toDate': (datetime.datetime.today() - datetime.timedelta(1)).strftime('%d/%m/%Y'),
        'eventCode': 'DIV,ISS,AIS',
        'dateType': 'ExrightDate',
        'language': 'vn'
        }
    response = requests.get('https://iboard-api.ssi.com.vn/statistics/company/corporate-actions?',params= params, headers= {'user-agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        data = response.json()
        dump = json.dumps(data)
        body = json.loads(dump)
        # Check if api_data has non-empty values
        if 'data' in body and all(body.values()) and isinstance(body['data'], list) and len(body['data']) > 0:          
            df = pd.DataFrame(body['data'])
            logging.info("Exright Data received successfully, inserting into the database.")
            return df['symbol'].drop_duplicates().tolist()
        else:
            logging.warning("Exright API response returned successfully but no data available.")
            print(body.values())
            return []
    else:
        print(f"Exright Failed to fetch data. Status Code: {response.status_code}")
        return []

print(get_ExRight_list())
'''        
def update_CW():
    response = requests.get('https://iboard-query.ssi.com.vn/v2/stock/type/w/hose', headers= {'user-agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        insert_query = """
        INSERT INTO cw (serial, ticker, issuer, last_trading_date, end_date, pre_close, ceil, floor, ref, bid_p3, bid_vol3, bid_p2, bid_vol2, bid_p1, bid_vol1, match_price, match_vol, change, change_percent, ask_p1, ask_vol1, ask_p2, ask_vol2, ask_p3, ask_vol3, total_vol, total_val, open, high, low, close, avg, symbol, strike_price, cvn_ratio, listed_share, break_even)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker) DO NOTHING;  -- Avoid inserting duplicates
        """
        data = response.json()
        dump = json.dumps(data)
        body = json.loads(dump)
        df = pd.DataFrame(body['data'])
        us_list = df['us'].drop_duplicates().tolist()
        # Check if api_data has non-empty values
        if 'data' in body and all(body.values()) and isinstance(body['data'], list) and len(body['data']) > 0:   
            try:
                # Open DB
                connection = psycopg2.connect(host="35.236.185.5", database="trading_data", user="trading_user", password="123456")
                cursor = connection.cursor()
                
                # Truncate CW table
                cursor.execute("TRUNCATE TABLE CW;")
                connection.commit()
                
                # Insert CW data
                for i in range(len(body['data'])):
                    try:
                        cursor.execute(insert_query, (body['data'][i]['sn'], body['data'][i]['ss'], body['data'][i]['isn'], dt.datetime.strptime(body['data'][i]['ltd'], '%Y%m%d'), dt.datetime.strptime(body['data'][i]['md'], '%Y%m%d'), body['data'][i]['pcp'], body['data'][i]['c'], body['data'][i]['f'], body['data'][i]['r'], body['data'][i]['b3'], body['data'][i]['b3v'], body['data'][i]['b2'], body['data'][i]['b2v'], body['data'][i]['b1'], body['data'][i]['b1v'], body['data'][i]['mp'], body['data'][i]['mv'], body['data'][i]['pc'], body['data'][i]['cp'], body['data'][i]['o1'], body['data'][i]['o1v'], body['data'][i]['o2'], body['data'][i]['o2v'], body['data'][i]['o3'], body['data'][i]['o3v'], body['data'][i]['mtq'], body['data'][i]['mtv'], body['data'][i]['o'], body['data'][i]['h'], body['data'][i]['l'], body['data'][i]['lmp'], body['data'][i]['ap'], body['data'][i]['us'], body['data'][i]['ep'], decimal.Decimal(body['data'][i]['er'][:-2]), body['data'][i]['rfq'], body['data'][i]['mp']*decimal.Decimal(body['data'][i]['er'][:-2])+body['data'][i]['ep']))
                        connection.commit()
                        logging.info(f"{dt.date.today()} Success {body['data'][i]['sn']} ")
                    except Exception as e:
                        logging.error(f"{dt.date.today()} Fail {body['data'][i]['sn']} ")
        
                cursor.close()
                connection.close()
                logging.info("CW Data received successfully, inserting into the database.")
            
            except Exception as e:
                logging.error(f"Failed to insert data: {e}")
                us_list = []

        else:
            logging.warning("CW API response returned successfully but no data available.")
            print(body.values())
            us_list = []
        return us_list
    else:
        print(f"CW Failed to fetch data. Status Code: {response.status_code}")
        return []

#print(update_CW())

from sqlalchemy import create_engine

# Create SQLAlchemy engine for PostgreSQL
engine = create_engine('postgresql+psycopg2://trading_user:123456@35.236.185.5/trading_data')

# Insert the DataFrame into PostgreSQL (None values will be inserted as NULL)
expected_fields = ['sn', 'ss', 'isn', 'ltd', 'md', 'pcp', 'c', 'f', 'r', 'b3', 'b3v', 'b2', 'b2v', 'b1', 'b1v', 'mp', 'mv', 'pc', 'cp', 'o1', 'o1v', 'o2', 'o2v', 'o3', 'o3v', 'mtq', 'mtv', 'o', 'h', 'l', 'lmp', 'ap', 'us', 'ep', 'er', 'rfq', 'be']



response = requests.get('https://iboard-query.ssi.com.vn/v2/stock/type/w/hose', headers= {'user-agent': 'Mozilla/5.0'})
if response.status_code == 200:

    data = response.json()
    dump = json.dumps(data)
    body = json.loads(dump)
    
    '''
    for column in df.columns:
        print(f"Checking column: {column}")
        for value in df[column]:
            if isinstance(value, dict):
                print(f"Found in column {column}, value: {value}")
     '''         
    #print(body['data'])
    
    clean_data = []
    for record in body['data']:
        
        clean_record = {}
        for field in expected_fields:
            #print(f"{field}:{record.get(field)}")
            clean_record[field] = record.get(field)
        clean_data.append(clean_record)

    df = pd.DataFrame(clean_data)
    print(df)
    

    #df = pd.json_normalize(df['mv'].fillna('').apply(dict).tolist())
    #df = df.where(pd.notnull(df), None)
    #us_list = df['us'].drop_duplicates().tolist()
    
    #df.to_sql('cw', engine, if_exists='append', index=False)
    #print(df.to_markdown())

'''
URL_AUTHENTICATION = 'https://auth.fiintrade.vn/'
URL_ROOT = 'http://df31.fiintek.com'
USERNAME = 'StoxPlus.FiinTrade.SPA'
PASSWORD = 'fiin%**(trade'

def get_token():
    body = {
        'grant_type': 'refresh_token',
        'client_id': 'StoxPlus.FiinTrade.SPA',
        'client_secret': 'fiin%**(trade',
        #'scope': 'openid fiintek.datafeed',
        #'username': USERNAME,
        #'password': PASSWORD,
    }
    res = requests.post(URL_AUTHENTICATION, data=body)
    return json.loads(res.text)

token = get_token()
print(token)
'''

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