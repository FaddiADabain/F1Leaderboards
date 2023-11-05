import customtkinter as ctk
import sqlite3
from screens.leaderboard import Leaderboard
from screens.penalties import Penalties


class MainApplication(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_db()
        self.after(100, lambda: self.state("zoomed"))
        self.title("F1 Leaderboards")
        ctk.set_appearance_mode("DARK")
        ctk.set_default_color_theme("blue")

        # Create the segmented buttons
        self.segmented_buttons = ctk.CTkSegmentedButton(self,
                                                        values=["Leaderboards", "Standings", "Race Penalties",
                                                                "Tyre Strategies"],
                                                        command=self.segmented_button_callback, selected_color="pink",
                                                        text_color="black")
        self.segmented_buttons.set("Leaderboards")
        self.segmented_buttons.pack(pady=10, padx=10)

        self.frames = {}
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {
            "Leaderboards": Leaderboard(self.container, self, self.data),
            "Race Penalties": Penalties(self.container, self, self.data)
        }

        # Add frames to the application
        for FrameClass in (Leaderboard, Penalties):
            frame = FrameClass(parent=self.container, controller=self, db=self.data)
            frame_name = FrameClass.__name__
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

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
            frame.grid_remove()

        # Show the selected frame
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")

    def segmented_button_callback(self, selected_value):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the selected frame
        self.show_frame(selected_value)


def main():
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_exit)
    app.mainloop()


if __name__ == "__main__":
    main()
