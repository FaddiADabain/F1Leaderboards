import customtkinter as ctk  # Import CustomTkinter for enhanced tkinter widgets
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import TkAgg backend for embedding matplotlib in tkinter
from datetime import date  # Import date class from datetime module for handling dates

# Define a class 'Standings' that inherits from CTkFrame, a customtkinter class for frames
class Standings(ctk.CTkFrame):
    # Constructor for the Standings class
    def __init__(self, parent, controller, db):
        super().__init__(parent)  # Call the constructor of the base class
        self.scrollable_frame = None  # Initialize a variable for the scrollable frame
        self.controller = controller  # Store the reference to the controller
        self.data = db  # Store the database connection
        self.table = "Drivers' Championship"  # Default table for standings
        self.load_data(self.table)  # Load the data from the database
        self.setup_ui()  # Call the method to setup the user interface

    # Define a method to setup the user interface
    def setup_ui(self):
        # Configure the grid layout for the frame
        self.grid_rowconfigure(3, weight=1)  # Configure row for scrollable frame
        self.grid_columnconfigure(0, weight=1)  # Configure column

        # Create and position the scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

    # Define a method to load data from the database
    def load_data(self, table="Drivers' Championship", season=date.today().year):
        # Choose the query based on the selected table
        if table == "Drivers' Championship":
            query = f"SELECT name, points, team FROM drivers WHERE season = {season} ORDER BY points DESC"
        elif table == "Constructors' Championship":
            query = f"SELECT name, points FROM teams WHERE season = {season} ORDER BY points DESC"
        else:
            print("Error in table selected")

        self.data.execute(query)  # Execute the query
        self.table = table  # Update the table attribute

    # Define a method to populate the standings
    def fill(self):
        # Clear existing widgets in scrollable frame before updating
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        fetched = self.data.fetchall()  # Fetch data from the database

        # Initialize lists for the pie chart data
        labels = []
        sizes = []
        team_colors_list = []
        colors = {...}  # Define colors for teams

        # Fetch data and fill the labels and sizes lists for the pie chart
        if self.table == "Drivers' Championship":
            # Process data for drivers' championship
            for name, points, team in fetched:
                ...
        else:
            # Process data for constructors' championship
            for name, points in fetched:
                ...

        # Create a figure for the pie chart
        fig, ax = plt.subplots()
        ...

        # Create a canvas and add the figure to it
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=3)

        # Add other widgets (labels) below the pie chart
        for index, item in enumerate(fetched):
            ...
