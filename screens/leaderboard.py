import customtkinter as ctk  # Import CustomTkinter for enhanced tkinter widgets
from datetime import date  # Import date class from datetime module for handling dates

# Define a class 'Leaderboard' that inherits from CTkFrame, a customtkinter class for frames
class Leaderboard(ctk.CTkFrame):
    # Constructor for the Leaderboard class
    def __init__(self, parent, controller, db):
        super().__init__(parent)  # Call the constructor of the base class
        # Initialize various attributes to store leaderboard data and UI elements
        self.lapsT = None
        self.trackT = None
        self.countryT = None
        self.ptsL = None
        self.lapsL = None
        self.trackL = None
        self.countryL = None
        self.scrollable_frame = None
        self.controller = controller  # Store the reference to the controller
        self.data = db  # Store the database connection
        self.setup_ui()  # Call the method to setup the user interface

    # Define a method to setup the user interface
    def setup_ui(self):
        # Configure the grid layout for the frame
        self.grid_rowconfigure([1, 2], weight=0)  # Configure rows for labels
        self.grid_rowconfigure(3, weight=1)  # Configure row for scrollable frame
        self.grid_columnconfigure([0, 1, 2], weight=1)  # Configure columns

        # Create and position UI elements: labels and scrollable frame
        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.ptsL = ctk.CTkLabel(self, text="Pts.", font=("Lucidia Sans", 20))
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)

        # Position labels and scrollable frame using grid layout
        self.countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)
        self.trackL.grid(row=2, column=0, sticky="nw", padx=20)
        self.lapsL.grid(row=1, column=1, sticky="ne", columnspan=3, padx=20, pady=10)
        self.ptsL.grid(row=2, column=1, sticky="ne", columnspan=3, padx=20)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.fill_leader()  # Call method to populate leaderboard

    # Define a method to fill the leaderboard with data
    def fill_leader(self):
        # Update labels with current data
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        # Clear existing widgets in scrollable frame before updating
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Populate scrollable frame with leaderboard data
        for index, item in enumerate(self.data):
            resultT, leaderT, ptsT = item  # Unpack data tuple
            # Format points value
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)
            # Create and position labels for each item in the data
            resultL, leaderL, ptsL = [ctk.CTkLabel(self.scrollable_frame, text=value, font=("Lucidia Sans", 17)) for value in [resultT, leaderT, ptsT_formatted]]
            resultL.grid(row=index, column=0, sticky="nw", padx=20, pady=10)
            leaderL.grid(row=index, column=1, sticky="nw", padx=20, pady=10)
            ptsL.grid(row=index, column=2, sticky="e", padx=20, pady=10)

    # Define a method to load data for the leaderboard
    def load_data(self, race, season=date.today().year):
        # SQL query to fetch race details
        query = ("SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = ? AND r.track = ? ORDER BY date DESC")
        self.data.execute(query,
