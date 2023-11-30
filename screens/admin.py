import customtkinter as ctk
import sqlite3


class Admin(ctk.CTkToplevel):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db = db
        self.after(100, lambda: self.state("zoomed"))
        self.iconbitmap("data/logo.ico")
        self.title("F1 Leaderboards Admin Panel")
        ctk.set_appearance_mode("DARK")
        ctk.set_default_color_theme("blue")

        # Create a frame for the SQL input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

        # SQL Input Field
        self.sql_input = ctk.CTkEntry(self.input_frame)
        self.sql_input.pack(side="left", fill="x", expand=True)

        # Execute Button
        self.execute_button = ctk.CTkButton(self.input_frame, text="Execute", command=self.execute_query)
        self.execute_button.pack(side="right")

        # Results Display
        self.results_display = ctk.CTkTextbox(self, state="disabled", height=10)
        self.results_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Binding Enter key to execute query
        self.sql_input.bind("<Return>", self.execute_query)

    def execute_query(self, event=None):
        query = self.sql_input.get()
        try:
            self.db.execute(query)
            results = self.db.fetchall()
            self.display_results(results)
        except sqlite3.Error as e:
            self.display_results(f"Error: {e}", error=True)
        finally:
            self.sql_input.delete(0, 'end')

    def display_results(self, results, error=False):
        self.results_display.configure(state="normal")
        if error:
            self.results_display.insert("end", f"{results}\n")
        else:
            for row in results:
                self.results_display.insert("end", f"{row}\n")
        self.results_display.configure(state="disabled")

    def on_exit(self):
        self.destroy()

    def main(self):
        app = Admin()
        app.protocol("WM_DELETE_WINDOW", app.on_exit)
        app.mainloop()
