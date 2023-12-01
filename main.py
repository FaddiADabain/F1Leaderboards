import customtkinter as ctk
import sqlite3
from datetime import date
from screens.leaderboard import Leaderboard
from screens.penalties import Penalties
from screens.standings import Standings
from screens.tyrestrats import Strategies
from collections import OrderedDict
from screens.admin import Admin
from screens.login import Login
import keyboard


class MainApplication(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = None
        self.admin = None
        self.data = None
        self.db = None
        self.last_selected_race = None
        self.last_selected_season = 2023
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

        # Initialize a list to store race values
        self.race_values = []

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

        self.frames["Leaderboards"].load_data(self.race_menu.get())
        self.frames["Leaderboards"].fill_leader()
        self.show_frame("Leaderboards")
        self.last_selected_race = self.race_menu.get()
        keyboard.on_press_key("f1", lambda _: self.open_login())

    def open_login(self):
        if self.login is None or not self.login.winfo_exists():
            self.login = Login(self, self.adminDb, self.adminCursor)

    def open_admin(self):
        if self.admin is None or not self.admin.winfo_exists():
            self.admin = Admin(self, self.data)

    def init_db(self):
        self.db = sqlite3.connect("data/f1leaderboard.db")
        self.data = self.db.cursor()

        self.adminDb = sqlite3.connect("data/admin.db")
        self.adminCursor = self.adminDb.cursor()

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

        # Check if the selected frame is 'Standings'
        if selected_value == "Standings":
            # Configure the race menu for the 'Standings' frame
            self.race_menu.configure(values=("Drivers' Championship", "Constructors' Championship"))
            self.race_menu.set("Drivers' Championship")
            self.standingsF.load_data(table="Drivers' Championship", season=self.season_menu.get())
            self.standingsF.fill()

        else:
            # Configure the race menu for other frames
            self.race_menu_vals(self.season_menu.get())
            if self.last_selected_race is not None and self.last_selected_race in self.race_menu.values:
                self.race_menu.set(self.last_selected_race)
            else:
                self.last_selected_race = self.race_menu.values[0]
                self.race_menu.set(self.last_selected_race)

            self.update_frames(selected_value, self.race_menu.get(), self.season_menu.get())

    def season_menu_callback(self, selected_value):
        if selected_value != self.last_selected_season:
            self.last_selected_season = selected_value
            self.race_menu_vals(selected_value)
            self.last_selected_race = self.race_menu.values[0]
            self.race_menu.set(self.last_selected_race)

        self.segmented_button_callback(self.segmented_buttons.get())

    def race_menu_callback(self, selected_value):
        self.last_selected_race = selected_value
        self.show_frame(self.segmented_buttons.get())
        self.update_frames(self.segmented_buttons.get(), selected_value, self.season_menu.get())

    def update_frames(self, frame_name, race, season):
        if frame_name == "Leaderboards":
            self.leaderboardF.load_data(race, season=season)
            self.leaderboardF.fill_leader()
        elif frame_name == "Race Penalties":
            self.penaltiesF.load_data(race, season=season)
            self.penaltiesF.fill_penalties()
        elif frame_name == "Tyre Strategies":
            self.strategiesF.load_data(race, season=season)
            self.strategiesF.fill()
        elif frame_name == "Standings":
            self.standingsF.load_data(table=self.race_menu.get(), season=season)
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

        # Clear the race_values list
        self.race_values.clear()

        for i in self.data:
            self.countries[i[1]] = i[0]
            # Append race values to the race_values list
            self.race_values.append(i[0])

        # Configure the race menu with the race_values list
        self.race_menu.configure(values=self.race_values)


def main():
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_exit)
    app.mainloop()


if __name__ == "__main__":
    main()