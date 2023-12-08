import customtkinter as ctk  # Enhanced tkinter module for improved UI elements
from datetime import date  # Date module for handling date operations
from tkinter import Canvas  # Import Canvas for creating custom drawing areas

# Define a custom canvas class for drawing colored line segments
class ColoredLine(Canvas):
    def __init__(self, parent, segments, **kwargs):
        super().__init__(parent, **kwargs)  # Initialize the base Canvas class
        self.segments = segments  # Store the segments data (percentage and color for each segment)
        self.configure(height=20, bg='gray17', highlightthickness=0)  # Configure the canvas appearance
        self.draw_segments()  # Draw the initial segments on the canvas
        self.bind("<Configure>", self.on_resize)  # Bind the resize event to redraw segments

    def draw_segments(self):
        self.delete("segment")  # Clear existing line segments
        total_width = self.winfo_width()  # Get the width of the canvas
        x_start = 0  # Starting position for the first segment

        # Ensure segments are in list format
        if isinstance(self.segments, tuple):
            self.segments = [self.segments]

        # Check if all segments are tuples (percentage, color)
        if not all(isinstance(segment, tuple) for segment in self.segments):
            raise ValueError("All items in self.segments should be tuples.")

        # Draw each segment as a colored rectangle on the canvas
        for percentage, color in self.segments:
            x_end = x_start + (total_width * (percentage / 100))  # Calculate end position of segment
            self.create_rectangle(x_start, 0, x_end, self.winfo_height(), fill=color, tags="segment")
            x_start = x_end  # Update start position for next segment

    def on_resize(self, event):
        self.draw_segments()  # Redraw segments when canvas is resized


# Define the 'Strategies' class, inheriting from customtkinter's CTkFrame
class Strategies(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)    # Initialize the parent class (CTkFrame)
        # Initialize various attributes for data storage and UI elements
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
        
        self.controller = controller  # Controller reference
        self.data = db  # Database connection
        self.load_data(self.controller.race_menu.get())  # Load data based on the selected race
        self.setup_ui()  # Setup the user interface
        self.fill()  # Populate the frame with data

    # Configure grid weights for layout management and create UI elements
    def setup_ui(self):
        # Set weights for rows and columns
        self.grid_rowconfigure(1, weight=0)  # Country label row
        self.grid_rowconfigure(2, weight=0)  # Track row
        self.grid_rowconfigure(4, weight=1)  # Scrollable Frame row

        self.grid_columnconfigure(0, weight=1)  # Country and track label column
        self.grid_columnconfigure(1, weight=1)  # This will be the container for the segmented button
        self.grid_columnconfigure(2, weight=1)  # Laps and Pts label column
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # UI Elements
        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)

        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.trackL.grid(row=2, column=0, sticky="nw", padx=20)

        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.lapsL.grid(row=1, column=1, sticky="ne", columnspan=5, padx=20, pady=10)

        red = ctk.CTkLabel(self, text="Red = Soft", font=("Lucidia Sans", 15))
        red.grid(row=3, column=0, sticky="ns", padx=10, pady=10)

        yellow = ctk.CTkLabel(self, text="Yellow = Medium", font=("Lucidia Sans", 15))
        yellow.grid(row=3, column=1, sticky="ns", padx=10, pady=10)

        white = ctk.CTkLabel(self, text="White = Hard", font=("Lucidia Sans", 15))
        white.grid(row=3, column=2, sticky="ns", padx=10, pady=10)

        green = ctk.CTkLabel(self, text="Green = Inter", font=("Lucidia Sans", 15))
        green.grid(row=3, column=3, sticky="ns", padx=10, pady=10)

        blue = ctk.CTkLabel(self, text="Blue = Wet", font=("Lucidia Sans", 15))
        blue.grid(row=3, column=4, sticky="ns", padx=10, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=4, column=0, columnspan=5, pady=10, sticky="nsew")

        self.fill()

    # Load strategy data based on the selected race and season
    def load_data(self, race, season=date.today().year):
        query = (
            f"SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = {season} AND r.track ="
            "? ORDER BY date DESC")
        self.data.execute(query, (race, ))
        fetched = self.data.fetchone()

        self.countryT = fetched[0]
        self.trackT = fetched[1]
        if fetched[2] is not None:
            self.lapsT = str(int(fetched[2]))
        else:
            self.lapsT = "Not Updated Yet"
        seasonT = fetched[3]
        roundT = fetched[4]

        query = ("SELECT d.name, s.tirestrat FROM drivers d JOIN strategies s ON d.number = s.number AND d.season = "
                 "s.season JOIN results r ON d.number = r.number AND d.season = r.season AND s.round = r.round "
                 f"WHERE d.season = {seasonT} AND r.round = {roundT} "
                 "ORDER BY r.result")
        self.data.execute(query)
        self.fetched = self.data.fetchall()

    # Update UI elements with the fetched data and create colored lines for each strategy
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

    # Process the fetched data into a format suitable for colored line representation
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
