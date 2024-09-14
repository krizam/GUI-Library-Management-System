from tkinter import messagebox

class Library:
    def __init__(self):
        self.books = []  # List to store all books
        self.users = []  # List to store all users
        self.borrowed_books = {}  # Dictionary to map ISBNs to user names

    def add_book(self, book):
        # Add book to the library's book collection
        self.books.append(book)

    def get_books(self):
        # Return the list of books
        return self.books

    def add_user(self, user):
        # Add a user to the library's user list
        self.users.append(user)

    def get_users(self):
        # Return the list of users
        return self.users

    def borrow_book(self, user_id, isbn):
        # Check if the user and book exist and if the book is not borrowed
        user = self.find_user(user_id)
        book = self.find_book(isbn)
        if user and book and not book.is_borrowed:
            # Mark the book as borrowed
            book.is_borrowed = True
            # Add the book to the user's borrowed list
            user.borrowed_books.append(book)
            # Store the borrowed book's ISBN and the user's name in borrowed_books
            self.borrowed_books[isbn] = user.name
            return True
        return False

    def return_book(self, user_id, isbn):
        # Check if the user and book exist and if the book is borrowed
        user = self.find_user(user_id)
        book = self.find_book(isbn)
        if user and book and book.is_borrowed:
            # Mark the book as not borrowed
            book.is_borrowed = False
            # Remove the book from the user's borrowed list
            user.borrowed_books.remove(book)
            # Remove the book from the borrowed_books dictionary
            self.borrowed_books.pop(isbn, None)
            return True
        return False

    def get_borrowed_books(self):
        # Return the dictionary of borrowed books
        return self.borrowed_books

    def find_user(self, user_id):
        # Search for the user by user_id in the user list
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def find_book(self, isbn):
        # Search for the book by ISBN in the book list
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
