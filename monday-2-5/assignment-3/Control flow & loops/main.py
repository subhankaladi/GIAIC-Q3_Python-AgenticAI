#Python Control flow loops 

#if else stratement

def check_number(num):
    if num > 0:
        print("The Number is positive")
    elif num < 0: 
        print("The Number is negative")
    else :
        print("The Number is Zero")

def print_numbers(n):
    print("Printing Numbers from 1 to", n)
    for i in range(1, n+1):
        print(i, end=" ")
    print()

def countdown(n):
    print("Countdown From", n)
    while n > 0:
        print(n, end=" ")
        n -= 1
    print("Blast Off")

def find_first_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            print("First even number found", num)
            break

def skip_odd_numbers(n):
    print("Even Number from 1 to", n)
    for i in range(1, n + 1):
        if 1 % 2 != 0:
            continue
        print(i, end=" ")
    print()

age: int = 21 
is_student: bool = True

if age > 18 and is_student:
    print("You are elgible for a student discout")

if age < 12 or age > 60:
    print("you qualify for a special discout")


word : str = "Python"

for letter in word:
    print(letter)


numbers = [1,2,3,4,5]

for num in numbers:
    print(num)
else :
    print("Loop Complete Successfully")

check_number(5)
check_number(-3)
check_number(3)

print_numbers(5)
countdown(-3)

find_first_even([1,3,5,6,7])
skip_odd_numbers(10)