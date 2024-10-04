import tkinter as tk
from tkinter import messagebox

# Global list to store books
book_list = []

class Book:
    def __init__(self, name, author, genre, price, quantity, available=True):
        self.name = name
        self.author = author
        self.genre = genre
        self.price = price
        self.quantity = quantity
        self.available = available

    def __str__(self):
        return f"Name: {self.name}, Author: {self.author}, Genre: {self.genre}, Price: {self.price}, Quantity: {self.quantity}, Available: {self.available}"

def save_list():
    with open("books.txt", "w") as file:
        for book in book_list:
            file.write(f"{book.name}, {book.author}, {book.genre}, {book.price}, {book.quantity}, {book.available}\n")

def load_list():
    try:
        with open("books.txt", "r") as file:
            for line in file:
                name, author, genre, price, quantity, available = line.strip().split(", ")
                book = Book(name, author, genre, float(price), int(quantity), available == "True")
                book_list.append(book)
    except FileNotFoundError:
        print("No book list found")

def add_book():
    name = name_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if not (name and author and genre and price and quantity):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Price and quantity must be numeric")
        return

    book = Book(name, author, genre, price, quantity)
    book_list.append(book)
    messagebox.showinfo("Success", "Book added successfully")
    save_list()
    clear_entries()

def update_book():
    name = update_name_entry.get()
    author = update_author_entry.get()
    genre = update_genre_entry.get()
    price = update_price_entry.get()
    quantity = update_quantity_entry.get()

    if not (name and author and genre and price and quantity):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Price and quantity must be numeric")
        return

    found_books = [book for book in book_list if book.name.lower() == name.lower()]
    if found_books:
        for book in found_books:
            book.author = author
            book.genre = genre
            book.price = price
            book.quantity = quantity
        messagebox.showinfo("Success", "Book updated successfully")
        save_list()
        clear_update_entries()
    else:
        messagebox.showerror("Error", f"No book found with the name {name}")

def remove_book():
    name = remove_name_entry.get()

    found_books = [book for book in book_list if book.name.lower() == name.lower()]
    if found_books:
        for book in found_books:
            book_list.remove(book)
        messagebox.showinfo("Success", "Book removed successfully")
        save_list()
        clear_remove_entry()
    else:
        messagebox.showerror("Error", f"No book found with the name {name}")

def search_book():
    search_query = search_entry.get().lower()
    found_books = [book for book in book_list if search_query in book.name.lower()]
    search_result.delete(1.0, tk.END)
    if found_books:
        for book in found_books:
            search_result.insert(tk.END, f"{book}\n")
    else:
        messagebox.showinfo("Info", f"No book found with the name {search_query}")

def display_books():
    display_result.delete(1.0, tk.END)
    for book in book_list:
        display_result.insert(tk.END, f"{book}\n")

def total_quantity():
    total = sum(book.quantity for book in book_list)
    messagebox.showinfo("Total Quantity", f"Total Quantity: {total}")

def clear_entries():
    name_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

def clear_update_entries():
    update_name_entry.delete(0, tk.END)
    update_author_entry.delete(0, tk.END)
    update_genre_entry.delete(0, tk.END)
    update_price_entry.delete(0, tk.END)
    update_quantity_entry.delete(0, tk.END)

def clear_remove_entry():
    remove_name_entry.delete(0, tk.END)

# Create a login window
def login():
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        # Simple validation logic (you can modify this)
        if username == "admin" and password == "password":
            login_window.destroy()  # Close login window
            root.deiconify()  # Show the main window
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.configure(bg="#f0f8ff")

    tk.Label(login_window, text="Username:", bg="#f0f8ff").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg="#f0f8ff").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=validate_login)
    login_button.pack(pady=20)

# Create GUI window
root = tk.Tk()
root.title("Online Bookstore Inventory Management")
root.geometry("600x600")
root.configure(bg="#f0f8ff")  # Set background color
root.withdraw()  # Hide main window until login is successful

# Load existing data
load_list()

# Show the login window
login()

# Create a canvas and a scrollbar
canvas = tk.Canvas(root, bg="#f0f8ff")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Add the rest of your UI elements inside scrollable_frame
# Create a frame for adding books
add_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
add_frame.pack(pady=10)

tk.Label(add_frame, text="Add Book", font=("Arial", 14), bg="#f0f8ff").grid(row=0, columnspan=2)

tk.Label(add_frame, text="Name:", bg="#f0f8ff").grid(row=1, column=0, sticky="e")
name_entry = tk.Entry(add_frame)
name_entry.grid(row=1, column=1)

tk.Label(add_frame, text="Author:", bg="#f0f8ff").grid(row=2, column=0, sticky="e")
author_entry = tk.Entry(add_frame)
author_entry.grid(row=2, column=1)

tk.Label(add_frame, text="Genre:", bg="#f0f8ff").grid(row=3, column=0, sticky="e")
genre_entry = tk.Entry(add_frame)
genre_entry.grid(row=3, column=1)

tk.Label(add_frame, text="Price:", bg="#f0f8ff").grid(row=4, column=0, sticky="e")
price_entry = tk.Entry(add_frame)
price_entry.grid(row=4, column=1)

tk.Label(add_frame, text="Quantity:", bg="#f0f8ff").grid(row=5, column=0, sticky="e")
quantity_entry = tk.Entry(add_frame)
quantity_entry.grid(row=5, column=1)

# Button to add book
add_button = tk.Button(add_frame, text="Add Book", command=add_book)
add_button.grid(row=6, columnspan=2, pady=5)

# Create a frame for updating books
update_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
update_frame.pack(pady=10)

tk.Label(update_frame, text="Update Book", font=("Arial", 14), bg="#f0f8ff").grid(row=0, columnspan=2)

tk.Label(update_frame, text="Name:", bg="#f0f8ff").grid(row=1, column=0, sticky="e")
update_name_entry = tk.Entry(update_frame)
update_name_entry.grid(row=1, column=1)

tk.Label(update_frame, text="Author:", bg="#f0f8ff").grid(row=2, column=0, sticky="e")
update_author_entry = tk.Entry(update_frame)
update_author_entry.grid(row=2, column=1)

tk.Label(update_frame, text="Genre:", bg="#f0f8ff").grid(row=3, column=0, sticky="e")
update_genre_entry = tk.Entry(update_frame)
update_genre_entry.grid(row=3, column=1)

tk.Label(update_frame, text="Price:", bg="#f0f8ff").grid(row=4, column=0, sticky="e")
update_price_entry = tk.Entry(update_frame)
update_price_entry.grid(row=4, column=1)

tk.Label(update_frame, text="Quantity:", bg="#f0f8ff").grid(row=5, column=0, sticky="e")
update_quantity_entry = tk.Entry(update_frame)
update_quantity_entry.grid(row=5, column=1)

# Button to update book
update_button = tk.Button(update_frame, text="Update Book", command=update_book)
update_button.grid(row=6, columnspan=2, pady=5)

# Create a frame for removing books
remove_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
remove_frame.pack(pady=10)

tk.Label(remove_frame, text="Remove Book", font=("Arial", 14), bg="#f0f8ff").grid(row=0, columnspan=2)

tk.Label(remove_frame, text="Name:", bg="#f0f8ff").grid(row=1, column=0, sticky="e")
remove_name_entry = tk.Entry(remove_frame)
remove_name_entry.grid(row=1, column=1)

# Button to remove book
remove_button = tk.Button(remove_frame, text="Remove Book", command=remove_book)
remove_button.grid(row=2, columnspan=2, pady=5)

# Create a frame for searching books
search_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search Book", font=("Arial", 14), bg="#f0f8ff").grid(row=0, columnspan=2)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=1, column=0, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_book)
search_button.grid(row=1, column=1)

search_result = tk.Text(search_frame, height=5, width=40)
search_result.grid(row=2, columnspan=2, pady=5)

# Create a frame for displaying all books
display_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
display_frame.pack(pady=10)

tk.Label(display_frame, text="Display All Books", font=("Arial", 14), bg="#f0f8ff").grid(row=0, columnspan=2)

display_result = tk.Text(display_frame, height=10, width=50)
display_result.grid(row=1, columnspan=2, pady=5)

display_button = tk.Button(display_frame, text="Display Books", command=display_books)
display_button.grid(row=2, columnspan=2, pady=5)

# Create a button to calculate total quantity
total_quantity_button = tk.Button(scrollable_frame, text="Total Quantity", command=total_quantity)
total_quantity_button.pack(pady=10)

# Show the main window
root.mainloop()
