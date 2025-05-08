class Engine:
    def start(self):
        print("Engine started.")

class Car:
    def __init__(self, engine):
        self.engine = engine

    def start_car(self):
        self.engine.start()

# Test
e = Engine()
c = Car(e)
c.start_car()
