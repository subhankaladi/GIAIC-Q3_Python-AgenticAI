def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    except TypeError:
        print("Error: Invalid input type. Please enter numbers")
    else:
        print(f"Division successfull Result:", {result})
    finally:
        print("Operation complete.")

divide_numbers(10, 2)
divide_numbers(10, 0)
divide_numbers(10, "2")