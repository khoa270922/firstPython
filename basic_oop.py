# Queues (FIFO - First In, First Out):
from collections import deque

class myQueue:
    def __init__(self):
        self.queue = deque() # Initialize an empty deque to store queue elements
    def enqueue(self, item):
        self.queue.append(item) # Add an item to the end of the queue
    def dequeue(self):
        if len(self.queue) == 0: # Handle empty queue case
            return "Queue is empty."
        return self.queue.popleft() # Remove and return the front element (FIFO)
    def front(self):
        if len(self.queue) == 0:
            return "Queue is empty."  # Handle empty queue case
        return self.queue[0]  # Return the front element without removing it
    def is_empty(self):
        return len(self.queue) == 0 # Check if the queue is empty
    def size(self):
        return len(self.queue)  # Return the number of elements in the queue

queue = myQueue()
queue.enqueue(240)
queue.enqueue(250)
queue.enqueue(260)
print(queue.dequeue())
print(queue.dequeue())
print(queue.size())

# Stacks (LIFO - Last In, First Out):
'''
class myStack:
    def __init__(self): 
        self.Stack = [] # Initialize an empty list to store stack elements
    def push(self, item):
        self.Stack.append(item) # Add an item to the stack
    def pop(self):
        if len(self.Stack) == 0:
            return "Stack is empty" # Handle empty stack case
        return self.Stack.pop() # Remove and return the last element (LIFO)
    def peek(self):
        if len(self.Stack) == 0:
            return "Stack is empty" # Handle empty stack case
        return self.Stack[-1] # Return the last element without removing it
    def is_empty(self):
        return len(self.Stack) == 0 # Check if the stack is empty
    def size(self):
        return len(self.stack)  # Return the number of elements in the stack
    
stack = myStack()
stack.push(10)
stack.push(20)
stack.push(30)
#print(stack.pop())
print(stack.peek())
'''

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
    print(f"Toi la xe dap nhan hieu {self.brand}, model {self.model}")

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