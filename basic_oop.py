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