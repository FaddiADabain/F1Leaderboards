import customtkinter as ctk  # Enhanced tkinter module for improved UI elements
from datetime import date  # Date module for handling date operations

# Define the 'Leaderboard' class, inheriting from customtkinter's CTkFrame
class Leaderboard(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)  # Initialize the parent class (CTkFrame)
        # Initialize attributes for storing various data and UI elements
        self.lapsT = None  # Variable to store laps
        self.trackT = None  # Variable to store track information
        self.countryT = None  # Variable to store country information
        self.ptsL = None  # Label for points
        self.lapsL = None  # Label for laps
        self.trackL = None  # Label for track
        self.countryL = None  # Label for country
        self.scrollable_frame = None  # Scrollable frame for displaying leaderboard
        self.controller = controller  # Controller reference
        self.data = db  # Database connection
        self.load_data(self.controller.race_menu.get())  # Load data based on the selected race
        self.setup_ui()  # Setup the user interface

    def setup_ui(self):
        # Set grid weights for layout management
        self.grid_rowconfigure(1, weight=0)  # Weight for the country label row
        self.grid_rowconfigure(2, weight=0)  # Weight for the track row
        self.grid_rowconfigure(3, weight=1)  # Weight for the scrollable frame row

        self.grid_columnconfigure(0, weight=1)  # Weight for the first column
        self.grid_columnconfigure(1, weight=1)  # Weight for the second column
        self.grid_columnconfigure(2, weight=1)  # Weight for the third column

        # Create and configure UI elements (labels, scrollable frame)
        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.ptsL = ctk.CTkLabel(self, text="Pts.", font=("Lucidia Sans", 20))
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)

        # Position the UI elements in the grid
        self.countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)
        self.trackL.grid(row=2, column=0, sticky="nw", padx=20)
        self.lapsL.grid(row=1, column=1, sticky="ne", columnspan=3, padx=20, pady=10)
        self.ptsL.grid(row=2, column=1, sticky="ne", columnspan=3, padx=20)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.fill_leader()  # Populate the leaderboard data

    def fill_leader(self):
        # Update label text with the current data
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        # Clear existing content in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Populate the leaderboard with fetched data
        for index, item in enumerate(self.data):
            resultT = item[0]  # Result text
            leaderT = item[1]  # Leader text
            ptsT = item[2]  # Points text

            # Format points as integer if possible
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

            # Configure columns in the scrollable frame
            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            self.scrollable_frame.grid_columnconfigure(1, weight=1)
            self.scrollable_frame.grid_columnconfigure(2, weight=1)

            # Create and position labels for result, leader, and points
            resultL = ctk.CTkLabel(self.scrollable_frame, text=resultT, font=("Lucidia Sans", 17))
            leaderL = ctk.CTkLabel(self.scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
            ptsL = ctk.CTkLabel(self.scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
            
            # Grid placement for the result, leader, and points labels in the scrollable frame
            resultL.grid(row=index, column=0, sticky="nw", padx=20, pady=10)
            leaderL.grid(row=index, column=1, sticky="nw", padx=20, pady=10)
            ptsL.grid(row=index, column=2, sticky="e", padx=20, pady=10)

    def load_data(self, race, season=2023):
        # Load leaderboard data based on the selected race and season
        # SQL query to fetch race details
        query = ("SELECT r.country, r.track, r.laps, r.season, r.round FROM races r "
                f"WHERE r.season = {season} AND r.track = ? ORDER BY date DESC")
        self.data.execute(query, (race, ))  # Execute the query with the selected race
        fetched = self.data.fetchone()  # Fetch the first record from the query result

        # Update class attributes with the fetched race details
        self.countryT = fetched[0]  # Country name
        self.trackT = fetched[1]  # Track name
        # Laps count, check if it is available; otherwise, use placeholder text
        self.lapsT = str(int(fetched[2])) if fetched[2] is not None else "Not Updated Yet"
        seasonT = fetched[3]  # Season year
        roundT = fetched[4]  # Round number

        # SQL query to fetch leaderboard data for the given race and season
        query = (
            "SELECT r.status, d.name, r.points "
            "FROM results r "
            "JOIN drivers d ON r.number = d.number AND r.season = d.season "
            "JOIN races ra ON r.season = ra.season AND r.round = ra.round "
            f"WHERE r.season = {seasonT} AND r.round = {roundT} "
            "ORDER BY r.season, r.round, r.result")
        self.data.execute(query)  # Execute the query for leaderboard data
