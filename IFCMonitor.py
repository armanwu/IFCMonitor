import tkinter as tk
from tkinter import filedialog
import ifcopenshell
from collections import Counter

def load_ifc_file():
    filepath = filedialog.askopenfilename(filetypes=[("IFC Files", "*.ifc")])

    if filepath:
        ifc_file = ifcopenshell.open(filepath)

        entities = ifc_file.by_type("IfcProduct")
        entity_names = [entity.is_a() for entity in entities]
        entity_counts = Counter(entity_names)

        entity_listbox.delete(0, tk.END)

        for name, count in entity_counts.items():
            display_text = f"{name} ({count})"
            entity_listbox.insert(tk.END, display_text)


def main():
    global entity_listbox

    root = tk.Tk()
    root.title("IFC Monitor")

    root.geometry("400x500")
    root.resizable(0, 0)

    filename_label = tk.Label(root, text="Selected File: ")
    filename_label.pack(pady=10)

    entity_listbox = tk.Listbox(root, height=20, width=50)
    entity_listbox.pack(pady=10)

    load_button = tk.Button(root, text="Load IFC", command=load_ifc_file)
    load_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
