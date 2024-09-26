'''
CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    stock VARCHAR(10) NOT NULL,  -- Stock ticker symbol
    date DATE NOT NULL,  -- Trading date
    open DECIMAL(10, 2),  -- Opening price
    high DECIMAL(10, 2),  -- Highest price
    low DECIMAL(10, 2),  -- Lowest price
    close DECIMAL(10, 2),  -- Closing price
    volume BIGINT,  -- Trading volume
    UNIQUE(stock, date)  -- Ensure no duplicate stock data for the same day
);
'''

import psycopg2
# connection info
connection = psycopg2.connect(
    host="35.236.185.5",
    database="trading_data",
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