import customtkinter as ctk  # Enhanced tkinter module for improved UI elements
from datetime import date  # Date module for handling date operations


# Define the 'Penalties' class, inheriting from customtkinter's CTkFrame
class Penalties(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)    # Initialize the parent class (CTkFrame)
        # Initialize attributes for storing various data and UI elements
        self.scrollable_frame = None
        self.lapsL = None
        self.trackL = None
        self.countryL = None
        self.penalties = None
        self.lapsT = None
        self.trackT = None
        self.countryT = None
        
        self.controller = controller  # Controller reference
        self.data = db  # Database connection
        self.load_data(self.controller.race_menu.get())  # Load data based on the selected race
        self.setup_ui()  # Setup the user interface

    def setup_ui(self):
        # Set grid weights for layout management and create UI elements
        # Configure rows and columns with appropriate weights for the layout

        # Set weights for rows and columns
        self.grid_rowconfigure(1, weight=0)  # Country label row
        self.grid_rowconfigure(2, weight=0)  # Track row
        self.grid_rowconfigure(3, weight=1)  # Scrollable Frame row

        self.grid_columnconfigure(1, weight=1)  # Country and track label column
        self.grid_columnconfigure(2, weight=1)  # This will be the container for the segmented button
        self.grid_columnconfigure(3, weight=1)  # Laps and Pts label column

        # UI Elements

        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.countryL.grid(row=1, column=1, sticky="nw", padx=20, pady=10)

        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.trackL.grid(row=2, column=1, sticky="nw", padx=20)

        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.lapsL.grid(row=1, column=2, sticky="ne", columnspan=3, padx=20, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=1, columnspan=3, pady=10, sticky="nsew")

        self.fill_penalties()

    def fill_penalties(self):
        # Update label text with the current data and populate penalties
        # Clear existing content in the scrollable frame
        # Iterate over fetched penalty data, creating and positioning labels
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        i = 0
        while self.penalties:
            nameT = self.penalties[0]
            sessionT = self.penalties[1]
            offenceT = self.penalties[2]
            decisionT = self.penalties[3]

            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            self.scrollable_frame.grid_columnconfigure(1, weight=1)
            self.scrollable_frame.grid_columnconfigure(2, weight=1)

            nameL = ctk.CTkLabel(self.scrollable_frame, text=nameT, font=("Lucidia Sans", 17))
            nameL.grid(row=i, column=0, sticky="nw", padx=20, pady=10)

            sessionL = ctk.CTkLabel(self.scrollable_frame, text=sessionT, font=("Lucidia Sans", 17))
            sessionL.grid(row=i, column=1, sticky="nw", padx=20, pady=10)

            offenceL = ctk.CTkLabel(self.scrollable_frame, text=offenceT, font=("Lucidia Sans", 17))
            offenceL.grid(row=i, column=2, sticky="nw", padx=20, pady=10)

            decisionL = ctk.CTkLabel(self.scrollable_frame, text=decisionT, font=("Lucidia Sans", 17))
            decisionL.grid(row=i, column=3, sticky="nw", padx=20, pady=10)

            self.penalties = self.data.fetchone()
            i += 1

    def load_data(self, race, season=2023):
        # Load penalty data based on the selected race and season
        # Execute SQL queries to fetch race details and penalty data
        # Update class attributes with fetched data
        query = (
            f"SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = {season} AND r.track ="
            "? ORDER BY date DESC")
        self.data.execute(query, (race,))
        fetched = self.data.fetchone()

        self.countryT = fetched[0]
        self.trackT = fetched[1]
        if fetched[2] is not None:
            self.lapsT = str(int(fetched[2]))
        else:
            self.lapsT = "Not Updated Yet"
        seasonT = fetched[3]
        roundT = fetched[4]

        query = ("SELECT d.name, p.session, p.offence, p.decision "
                 "FROM drivers d "
                 "JOIN penalties p ON d.number = p.number AND d.season = p.season "
                 f"WHERE p.round = {roundT} AND p.season = {seasonT} "
                 "ORDER BY p.incident")
        self.data.execute(query)

        self.penalties = self.data.fetchone()
