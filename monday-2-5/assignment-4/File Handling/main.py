import os

def create_file(filename, content):
    """Create a file and writes content to it."""

    with open(filename, 'w') as file:
        file.write(content)
    print(f"File {filename} created successfully")

#Demo File:
demo_file = "example.txt"

create_file(demo_file, "Hello this is a file handling example")

def read_file(filename):
    """Read and prints the content of a file"""

    try:
        with open(filename, "r") as file:
            content = file.read()
            print(f"Content of {filename} : \n {content}")
    except FileNotFoundError:
        print(f"error file {filename} not found")


read_file(demo_file)


def append_to_file(filename, content):
    """Appends content to asn existing file."""

    try:
        with open(filename, "a") as file:
            file.write("\n" + content)
        print(f"Content appended to {filename} Successfully")
    except FileNotFoundError:
        print(f"Error File {filename} Not Found")

append_to_file(demo_file, "This is additional line of text")


def delete_file(filename):
    """Delete a file if it exists."""

    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} delete successfully")
    else:
        print(f"Error File {filename} does not exists.")

# delete_file(demo_file)  #run this if you delete the exist file.

