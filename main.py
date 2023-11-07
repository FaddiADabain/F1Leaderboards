import customtkinter as ctk
import sqlite3
from datetime import date
from screens.leaderboard import Leaderboard
from screens.penalties import Penalties
from screens.standings import Standings
from screens.tyrestrats import Strategies
from collections import OrderedDict


class MainApplication(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.db = None
        self.countries = {}
        self.init_db()
        self.after(100, lambda: self.state("zoomed"))
        self.iconbitmap("data/logo.ico")
        self.title("F1 Leaderboards")
        ctk.set_appearance_mode("DARK")
        ctk.set_default_color_theme("blue")

        # Create a frame to hold the option menus
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(side="top", pady=10)

        # Create the segmented buttons
        self.segmented_buttons = ctk.CTkSegmentedButton(self,
                                                        values=["Leaderboards", "Standings", "Race Penalties",
                                                                "Tyre Strategies"],
                                                        command=self.segmented_button_callback, selected_color="pink",
                                                        text_color="black", font=("Lucidia Sans", 15))
        self.segmented_buttons.set("Leaderboards")
        self.segmented_buttons.pack(side="top", fill="x", pady=10, padx=10)

        # Create the season option menu inside the frame
        self.season_menu = ctk.CTkOptionMenu(self.options_frame, values=["2021", "2022", "2023"],
                                             command=self.season_menu_callback, button_color="grey", fg_color="grey",
                                             text_color="black", font=("Lucidia Sans", 15))
        self.season_menu.set("2023")
        self.season_menu.pack(side="left", padx=10)

        # Create the race option menu inside the frame
        self.race_menu = ctk.CTkOptionMenu(self.options_frame,
                                           command=self.race_menu_callback, button_color="grey", fg_color="grey",
                                           text_color="black", font=("Lucidia Sans", 15))
        self.race_menu.pack(side="left", padx=10)
        self.race_menu_init()

        self.frames = {}
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.leaderboardF = Leaderboard(self.container, self, self.data)
        self.penaltiesF = Penalties(self.container, self, self.data)
        self.standingsF = Standings(self.container, self, self.data)
        self.strategiesF = Strategies(self.container, self, self.data)

        self.frames = {
            "Leaderboards": self.leaderboardF,
            "Race Penalties": self.penaltiesF,
            "Standings": self.standingsF,
            "Tyre Strategies": self.strategiesF
        }

        # Add frames to the application
        for FrameClass in (Leaderboard, Penalties):
            frame = FrameClass(parent=self.container, controller=self, db=self.data)
            frame_name = FrameClass.__name__
            self.frames[frame_name] = frame
            frame.pack(side="top", fill="both", expand=True)

        self.show_frame("Leaderboard")

    def init_db(self):
        self.db = sqlite3.connect("data/f1leaderboard.db")
        self.data = self.db.cursor()

    def on_exit(self):
        # Close the database connection when the app is closing
        self.data.close()
        self.db.close()
        self.destroy()

    def show_frame(self, page_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the selected frame
        frame = self.frames[page_name]
        frame.pack(side="top", fill="both", expand=True)

    def segmented_button_callback(self, selected_value):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the selected frame
        self.show_frame(selected_value)

        if (selected_value == "Leaderboards" or selected_value == "Race Penalties"
                or selected_value == "Tyre Strategies"):
            self.race_menu_vals(self.season_menu.get())
            self.race_menu.set(self.leaderboardF.trackT)
        if selected_value == "Standings":
            self.race_menu.configure(values=("Drivers' Championship", "Constructors' Championship"))
            self.race_menu.set("Drivers' Championship")

    def season_menu_callback(self, selected_value):
        if (self.segmented_buttons.get() == "Leaderboards" or self.segmented_buttons.get() == "Race Penalties"
                or self.segmented_buttons.get() == "Tyre Strategies"):
            self.countries.clear()
            self.data.execute(f"SELECT track, date FROM races WHERE season = {str(selected_value)} ORDER BY round")

            for i in self.data:
                self.countries[i[1]] = i[0]

            self.race_menu.configure(values=list(self.countries.values()))
            self.race_menu.set(self.countries[list(self.countries.keys())[0]])

            self.race_menu_callback(self.race_menu.get())

            self.segmented_button_callback(self.segmented_buttons.get())

        elif self.segmented_buttons.get() == "Standings" and self.race_menu.get() == "Drivers' Championship":
            self.standingsF.load_data("drivers", season=selected_value)
            self.standingsF.fill()

        elif self.segmented_buttons.get() == "Standings" and self.race_menu.get() == "Constructors' Championship":
            self.standingsF.load_data("teams", season=selected_value)
            self.standingsF.fill()

    def race_menu_callback(self, selected_value):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the selected frame
        self.show_frame(self.segmented_buttons.get())
        
        if (self.segmented_buttons.get() == "Leaderboards" or self.segmented_buttons.get() == "Race Penalties"
                or self.segmented_buttons.get() == "Tyre Strategies"):
            self.leaderboardF.load_data(selected_value, season=self.season_menu.get())
            self.leaderboardF.fill_leader()

            self.penaltiesF.load_data(selected_value, season=self.season_menu.get())
            self.penaltiesF.fill_penalties()

            self.strategiesF.load_data(selected_value, season=self.season_menu.get())
            self.strategiesF.fill()

        elif selected_value == "Drivers' Championship":
            self.standingsF.load_data("drivers", season=self.season_menu.get())
            self.standingsF.fill()

        elif selected_value == "Constructors' Championship":
            self.standingsF.load_data("teams", season=self.season_menu.get())
            self.standingsF.fill()

    def race_menu_init(self):
        self.race_menu_vals(2023)

        today = str(date.today())
        if today in self.countries:
            self.race_menu.set(self.countries[today])
        else:
            reversed_dict = OrderedDict(sorted(self.countries.items(), reverse=True))
            for i in reversed_dict.keys():
                if today > i:
                    self.race_menu.set(self.countries[i])
                    break

    def race_menu_vals(self, season):
        self.countries = {}
        self.data.execute(f"SELECT track, date FROM races WHERE season = {season} ORDER BY round")

        for i in self.data:
            self.countries[i[1]] = i[0]

        self.race_menu.configure(values=list(self.countries.values()))


def main():
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_exit)
    app.mainloop()


if __name__ == "__main__":
    main()
