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

query = "SELECT r.country, r.track, r.laps, r.season, r.round FROM races r WHERE r.season = %s AND r.round = 18 ORDER BY date DESC"
data.execute(query, (date.today().year,))
fetched = data.fetchone()
country = fetched[0]
track = fetched[1]
laps = fetched[2]
season = fetched[3]
rround = fetched[4]
data.reset()

query = "SELECT r.status, d.name " \
        "FROM results r " \
        "JOIN drivers d ON r.number = d.number AND r.season = d.season " \
        "JOIN races ra ON r.season = ra.season AND r.round = ra.round " \
        "WHERE r.season = %s AND r.round = 18 " \
        "ORDER BY r.season, r.round, r.result"
data.execute(query, (season,))


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

countryL = ctk.CTkLabel(app, text=country, font=("Lucidia Sans", 25))
countryL.grid(row=1, column=0, sticky="nw", padx=20, pady=10)

trackL = ctk.CTkLabel(app, text=track, font=("Lucidia Sans", 20))
trackL.grid(row=2, column=0, sticky="nw", padx=20)

lapsL = ctk.CTkLabel(app, text=f"Laps: {laps}", font=("Lucidia Sans", 20))
lapsL.grid(row=1, column=1, sticky="ne", columnspan=3, padx=20, pady=10)

ptsL = ctk.CTkLabel(app, text="Pts.", font=("Lucidia Sans", 20))
ptsL.grid(row=2, column=1, sticky="ne", columnspan=3, padx=20)

scrollable_frame = ctk.CTkScrollableFrame(app, width=720, height=200)
scrollable_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

for i in range(20):
    leader = data.fetchone()
    resultT = leader[0]
    leaderT = leader[1]

    if resultT == "1":
        ptsT = "25"
    elif resultT == "2":
        ptsT = "18"
    elif resultT == "3":
        ptsT = "15"
    elif resultT == "4":
        ptsT = "12"
    elif resultT == "5":
        ptsT = "10"
    elif resultT == "6":
        ptsT = "8"
    elif resultT == "7":
        ptsT = "6"
    elif resultT == "8":
        ptsT = "4"
    elif resultT == "9":
        ptsT = "2"
    elif resultT == "10":
        ptsT = "1"
    else:
        ptsT = "0"

    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)

    resultL = ctk.CTkLabel(scrollable_frame, text=resultT, font=("Lucidia Sans", 17))
    resultL.grid(row=i, column=0, sticky="nw", padx=20, pady=10)

    leaderL = ctk.CTkLabel(scrollable_frame, text=leaderT, font=("Lucidia Sans", 17))
    leaderL.grid(row=i, column=1, sticky="nw", padx=20, pady=10)

    ptsL = ctk.CTkLabel(scrollable_frame, text=ptsT, font=("Lucidia Sans", 17))
    ptsL.grid(row=i, column=2, sticky="e", padx=20, pady=10)

# Main Loop
app.mainloop()
