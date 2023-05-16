import tkinter as tk
from tkinter import filedialog
import ifcopenshell

def load_ifc_file():
    filepath = filedialog.askopenfilename(filetypes=[("IFC Files", "*.ifc")])

    if filepath:
        ifc_file = ifcopenshell.open(filepath)

        entities = ifc_file.by_type("IfcProduct")
        for entity in entities:
            print(entity.is_a())

 
def main():
    root = tk.Tk()
    root.title("IFC Monitor")

    load_button = tk.Button(root, text="Load IFC File", command=load_ifc_file)
    load_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
