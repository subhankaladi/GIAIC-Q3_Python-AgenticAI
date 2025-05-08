class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name          # public
        self._salary = salary     # protected
        self.__ssn = ssn          # private

# Test
emp = Employee("John", 50000, "123-45-6789")
print(emp.name)           # Accessible
print(emp._salary)        # Accessible but discouraged
# print(emp.__ssn)        # Will raise AttributeError
print(emp._Employee__ssn) # Correct way to access private
