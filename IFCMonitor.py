import tkinter as tk
from tkinter import filedialog
import ifcopenshell
import os
from collections import Counter

def load_ifc_file():
    filepath = filedialog.askopenfilename(filetypes=[("IFC Files", "*.ifc")])

    if filepath:
        ifc_file = ifcopenshell.open(filepath)

        entities = ifc_file.by_type("IfcProduct")
        entity_info = [(entity.is_a(), entity.Name) for entity in entities]
        entity_counts = Counter(entity_info)

        entity_listbox.delete(0, tk.END)

        for (entity_type, entity_name), count in entity_counts.items():
            display_text = f"{entity_type}: {entity_name} ({count})"
            entity_listbox.insert(tk.END, display_text)

        filename = os.path.basename(filepath)
        filename_label.config(text=f"Selected File: {filename}")


def main():
    global entity_listbox, filename_label

    root = tk.Tk()
    root.title("IFC Monitor")

    root.geometry("500x500")
    root.resizable(0, 0)

    filename_label = tk.Label(root, text="Selected File: ")
    filename_label.pack(pady=10)

    entity_listbox = tk.Listbox(root, height=20, width=60)
    entity_listbox.pack(pady=10)

    load_button = tk.Button(root, text="Load IFC", command=load_ifc_file)
    load_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
