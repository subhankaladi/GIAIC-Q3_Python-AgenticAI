class Employee:
    def __init__(self, name):
        self.name = name

class Department:
    def __init__(self, employee):
        self.employee = employee

# Test
emp = Employee("Sara")
dept = Department(emp)
print(dept.employee.name)
