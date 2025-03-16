# Different ways to create a strings in Python

single_quote = 'Subhan Kaladi'
double_quote = "Python is fun"
triple_quote = '''Here There!
Subhan Kaladi Write a Multi Line String Code'''

raw_string = r'This is a Raw string with \n and \t'

print(single_quote)
print(double_quote)
print(triple_quote)
print(raw_string)

# Special characters used in python.

print("Subhan \nKaladi") #new line
print("Subhan \tKaladi") #tab space
print("This is a backslash: \\")
print("Subhan Said, \"Python is Awesome\"") #using double quote inside a string
print("BackSpace example : Subhan\bKaladi") #Backspace
print("Unicode Characters : \u0041") #Unicode for 'A'


my_string = "SubhanKaladi"

#Joining two strings together

concat_string = my_string + " is a Python Developer"
print(concat_string)


#Assignnig first charater using indexing

print(my_string[0])
print(my_string[1])

#Cutting out parts of the string using slicing

print(my_string[0:6]) #Subhan
print(my_string[6:0]) #Kaladi
print(my_string[:]) #SubhanKaladi


#Checking legnth for string

print(len(my_string))

# Changing string to uppercase and lowercase

print(my_string.upper())
print(my_string.lower())

#String Methods
sample_string = "Python is fun and python is powerful."


words = sample_string.split(" ")
print(words)

joining_string = "-".join(words)
print(joining_string)

replaced_string = sample_string.replace("Python", "JavaScript")
print(replaced_string)

index = sample_string.find("Python")
print(index)

count_python =sample_string.count("Python")
print(count_python)

#String Formatting

name = 'Subhan'
age = 20

#Using % to add variable in string

print("My name is %s and I amd %d Years old"% (name, age))

#Using .format() to add variable in string

print("My Name is {} and I am {} years old.".format(name, age))

#Using f-string to add variable in string

print(f"My name is {name} and I am {age} Years old.")

#Type Casting 

num_str = "100"

num_int = int(num_str)
print(num_int, type(num_int))

num_float = bool(num_int)
print(num_float, type(num_float))

num_str_again = str(num_float)
print(num_str_again, type(num_str_again))


#Convert string to list

list_example = list("Python")
print(list_example, type(list_example))

#Convert list to tuple

tuple_example = tuple(list_example)
print(tuple_example, type(tuple_example))

#Convert tuple to set

set_example = set(tuple_example)
print(set_example, type(set_example))

#Create dictionary from list of tuples

dict_example = dict([('name', 'Subhan'), ('age', 23)])
print(dict_example, type(dict_example))

