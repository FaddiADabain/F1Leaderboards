import customtkinter as ctk
from datetime import date


class Standings(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.data = db
        self.load_data("drivers")
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=720, height=200)
        self.scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

        self.fill()

    def load_data(self, table, season=date.today().year):
        query = f"SELECT name, points FROM {table} WHERE season = {season} ORDER BY points DESC"
        self.data.execute(query)

    def fill(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, item in enumerate(self.data):
            leaderT = item[0]
            ptsT = item[1]

            # Check if ptsT is an integer value, and if so, cast to int. Otherwise, keep it as a float.
            ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

            resultL = ctk.CTkLabel(self.scrollable_frame, text=index + 1, font=("Lucidia Sans", 17))
            resultL.grid(row=index, column=0, sticky="nw", padx=20, pady=10)

            leaderL = ctk.CTkLabel(self.scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
            leaderL.grid(row=index, column=1, sticky="nw", padx=20, pady=10)

            ptsL = ctk.CTkLabel(self.scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
            ptsL.grid(row=index, column=2, sticky="e", padx=20, pady=10)

    def run(self):
        self.mainloop()
