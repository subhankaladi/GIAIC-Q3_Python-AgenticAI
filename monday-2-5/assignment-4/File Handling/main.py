import os

def create_file(filename, content):
    """Create a file and writes content to it."""

    with open(filename, 'w') as file:
        file.write(content)
    print(f"File {filename} created successfully")
demo_file = "example.txt"

create_file(demo_file, "Hello this is a file handling example")