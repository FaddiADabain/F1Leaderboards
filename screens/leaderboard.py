import customtkinter as ctk
from datetime import date


class Leaderboard(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.data = db
        self.load_data()
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
        countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)

        trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        trackL.grid(row=2, column=0, sticky="nw", padx=20)

        lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        lapsL.grid(row=1, column=1, sticky="ne", columnspan=3, padx=20, pady=10)

        ptsL = ctk.CTkLabel(self, text="Pts.", font=("Lucidia Sans", 20))
        ptsL.grid(row=2, column=1, sticky="ne", columnspan=3, padx=20)

        scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        for i in range(20):
            leader = self.data.fetchone()
            resultT = leader[0]
            leaderT = leader[1]
            ptsT = leader[2]

            # Check if ptsT is an integer value, and if so, cast to int. Otherwise, keep it as a float.
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=1)
            scrollable_frame.grid_columnconfigure(2, weight=1)

            resultL = ctk.CTkLabel(scrollable_frame, text=resultT, font=("Lucidia Sans", 17))
            resultL.grid(row=i, column=0, sticky="nw", padx=20, pady=10)

            leaderL = ctk.CTkLabel(scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
            leaderL.grid(row=i, column=1, sticky="nw", padx=20, pady=10)

            ptsL = ctk.CTkLabel(scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
            ptsL.grid(row=i, column=2, sticky="e", padx=20, pady=10)

    def load_data(self):
        query = (
            f"SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = {date.today().year} AND r.round = 19 ORDER "
            "BY date DESC")
        self.data.execute(query)
        fetched = self.data.fetchone()

        self.countryT = fetched[0]
        self.trackT = fetched[1]
        self.lapsT = str(int(fetched[2]))
        seasonT = fetched[3]
        roundT = fetched[4]

        self.data.fetchall()

        query = ("SELECT r.status, d.name, r.points "
                 "FROM results r "
                 "JOIN drivers d ON r.number = d.number AND r.season = d.season "
                 "JOIN races ra ON r.season = ra.season AND r.round = ra.round "
                 f"WHERE r.season = {seasonT} AND r.round = {roundT} "
                 "ORDER BY r.season, r.round, r.result")
        self.data.execute(query)

    def run(self):
        self.mainloop()
