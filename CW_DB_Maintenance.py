'''
create_table_query = """
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
"""
'''
'''
create_table_query = """
CREATE TABLE cw (
    id SERIAL PRIMARY KEY,
    serial VARCHAR(10),
    Ticker VARCHAR(10) NOT NULL,
    Issuer VARCHAR(10),
    Last_Trading_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Pre_Close DECIMAL(10, 2),
    Ceil DECIMAL(10, 2),
    Floor DECIMAL(10, 2),
    Ref DECIMAL(10, 2),
    Bid_P3 DECIMAL(10, 2),
    Bid_Vol3 BIGINT,
    Bid_P2 DECIMAL(10, 2),
    Bid_Vol2 BIGINT,
    Bid_P1 DECIMAL(10, 2),
    Bid_Vol1 BIGINT,
    Match_Price DECIMAL(10, 2),
    Match_Vol BIGINT,
    Change DECIMAL(10, 2),
    Change_Percent DECIMAL(10, 2),
    Ask_P1 DECIMAL(10, 2),
    Ask_Vol1 BIGINT,
    Ask_P2 DECIMAL(10, 2),
    Ask_Vol2 BIGINT,
    Ask_P3 DECIMAL(10, 2),
    Ask_Vol3 BIGINT,
    Total_Vol BIGINT,
    Total_Val DECIMAL(14, 2),
    Open DECIMAL(10, 2),
    High DECIMAL(10, 2),
    Low DECIMAL(10, 2),
    Close DECIMAL(10, 2),
    Avg DECIMAL(10, 2),
    Symbol VARCHAR(10) NOT NULL,
    Strike_Price DECIMAL(10, 2),
    CVN_Ratio DECIMAL(10, 6),
    Listed_Share BIGINT,
    Break_Even DECIMAL(10, 2),
    UNIQUE(Ticker)  -- Ensure no duplicate stock data for the same day
);
"""
'''
import psycopg2

connection = psycopg2.connect(host="35.236.185.5", database="trading_data", user="trading_user", password="123456")
cursor = connection.cursor()

# Example query to check connection
#cursor.execute("SELECT version();")
#db_version = cursor.fetchone()
#print(f"Connected to: {db_version}")

#cursor.execute(create_table_query)
#connection.commit()
cursor.execute("TRUNCATE TABLE CW;")

cursor.close()
connection.close()


# Initialize connection. # Perform query using pandas.
# conn = st.connection("postgresql", type="sql")
# query = f"SELECT * FROM history WHERE stock = '{stock_name}'  order by date desc limit 10"    
# data = pd.read_sql(query, conn)
    