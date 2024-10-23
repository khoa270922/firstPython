#import decimal
import datetime as dt
import time
#import psycopg2

#import requests
#import json
'''
def cal_date():
    today = dt.date.today()
    return today
name = 'Hello {}!'.format(cal_date())
print(dt.date.today().timetuple().tm_yday)
print(dt.date.today().isocalendar()[1])
print(dt.date.today().timetuple().tm_mon)
print(dt.date.today().timetuple().tm_year)
print(dt.datetime.today())
'''
#fromdate = round(time.mktime((2024, 10, 2, 0, 0, 0, 0, 0, 0)))
#todate = round(time.mktime((2024, 10, 10, 0, 0, 0, 0, 0, 0)))
#print(fromdate)
#print(todate)
print(round(dt.datetime.strptime('2019-05-31', "%Y-%m-%d").timestamp()))
fromdate_u = dt.datetime.strptime('20241006', "%Y%m%d").timetuple() # from last 1 year
#todate_u = round(time.mktime((today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)))
#print(time.mktime)
1559260800
#from datetime import datetime
#chuoi = "3.4556:1"
#date = "20240910"
#a= [(1,2),(1,4),(3,5),(5,7)]
#b= [('ACB', '20240927'), ('FPT', '20240927')]
#print(dt.datetime.today().strftime('%Y-%m-%d'))
#print(decimal.Decimal(chuoi[:-2]))  # Output: Pytho
#print(dt.datetime.strptime(date, '%Y%m%d'))
#print(dt.datetime.now())
#print(dt.datetime.today().date().strftime('%Y-%m-%d'))
#print(dt.datetime.fromtimestamp(1726444800).strftime('%Y-%m-%d'))
#print( '2' in dict(a))
#print(dict(a))
#print(any (9  in tub for tub in a))
#print(any('ACB' not in tup for tup in b))
'''
today = dt.date.today()
from_date = round(time.mktime((today.year - 1, today.month, today.day, 0, 0, 0, 0, 0, 0)))
to_date = round(time.mktime((today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)))
print(today)
print(from_date)
print(to_date)
'''
'''
today = dt.date.today()

from_date = round(time.mktime((today.year - 1, today.month, today.day, 0, 0, 0, 0, 0, 0)))
to_date = round(time.mktime((today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)))
print(today)
print(from_date)
print(to_date)
print(dt.datetime.today().strftime('%Y%m%d'))
'''
'''
try:
    # Open DB
    #connection = psycopg2.connect(host="35.236.185.5", database="trading_data", user="trading_user", password="123456")
    #cursor = connection.cursor()
    
    ssi_headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip,deflate, br, zstd',
        'Connection': 'keep-alive',
    }
    #cursor.execute("SELECT DISTINCT (stock), to_char(date,'YYYYmmdd')  FROM public.stock_prices where date = ( select MAX(date)  FROM public.stock_prices)")
    #fetch = cursor.fetchall()
    #cur_list = [row for row in fetch]
   

    ssi_url = 'https://iboard-query.ssi.com.vn/v2/stock/ACB'
    response = requests.get(ssi_url, headers = ssi_headers)
    
    if response.status_code == 200:
        data = response.json()
        print(type(data))
        if 'data' in data and isinstance(data['data'], dict) and len(data['data']) > 0:
            clean_data = []
    
            #for record in data['data']:
            try:
                clean_data.append((data['data']['ss'], data['data']['b2']))
                #clean_data.append((to_date, dt.datetime.today().strftime('%Y-%m-%d'), record.get('ss'), record.get('o')/1000, record.get('h')/1000, record.get('l')/1000, record.get('c')/1000, record.get('mtq')/1000, dt.datetime.now()))
            except Exception as e:
                print(f"Data processing error for")# {record.get('ss')}: {e}")
            # Perform batch insert:
            #cursor.executemany(insert_query, clean_data)
            print(clean_data)
        else:
            print("Empty CURRENT data")

    #cursor.close()
    #connection.close()

except Exception as e:
    print(e)
    #logging.error(f"Failed to insert data: {e}")
'''
#date = datetime.strptime(a, '%Y%m%d').strftime('%m/%d/%Y')

# Context Managers
# allow you to manage resources:
#     - files
#     - network connections
#     - locks efficiently. 
# using with blocks to manage resources (in this case, files). 
# no matter what happens inside the with block, 
# the file (resource) is always closed after its use.
# the Flow:
# __enter__: What happens when the with block starts.
# __exit__: What happens when the with block ends, even if there’s an error.
# Check for Exceptions: 
# If something is not working, 
# try printing debug messages inside __enter__ and __exit__ to see what's happening step by step.

# Create a context manager that opens and closes a file, 
# ensuring the file is always closed after reading or writing.
# Use this context manager to read from and write to a text file.

'''
# Alternative: using contextlib library
# easier to work with, especially for simpler resource management tasks like file handling.

from contextlib import contextmanager

@contextmanager

def My_file_manager(filename, mode):
    f = open(filename, mode)
    try:
        yield f
    finally:
        f.close()

with My_file_manager('list_num.txt', 'w') as f:
    f.write('Hello using contextlib')

with My_file_manager('list_num.txt', 'r') as f:
    print(f.read())
'''

# Self-define a customer context manager class
'''
class MyFileManager:
# The __init__ method initializes the object with the filename and mode
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode 
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

with MyFileManager('list_num.txt', 'w') as f:
    f.write('Hello My Context Manager')

with MyFileManager('list_num.txt', 'r') as f:
    content = f.read()
    print(content)
'''

# Generators and Iterators
# Generators allow you to iterate over data in a memory-efficient way, 
# especially when dealing with large datasets. 
# They use the yield keyword to produce a value and pause the function, 
# resuming where it left off when the next value is requested.
'''
def count_fibo_to(max_value):
    a, b = 0, 1
    while a <= max_value:
        yield a # The yield keyword turns the count_up_to function into a generator, producing values one at a time.
        a, b = b, a + b
        
max_value = 1000000

for number in count_fibo_to(max_value):
    print(number)
'''

# Decorators
# are a powerful way to modify the behavior of functions or methods
# They allow you to "wrap" a function with another function, 
# adding extra functionality before or after the original function runs.

# Create a decorator that logs the execution time of a function.
# Apply this decorator to a function that performs a complex calculation.
'''
import time

def exec_time_decor(func):
    def wrapper(*args, **kwargs):
        start_time = time.time() # get current time
        # Execute the original function
        result = func(*args, **kwargs) 
        # '*args' and '**kwargs' allow the decorator to accept any number of positional and keyword arguments.
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"Thoi gian thuc hen cua {func.__name__}: {exec_time:.6f} seconds")
        return result
    return wrapper

@exec_time_decor
def cal_factorial(n):
    factorial = 1
    for i in range(1, n+1):
        factorial *=i
    return factorial
    
factorial_result = cal_factorial(10000)
print(f"Factorial calculated")
'''

'''
def my_decorator(func): # function that takes another function (func) as an argument.
    def wrapper(): # unction adds functionality before and after calling func.
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper
# The @my_decorator syntax is a shorthand for applying the decorator to say_hello.
@my_decorator
def say_hello():
    print("Hello!")

say_hello()
'''

# Advanced Data Analysis with Pandas
'''
import pandas as pd
# Load a dataset into a DataFrame, perform a groupby operation to aggregate data by one column, 
# and then create a pivot table from the aggregated data.

df = pd.read_csv('sample_data.csv')

#print(df.columns)
#print(df.index)
#print(df.values)
#print(df.head()) # Display the first few rows of the DataFrame

# Group by a specific column (e.g., 'Category') and aggregate the 'Sales' column by summing the values
grouped_df = df.groupby('Category')['Sales'].sum().reset_index()
print(grouped_df)
# Creating a pivot table to summarize data
pivot_table = df.pivot_table(index='Category', columns='Region', values='Sales', aggfunc='mean')
print(pivot_table)

#pivot_table.to_csv('pivot_table.csv')
'''

'''
# b. Pivot Tables
data = {
    'Name': ['Alice', 'Bob', 'Charlie', '', 'Bob', 'Charlie'],
    'Month': ['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb'],
    'Sales': [200, 150, 300, 250, 200, 350]
}
df = pd.DataFrame(data)

pivot_table = df.pivot_table(index='Name', columns='Month', values='Sales', aggfunc='sum')
print(pivot_table)
'''

'''
# a. Merging DataFrames:
df1 = pd.DataFrame({
    'ID': [1,2,3,4],
    'Name': ['Alice', 'Bob', 'Charlie', '']
})

df2 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Age': [15, '', 5, 1]
})
merged_df = pd.merge(df1, df2, on = 'ID', how = 'inner')
print(df1)
print(df2)
print(merged_df)
'''

# Basic web scraping 
'''
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Target URL
URL = "https://cafef.vn"

# Step 1: Fetch the Webpage Content
response = requests.get(URL) 

if response.status_code == 200:
    page_content = response.text
else:
    print(f"Failed. Statuscode: {response.status_code}")
    exit()

# Step2: Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser') 

# Step 3: Extract Titles and Links: Depending on the structure of the webpage, 
# you need to identify the HTML tags that contain the article titles and links. 
# Common tags used are <h2>, <h3>, or within anchor tags <a>

articles = soup.find_all('h2') #, class_='article-title') # Adjust the tag and class as needed
    
for article in articles:
    title = article.get_text() # Extract the title text
    a_tag = article.find('a') # Find the anchor tag within the article element.

    if a_tag: # Check if the anchor tag exists
        relative_link = a_tag['href'] # Extract the href attribute from the anchor tag
        full_link = urljoin(URL, relative_link)  # Combine base URL with relative path
        print(f"Title of link: {title}")
        print(f"Link: {full_link}")
    else:
        print(f"Title: {title} (No link found)")
        print("-----------------------------")
'''

# Use BeautifulSoup to scrape the titles and links of all articles from a news website's homepage 
# (make sure to check the website’s robots.txt file to ensure scraping is allowed).

# BeautifulSoup: Parses the HTML content of the page.
# find() Method: Extracts specific HTML elements, like the page title.
'''
url = "https://www.hsc.com.vn"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    print(f"Title of the page: {title}")
else:
    print(f"failed to retrieve webpage")
'''

# Creating a simple API with Flask
'''
from flask import Flask, jsonify, request

# Extend the Flask API example to add a new route that accepts POST requests 
# and returns the posted data in JSON format.
app = Flask(__name__)

# Existing GET route
@app.route('/api/data', methods = ['GET'])

def get_data():
    sample_data = {
        "name": "Peter",
        "age": 35,
        "city": "Cali Que"
    }
    return jsonify(sample_data)

# New POST route
@app.route('/api/data', methods = ['POST'])
def post_data():
    data = request.json # Get the posted data as JSON
    if not data:
        return jsonify({"error": "no data provided"}), 400 # Return an error if no data is provided
    
    return jsonify(data), 201 # 201 status code indicates successful creation

if __name__ == "__main__":
    app.run(debug=True)
'''

# Consuming an API
'''
import requests

response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
if response.status_code == 200:
    data = response.json()
    print(data)
    print(f"Bitcoin price in USD: {data['bpi']['USD']['rate']}")
else:
    print(f"failed to retreived data. Status code: {response.status_code}")
'''


# Flask Exercise:
'''
from flask import Flask
# Build a simple Flask web application with at least two routes: 
# a home page and an about page. 
# The home page should display a welcome message, 
# and the about page should display some information about the app.

# Flask class is used to create a web application
app = Flask(__name__)

# define the home page of the web app
@app.route('/')
def home():
    return "Jade homepage welcome!"

@app.route('/noive')
def about():
    return "A web by Jade"

# start the web server with debugging enabled
if __name__ == "__main__":
    app.run(debug=True)
'''

# Multiprocessing
'''
import multiprocessing as mp
import math as m

def cal_factorial(n):
    return m.factorial(n)

if __name__ == "__main__":
    numbers = [5, 7, 10, 12, 15]

# Create a Pool of worker processes
    with mp.Pool() as pool:
# The map() method applies a cal_factorial function to every item in the input list
        result = pool.map(cal_factorial, numbers)
# The result are returned as a list
    print(result)
'''


# Working with Pandas for Data Analysis
# It provides data structures like Series and DataFrame
'''
import pandas as pd

# Load a CSV file into a DataFrame. 
# Perform basic operations like filtering rows, adding new columns, and grouping data by a specific column. 
# Save the modified DataFrame to a new CSV file.
# Read from CSV:
de = pd.read_csv('cw_20240823.csv')
filtered_ACB = de[de['CK'] == 'ACB']
print(filtered_ACB)
de['FairValue'] =  [0] * 96
print(de)
de.to_csv('cw_20240823_refine.csv')
'''

'''
# Dictionary
data = {
    'Name': ['Alice','Bob', 'Charlie', 'David'],
    'Age': [24, 27, 22, 32],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}
# Create a Dataframe from a dictionary
df = pd.DataFrame(data)
print(df)

# Display column names:
print(df.columns)
print(df.describe())

# Filtering data
filtered_df = df[df['Age'] > 25]
print(filtered_df)
# Adding new column
df['Salary'] = [50000, 60000, 55000, 70000]
print(df)
# Grouping data
grouped_df = df.groupby('City').mean(numeric_only=True)
print(grouped_df)
'''


'''
# Abstract Classes are classes that cannot be instantiated on their own and are meant to be subclasses. 
# They can define methods that must be implemented by child classes.

from abc import ABC, abstractmethod
# ABC is a base class for defining abstract classes.
# @abstractmethod decorator is used to define abstract methods that must be implemented by any subclass.

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle (5,4)
print(f"Area: {rect.area()}")
print(f"Perimeter: {rect.perimeter()}")
'''

'''
# Database Interations with SQLite
# Create a database that stores books with columns for title, author, and publication year. 
# Insert some sample data, then write a query to retrieve all books by a specific author.

import sqlite3

conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Query the data
author_to_find = input("nhap ten tac gia can tim: ")
#cursor.execute("SELECT * FROM bookstore")
cursor.execute("SELECT title, pub_year FROM bookstore WHERE author = ?", (author_to_find,))
rows = cursor.fetchall()
print(f"Books by {author_to_find}:")
for row in rows:
    print(f"Title: {row[0]}, pub_Year: {row[1]}")
    print(row)
conn.close()
'''


'''
import sqlite3
# Connect to a database (or create it if it doesn't exists)
conn = sqlite3.connect("example.db")
cursor = conn.cursor()
'''
# Create a table

#cursor.execute('''
#    CREATE TABLE IF NOT EXISTS bookstore (
#               id INTERGER PRIMARY KEY,
#               title TEXT,
#               author TEXT,
#               pub_year INTEGER
#               )
#               ''')
'''
# Sample data
books = [
    ("To Kill a Mockingbird", "Harper Lee", 1960),
    ("1984", "George Orwell", 1949),
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    ("Pride and Prejudice", "Jane Austen", 1813)
]

# Insert the sample data into the table
cursor.executemany("INSERT INTO bookstore (title, author, pub_year) VALUES (?, ?, ?)", books)
cursor.execute("INSERT INTO bookstore(title, author, pub_year) VALUES(?, ?, ?)", (input("nhap ten sach: "), input("nhap tac gia: "), int(input("nam xuat ban: "))))

# Commit the changes and close the connection
conn.commit()
conn.close()
'''


# Working with APIs
# Fetching Data from an API
'''
import requests
import json

# Make an HTTP GET request to the specified URL
response = requests.get("https://priceonline.hsc.com.vn/stock/ACB")
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

# Regular Expressions
'''
# Find email addresses in text
import re

# Define pattern
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
# '[a-zA-Z0-9._%+-]+': Matches the username part (e.g., 'user.name')
# '@': Matches the '@' symbol
# '[a-zA-Z0-9.-]+: Matches the domain name (e.g., example.com).
# '\\.[a-zA-Z]{2,}: Matches the dot and the top-level domain (e.g., .com, .org). 
# The {2,} ensures at least two characters in the domain extension.
text = """
Here are some email addresses: alice@example.com, bob_smith@work.net,
john.doe@company.org. Please contact us!
"""

email_addresses = re.findall(email_pattern, text)
for each in email_addresses:
    print(each)
'''

# Regex are powerful tools for pattern matching in strings
'''
import re

# Search for a pattern in a string
pattern = r"\b[Aa]lice\b"
text = "Alice is a good friend of alice."

matches = re.findall(pattern, text)
print(matches)

# Common Regex Patterns:
# \\d: Matches any digit.
# \\w: Matches any word character (letters, digits, underscores).
# \\s: Matches any whitespace character.
# \\.: Matches any character except a newline.
# *: Matches 0 or more repetitions of the preceding element.
# +: Matches 1 or more repetitions of the preceding element.
# []: Matches any one of the characters inside the brackets.
'''


# Working with Files and Data Serialization

# JSON (JavaScript Object Notaion): 
'''
import json

# Python dictionary
data = {
    "name": "Alice",
    "age": 30,
    "is_student": False
}
# Serialize to JSON
json_data = json.dumps(data)
print(json_data)

# Deserialize from JSON
python_data = json.loads(json_data)
print(python_data)

# Write JSON data to a file
with open("data.json", "w") as file:
    json.dump(data, file)

# Read JSON data from a file
with open("data.json", "r") as file:
    data_fromfile = json.load(file)
    print(data_fromfile) 
'''


# Modules and Packages Exercise:
'''
# Create a module with a function that returns the factorial of a number. 
# Import this module in another script and use the function.
import Factorial_num
num1 = int(input("nhap so bi chia: "))
num2 = int(input("nhap so chia: "))
print("ket qua phep chia la: ", Factorial_num.fac_num(num1, num2))
'''


# Lambda, Map, Filter, Reduce functions
'''
from functools import reduce
# Use reduce() to find the maximum number in a list.
list_numbers = [34, 56, 34, 1, 3456, -20, 300, 20]
max_func = lambda i,j: i if i > j else j
max_num = reduce(max_func, list_numbers)
#max_num = reduce(lambda i,j: i if i > j else j, list_numbers)
print("the maximum number in the list is: ", max_num)

# Use filter() to find all words in a list that start with the letter "a".
list_words = ["nhung", "gi", "se", "cho", "doi", "ta", "mai"]
list_a_words = list(filter(lambda i: "a" in i, list_words))
print(list_a_words)

# Use map() to convert a list of temperatures in Celsius to Fahrenheit.
list_temp_C = [25, 26, 27, 28, 29, 30]
list_temp_F = list(map(lambda i: (i * 9/5) + 32, list_temp_C))
print(list_temp_F)
'''


# Using an External Library:
'''
import requests
# Make a GET request to a website
response = requests.get("https://priceonline.hsc.com.vn/stock/ACB")

# Print the status code and content
print(response.status_code) # 200 indicates success
print(response.json()) # Print the JSON content
'''


# Write a program that asks the user to enter two numbers and divides them. 
# Handle exceptions for division by zero and invalid input types.
'''
# ask the user for 2 numbers
try:
    num1 = float(input("nhap so bi chia: "))
    num2 = float(input("nhap so chia: "))

# perform division
    result = num1 / num2

    print(f"ket qua phep chia: {num1} chia {num2} la: {result}")

# handle divide by zero
except ZeroDivisionError:
    print("khong chia duoc cho 0")
# handle invalid input types (e.g., non-numeric numbers)
except ValueError:
    print("gia tri bi loi")
# code that always execute
finally:
    print("xu ly xong")
'''





# List Comprehensions
# new_list = [expression for item in iterable if condition]
# Create a list of squares from 1 to 10 using list comprehension
'''
# Create a list of squares from 1 to 10 using list comprehension
squares = [x * x for x in range(1, 11)]
print(squares)
'''


# Dictionaries are created using curly braces {}.
# You access values using keys (person["name"]).
# items() allows you to loop through both keys and values.
'''
# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])  # Output: Alice

# Modifying values
person["age"] = 31

# Adding a new key-value pair
person["job"] = "Engineer"

# Looping through a dictionary
for key, value in person.items():
    print(f"{key}: {value}")
'''


# Lists are created using square brackets [].
# You can access and modify elements using their index (fruits[0] for the first element).
# append() adds a new item to the end of the list.
'''
# Creating a list
fruits = ["apple", "banana", "cherry"]

# Accessing elements
print(fruits[0])  # Output: apple

# Modifying elements
fruits[1] = "blueberry"

# Adding elements
fruits.append("date")

# Looping through a list
for fruit in fruits:
    print(fruit)
'''