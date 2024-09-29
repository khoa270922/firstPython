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
        'fromDate': (dt.datetime.today() - dt.timedelta(2)).strftime('%d/%m/%Y'),
        'toDate': (dt.datetime.today() - dt.timedelta(2)).strftime('%d/%m/%Y'),
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
            logging.info("Exright Data received successfully")
            return df['symbol'].drop_duplicates().tolist()
        else:
            logging.warning("Exright API response returned successfully but no data available.")
            #print(body.values())
            return []
    else:
        print(f"Exright Failed to fetch data. Status Code: {response.status_code}")
        return []

def update_CW():
    response = requests.get('https://iboard-query.ssi.com.vn/v2/stock/type/w/hose', headers= {'user-agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        insert_query = """
        INSERT INTO cw (serial, ticker, issuer, last_trading_date, end_date, pre_close, ceil, floor, ref, bid_p3, bid_vol3, bid_p2, bid_vol2, bid_p1, bid_vol1, match_price, match_vol, change, change_percent, ask_p1, ask_vol1, ask_p2, ask_vol2, ask_p3, ask_vol3, total_vol, total_val, open, high, low, close, avg, symbol, strike_price, cvn_ratio, listed_share, break_even, created_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                        cursor.execute(insert_query, (body['data'][i]['sn'], body['data'][i]['ss'], body['data'][i]['isn'], dt.datetime.strptime(body['data'][i]['ltd'], '%Y%m%d'), dt.datetime.strptime(body['data'][i]['md'], '%Y%m%d'), body['data'][i]['pcp'], body['data'][i]['c'], body['data'][i]['f'], body['data'][i]['r'], body['data'][i]['b3'], body['data'][i]['b3v'], body['data'][i]['b2'], body['data'][i]['b2v'], body['data'][i]['b1'], body['data'][i]['b1v'], body['data'][i]['mp'], body['data'][i]['mv'], body['data'][i]['pc'], body['data'][i]['cp'], body['data'][i]['o1'], body['data'][i]['o1v'], body['data'][i]['o2'], body['data'][i]['o2v'], body['data'][i]['o3'], body['data'][i]['o3v'], body['data'][i]['mtq'], body['data'][i]['mtv'], body['data'][i]['o'], body['data'][i]['h'], body['data'][i]['l'], body['data'][i]['lmp'], body['data'][i]['ap'], body['data'][i]['us'], body['data'][i]['ep'], decimal.Decimal(body['data'][i]['er'][:-2]), body['data'][i]['rfq'], body['data'][i]['mp']*decimal.Decimal(body['data'][i]['er'][:-2])+body['data'][i]['ep'], dt.datetime.now()))
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
    
EX_LIST = get_ExRight_list()
US_LIST = update_CW()
print(EX_LIST)
print(US_LIST)
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