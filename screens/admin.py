import customtkinter as ctk  # Import CustomTkinter for enhanced tkinter widgets
import sqlite3  # Import sqlite3 for database interactions

# Define a class 'Admin' that inherits from CTkToplevel, a customtkinter class for top-level windows
class Admin(ctk.CTkToplevel):
    # Constructor for the Admin class
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)  # Call the constructor of the base class
        self.db = db  # Store the database connection
        self.after(100, lambda: self.state("zoomed"))  # Maximize window after 100ms
        self.iconbitmap("data/logo.ico")  # Set the window icon
        self.title("F1 Leaderboards Admin Panel")  # Set the window title
        ctk.set_appearance_mode("DARK")  # Set the theme to dark mode
        ctk.set_default_color_theme("blue")  # Set the color theme to blue

        # Create a frame for SQL input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Create an input field for SQL queries
        self.sql_input = ctk.CTkEntry(self.input_frame)
        self.sql_input.pack(side="left", fill="x", expand=True)

        # Create a button to execute SQL queries
        self.execute_button = ctk.CTkButton(self.input_frame, text="Execute", command=self.execute_query)
        self.execute_button.pack(side="right")

        # Create a textbox to display results
        self.results_display = ctk.CTkTextbox(self, state="disabled", height=10)
        self.results_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Bind the Enter key to execute the SQL query
        self.sql_input.bind("<Return>", self.execute_query)

    # Define a method to execute SQL queries
    def execute_query(self, event=None):
        query = self.sql_input.get()  # Get the query from the input field
        try:
            self.db.execute(query)  # Try executing the query
            results = self.db.fetchall()  # Fetch all results
            self.display_results(results)  # Display the results
        except sqlite3.Error as e:
            self.display_results(f"Error: {e}", error=True)  # Display error if query fails
        finally:
            self.sql_input.delete(0, 'end')  # Clear the input field

    # Define a method to display results or errors
    def display_results(self, results, error=False):
        self.results_display.configure(state="normal")  # Enable the textbox
        if error:
            self.results_display.insert("end", f"{results}\n")  # Insert error message
        else:
            for row in results:
                self.results_display.insert("end", f"{row}\n")  # Insert each row of results
        self.results_display.configure(state="disabled")  # Disable the textbox

    # Define a method to handle window close event
    def on_exit(self):
        self.destroy()  # Destroy the window

    # Main function to run the application
    def main(self):
        app = Admin()  # Create an instance of Admin
        app.protocol("WM_DELETE_WINDOW", app.on_exit)  # Bind window close event
        app.mainloop()  # Start the event loop
