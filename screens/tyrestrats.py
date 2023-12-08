import customtkinter as ctk  # Import CustomTkinter for enhanced tkinter widgets
from datetime import date  # Import date for handling date-related operations
from tkinter import Canvas  # Import Canvas for creating custom drawing areas

# Custom canvas class for drawing colored line segments
class ColoredLine(Canvas):
    def __init__(self, parent, segments, **kwargs):
        super().__init__(parent, **kwargs)  # Initialize the base Canvas class
        self.segments = segments  # Store segment data (percentage and color for each segment)
        self.configure(height=20, bg='gray17', highlightthickness=0)  # Configure the appearance of the canvas
        self.draw_segments()  # Draw the initial segments on the canvas
        self.bind("<Configure>", self.on_resize)  # Bind the resize event to redraw segments

    def draw_segments(self):
        self.delete("segment")  # Clear existing segments before redrawing
        total_width = self.winfo_width()  # Get the current width of the canvas
        x_start = 0  # Starting position for drawing segments

        # Ensure the segments are in a list format
        if isinstance(self.segments, tuple):
            self.segments = [self.segments]

        # Check that each segment is a tuple (percentage, color)
        if not all(isinstance(segment, tuple) for segment in self.segments):
            raise ValueError("All items in self.segments should be tuples.")

        # Draw each segment as a colored rectangle
        for percentage, color in self.segments:
            x_end = x_start + (total_width * (percentage / 100))  # Calculate the end position of the segment
            self.create_rectangle(x_start, 0, x_end, self.winfo_height(), fill=color, tags="segment")
            x_start = x_end  # Update the start position for the next segment

    def on_resize(self, event):
        self.draw_segments()  # Redraw the segments when the canvas is resized

# Class for displaying racing strategies
class Strategies(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)  # Initialize the base CTkFrame class
        # Initialize attributes to store data and UI elements
        self.fetched = None  # To store fetched data from the database
        self.result = None  # To store processed strategy data for visualization
        self.trackT = None  # Track name
        self.lapsL = None  # Laps label
        self.trackL = None  # Track label
        self.countryL = None  # Country label
        self.ptsL = None  # Points label
        self.lapsT = None  # Total laps
        self.countryT = None  # Country name
        self.scrollable_frame = None  # Scrollable frame for displaying content
        self.controller = controller  # Reference to the controller
        self.data = db  # Database connection

        self.load_data(self.controller.race_menu.get())  # Load data for the selected race
        self.setup_ui()  # Setup the user interface

    def setup_ui(self):
        # Set up grid weights for rows and columns
        self.grid_rowconfigure(1, weight=0)  # Set weight for country label row
        self.grid_rowconfigure(2, weight=0)  # Set weight for track row
        self.grid_rowconfigure(4, weight=1)  # Set weight for scrollable frame row

        self.grid_columnconfigure(0, weight=1)  # Set weight for first column
        self.grid_columnconfigure(1, weight=1)  # Set weight for second column
        self.grid_columnconfigure(2, weight=1)  # Set weight for third column
        self.grid_columnconfigure(3, weight=1)  # Set weight for fourth column
        self.grid_columnconfigure(4, weight=1)  # Set weight for fifth column

        # Create and configure UI elements
        self.countryL = ctk.CTkLabel(self, text=self.countryT, font=("Lucidia Sans", 25))
        self.countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)  # Position the country label

        self.trackL = ctk.CTkLabel(self, text=self.trackT, font=("Lucidia Sans", 20))
        self.trackL.grid(row=2, column=0, sticky="nw", padx=20)  # Position the track label

        self.lapsL = ctk.CTkLabel(self, text=f"Laps: {self.lapsT}", font=("Lucidia Sans", 20))
        self.lapsL.grid(row=1, column=1, sticky="ne", columnspan=5, padx=20, pady=10)  # Position the laps label

        # Create and position color code labels
        red = ctk.CTkLabel(self, text="Red = Soft", font=("Lucidia Sans", 15))
        red.grid(row=3, column=0, sticky="ns", padx=10, pady=10)  # Position the red label

        yellow = ctk.CTkLabel(self, text="Yellow = Medium", font=("Lucidia Sans", 15))
        yellow.grid(row=3, column=1, sticky="ns", padx=10, pady=10)  # Position the yellow label

        white = ctk.CTkLabel(self, text="White = Hard", font=("Lucidia Sans", 15))
        white.grid(row=3, column=2, sticky="ns", padx=10, pady=10)  # Position the white label

        green = ctk.CTkLabel(self, text="Green = Inter", font=("Lucidia Sans", 15))
        green.grid(row=3, column=3, sticky="ns", padx=10, pady=10)  # Position the green label

        blue = ctk.CTkLabel(self, text="Blue = Wet", font=("Lucidia Sans", 15))
        blue.grid(row=3, column=4, sticky="ns", padx=10, pady=10)  # Position the blue label

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=4, column=0, columnspan=5, pady=10, sticky="nsew")  # Position the scrollable frame

        self.fill()  # Call the fill method to populate the frame

    def load_data(self, race, season=date.today().year):
        # SQL query to fetch race details
        query = (
            "SELECT r.country, r.track, r.laps, r.season, r.round FROM races r "
            "WHERE r.season = ? AND r.track = ? ORDER BY date DESC")
        self.data.execute(query, (season, race))  # Execute the query with provided season and race
        fetched = self.data.fetchone()  # Fetch race details

        # Update class attributes with race details
        self.countryT = fetched[0]  # Country of the race
        self.trackT = fetched[1]  # Track name
        self.lapsT = str(int(fetched[2])) if fetched[2] is not None else "Not Updated Yet"  # Number of laps

        # SQL query to fetch strategy data
        query = (
            "SELECT d.name, s.tirestrat FROM drivers d "
            "JOIN strategies s ON d.number = s.number AND d.season = s.season "
            "JOIN results r ON d.number = r.number AND d.season = r.season AND s.round = r.round "
            "WHERE d.season = ? AND r.round = ? "
            "ORDER BY r.result")
        self.data.execute(query, (season, fetched[4]))  # Execute the query with season and round number
        self.fetched = self.data.fetchall()  # Fetch strategy data

    def fill(self):
        # Update UI elements with the fetched data
        self.countryL.configure(text=self.countryT)
        self.trackL.configure(text=self.trackT)
        self.lapsL.configure(text=f"Laps: {self.lapsT}")

        # Clear existing widgets in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Process and visualize the strategy data
        self.get_line_data()
        for name, segments in zip(self.fetched, self.result):
            leaderL = ctk.CTkLabel(self.scrollable_frame, text=name[0], font=("Lucidia Sans", 17))
            leaderL.pack(padx=20, pady=10)  # Pack the driver's name label

            # Create and pack a colored line for each driver's strategy
            colored_line = ColoredLine(self.scrollable_frame, segments=segments, width=self.scrollable_frame.winfo_width())
            colored_line.pack(fill='x', expand=True, pady=5)

    def get_line_data(self):
        # Prepare the line data for visual representation
        self.result = []

        for _, item in enumerate(self.fetched):
            # Define the mapping of tire codes to color names
            color_map = {
                'm': 'yellow', 'h': 'white', 's': 'red', 'w': 'blue', 'i': 'green'
            }

            # Split the tire strategy string into segments
            pairs = item[1].split(';')
            driver_stints = []  # List to store segments for each driver

            # Process each pair to create a segment (percentage and color)
            for pair in pairs:
                code, laps_str = pair.split('-')
                color = color_map.get(code, 'unknown')  # Get the color for the tire code
                percentage = (int(laps_str) / int(self.lapsT)) * 100  # Calculate the percentage of the stint
                driver_stints.append((round(percentage, 2), color))  # Append the segment to the driver's stints

            self.result.append(driver_stints)  # Add the driver's stints to the result list
