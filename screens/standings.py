import customtkinter as ctk  # Import the customtkinter library for advanced GUI elements
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Backend for embedding matplotlib in tkinter GUI
from datetime import date  # Import date for handling date-related operations

# Define the 'Standings' class, inheriting from customtkinter's CTkFrame
class Standings(ctk.CTkFrame):
    # Constructor for the 'Standings' class
    def __init__(self, parent, controller, db):
        super().__init__(parent)  # Initialize the parent class (CTkFrame)
        self.scrollable_frame = None  # Attribute for the scrollable frame
        self.controller = controller  # Store the reference to the controller
        self.data = db  # Database connection
        self.table = "Drivers' Championship"  # Default table for standings
        self.load_data(self.table)  # Load data for the default table
        self.setup_ui()  # Set up the user interface

    # Method to set up the user interface
    def setup_ui(self):
        # Configure grid layout for the frame
        self.grid_rowconfigure(3, weight=1)  # Assign weight to row for scaling
        self.grid_columnconfigure(0, weight=1)  # Assign weight to column for scaling

        # Create a scrollable frame and add it to the grid
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        # Configure columns inside the scrollable frame for layout management
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

    # Method to load data from the database
    def load_data(self, table="Drivers' Championship", season=2023):
        # Fetch data based on the selected table (Drivers' or Constructors' Championship)
        if table == "Drivers' Championship":
            query = f"SELECT name, points, team FROM drivers WHERE season = {season} ORDER BY points DESC"
        elif table == "Constructors' Championship":
            query = f"SELECT name, points FROM teams WHERE season = {season} ORDER BY points DESC"
        else:
            print("Error in table selected")  # Print an error if the table is not recognized

        self.data.execute(query)  # Execute the database query
        self.table = table  # Update the current table

    # Method to fill the frame with fetched data
    def fill(self):
        # Clear existing widgets in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        fetched = self.data.fetchall()  # Fetch the data from the database

        # Initialize lists to store data for the pie chart
        labels = []  # Labels for pie chart segments
        sizes = []  # Sizes of pie chart segments
        team_colors_list = []  # Colors for pie chart segments
        # Dictionary to map team names to colors
        colors = {
            'Red Bull': '#1E41FF',
            'Mercedes': '#00D2BE',
            'Ferrari': '#DC0000',
            'Aston Martin': '#006F62',
            'McLaren': '#FF8700',
            'Alpine': '#0090FF',
            'Williams': '#005AFF',
            'Haas': '#FFFFFF',
            'Alfa Romeo': '#900000',
            'AlphaTauri': '#2B4562'
        }  # Define colors for teams

        # Process the fetched data to populate labels, sizes, and colors
        if self.table == "Drivers' Championship":
            for name, points, team in fetched:
                labels.append(name)
                sizes.append(points)    
                team_colors_list.append(colors.get(team))
        else:
            for name, points in fetched:
                labels.append(name)
                sizes.append(points)
                team_colors_list.append(colors.get(name))

        # Create a matplotlib figure for the pie chart
        fig, ax = plt.subplots()
        # Set figure and axis background color
        background_color = "#2e2e2e"
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)
        # Create the pie chart with the collected data
        # Create the pie chart and store the text and autotext elements
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=team_colors_list)

        # Set the color of the labels to white
        for text in texts:
            text.set_color('white')

        # Embed the matplotlib figure in the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=3)

        # Add additional widgets below the pie chart for detailed standings
        for index, item in enumerate(fetched):
            # Process points data for display
            leaderT = item[0]
            ptsT = item[1]
            ptsT_formatted = str
            
            # Process points data for display
            leaderT = item[0]  # Name of the leader/driver or team
            ptsT = item[1]  # Points achieved

            # Check if points (ptsT) is an integer value and format it accordingly
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

            # Create and position a label for the ranking/order number
            resultL = ctk.CTkLabel(self.scrollable_frame, text=index + 1, font=("Lucidia Sans", 17))
            resultL.grid(row=index + 1, column=0, sticky="nw", padx=20, pady=10)

            # Create and position a label for the leader/driver or team name
            leaderL = ctk.CTkLabel(self.scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
            leaderL.grid(row=index + 1, column=1, sticky="nw", padx=20, pady=10)

            # Create and position a label for the points
            ptsL = ctk.CTkLabel(self.scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
            ptsL.grid(row=index + 1, column=2, sticky="e", padx=20, pady=10)
