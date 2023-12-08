import customtkinter as ctk  # Enhanced tkinter module for improved UI elements
import sqlite3  # SQLite3 for database operations
from datetime import date  # Date module to work with dates
# Import various screens (modules) for different functionalities
from screens.leaderboard import Leaderboard
from screens.penalties import Penalties
from screens.standings import Standings
from screens.tyrestrats import Strategies
from collections import OrderedDict  # Ordered dictionary to maintain order
from screens.admin import Admin
from screens.login import Login
import keyboard  # Module to capture keyboard events

# Main application class inheriting from customtkinter CTk class
class MainApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Initialize the base class constructor
        # Initialize various attributes
        self.login = None
        self.admin = None
        self.data = None  # Database cursor
        self.db = None  # Database connection
        self.last_selected_race = None
        self.last_selected_season = 2023  # Default selected season
        self.countries = {}  # To store country data
        self.init_db()  # Initialize database connection
        self.after(100, lambda: self.state("zoomed"))  # Maximize the window after 100ms
        self.iconbitmap("data/logo.ico")  # Set window icon
        self.title("F1 Leaderboards")  # Set window title
        ctk.set_appearance_mode("DARK")  # Set dark mode for the UI
        ctk.set_default_color_theme("blue")  # Set default color theme

        # Create and configure frames and widgets
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(side="top", pady=10)

        # Segmented buttons for navigation
        self.segmented_buttons = ctk.CTkSegmentedButton(self,
                                                        values=["Leaderboards", "Standings", "Race Penalties", "Tyre Strategies"],
                                                        command=self.segmented_button_callback, selected_color="pink",
                                                        text_color="black", font=("Lucidia Sans", 15))
        self.segmented_buttons.set("Leaderboards")
        self.segmented_buttons.pack(side="top", fill="x", pady=10, padx=10)

        # Season and race option menus
        self.season_menu = ctk.CTkOptionMenu(self.options_frame, values=["2021", "2022", "2023"],
                                             command=self.season_menu_callback, button_color="grey", fg_color="grey",
                                             text_color="black", font=("Lucidia Sans", 15))
        self.season_menu.set("2023")
        self.season_menu.pack(side="left", padx=10)

        self.race_values = []  # List to store race values for the option menu
        self.race_menu = ctk.CTkOptionMenu(self.options_frame,
                                           command=self.race_menu_callback, button_color="grey", fg_color="grey",
                                           text_color="black", font=("Lucidia Sans", 15))
        self.race_menu.pack(side="left", padx=10)
        self.race_menu_init()  # Initialize race menu with races

        # Container for different frames (screens)
        self.frames = {}
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize different frames for various screens
        self.leaderboardF = Leaderboard(self.container, self, self.data)
        self.penaltiesF = Penalties(self.container, self, self.data)
        self.standingsF = Standings(self.container, self, self.data)
        self.strategiesF = Strategies(self.container, self, self.data)

        # Dictionary to store frames for easy access
        self.frames = {
            "Leaderboards": self.leaderboardF,
            "Race Penalties": self.penaltiesF,
            "Standings": self.standingsF,
            "Tyre Strategies": self.strategiesF
        }

        # Initialize frame data and show the default frame
        self.frames["Leaderboards"].load_data(self.race_menu.get())
        self.frames["Leaderboards"].fill_leader()
        self.show_frame("Leaderboards")
        self.last_selected_race = self.race_menu.get()
        keyboard.on_press_key("f1", lambda _: self.open_login())  # Bind F1 key to open login

    def open_login(self):
        # Open the login frame when the 'F1' key is pressed
        if self.login is None or not self.login.winfo_exists():
            self.login = Login(self, self.adminDb, self.adminCursor)

    def open_admin(self):
        # Open the admin frame
        if self.admin is None or not self.admin.winfo_exists():
            self.admin = Admin(self, self.data)

    def init_db(self):
        # Initialize database connections
        self.db = sqlite3.connect("data/f1leaderboard.db")  # Connect to the F1 leaderboard database
        self.data = self.db.cursor()  # Create a cursor for database operations

        self.adminDb = sqlite3.connect("data/admin.db")  # Connect to the admin database
        self.adminCursor = self.adminDb.cursor()  # Create a cursor for admin database operations

    def on_exit(self):
        # Close the database connections and destroy the window when the application exits
        self.data.close()  # Close the main database cursor
        self.db.close()  # Close the main database connection
        self.adminCursor.close()  # Close the admin database cursor
        self.adminDb.close()  # Close the admin database connection
        self.destroy()  # Destroy the main application window

    def show_frame(self, page_name):
        # Show a frame from the frames dictionary based on the provided page name
        # Hide all frames first
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the selected frame
        frame = self.frames[page_name]
        frame.pack(side="top", fill="both", expand=True)

    def segmented_button_callback(self, selected_value):
        # Callback for the segmented buttons to display the appropriate frame
        # Hide all frames first
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the selected frame based on the segmented button selection
        self.show_frame(selected_value)

        # Special handling for the 'Standings' frame
        if selected_value == "Standings":
            self.race_menu.configure(values=("Drivers' Championship", "Constructors' Championship"))
            self.race_menu.set("Drivers' Championship")
            self.standingsF.load_data(table="Drivers' Championship", season=self.season_menu.get())
            self.standingsF.fill()
        else:
            # Update the race menu based on the last selected race
            if self.last_selected_race in self.race_values:
                self.race_menu.set(self.last_selected_race)
            else:
                self.last_selected_race = self.race_values[0]
                self.race_menu.set(self.last_selected_race)

            self.race_menu_vals(self.season_menu.get())
            self.update_frames(selected_value, self.race_menu.get(), self.season_menu.get())

    def season_menu_callback(self, selected_value):
        # Callback function for the season option menu
        # Handles updates when the season value is changed
        if self.segmented_buttons.get() != "Standings":
            # Update the race menu values for the selected season
            self.race_menu_vals(selected_value)

            # Set the race menu to the first race of the season, if available
            if self.race_values:
                self.last_selected_race = self.race_values[0]
                self.race_menu.set(self.last_selected_race)

        # Update the displayed frame according to the new season selection
        self.segmented_button_callback(self.segmented_buttons.get())

    def race_menu_callback(self, selected_value):
        # Callback function for the race option menu
        # Handles updates when a race is selected
        self.last_selected_race = selected_value
        # Update and show the frame corresponding to the selected race
        self.show_frame(self.segmented_buttons.get())
        # Update frames with new race selection
        self.update_frames(self.segmented_buttons.get(), selected_value, self.season_menu.get())

    def update_frames(self, frame_name, race, season):
        # Update the data in different frames based on the selected race and season
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
        # Initialize the race menu with races from the latest season
        self.race_menu_vals(2023)

        # Set the race menu to the current or next closest race date
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
        # Update the race menu values based on the selected season
        self.countries = {}  # Dictionary to store countries and their corresponding races
        self.data.execute(f"SELECT track, date FROM races WHERE season = {season} ORDER BY round")

        # Clear existing values from the race_values list
        self.race_values.clear()

        # Populate the countries dictionary and race_values list with fetched data
        for i in self.data:
            self.countries[i[1]] = i[0]
            self.race_values.append(i[0])

        # Update the race option menu with new values
        self.race_menu.configure(values=self.race_values)

# Main function to run the application
def main():
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_exit)  # Set the action on window close
    app.mainloop()  # Start the application's main loop

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
