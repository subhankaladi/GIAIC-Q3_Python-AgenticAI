class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return self.factor * value

# Test
m = Multiplier(5)
print(callable(m))
print(m(10))
