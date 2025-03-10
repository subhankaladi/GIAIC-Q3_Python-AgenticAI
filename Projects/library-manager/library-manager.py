import streamlit as st
import json
import os

# File path for saving the library
data_file = 'library.txt'

# Load library from file
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

# Add a book to the library
def add_book(library, book):
    library.append(book)
    save_library(library)

# Remove a book by title
def remove_book(library, title):
    library[:] = [book for book in library if book['title'].lower() != title.lower()]
    save_library(library)

# Search for books by title or author
def search_books(library, search_term, search_by):
    return [book for book in library if search_term.lower() in book[search_by].lower()]

# Display statistics
def display_statistics(library):
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# Main Streamlit app
def main():
    st.title("📚 Personal Library Manager")
    library = load_library()

    menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read this book?", ["Yes", "No"]) == "Yes"

        if st.button("Add Book"):
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            add_book(library, new_book)
            st.success(f'Book "{title}" added successfully!')

    elif choice == "Remove Book":
        st.subheader("Remove a Book")
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            remove_book(library, title)
            st.success(f'Book "{title}" removed successfully!')

    elif choice == "Search Book":
        st.subheader("Search for a Book")
        search_by = st.selectbox("Search by", ["title", "author"])
        search_term = st.text_input(f"Enter the {search_by}")
        if st.button("Search"):
            results = search_books(library, search_term, search_by)
            if results:
                for book in results:
                    st.write(f'**{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"Read" if book["read"] else "Unread"}')
            else:
                st.info("No matching books found.")

    elif choice == "Display All Books":
        st.subheader("All Books in the Library")
        if library:
            for book in library:
                st.write(f'**{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"Read" if book["read"] else "Unread"}')
        else:
            st.info("No books in the library.")

    elif choice == "Display Statistics":
        st.subheader("Library Statistics")
        total, percentage = display_statistics(library)
        st.write(f"Total Books: {total}")
        st.write(f"Percentage Read: {percentage:.2f}%")

if __name__ == "__main__":
    main()
