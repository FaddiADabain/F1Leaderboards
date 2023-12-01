import customtkinter as ctk
import sqlite3

class Login(ctk.CTkToplevel):
    def __init__(self, master, db_connection, db_cursor, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db_connection = db_connection  # The actual database connection
        self.db_cursor = db_cursor  # The database cursor
        self.master = master
        self.title("Login")

        # Set the window to be always on top
        self.transient(master)

        # Create fields for username and password
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        # Create a login button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Separator
        separator = ctk.CTkLabel(self, text="Create New Admin")
        separator.pack(pady=10)

        # Create fields for new admin username and password
        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="New Username")
        self.new_username_entry.pack(pady=10, padx=100)
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_password_entry.pack(pady=10)

        # Create a create account button
        self.create_account_button = ctk.CTkButton(self, text="Create Admin Account", command=self.create_account)
        self.create_account_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.verify_credentials(username, password):
            self.destroy()
            self.master.open_admin()

    def verify_credentials(self, username, password):
        try:
            self.db_cursor.execute("SELECT * FROM admins WHERE user = ? AND pass = ?", (username, password))
            admin = self.db_cursor.fetchone()
            return admin is not None
        except Exception as e:
            print(f"Error: {e}")
            return False

    def create_account(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if new_username and new_password:  # Ensure that the fields are not empty
            try:
                self.db_cursor.execute("INSERT INTO admins (user, pass) VALUES (?, ?)", (new_username, new_password))
                self.db_connection.commit()  # Commit changes using the connection object
                print("New admin account created successfully.")
                self.new_username_entry.delete(0, 'end')  # Clear the username field
                self.new_password_entry.delete(0, 'end')  # Clear the password field
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Username and password cannot be empty.")
