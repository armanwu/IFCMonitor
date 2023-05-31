import tkinter as tk
from tkinter import filedialog
import os
import ifcopenshell

def count_doors_windows(ifc_file):
    doors = 0
    windows = 0

    # Load the IFC file
    ifc_model = ifcopenshell.open(ifc_file)

    # Get all elements in the model
    elements = ifc_model.by_type("IfcWindow") + ifc_model.by_type("IfcDoor")

    # Count the doors and windows
    for element in elements:
        if element.is_a("IfcDoor"):
            doors += 1
        elif element.is_a("IfcWindow"):
            windows += 1

    return doors, windows

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("IFC Files", "*.ifc")])
    door_count, window_count = count_doors_windows(file_path)
    result_label.config(text="Total doors: {}\nTotal windows: {}".format(door_count, window_count))
    file_label.config(text="Selected file: {}".format(os.path.basename(file_path)))

# Create the main window
window = tk.Tk()
window.title("IFC Door and Window Counter")
window.geometry("400x200")
window.resizable(False, False)

# Create the "Open File" button
open_button = tk.Button(window, text="Open File", command=open_file_dialog, width=15)
open_button.pack(pady=20)

# Create a label to display the selected file
file_label = tk.Label(window, font=("Arial", 10), wraplength=300)
file_label.pack()

# Create a label to display the result
result_label = tk.Label(window, font=("Arial", 12))
result_label.pack()

# Run the main window event loop
window.mainloop()
