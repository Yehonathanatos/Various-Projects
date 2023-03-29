import sqlite3

# connect to the database
conn = sqlite3.connect('ebookstore.db')
c = conn.cursor()

# create the books table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY,
              title TEXT,
              author TEXT,
              qty INTEGER)''')

# function to add a new book
def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author name: ")
    qty = int(input("Enter the quantity: "))
    c.execute("INSERT INTO books (title, author, qty) VALUES (?, ?, ?)", (title, author, qty))
    conn.commit()
    print("Book added successfully!")

# function to update book information
def update_book():
    book_id = int(input("Enter the book ID: "))
    title = input("Enter the new book title (press enter to leave unchanged): ")
    author = input("Enter the new author name (press enter to leave unchanged): ")
    qty = input("Enter the new quantity (press enter to leave unchanged): ")
    if title:
        c.execute("UPDATE books SET title = ? WHERE id = ?", (title, book_id))
    if author:
        c.execute("UPDATE books SET author = ? WHERE id = ?", (author, book_id))
    if qty:
        c.execute("UPDATE books SET qty = ? WHERE id = ?", (qty, book_id))
    conn.commit()
    print("Book information updated successfully!")

# function to delete a book
def delete_book():
    book_id = int(input("Enter the book ID: "))
    c.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")

# function to search for a book
def search_books():
    search_term = input("Enter a search term: ")
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%'+search_term+'%', '%'+search_term+'%'))
    results = c.fetchall()
    if results:
        print("Search results:")
        for row in results:
            print(row)
    else:
        print("No matching books found.")

# main program loop
while True:
    print("\nBOOKSTORE CLERK PROGRAM")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        add_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# close the database connection
conn.close()
