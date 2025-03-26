#Python data structure : List Tuples and Dictionaries


fruits = ["apple", "banana", "cherry"]
print("Fruit List", fruits)

#call first element by indexing
print("First Fruit",fruits[0])

#adding element at the end
fruits.append("Orange")
print("Updated List", fruits)

#adding element at the start
fruits.insert(0, "Mango")
print("after adding mango at the start",fruits)

fruits.insert(2, "grapes")
print("After adding grapes in the middle", fruits)

fruits.pop(0)
print("After Removing first element", fruits)

fruits.pop(2)
print("After removing middle element", fruits)

fruits.pop()
print("After removing last element")

fruits.remove("cherry")
print("after removing specific element cherry", fruits)

for fruit in fruits:
    print("Fruit", fruit)
    
coordinate = (10,20)
print("Coordinates:", coordinate)

print("X Coordinate:", coordinate[0])
print("Y Coordinate:", coordinate[1])

for crdnte in coordinate:
    print("Coordinate Value", coordinate)

student = {
    "name": "Subhan",
    "age": 20,
    "grade": "A"
}

print("Student Name:", student["name"])
print("Student Age:", student.get("age"))

student["age"] = 22
student["course"] = "Computer Science"
print("Updated Dictionaries", student)

del student["grade"]
print("After Removing Grade", student)

for key, value in student.items():
    print(f"{key}: {value}")

