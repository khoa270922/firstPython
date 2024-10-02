import time
import datetime as dt
import requests
import json
import pandas as pd
import psycopg2
import logging
import decimal

# Configure logging
logging.basicConfig(filename='data_insertion.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_ExRight_list():      
    params = {
        'fromDate': (dt.datetime.today()).strftime('%d/%m/%Y'), #  - dt.timedelta(2)
        'toDate': (dt.datetime.today()).strftime('%d/%m/%Y'), #  - dt.timedelta(2)
        'eventCode': 'DIV,ISS,AIS',
        'dateType': 'ExrightDate',
        'language': 'vn'
        }
    response = requests.get('https://iboard-api.ssi.com.vn/statistics/company/corporate-actions?',params= params, headers= {'user-agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        data = response.json()
        dump = json.dumps(data)
        body = json.loads(dump)
        ex_list = []
        # Check if api_data has non-empty values
        if 'data' in body and all(body.values()) and isinstance(body['data'], list) and len(body['data']) > 0:            
            for record in body['data']:
                if record.get('exrightDate'):
                    unique_t = (record.get('symbol'), dt.datetime.strftime(dt.datetime.strptime(record.get('exrightDate'), '%d/%m/%Y'), '%Y%m%d'))
                    if unique_t not in ex_list:
                        ex_list.append(unique_t)
                    #ex_set.add(({record.get('symbol')}, {dt.datetime.strftime(dt.datetime.strptime(record.get('exrightDate'), '%d/%m/%Y'), '%Y%m%d')}))
            return ex_list
 
        # Check if api_data has non-empty values 
        else:
            logging.warning("Exright API response returned successfully but no data available.")
            #print(body.values())
            return []
    else:
        print(f"Exright Failed to fetch data. Status Code: {response.status_code}")
        return []

def update_CW(connection, cursor):
    response = requests.get('https://iboard-query.ssi.com.vn/v2/stock/type/w/hose', headers= {'user-agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        
        # Insert the DataFrame into PostgreSQL (None values will be inserted as NULL)
        expected_fields = ['sn', 'ss', 'isn', 'ltd', 'md', 'pcp', 'c', 'f', 'r', 'b3', 'b3v', 'b2', 'b2v', 'b1', 'b1v', 'mp', 'mv', 'pc', 'cp', 'o1', 'o1v', 'o2', 'o2v', 'o3', 'o3v', 'mtq', 'mtv', 'o', 'h', 'l', 'lmp', 'ap', 'us', 'ep', 'er', 'rfq', 'be']

        insert_query = """
        INSERT INTO cw (serial, ticker, issuer, last_trading_date, end_date, pre_close, ceil, floor, ref, bid_p3, bid_vol3, bid_p2, bid_vol2, bid_p1, bid_vol1, match_price, match_vol, change, change_percent, ask_p1, ask_vol1, ask_p2, ask_vol2, ask_p3, ask_vol3, total_vol, total_val, open, high, low, close, avg, symbol, strike_price, cvn_ratio, listed_share, break_even, created_date, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, date) 
            DO UPDATE 
                SET bid_p3=excluded.bid_p3, bid_vol3=excluded.bid_vol3, bid_p2=excluded.bid_p2, bid_vol2=excluded.bid_vol2, bid_p1=excluded.bid_p1, bid_vol1=excluded.bid_vol1, match_price=excluded.match_price, match_vol=excluded.match_vol, change=excluded.change, change_percent=excluded.change_percent, ask_p1=excluded.ask_p1, ask_vol1=excluded.ask_vol1, ask_p2=excluded.ask_p2, ask_vol2=excluded.ask_vol2, ask_p3=excluded.ask_p3, ask_vol3=excluded.ask_vol3, total_vol=excluded.total_vol, total_val=excluded.total_val, open=excluded.open, high=excluded.high, low=excluded.low, close=excluded.close, avg=excluded.avg, break_even=excluded.break_even
        ;  -- Avoid inserting duplicates
        """
        
        data = response.json()
        dump = json.dumps(data)
        body = json.loads(dump)
        
        # Check if api_data has non-empty values
        if 'data' in body and all(body.values()) and isinstance(body['data'], list) and len(body['data']) > 0:
            # Get clean data:
            clean_data = []
            stocks_list = []

            for record in body['data']:
                # Get clean record        
                clean_record = {}
                for field in expected_fields:
                    clean_record['Date'] = dt.datetime.today().strftime('%Y-%m-%d')
                    clean_record[field] = record.get(field)
                clean_data.append(clean_record) 
                # Get underlying stocks
                unique_t = (record.get('us'), dt.datetime.today().strftime('%Y%m%d'))
                if unique_t not in stocks_list:
                    stocks_list.append(unique_t)

            # Delete CW today
            #cursor.execute(f"DELETE FROM cw where date = '{dt.datetime.today().strftime('%Y-%m-%d')}'")
            #connection.commit()

            # Insert CW data
            for i in range(len(clean_data)):
                try:
                    cursor.execute(insert_query, (clean_data[i]['sn'],  clean_data[i]['ss'],  clean_data[i]['isn'], dt.datetime.strptime( clean_data[i]['ltd'], '%Y%m%d'), dt.datetime.strptime( clean_data[i]['md'], '%Y%m%d'),  clean_data[i]['pcp'],  clean_data[i]['c'],  clean_data[i]['f'],  clean_data[i]['r'],  clean_data[i]['b3'],  clean_data[i]['b3v'],  clean_data[i]['b2'],  clean_data[i]['b2v'],  clean_data[i]['b1'],  clean_data[i]['b1v'],  clean_data[i]['mp'],  clean_data[i]['mv'],  clean_data[i]['pc'],  clean_data[i]['cp'],  clean_data[i]['o1'],  clean_data[i]['o1v'],  clean_data[i]['o2'],  clean_data[i]['o2v'],  clean_data[i]['o3'],  clean_data[i]['o3v'],  clean_data[i]['mtq'],  clean_data[i]['mtv'],  clean_data[i]['o'],  clean_data[i]['h'],  clean_data[i]['l'],  clean_data[i]['lmp'],  clean_data[i]['ap'],  clean_data[i]['us'],  clean_data[i]['ep'], decimal.Decimal( clean_data[i]['er'][:-2]),  clean_data[i]['rfq'],  clean_data[i]['mp']*decimal.Decimal( clean_data[i]['er'][:-2])+ clean_data[i]['ep'], dt.datetime.now(), clean_data[i]['Date']))
                    connection.commit()
                    logging.info(f"{dt.date.today()} Success {clean_data[i]['sn']} ")
                except Exception as e:
                    logging.error(f"{dt.date.today()} Fail {clean_data[i]['sn']} ")
                    print(e)
            logging.info("CW Data received successfully, inserting into the database.")
            
            return(stocks_list)

        else:
            logging.warning("CW API response returned successfully but no data available.")
            logging.warning(f"{body.values()}")
            return []
    else:
        logging.warning(f"CW Failed to fetch data. Status Code: {response.status_code}")
        return []

def stock_prices(ex_list, us_list, connection, cursor):
    
    INTERVAL = '1D'
    
    today = dt.date.today()
    last_year = round(time.mktime((today.year - 1, today.month, today.day, 0, 0, 0, 0, 0, 0)))
    to_date = round(time.mktime((today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)))
    
    ssi_headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip,deflate, br, zstd',
        'Connection': 'keep-alive',
    }

    # Insert data into PostgreSQL
    insert_query = """
    INSERT INTO stock_prices (time, date, stock, open, high, low, close, volume, created_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (stock, date) 
            DO UPDATE 
                SET time=excluded.time, date=excluded.date, stock=excluded.stock, open=excluded.open, high=excluded.high, low=excluded.low, close=excluded.close, volume=excluded.volume, created_date=excluded.created_date
        ;  -- Avoid inserting duplicates
    """
    
    # Get current underlying stocks
    cur_list = []
    cursor.execute("SELECT DISTINCT (stock), to_char(date,'YYYYmmdd')  FROM public.stock_prices where date = ( select MAX(date)  FROM public.stock_prices)")
    fetch = cursor.fetchall()
    cur_list = [row for row in fetch]
   
    for stock in us_list:
        if (stock not in ex_list) and any(stock[0] in tup for tup in cur_list):
            ssi_url = 'https://iboard-query.ssi.com.vn/v2/stock/' + stock[0]
            response = requests.get(ssi_url, headers = ssi_headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and all(data.values()) and len(data) > 0:
                    cursor.execute(insert_query, [to_date, dt.datetime.today().strftime('%Y-%m-%d'), stock[0], data['data']['o'],data['data']['h'],data['data']['l'],data['data']['c'],data['data']['mtq'],dt.datetime.now()])
                    connection.commit()
                    logging.info(f"Underlying Stock {stock[0]} history received successfully, inserting into the database.")
                else:
                    logging.info("Empty data")                
            else:
                logging.error(response.status_code)        
        else:
            ssi_url = 'https://iboard-api.ssi.com.vn/statistics/charts/history?resolution=' + INTERVAL + '&symbol=' + stock[0] + '&from=' + str(last_year) + '&to=' + str(to_date)        
            response = requests.get(ssi_url, headers = ssi_headers)

            if response.status_code == 200:
                data = response.json()
                dump = json.dumps(data)
                body = json.loads(dump)

                # Check if api_data has non-empty values
                if 'data' in body and all(body['data'].values()) and len(body['data']) > 0:
                    # Extract the time array and high array from the JSON response
                    time_array = body['data']['t']  # list of UNIX timestamps
                    high_array = body['data']['h']  # list of high prices
                    low_array = body['data']['l']
                    open_array = body['data']['o']
                    close_array = body['data']['c']
                    vol_array = body['data']['v']

                    # Create a list of tuples, converting timestamps to readable dates
                    combined_data = []
                    for i in range(len(time_array)):
                        # Convert each UNIX timestamp to a datetime object
                        date = dt.datetime.fromtimestamp(time_array[i]).strftime('%Y-%m-%d')
                        # Create a tuple with the converted time, high value, and the current date
                        combined_data.append((time_array[i], date, stock[0], open_array[i], high_array[i], low_array[i], close_array[i], vol_array[i], dt.datetime.now()))
                    
                    cursor.executemany(insert_query, combined_data)
                    
                    connection.commit()

                    logging.info(f"Underlying Stock {stock[0]} history received successfully, inserting into the database.")
                else:
                    logging.info("Empty data")
            else:
                logging.error(response.status_code)
        
try:
    EX_LIST = get_ExRight_list() # [('PNJ', '20240930')]
    
    # Open DB
    connection = psycopg2.connect(host="35.236.185.5", database="trading_data", user="trading_user", password="123456")
    cursor = connection.cursor()
    
    US_LIST = update_CW(connection, cursor) # [('FPT', '20241002')]

    stock_prices(EX_LIST, US_LIST, connection, cursor)

    # Close DB
    cursor.close()
    connection.close()

except Exception as e:
    logging.error(f"Failed to insert data: {e}")


'''
today = datetime.date.today()
#today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
from_date = round(time.mktime((today.year - 1, today.month, today.day, 0, 0, 0, 0, 0, 0)))
to_date = round(time.mktime((today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)))
#print(from_date, to_date)

LIST_STOCK = ('ACB', 'VNM')
INTERVAL = '1D'
ssi_url = 'https://iboard-api.ssi.com.vn/statistics/charts/history?resolution=' + INTERVAL + '&symbol=' + LIST_STOCK[0] + '&from=' + str(from_date) + '&to=' + str(to_date)
#vietstock_url = 'https://api.vietstock.vn/ta/history?symbol=' + LIST_STOCK[0] + '&resolution=D&from=' + str(from_date) + '&to=' + str(to_date)

ssi_headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip,deflate, br',
    'Connection': 'keep-alive',
}


vietstock_headers = {
    'Referer': 'https://ta.vietstock.vn',
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Host': 'api.vietstock.vn',
    'Accept-Encoding': 'gzip,deflate, br',
    'Connection': 'keep-alive',
}

# Insert data into PostgreSQL
insert_query = """
INSERT INTO stock_prices (time, date, stock, open, high, low, close, volume)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (stock, date) DO NOTHING;  -- Avoid inserting duplicates
"""


response = requests.get(ssi_url, headers = ssi_headers)
if response.status_code == 200:
    data = response.json()
    dump = json.dumps(data)
    body = json.loads(dump)
    
    # Create data frame
    df = pd.DataFrame({'Time': body['data']['t'], 'High': body['data']['h'], 'Low': body['data']['l'], 'Open': body['data']['o'], 'Close': body['data']['c'], 'Volume': body['data']['v']})
    df['Date'] = pd.to_datetime(df['Time'],unit='s')
    df['Stock'] = LIST_STOCK[0]
    print(df)
'''

'''
    connection = None

    try:
        # Open DB
        connection = psycopg2.connect(
            host="35.236.185.5", #104.199.242.171",
            database="trading_data", #"postgres",
            user="trading_user", #"postgres"
            password="123456" #"J,@CC2@oCa{R'^O]"
        )
        cursor = connection.cursor()

        # Loop over the length of the data and insert row by row
        for i  in range(len(body['data']['t'])):
            try:
                cursor.execute(insert_query, (body['data']['t'][i], datetime.datetime.fromtimestamp(body['data']['t'][i]), LIST_STOCK[0], body['data']['h'][i], body['data']['l'][i], body['data']['o'][i], body['data']['c'][i], body['data']['v'][i]))
                logging.info(f"{datetime.date.today()} Success {LIST_STOCK[0]} on {datetime.datetime.fromtimestamp(body['data']['t'][i])}")
            except Exception as e:
                logging.error(f"{datetime.date.today()} Fail {LIST_STOCK[0]} on {datetime.datetime.fromtimestamp(body['data']['t'][i])}")
        
        connection.commit()
        logging.info("All data committed successfully")
    
    except Exception as e:
        logging.critical(f"Database connection error: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info("Database connection closed")
'''
#else:
#    print(f"fail: {response.status_code} {response.text}")


'''
# Api Data return as a list
import psycopg2
import logging

# Configure logging
logging.basicConfig(filename='data_insertion.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Example API response (mock data)
api_data = [
    {'stock': 'AAPL', 'date': '2024-09-18', 'open': 150.25, 'high': 152.50, 'low': 149.75, 'close': 151.00, 'volume': 50000000},
    {'stock': 'GOOG', 'date': '2024-09-18', 'open': 2700.50, 'high': 2750.00, 'low': 2680.25, 'close': 2725.75, 'volume': 3000000}
]

# Database connection details
connection = None

try:
    connection = psycopg2.connect(
        host="YOUR_PUBLIC_IP",
        database="trading_data",
        user="trading_user",
        password="YOUR_PASSWORD"
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO stock_prices (stock, date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (stock, date) DO NOTHING;
    """

    for data in api_data:
        try:
            cursor.execute(insert_query, (
                data['stock'], 
                data['date'], 
                data['open'], 
                data['high'], 
                data['low'], 
                data['close'], 
                data['volume']
            ))
            logging.info(f"Data inserted successfully for {data['stock']} on {data['date']}")
        except Exception as e:
            logging.error(f"Failed to insert data for {data['stock']} on {data['date']}: {e}")

    connection.commit()
    logging.info("All data committed successfully")

except Exception as e:
    logging.critical(f"Database connection error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
        logging.info("Database connection closed")
'''

'''
# Api_data is structured as a dictionary 
# Method 1:
import psycopg2
import logging

# Configure logging
logging.basicConfig(filename='data_insertion.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Example API response with lists as values
api_data = {
    'stock': ['AAPL', 'GOOG'],
    'date': ['2024-09-18', '2024-09-18'],
    'open': [150.25, 2700.50],
    'high': [152.50, 2750.00],
    'low': [149.75, 2680.25],
    'close': [151.00, 2725.75],
    'volume': [50000000, 3000000]
}

# Database connection details
connection = None

try:
    connection = psycopg2.connect(
        host="YOUR_PUBLIC_IP",
        database="trading_data",
        user="trading_user",
        password="YOUR_PASSWORD"
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO stock_prices (stock, date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (stock, date) DO NOTHING;
    """

    # Loop over the length of the data and insert row by row
    for i in range(len(api_data['stock'])):
        try:
            cursor.execute(insert_query, (
                api_data['stock'][i],
                api_data['date'][i],
                api_data['open'][i],
                api_data['high'][i],
                api_data['low'][i],
                api_data['close'][i],
                api_data['volume'][i]
            ))
            logging.info(f"Data inserted successfully for {api_data['stock'][i]} on {api_data['date'][i]}")
        except Exception as e:
            logging.error(f"Failed to insert data for {api_data['stock'][i]} on {api_data['date'][i]}: {e}")

    connection.commit()
    logging.info("All data committed successfully")

except Exception as e:
    logging.critical(f"Database connection error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
        logging.info("Database connection closed")

'''

'''
# Api data is structured as a dictionary
# Method 2: using dataframe
import pandas as pd

# Example API response with lists as values
api_data = {
    'stock': ['AAPL', 'GOOG'],
    'date': ['2024-09-18', '2024-09-18'],
    'open': [150.25, 2700.50],
    'high': [152.50, 2750.00],
    'low': [149.75, 2680.25],
    'close': [151.00, 2725.75],
    'volume': [50000000, 3000000]
}

# Convert the dictionary into a DataFrame
df = pd.DataFrame(api_data)
print(df)

from sqlalchemy import create_engine
import psycopg2

# Create the SQLAlchemy engine
engine = create_engine('postgresql+psycopg2://trading_user:YOUR_PASSWORD@YOUR_PUBLIC_IP/trading_data')

# Insert the DataFrame into PostgreSQL
# 'stock_prices' is the table name in the PostgreSQL database
df.to_sql('stock_prices', engine, if_exists='append', index=False)
from sqlalchemy.dialects.postgresql import insert

# Create an insert statement that handles conflicts
insert_stmt = insert(df).on_conflict_do_nothing()

with engine.connect() as conn:
    conn.execute(insert_stmt)

'''