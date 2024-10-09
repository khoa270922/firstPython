import time
import datetime as dt
import requests
import pandas as pd
import psycopg2
import logging
import decimal

# Configure logging
logging.basicConfig(
    filename='data_insertion.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_ExRight_list(): # Fetches the list of stocks with ExRight events for the current date.
    
    params = {
        'fromDate': (dt.datetime.today()).strftime('%d/%m/%Y'), #  - dt.timedelta(2)
        'toDate': (dt.datetime.today()).strftime('%d/%m/%Y'), #  - dt.timedelta(2)
        'eventCode': 'DIV,ISS,AIS',
        'dateType': 'ExrightDate',
        'language': 'vn'
    }
    response = requests.get(
        'https://iboard-api.ssi.com.vn/statistics/company/corporate-actions?',
        params= params, 
        headers= {'user-agent': 'Mozilla/5.0'}
    )
    if response.status_code == 200:
        data = response.json()
        ex_list = []
        
        if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
            for record in data['data']:
                if record.get('exrightDate'):
                    unique_t = (record.get('symbol'), dt.datetime.strptime(record.get('exrightDate'), '%d/%m/%Y').strftime('%Y%m%d'))
                    if unique_t not in ex_list:
                        ex_list.append(unique_t)
            return ex_list    
        logging.warning("Exright API returned no data.")
        return []
    else:
        logging.error(f"Exright Failed to fetch data. Status Code: {response.status_code}")
        return []

def update_CW(connection, cursor): # Fetches and updates Cover Warrant data into the database.

    response = requests.get(
        'https://iboard-query.ssi.com.vn/v2/stock/type/w/hose', 
        headers= {'user-agent': 'Mozilla/5.0'}
    )

    if response.status_code == 200:
        
        insert_query = """
        INSERT INTO cw (serial, ticker, issuer, last_trading_date, end_date, pre_close, ceil, floor, ref, bid_p3, bid_vol3, bid_p2, bid_vol2, bid_p1, bid_vol1, match_price, match_vol, change, change_percent, ask_p1, ask_vol1, ask_p2, ask_vol2, ask_p3, ask_vol3, total_vol, total_val, open, high, low, close, avg, symbol, strike_price, cvn_ratio, listed_share, break_even, created_date, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, date) 
            DO UPDATE 
                SET bid_p3=excluded.bid_p3, bid_vol3=excluded.bid_vol3, bid_p2=excluded.bid_p2, bid_vol2=excluded.bid_vol2, bid_p1=excluded.bid_p1, bid_vol1=excluded.bid_vol1, match_price=excluded.match_price, match_vol=excluded.match_vol, change=excluded.change, change_percent=excluded.change_percent, ask_p1=excluded.ask_p1, ask_vol1=excluded.ask_vol1, ask_p2=excluded.ask_p2, ask_vol2=excluded.ask_vol2, ask_p3=excluded.ask_p3, ask_vol3=excluded.ask_vol3, total_vol=excluded.total_vol, total_val=excluded.total_val, open=excluded.open, high=excluded.high, low=excluded.low, close=excluded.close, avg=excluded.avg, break_even=excluded.break_even
        ;  -- Avoid inserting duplicates
        """
        
        data = response.json()

        if 'data' in data and all(data.values()) and isinstance(data['data'], list) and len(data['data']) > 0:
            # Get clean data:
            clean_data = []
            stocks_list = []

            for record in data['data']:
                try:
                    # Clean the record and prepare for insert
                    er = decimal.Decimal(record.get('er')[:-2]) # if record.get('er') else None
                    break_even = record['mp'] * er + record.get('ep', 0)# if record.get('mp') and er else None
                    
                    # Append the cleaned data for batch insert
                    clean_data.append((
                        record.get('sn'), record.get('ss'), record.get('isn'), 
                        #ltd = dt.datetime.strptime(record.get('ltd', '19700101'), '%Y%m%d') if record.get('ltd') else None
                        dt.datetime.strptime( record.get('ltd'), '%Y%m%d'), dt.datetime.strptime( record.get('md'), '%Y%m%d'),
                        record.get('pcp'), record.get('c'), record.get('f'), record.get('r'),
                        record.get('b3'), record.get('b3v'), record.get('b2'), record.get('b2v'),
                        record.get('b1'), record.get('b1v'), record.get('mp'), record.get('mv'),
                        record.get('pc'), record.get('cp'), record.get('o1'), record.get('o1v'),
                        record.get('o2'), record.get('o2v'), record.get('o3'), record.get('o3v'),
                        record.get('mtq'), record.get('mtv'), record.get('o'), record.get('h'),
                        record.get('l'), record.get('lmp'), record.get('ap'), record.get('us'),
                        record.get('ep'), er, record.get('rfq'), break_even, dt.datetime.now(),
                        dt.datetime.today().strftime('%Y-%m-%d')
                    ))
                    # Get underlying stocks
                    unique_t = (record.get('us'), dt.datetime.today().strftime('%Y%m%d'))
                    if unique_t not in stocks_list:
                        stocks_list.append(unique_t)
                except Exception as e:
                    logging.error(f"Data processing error for {record.get('sn')}: {e}")

            # Insert CW data
            cursor.executemany(insert_query, clean_data)
            connection.commit()
            logging.info("CW Data received successfully, inserting into the database.")

            return stocks_list

        else:
            logging.warning("CW API response returned successfully but no data available.")
            logging.warning(f"{data.values()}")
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

    clean_data = []
    for stock in us_list:
        if (stock not in ex_list) and any(stock[0] in tup for tup in cur_list):
            ssi_url = 'https://iboard-query.ssi.com.vn/v2/stock/' + stock[0]
            response = requests.get(ssi_url, headers = ssi_headers)

            if response.status_code == 200:
                data = response.json()

                if 'data' in data and isinstance(data['data'], dict) and len(data['data']) > 0:                    
                    try:
                        clean_data.append((to_date, dt.datetime.today().strftime('%Y-%m-%d'), data['data']['ss'], data['data']['o']/1000, data['data']['h']/1000, data['data']['l']/1000, data['data']['lmp']/1000, data['data']['mtq'], dt.datetime.now()))
                    except Exception as e:
                        logging.error(f"Data processing error for {data['data']['ss']}: {e}")                    
                else:
                    logging.info("Empty CURRENT data")
            else:
                logging.error(response.status_code)        
        else:
            ssi_url = 'https://iboard-api.ssi.com.vn/statistics/charts/history?resolution=' + INTERVAL + '&symbol=' + stock[0] + '&from=' + str(last_year) + '&to=' + str(to_date)        
            response = requests.get(ssi_url, headers = ssi_headers)

            if response.status_code == 200:
                data = response.json()

                # Check if api_data has non-empty values
                if 'data' in data and isinstance(data['data'], dict) and len(data['data']) > 0: 
                    try:
                        # Extract the time array and high array from the JSON response
                        time_array = data['data']['t']  # list of UNIX timestamps
                        high_array = data['data']['h']  # list of high prices
                        low_array = data['data']['l']
                        open_array = data['data']['o']
                        close_array = data['data']['c']
                        vol_array = data['data']['v']

                        # Create a list of tuples, converting timestamps to readable dates
                        for i in range(len(time_array)):
                            # Convert each UNIX timestamp to a datetime object
                            date = dt.datetime.fromtimestamp(time_array[i]).strftime('%Y-%m-%d')
                            # Create a tuple with the converted time, high value, and the current date
                            clean_data.append((time_array[i], date, stock[0], open_array[i], high_array[i], low_array[i], close_array[i], vol_array[i], dt.datetime.now()))
                    
                        logging.info(f"Underlying Stock {stock[0]} HISTORY received successfully, inserting into the database.")                    
                    except Exception as e:
                        logging.error(f"Data processing error for {stock[0]}: {e}")     
                else:
                    logging.info("Empty HISTORY data")
            else:
                logging.error(response.status_code)

    cursor.executemany(insert_query, clean_data)                    
    connection.commit()
    logging.info("History Data received successfully and inserted into the database.")

def main():
    try:
        logging.error("Starting program")

        # Step 1: Get ExRight list
        EX_LIST = get_ExRight_list()  # [('PNJ', '20240930')]
        print(EX_LIST)

        # Step 2: Open DB connection
        connection = psycopg2.connect(host="35.236.185.5", database="trading_data", user="trading_user", password="123456")
        cursor = connection.cursor()

        # Step 3: Update Cover Warrant (CW) data
        US_LIST = update_CW(connection, cursor)  # [('FPT', '20241002')]

        # Step 4: Fetch stock prices
        stock_prices(EX_LIST, US_LIST, connection, cursor)

    except Exception as e:
        logging.error(f"Error during execution: {e}")
    
    finally:
        # Step 5: Close DB connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()

'''
vietstock_headers = {
    'Referer': 'https://ta.vietstock.vn',
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Host': 'api.vietstock.vn',
    'Accept-Encoding': 'gzip,deflate, br',
    'Connection': 'keep-alive',
}

response = requests.get(ssi_url, headers = ssi_headers)
if response.status_code == 200:
    data = response.json()
    dump = json.dumps(data)
    body = json.loads(dump)
    
    # Create data frame
    df = pd.DataFrame({'Time': body['data']['t'], 'High': body['data']['h'], 'Low': body['data']['l'], 'Open': body['data']['o'], 'Close': body['data']['c'], 'Volume': body['data']['v']})
    df['Date'] = pd.to_datetime(df['Time'],unit='s')
    df['Stock'] = LIST_STOCK[0]
'''

'''
# Api Data return as a list OF DICTS

# Example API response (mock data)
api_data = [
    {'stock': 'AAPL', 'date': '2024-09-18', 'open': 150.25, 'high': 152.50, 'low': 149.75, 'close': 151.00, 'volume': 50000000},
    {'stock': 'GOOG', 'date': '2024-09-18', 'open': 2700.50, 'high': 2750.00, 'low': 2680.25, 'close': 2725.75, 'volume': 3000000}
]
for data in api_data:
    cursor.execute(insert_query, (data['stock'], data['date'], data['open'], data['high'], data['low'], data['close'], data['volume']))
'''

'''
# Api_data is structured as a dictionary 
# Method 1:
api_data = {
    'stock': ['AAPL', 'GOOG'],
    'date': ['2024-09-18', '2024-09-18'],
    'open': [150.25, 2700.50],
    'high': [152.50, 2750.00],
    'low': [149.75, 2680.25],
    'close': [151.00, 2725.75],
    'volume': [50000000, 3000000]
}
# Loop over the length of the data and insert row by row
for i in range(len(api_data['stock'])):
    cursor.execute(insert_query, (api_data['stock'][i], api_data['date'][i], api_data['open'][i], api_data['high'][i], api_data['low'][i], api_data['close'][i], api_data['volume'][i]))

'''

'''
# Api data is structured as a dictionary
# Method 2: using dataframe
# Convert the dictionary into a DataFrame
from sqlalchemy import create_engine
df = pd.DataFrame(api_data)
# Create the SQLAlchemy engine
engine = create_engine('postgresql+psycopg2://trading_user:YOUR_PASSWORD@YOUR_PUBLIC_IP/trading_data')

# Insert the DataFrame into PostgreSQL
df.to_sql('stock_prices', engine, if_exists='append', index=False)
from sqlalchemy.dialects.postgresql import insert

# Create an insert statement that handles conflicts
insert_stmt = insert(df).on_conflict_do_nothing()

with engine.connect() as conn:
    conn.execute(insert_stmt)
'''