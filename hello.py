# Creating a simple API with Flask
from flask import Flask, jsonify

# Extend the Flask API example to add a new route that accepts POST requests 
# and returns the posted data in JSON format.
app = Flask(__name__)

@app.route('/api/data', methods = ['GET'])

def get2_data():
    sample_data = {
        "name": "Peter",
        "age": 35,
        "city": "Cali Que"
    }
    return jsonify(sample_data)

if __name__ == "__main__":
    app.run(debug=True)

'''
app = Flask(__name__)

@app.route('/api/data', methods = ['GET'])
def get_data():
    sample_data = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }
    return jsonify(sample_data)

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
    

# OOP in depth

# Create a Shape class with a method area. 
# Create subclasses Rectangle and Circle, each with their own area method. 
# Use polymorphism to calculate the area of different shapes.
'''
class Shape:
    def __init__(self, name):
        self.name = name
    
    def area(self):
        raise NotImplementedError("Subclasses must implement this method")

class Retagle(Shape):
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    
class Circle(Shape):
    def __init__(self, name, diameter):
        self.name = name
        self.diameter = diameter
    def area(self):
        return self.diameter * self.diameter * 3.14

ASquare = Retagle("Asquare", 4, 8)
print("dien tich la: ", ASquare.area())

KCircle = Circle("Circle K", 5)
print("dien tich hinh tron la: ", KCircle.area())
'''

# Encapsulation:
'''
class BankAccount:
    def __init__(self, owner, balance =0):
        self.owner = owner
        self.__balance = balance # private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount < self.__balance:
            self.__balance -= amount
            return [self.__balance, amount]
        else:
            return "Insufficient balance"
        
    def get_balance(self):
        return self.__balance
    
# creating an object
account = BankAccount(input("nhap ten tai khoan: "), float(input("nhap so tien ban dau: ")))
account.deposit(float(input("ban muon nop bao nhieu: ")))
print("ten tai khoan duoc tao: ", account.owner)
print("so tien khoi tao: ", account.get_balance())
print(account.withdraw(float(input("ban muon rut bao nhieu: "))))
print(account.get_balance())
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


# Inheritance in Classes:
# Create a parent class Vehicle with attributes make and model, and a method start_engine. 
# Create a child class Car that inherits from Vehicle and adds a num_doors attribute. 
# Override the start_engine method to print a custom message for Car.
'''
# Define a parent class
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

def start_engine(self):
    print("the model ", self.model, "make by ", self.make, " kick start brmmm")

# Define a child class that inherits from Vehicle
class Car(Vehicle):
    def __init__(self, make, model, num_doors):
        super().__init__(make, model)   # Call the parent class's constructor
        self.num_doors = num_doors

    def start_engine(self):
        print("the model ", self.model, "make by ", self.make, " with", self.num_doors, " number of doors, kick start brmmm")

# Create an instance of the Car class
my_car = Car ("Mitsu", "Xpre2022", 4)

# Call methods
my_car.start_engine()
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