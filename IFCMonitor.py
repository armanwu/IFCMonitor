import tkinter as tk
from tkinter import filedialog
import ifcopenshell
import os
from collections import Counter


def load_ifc_file(root, properties_text):
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

        def on_entity_selected(event):
            selected_index = entity_listbox.curselection()
            if selected_index:
                entity = entities[selected_index[0]]
                properties = entity.get_info()
        
                # Clear previous content
                properties_text.delete("1.0", tk.END)
        
                # Format and display properties
                formatted_properties = format_properties(properties)
                properties_text.insert(tk.END, formatted_properties)

        def format_properties(properties):
            formatted_properties = ""
            for key, value in properties.items():
                formatted_properties += f"{key}: {value}\n"
            return formatted_properties

        entity_listbox.bind("<<ListboxSelect>>", on_entity_selected)
        
        filename = os.path.basename(filepath)
        filename_label.config(text=f"Selected File: {filename}")



def main():
    global entity_listbox, filename_label

    root = tk.Tk()
    root.title("IFC Monitor")

    root.geometry("700x700")
    root.resizable(0, 0)

    filename_label = tk.Label(root, text="Selected File: ")
    filename_label.pack(pady=10)

    load_button = tk.Button(root, text="Load IFC", command=lambda: load_ifc_file(root, properties_text))
    load_button.pack()

    entity_listbox = tk.Listbox(root, height=20, width=80)
    entity_listbox.pack(pady=10)

    properties_text = tk.Text(root, height=12, width=80)
    properties_text.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()