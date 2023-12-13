import tkinter as tk
from tkinter import filedialog, messagebox
import ifcopenshell

class IFCViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("IFC Object Monitor")

        self.create_widgets()

    def create_widgets(self):
        self.open_button = tk.Button(self.master, text="Open File", command=self.open_file)
        self.open_button.pack(pady=10)

        self.info_text = tk.Text(self.master, height=30, width=40)
        self.info_text.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("IFC Files", "*.ifc")])

        if file_path:
            self.read_ifc_model(file_path)

    def read_ifc_model(self, file_path):
        model = ifcopenshell.open(file_path)

        if not model:
            self.show_error_message("Invalid IFC file.")
            return

        floor_count_by_level = {}
        wall_count_by_level = {}
        column_count_by_level = {}
        door_count_by_level = {}

        for floor in model.by_type("IfcBuildingStorey"):
            level_name = floor.get_info()["Name"]
            floor_count_by_level[level_name] = floor_count_by_level.get(level_name, 0) + 1

        for wall in model.by_type("IfcWall"):
            if wall.ContainedInStructure:
                associated_levels = wall.ContainedInStructure[0].RelatingStructure.Name
                wall_count_by_level[associated_levels] = wall_count_by_level.get(associated_levels, 0) + 1

        for column in model.by_type("IfcColumn"):
            if column.ContainedInStructure:
                associated_levels = column.ContainedInStructure[0].RelatingStructure.Name
                column_count_by_level[associated_levels] = column_count_by_level.get(associated_levels, 0) + 1

        for door in model.by_type("IfcDoor"):
            if door.ContainedInStructure:
                associated_levels = door.ContainedInStructure[0].RelatingStructure.Name
                door_count_by_level[associated_levels] = door_count_by_level.get(associated_levels, 0) + 1

        info_text = "Floor Count Based on Level:\n"
        for level, count in floor_count_by_level.items():
            info_text += f"{level}: {count}\n"

        info_text += "\nWall Count Based on Level:\n"
        for level, count in wall_count_by_level.items():
            info_text += f"{level}: {count}\n"

        info_text += "\nColumn Count Based on Level:\n"
        for level, count in column_count_by_level.items():
            info_text += f"{level}: {count}\n"

        info_text += "\nDoor Count Based on Level:\n"
        for level, count in door_count_by_level.items():
            info_text += f"{level}: {count}\n"

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = IFCViewer(root)
    root.mainloop()
