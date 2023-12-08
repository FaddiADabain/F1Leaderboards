import customtkinter as ctk  # Import CustomTkinter for enhanced tkinter widgets
import sqlite3  # Import sqlite3 for database interactions

# Define a class 'Login' that inherits from CTkToplevel, a customtkinter class for top-level windows
class Login(ctk.CTkToplevel):
    # Constructor for the Login class
    def __init__(self, master, db_connection, db_cursor, *args, **kwargs):
        super().__init__(master, *args, **kwargs)  # Call the constructor of the base class
        self.db_connection = db_connection  # Store the database connection
        self.db_cursor = db_cursor  # Store the database cursor
        self.master = master  # Reference to the parent window
        self.title("Login")  # Set the window title

        # Set the window to be always on top
        self.transient(master)

        # Create entry fields for username and password
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.username_entry.pack(pady=10)
        self.password_entry.pack(pady=10)

        # Create a login button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Create a separator label
        separator = ctk.CTkLabel(self, text="Create New Admin")
        separator.pack(pady=10)

        # Create entry fields for creating a new admin account
        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="New Username")
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_username_entry.pack(pady=10, padx=100)
        self.new_password_entry.pack(pady=10)

        # Create a button for creating a new admin account
        self.create_account_button = ctk.CTkButton(self, text="Create Admin Account", command=self.create_account)
        self.create_account_button.pack(pady=10)

    # Define a method for login functionality
    def login(self):
        # Retrieve entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Verify credentials and proceed if correct
        if self.verify_credentials(username, password):
            self.destroy()  # Close the login window
            self.master.open_admin()  # Open the admin panel

    # Define a method to verify login credentials
    def verify_credentials(self, username, password):
        try:
            # Execute SQL query to find the admin with given username and password
            self.db_cursor.execute("SELECT * FROM admins WHERE user = ? AND pass = ?", (username, password))
            admin = self.db_cursor.fetchone()  # Fetch one record
            return admin is not None  # Return True if admin exists, else False
        except Exception as e:
            print(f"Error: {e}")
            return False

    # Define a method for creating a new admin account
    def create_account(self):
        # Retrieve entered new username and password
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        # Ensure that the fields are not empty
        if new_username and new_password:
            try:
                # Insert new admin data into the database
                self.db_cursor.execute("INSERT INTO admins (user, pass) VALUES (?, ?)", (new_username, new_password))
                self.db_connection.commit()  # Commit the transaction
                print("New admin account created successfully.")
                # Clear the entry fields
                self.new_username_entry.delete(0, 'end')
                self.new_password_entry.delete(0, 'end')
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Username and password cannot be empty.")
