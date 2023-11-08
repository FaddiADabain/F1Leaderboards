import customtkinter as ctk
from datetime import date


class Leaderboard(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.lapsT = None
        self.trackT = None
        self.countryT = None
        self.ptsL = None
        self.lapsL = None
        self.trackL = None
        self.countryL = None
        self.scrollable_frame = None
        self.controller = controller
        self.data = db
        self.load_data(self.controller.race_menu.get())
        self.setup_ui()

    def setup_ui(self):
        # Set weights for rows and columns
        self.grid_rowconfigure(1, weight=0)  # Country label row
        self.grid_rowconfigure(2, weight=0)  # Track row
        self.grid_rowconfigure(3, weight=1)  # Scrollable Frame row

        self.grid_columnconfigure(0, weight=1)  # Country and track label column
        self.grid_columnconfigure(1, weight=1)  # This will be the container for the segmented button
        self.grid_columnconfigure(2, weight=1)  # Laps and Pts label column

        # UI Elements
        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)

        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.trackL.grid(row=2, column=0, sticky="nw", padx=20)

        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.lapsL.grid(row=1, column=1, sticky="ne", columnspan=3, padx=20, pady=10)

        self.ptsL = ctk.CTkLabel(self, text="Pts.", font=("Lucidia Sans", 20))
        self.ptsL.grid(row=2, column=1, sticky="ne", columnspan=3, padx=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.fill_leader()

    def fill_leader(self):
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, item in enumerate(self.data):
            resultT = item[0]
            leaderT = item[1]
            ptsT = item[2]

            # Check if ptsT is an integer value, and if so, cast to int. Otherwise, keep it as a float.
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            self.scrollable_frame.grid_columnconfigure(1, weight=1)
            self.scrollable_frame.grid_columnconfigure(2, weight=1)

            resultL = ctk.CTkLabel(self.scrollable_frame, text=resultT, font=("Lucidia Sans", 17))
            resultL.grid(row=index, column=0, sticky="nw", padx=20, pady=10)

            leaderL = ctk.CTkLabel(self.scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
            leaderL.grid(row=index, column=1, sticky="nw", padx=20, pady=10)

            ptsL = ctk.CTkLabel(self.scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
            ptsL.grid(row=index, column=2, sticky="e", padx=20, pady=10)

    def load_data(self, race, season=date.today().year):
        query = (
            f"SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = {season} AND r.track ="
            "? ORDER BY date DESC")
        self.data.execute(query, (race, ))
        fetched = self.data.fetchone()

        self.countryT = fetched[0]
        self.trackT = fetched[1]
        self.lapsT = str(int(fetched[2]))
        seasonT = fetched[3]
        roundT = fetched[4]

        query = ("SELECT r.status, d.name, r.points "
                 "FROM results r "
                 "JOIN drivers d ON r.number = d.number AND r.season = d.season "
                 "JOIN races ra ON r.season = ra.season AND r.round = ra.round "
                 f"WHERE r.season = {seasonT} AND r.round = {roundT} "
                 "ORDER BY r.season, r.round, r.result")
        self.data.execute(query)
