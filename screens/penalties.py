import customtkinter as ctk  # Import CustomTkinter for enhanced tkinter widgets
from datetime import date  # Import date class from datetime module for handling dates

# Define a class 'Penalties' that inherits from CTkFrame, a customtkinter class for frames
class Penalties(ctk.CTkFrame):
    # Constructor for the Penalties class
    def __init__(self, parent, controller, db):
        super().__init__(parent)  # Call the constructor of the base class
        # Initialize various attributes to store penalties data and UI elements
        self.scrollable_frame = None
        self.lapsL = None
        self.trackL = None
        self.countryL = None
        self.penalties = None
        self.lapsT = None
        self.trackT = None
        self.countryT = None
        self.controller = controller  # Store the reference to the controller
        self.data = db  # Store the database connection
        self.load_data(self.controller.race_menu.get())  # Load the data based on the selected race
        self.setup_ui()  # Call the method to setup the user interface

    # Define a method to setup the user interface
    def setup_ui(self):
        # Configure the grid layout for the frame
        self.grid_rowconfigure([1, 2], weight=0)  # Configure rows for labels
        self.grid_rowconfigure(3, weight=1)  # Configure row for scrollable frame
        self.grid_columnconfigure([1, 2, 3], weight=1)  # Configure columns

        # Create and position UI elements: labels and scrollable frame
        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)

        # Position labels and scrollable frame using grid layout
        self.countryL.grid(row=1, column=1, sticky="nw", padx=20, pady=10)
        self.trackL.grid(row=2, column=1, sticky="nw", padx=20)
        self.lapsL.grid(row=1, column=2, sticky="ne", columnspan=3, padx=20, pady=10)
        self.scrollable_frame.grid(row=3, column=1, columnspan=3, pady=10, sticky="nsew")

        self.fill_penalties()  # Call method to populate the penalties section

    # Define a method to fill the penalties section with data
    def fill_penalties(self):
        # Update labels with current data
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        # Clear existing widgets in scrollable frame before updating
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Populate scrollable frame with penalties data
        i = 0
        while self.penalties:
            nameT, sessionT, offenceT, decisionT = self.penalties  # Unpack data tuple

            # Create and position labels for each item in the data
            nameL, sessionL, offenceL, decisionL = [ctk.CTkLabel(self.scrollable_frame, text=value, font=("Lucidia Sans", 17)) for value in [nameT, sessionT, offenceT, decisionT]]
            nameL.grid(row=i, column=0, sticky="nw", padx=20, pady=10)
            sessionL.grid(row=i, column=1, sticky="nw", padx=20, pady=10)
            offenceL.grid(row=i, column=2, sticky="nw", padx=20, pady=10)
            decisionL.grid(row=i, column=3, sticky="nw", padx=20, pady=10)

            self.penalties = self.data.fetchone()  # Fetch next row of penalties
            i += 1  # Increment row index

        # Define a method to load data for the penalties section
        def load_data(self, race, season=date.today().year):
            # SQL query to fetch race details
            query = ("SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = ? AND r.track = ? ORDER BY date DESC")
            self.data.execute(query, (season, race))  # Execute the query with provided season and race
            fetched = self.data.fetchone()  # Fetch one record

            # Extract and store race details
            self.countryT = fetched[0]  # Country of the race
            self.trackT = fetched[1]  # Track name
            # Store the number of laps; if it's not updated yet, use a placeholder string
            self.lapsT = str(int(fetched[2])) if fetched[2] is not None else "Not Updated Yet"
            seasonT = fetched[3]  # Season year
            roundT = fetched[4]  # Round number

            # SQL query to fetch penalties data
            query = ("SELECT d.name, p.session, p.offence, p.decision "
                     "FROM drivers d "
                     "JOIN penalties p ON d.number = p.number AND d.season = p.season "
                     f"WHERE p.round = {roundT} AND p.season = {seasonT} "
                     "ORDER BY p.incident")
            self.data.execute(query)  # Execute the query
            self.penalties = self.data.fetchone()  # Fetch the first record of penalties
