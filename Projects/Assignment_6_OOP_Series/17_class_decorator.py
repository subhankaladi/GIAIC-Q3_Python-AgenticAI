def add_greeting(cls):
    cls.greet = lambda self: "Hello from Decorator!"
    return cls

@add_greeting
class Person:
    def __init__(self, name):
        self.name = name

# Test
p = Person("Ali")
print(p.greet())
