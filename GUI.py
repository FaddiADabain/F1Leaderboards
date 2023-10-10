import tkinter as tk
from tkinter import ttk

# Function to handle the selection from the burger menu
def menu_selected(event):
    selected_menu_item = menu_var.get()
    print("Selected menu item:", selected_menu_item)

# Create the main application window
root = tk.Tk()
root.title("F1 Racing GUI")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a menu item
menu = tk.Menu(menu_bar, tearoff=0)
menu.add_command(label="Display Race Results")
menu.add_command(label="Display Driver Standings")
menu.add_command(label="Display Tire Strategy")

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
combo.pack(pady=10)

# Run the main event loop
root.mainloop()
