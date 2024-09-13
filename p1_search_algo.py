
# Binary Search requires a sorted list. 
# It repeatedly divides the list in half and compares the middle element to the target.
'''
def binary_search_recursive(arr, target, low, high):
    # Base case
    if low > high: # target is not present
        return -1
    
    mid = (low + high) // 2

    if arr[mid] == target: # target is found
        return mid
    
    # Target is smaller than mid, search the left half
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, low, mid -1)
    
    # Target is larger than mid, search the right half
    else:
        return binary_search_recursive(arr, target, mid + 1, high)
'''
'''
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1  # Return -1 if the target is not found
'''

# linear search,
# iterate through the list and check each element until you find the target.
'''
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i # Return the index of the target
    return -1  # Return -1 if the target is not found
print(linear_search([10,23,543,2,345,2,45,6], 5))
'''

# Sorting Algorithms
'''
# Quick sort
def quick_sort(arr):
    if len(arr) <= 1: 
        return arr # Base case: If the array has 0 or 1 elements, it's already sorted
    # Choose a pivot (in this case, we take the last element)
    # pivot = arr[-1] 
    pivot = arr[0]
    #pivot = arr[len(arr) // 2]

    # Partition the array into two sub-arrays
    # all elements less than the pivot are on its left 
    # and all elements greater than the pivot are on its right.
    # left = [x for x in arr[:-1] if x <= pivot]
    # right = [x for x in arr[:-1] if x > pivot]
    left = [x for x in arr[1:len(arr)] if x <= pivot] # Elements smaller or equal to pivot
    right = [x for x in arr[1:len(arr)] if x > pivot] # Elements larger than pivot
    
    # Recursively apply the same process to the sub-arrays 
    # until the entire array is sorted.
    #print(arr)
    return quick_sort(left) + [pivot] + quick_sort(right)

# Test the function
#arr = [10, 7, 8, 9, 1, 5]
#sorted_arr = quick_sort(arr)
#print(sorted_arr)  # Output should be [1, 5, 7, 8, 9, 10]
# Test the function

arr = [132,234,56,4,7,95,5,54,343,67,50]
arr1 = quick_sort(arr)
print(arr)
print(arr1)
print(binary_search_recursive(arr1, 7, 0, len(arr1) - 1))  # Output: 3
'''

'''
# Selection Sort
def select_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        # Swap the found minimum element with the current element
        arr[i], arr[min_index] = arr[min_index], arr[i]
        print(arr)
    return arr
print([64, 34, 25, 12, 22, 11, 90])
print(select_sort([64, 34, 25, 12, 22, 11, 90]))
'''

'''
# Merge sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)  # Recursively sort the left half
        merge_sort(right_half)  # Recursively sort the right half

        i = j = k = 0

        # Merging the two halves
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            print(arr)

        # Checking if any elements were left in the left half
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            print(arr)

        # Checking if any elements were left in the right half
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            print(arr)
    return arr

# Test the function
print([64, 34, 25, 12, 22, 11, 90])
print(merge_sort([64, 34, 25, 12, 22, 11, 90]))  # Output: [3, 9, 10, 27, 38, 43, 82]
'''

'''
# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print(arr)
    return arr

# Test the function
print([64, 34, 25, 12, 22, 11, 90])
print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))  # Output: [11, 12, 22, 25, 34, 64, 90]
'''

'''
# Recursion:
# a process in which a function calls itself as a part of its execution. 
# It’s an important concept for breaking down complex problems into smaller, 
# more manageable tasks.

# Key Concepts:
# Base Case: This stops the recursion. 
# Without a base case, the recursion will continue indefinitely, leading to a stack overflow.
# Recursive Case: This is the part where the function calls itself with modified arguments, 
# moving towards the base case.

# find the greatest common divisor (GCD) of two numbers 
# using the Euclidean Algorithm.
def UCLN(a, b):
    # Base case:
    if b == 0:
        return a
    if a == 0:
        return b
    if a == b:
        return a
    # Recursive case:
    if a > b:    
        return UCLN(b, a%b)
    return UCLN(a, b%a)

print(UCLN(986856457700,987))
'''

'''
# sum of digits of a number
def sum_digit(n):
    # Base case
    if n < 10:
        return n
    # Recursive case
    return (n % 10) + sum_digit (n//10)

print(sum_digit(-3456))
'''

'''
# Fibonacci using Recursion
def fibo(n):
    # Base case:
    if n == 0 :
        return 0
    elif n ==1: 
        return 1
    # Recursive case: sum of two preceding Fibonaci numbers
    return fibo(n-1) + fibo(n-2)

print(fibo(6))
'''

'''
# Factorial using Recursion
def factorial(n):
    # Base case
    if n == 0 or n ==1:
        return 1
    # Recursive case:
    return n * factorial(n-1)

print(factorial(-5))
'''