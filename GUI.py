import tkinter as tk
from tkinter import ttk

# Function to open a new window with a specified title
def open_new_window(title):
    new_window = tk.Toplevel(root)
    new_window.title(title)

    # Create a canvas with a white background
    canvas = tk.Canvas(new_window, width=400, height=300, bg='white')
    canvas.pack()

    # Adding text to the canvas
    canvas.create_text(200, 150, text="Data to be added here", fill='black', font=('Helvetica', 12))

    # Alternatively, you can use a Frame widget with a white background and a Label for the text
    # frame = tk.Frame(new_window, width=400, height=300, bg='white')
    # frame.pack()
    # label = tk.Label(frame, text="Data to be added here", bg='white', font=('Helvetica', 12))
    # label.place(relx=0.5, rely=0.5, anchor='center')

# Function to handle the selection from the burger menu
def menu_command(title):
    return lambda: open_new_window(title)

# Function to handle the selection from the combo box
def combo_selected(event):
    selected_option = combo.get()
    if selected_option != "Select an option":
        open_new_window(selected_option)

# Create the main application window
root = tk.Tk()
root.title("F1 Racing GUI")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a menu item
menu = tk.Menu(menu_bar, tearoff=0)
menu.add_command(label="Display Race Results", command=menu_command("Display Race Results"))
menu.add_command(label="Display Driver Standings", command=menu_command("Display Driver Standings"))
menu.add_command(label="Display Tire Strategy", command=menu_command("Display Tire Strategy"))

# Add the menu to the menu bar
menu_bar.add_cascade(label="Burger Menu", menu=menu)

# Configure the root to use the menu bar
root.config(menu=menu_bar)

# Create a label
label = ttk.Label(root, text="Welcome to the F1 Racing GUI!")
label.pack(pady=20)

# Create a Combobox with F1-related options
options = ["Select an option", "Main Screen", "Live Screen", "Team Points Screen", "Penalty Screen", "Strategy Screen"]
combo = ttk.Combobox(root, values=options)
combo.bind('<<ComboboxSelected>>', combo_selected)  # Bind the combo_selected function to the combobox
combo.pack(pady=10)

# Run the main event loop
root.mainloop()
