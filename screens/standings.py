import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date


class Standings(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.scrollable_frame = None
        self.controller = controller
        self.data = db
        self.table = "Drivers' Championship"
        self.load_data(self.table)
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

    def load_data(self, table="Drivers' Championship", season=date.today().year):
        if table == "Drivers' Championship":
            query = f"SELECT name, points, team FROM drivers WHERE season = {season} ORDER BY points DESC"
            self.data.execute(query)
        elif table == "Constructors' Championship":
            query = f"SELECT name, points FROM teams WHERE season = {season} ORDER BY points DESC"
            self.data.execute(query)
        else:
            print("Error in tabel selected")

        self.table = table

    def fill(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        fetched = self.data.fetchall()

        # Initialize lists for the pie chart data
        labels = []
        sizes = []
        team_colors_list = []
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
        }

        # Fetch data and fill the labels and sizes lists
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

        # Create a figure for the plot
        fig, ax = plt.subplots()

        background_color = "#2e2e2e"
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=team_colors_list)

        # Create a canvas and add the figure to it
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=3)

        # Add other widgets below the pie chart
        for index, item in enumerate(fetched):
            leaderT = item[0]
            ptsT = item[1]

            # Check if ptsT is an integer value, and if so, cast to int. Otherwise, keep it as a float.
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

            resultL = ctk.CTkLabel(self.scrollable_frame, text=index + 1, font=("Lucidia Sans", 17))
            resultL.grid(row=index + 1, column=0, sticky="nw", padx=20, pady=10)

            leaderL = ctk.CTkLabel(self.scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
            leaderL.grid(row=index + 1, column=1, sticky="nw", padx=20, pady=10)

            ptsL = ctk.CTkLabel(self.scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
            ptsL.grid(row=index + 1, column=2, sticky="e", padx=20, pady=10)
