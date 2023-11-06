import customtkinter as ctk
from datetime import date
from tkinter import Canvas


class ColoredLine(Canvas):
    def __init__(self, parent, segments, **kwargs):
        super().__init__(parent, **kwargs)
        self.segments = segments
        self.configure(height=20, bg='gray17', highlightthickness=0)
        self.draw_segments()
        self.bind("<Configure>", self.on_resize)

    def draw_segments(self):
        self.delete("segment")  # Clear existing line segments
        total_width = self.winfo_width()
        x_start = 0

        if isinstance(self.segments, tuple):  # If it's just a tuple, make it a list
            self.segments = [self.segments]

        if not all(isinstance(segment, tuple) for segment in self.segments):
            raise ValueError("All items in self.segments should be tuples.")

        for percentage, color in self.segments:
            x_end = x_start + (total_width * (percentage / 100))
            self.create_rectangle(x_start, 0, x_end, self.winfo_height(), fill=color, tags="segment")
            x_start = x_end

    def on_resize(self, event):
        self.draw_segments()


class Strategies(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.fetched = None
        self.result = None
        self.trackT = None
        self.lapsL = None
        self.trackL = None
        self.countryL = None
        self.ptsL = None
        self.lapsT = None
        self.countryT = None
        self.scrollable_frame = None
        self.controller = controller
        self.data = db
        self.load_data(self.controller.race_menu.get())
        self.setup_ui()
        self.fill()

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

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.fill()

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

        query = ("SELECT d.name, s.tirestat FROM drivers d JOIN strategies s ON d.number = s.number AND d.season = "
                 "s.season JOIN results r ON d.number = r.number AND d.season = r.season AND s.round = r.round "
                 f"WHERE d.season = {seasonT} AND r.round = {roundT} "
                 "ORDER BY r.result")
        self.data.execute(query)
        self.fetched = self.data.fetchall()

    def fill(self):
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.get_line_data()

        index = 0
        for name, segments in zip(self.fetched, self.result):
            leaderL = ctk.CTkLabel(self.scrollable_frame, text=name[0], font=("Lucidia Sans", 17))
            leaderL.pack(padx=20, pady=10)

            colored_line = ColoredLine(self.scrollable_frame, segments=segments,
                                       width=self.scrollable_frame.winfo_width())
            colored_line.pack(fill='x', expand=True, pady=5)
            index += 1

    def get_line_data(self):
        self.result = []

        for index, item in enumerate(self.fetched):
            # Define the mapping of codes to color names
            color_map = {
                'm': 'yellow',
                'h': 'white',
                's': 'red',
                'w': 'blue',
                'i': 'green'
            }

            # Split the input string by semicolons
            pairs = item[1].split(';')
            driver_stints = []  # List to hold tuples of percentage and color for each stint

            # Convert each pair into the desired tuple format
            for pair in pairs:
                code, laps_str = pair.split('-')
                color = color_map.get(code, 'unknown')  # Use get to handle unknown codes gracefully
                percentage = (int(laps_str) / int(self.lapsT)) * 100
                driver_stints.append((round(percentage, 2), color))  # Append to the driver's stints list

            self.result.append(driver_stints)  # Append the driver's entire stint list to the result list

    def run(self):
        self.mainloop()
