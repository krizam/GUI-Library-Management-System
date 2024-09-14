import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import time

from models.book import Book
from models.library import Library
from models.user import User

class MainWindow:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.setup_ui()

    def setup_ui(self):
        style = ttkb.Style(theme="flatly")
        self.root.configure(bg=style.colors.bg)
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        main_frame = ttkb.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_label = ttkb.Label(main_frame, text="Library Management System", 
                                  font=("Helvetica", 24, "bold"), bootstyle="inverse-primary")
        header_label.pack(pady=(0, 20), fill=X)

        self.notebook = ttkb.Notebook(main_frame, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)

        self.book_frame = ttkb.Frame(self.notebook, padding="20")
        self.user_frame = ttkb.Frame(self.notebook, padding="20")
        self.borrow_frame = ttkb.Frame(self.notebook, padding="20")

        self.notebook.add(self.book_frame, text="Book Management")
        self.notebook.add(self.user_frame, text="User Management")
        self.notebook.add(self.borrow_frame, text="Borrow & Return")

        self.setup_book_management()
        self.setup_user_management()
        self.setup_borrow_return()

    def setup_book_management(self):
        input_frame = ttkb.Frame(self.book_frame)
        input_frame.pack(fill=X, pady=(0, 20))

        self.book_entries = self.create_section(input_frame, "Book Title:", "Author:", "ISBN:")
        ttkb.Button(input_frame, text="Add Book", command=lambda: self.add_book(self.book_entries), 
                    bootstyle="success").pack(pady=10)

        self.books_table = Tableview(
            master=self.book_frame,
            coldata=[
                {"text": "Title", "stretch": True},
                {"text": "Author", "stretch": True},
                {"text": "ISBN", "stretch": False},
            ],
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle="primary",
        )
        self.books_table.pack(fill=BOTH, expand=YES)

        ttkb.Button(self.book_frame, text="Refresh Books", command=self.refresh_books, 
                    bootstyle="info").pack(pady=10)

    def setup_user_management(self):
        input_frame = ttkb.Frame(self.user_frame)
        input_frame.pack(fill=X, pady=(0, 20))

        self.user_entries = self.create_section(input_frame, "User ID:", "Name:")
        ttkb.Button(input_frame, text="Register User", command=lambda: self.add_user(self.user_entries), 
                    bootstyle="success").pack(pady=10)

        self.users_table = Tableview(
            master=self.user_frame,
            coldata=[
                {"text": "User ID", "stretch": False},
                {"text": "Name", "stretch": True},
            ],
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle="primary",
        )
        self.users_table.pack(fill=BOTH, expand=YES)

        ttkb.Button(self.user_frame, text="Refresh Users", command=self.refresh_users, 
                    bootstyle="info").pack(pady=10)

    def setup_borrow_return(self):
        input_frame = ttkb.Frame(self.borrow_frame)
        input_frame.pack(fill=X, pady=(0, 20))

        self.borrow_entries = self.create_section(input_frame, "User ID:", "Book ISBN:")
        ttkb.Button(input_frame, text="Borrow Book", command=lambda: self.borrow_book(self.borrow_entries), 
                    bootstyle="success").pack(side=LEFT, padx=(0, 10))
        ttkb.Button(input_frame, text="Return Book", command=self.return_book, 
                    bootstyle="warning").pack(side=LEFT)

        self.borrowed_books_table = Tableview(
            master=self.borrow_frame,
            coldata=[
                {"text": "ISBN", "stretch": False},
                {"text": "User", "stretch": True},
            ],
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle="primary",
        )
        self.borrowed_books_table.pack(fill=BOTH, expand=YES)

        ttkb.Button(self.borrow_frame, text="Refresh Borrowed Books", command=self.refresh_borrowed_books, 
                    bootstyle="info").pack(pady=10)

    def create_section(self, parent_frame, *labels):
        entries = {}
        for i, label_text in enumerate(labels):
            frame = ttkb.Frame(parent_frame)
            frame.pack(fill=X, pady=5)
            ttkb.Label(frame, text=label_text, width=10).pack(side=LEFT)
            entry = ttkb.Entry(frame, font=("Helvetica", 10))
            entry.pack(side=LEFT, expand=YES, fill=X)
            entries[f'entry{i+1}'] = entry
        return entries

    def add_book(self, entries):
        title = entries['entry1'].get()
        author = entries['entry2'].get()
        isbn = entries['entry3'].get()
        
        if title and author and isbn:
            book = Book(title, author, isbn)
            self.library.add_book(book)
            self.show_success_animation("Book added successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
            self.refresh_books()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def add_user(self, entries):
        user_id = entries['entry1'].get()
        name = entries['entry2'].get()
        
        if user_id and name:
            user = User(user_id, name)
            self.library.add_user(user)
            self.show_success_animation("User registered successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
            self.refresh_users()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def borrow_book(self, entries):
        user_id = entries['entry1'].get()
        isbn = entries['entry2'].get()
        
        if self.library.borrow_book(user_id, isbn):
            self.show_success_animation("Book borrowed successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
            self.refresh_borrowed_books()
        else:
            messagebox.showwarning("Error", "Book could not be borrowed. Check User ID or ISBN.")

    def return_book(self):
        user_id = self.borrow_entries['entry1'].get()
        isbn = self.borrow_entries['entry2'].get()
        
        if self.library.return_book(user_id, isbn):
            self.show_success_animation("Book returned successfully!")
            self.refresh_borrowed_books()
        else:
            messagebox.showwarning("Error", "Book could not be returned. Check User ID or ISBN.")

    def refresh_books(self):
        books = self.library.get_books()
        self.books_table.delete_rows()
        for book in books:
            self.books_table.insert_row("end", values=(book.title, book.author, book.isbn))
        self.animate_table(self.books_table)

    def refresh_users(self):
        users = self.library.get_users()
        self.users_table.delete_rows()
        for user in users:
            self.users_table.insert_row("end", values=(user.user_id, user.name))
        self.animate_table(self.users_table)

    def refresh_borrowed_books(self):
        borrowed_books = self.library.get_borrowed_books()
        self.borrowed_books_table.delete_rows()
        for isbn, user in borrowed_books.items():
            self.borrowed_books_table.insert_row("end", values=(isbn, user))
        self.animate_table(self.borrowed_books_table)

    def show_success_animation(self, message):
        success_window = ttkb.Toplevel(self.root)
        success_window.overrideredirect(True)
        success_window.attributes("-alpha", 0.0)
        success_window.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")

        frame = ttkb.Frame(success_window, padding=20)
        frame.pack()

        label = ttkb.Label(frame, text=message, font=("Helvetica", 16))
        label.pack()

        def fade_in():
            alpha = success_window.attributes("-alpha")
            if alpha < 1.0:
                success_window.attributes("-alpha", alpha + 0.1)
                success_window.after(50, fade_in)
            else:
                success_window.after(1000, fade_out)

        def fade_out():
            alpha = success_window.attributes("-alpha")
            if alpha > 0.0:
                success_window.attributes("-alpha", alpha - 0.1)
                success_window.after(50, fade_out)
            else:
                success_window.destroy()

        fade_in()

    def animate_table(self, table):
        rows = table.get_rows()
        table.delete_rows()
        
        def insert_row(index):
            if index < len(rows):
                table.insert_row("end", values=rows[index])
                self.root.after(50, insert_row, index + 1)

        insert_row(0)

