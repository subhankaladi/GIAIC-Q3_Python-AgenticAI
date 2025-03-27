#Import Complete File Module
import math_operations
#Import Specific Functions
from math_operations import multiplyy

#Python Functions

def add(x, y):
    return x + y

#function call
result = add(10, 20)
print("Sum:", result)

#Lambda (Anonymous) Functions
sum_lambda = lambda x, y: x + y
print("Lumbda Sum:", sum_lambda(20,30))


my_dict = {"apple": 5, "banana": 2, "cherry": 8, "date": 1}
sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]))
print(sorted_dict)

#Scope of variable (Local vs Global)
total = 0 
def sum_numbers(a,b):
    total = a + b # Local Variable
    print("Inside function", total)
sum_numbers(20,40)
print("Outside Function:", total)



def multiply(*numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

print(multiply(2,3,4))
print(multiply(5,10))



#Recursive Functions
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)
print(factorial(5))



#From Module
print(math_operations.add(20,25))
print(multiplyy(10,3))