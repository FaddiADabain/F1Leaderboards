import customtkinter as ctk
import mysql.connector
from datetime import date

# Connects to remote database
db = mysql.connector.connect(
    user='ugp2y3j5u6hpsadn',
    password='gV3KkHCbdMBE7ZvUPn9W',
    host='btaqr5zbdpvpwofg7vct-mysql.services.clever-cloud.com',
    database='btaqr5zbdpvpwofg7vct'
)

# Database Queries
data = db.cursor()

query = ("SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = %s AND r.round = 19 ORDER "
         "BY date DESC")
data.execute(query, (date.today().year,))
fetched = data.fetchone()
countryT = fetched[0]
trackT = fetched[1]
lapsT = fetched[2]
seasonT = fetched[3]
roundT = fetched[4]
data.reset()

query = "SELECT r.status, d.name, r.points " \
        "FROM results r " \
        "JOIN drivers d ON r.number = d.number AND r.season = d.season " \
        "JOIN races ra ON r.season = ra.season AND r.round = ra.round " \
        "WHERE r.season = %s AND r.round = 19 " \
        "ORDER BY r.season, r.round, r.result"
data.execute(query, (seasonT,))


# System Settings
ctk.set_appearance_mode("DARK")
ctk.set_default_color_theme("blue")

# App Frame
app = ctk.CTk()
app.geometry("720x420")
app.title("F1 Leaderboards")

# Set weights for rows and columns
app.grid_rowconfigure(0, weight=0)  # Segmented button label row
app.grid_rowconfigure(1, weight=0)  # Country label row
app.grid_rowconfigure(2, weight=0)  # Track row
app.grid_rowconfigure(3, weight=1)  # Scrollable Frame row

app.grid_columnconfigure(0, weight=1)  # Country and track label column
app.grid_columnconfigure(1, weight=1)  # This will be the container for the segmented button
app.grid_columnconfigure(2, weight=1)  # Laps and Pts label column


# UI Elements
def segmented_button_callback(value):
    print("segmented button clicked:", value)


# Create a container frame that spans the entire width
button_container = ctk.CTkFrame(app)
button_container.grid(row=0, column=0, columnspan=3, sticky="ew")

segmented_button = ctk.CTkSegmentedButton(button_container, values=["Leaderboards", "Standings", "Race Penalties", "Tyre Strategies"],
                                          command=segmented_button_callback, selected_color="pink", text_color="black")
segmented_button.set("Leaderboards")
segmented_button.pack(pady=5)

countryL = ctk.CTkLabel(app, text=countryT, font=("Lucidia Sans", 25))
countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)

trackL = ctk.CTkLabel(app, text=trackT, font=("Lucidia Sans", 20))
trackL.grid(row=2, column=0, sticky="nw", padx=20)

lapsL = ctk.CTkLabel(app, text=f"Laps: {lapsT}", font=("Lucidia Sans", 20))
lapsL.grid(row=1, column=1, sticky="ne", columnspan=3, padx=20, pady=10)

ptsL = ctk.CTkLabel(app, text="Pts.", font=("Lucidia Sans", 20))
ptsL.grid(row=2, column=1, sticky="ne", columnspan=3, padx=20)

scrollable_frame = ctk.CTkScrollableFrame(app, width=720, height=200)
scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

for i in range(20):
    leader = data.fetchone()
    resultT = leader[0]
    leaderT = leader[1]
    ptsT = leader[2]  # Keep the points as they are, without rounding

    # Check if ptsT is an integer value, and if so, cast to int. Otherwise, keep it as a float.
    ptsT_formatted = str(int(ptsT)) if ptsT.is_integer() else str(ptsT)

    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)

    resultL = ctk.CTkLabel(scrollable_frame, text=resultT, font=("Lucidia Sans", 17))
    resultL.grid(row=i, column=0, sticky="nw", padx=20, pady=10)

    leaderL = ctk.CTkLabel(scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
    leaderL.grid(row=i, column=1, sticky="nw", padx=20, pady=10)

    ptsL = ctk.CTkLabel(scrollable_frame, text=ptsT_formatted, font=("Lucidia Sans", 17))
    ptsL.grid(row=i, column=2, sticky="e", padx=20, pady=10)

# Main Loop
app.mainloop()
