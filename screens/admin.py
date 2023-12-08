import customtkinter as ctk  # Enhanced tkinter module for improved UI elements
import sqlite3  # SQLite3 for database operations

# Define the 'Admin' class, inheriting from customtkinter's CTkToplevel
class Admin(ctk.CTkToplevel):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)  # Initialize the parent class (CTkToplevel)
        self.db = db  # Database connection
        # Set up the initial state and appearance of the window
        self.after(100, lambda: self.state("zoomed"))  # Maximize the window after 100ms
        self.iconbitmap("data/logo.ico")  # Set window icon
        self.title("F1 Leaderboards Admin Panel")  # Set window title
        ctk.set_appearance_mode("DARK")  # Set dark mode for the UI
        ctk.set_default_color_theme("blue")  # Set default color theme

        # Create a frame for SQL input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

        # SQL Input Field
        self.sql_input = ctk.CTkEntry(self.input_frame)
        self.sql_input.pack(side="left", fill="x", expand=True)

        # Execute Button to run the SQL query
        self.execute_button = ctk.CTkButton(self.input_frame, text="Execute", command=self.execute_query)
        self.execute_button.pack(side="right")

        # Textbox for displaying results of SQL queries
        self.results_display = ctk.CTkTextbox(self, state="disabled", height=10)
        self.results_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Binding the Enter key to execute SQL query
        self.sql_input.bind("<Return>", self.execute_query)

    def execute_query(self, event=None):
        # Function to execute the SQL query entered in the input field
        query = self.sql_input.get()  # Get the query from the input field
        try:
            self.db.execute(query)  # Execute the SQL query
            results = self.db.fetchall()  # Fetch the results of the query
            self.display_results(results)  # Display the results
        except sqlite3.Error as e:
            # Handle any SQLite errors
            self.display_results(f"Error: {e}", error=True)
        finally:
            # Clear the SQL input field after query execution
            self.sql_input.delete(0, 'end')

    def display_results(self, results, error=False):
        # Function to display the results or errors in the results textbox
        self.results_display.configure(state="normal")  # Enable the textbox to modify text
        if error:
            # Display the error message
            self.results_display.insert("end", f"{results}\n")
        else:
            # Display each row of the query results
            for row in results:
                self.results_display.insert("end", f"{row}\n")
        self.results_display.configure(state="disabled")  # Disable the textbox after updating text

    def on_exit(self):
        # Function to handle the window closing event
        self.destroy()  # Destroy the window

    def main(self):
        # Main function to run the application (not typically used as Admin is a Toplevel window)
        app = Admin()
        app.protocol("WM_DELETE_WINDOW", app.on_exit)
        app.mainloop()  # Start the application's main loop
