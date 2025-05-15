import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
from datetime import datetime, timedelta
import random

class CargoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargo Listings Editor")
        self.root.geometry("1200x700")
        
        # Load configuration and cargo data
        self.load_config()
        self.load_cargo_data()
        
        self.create_gui()
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists("cargo_config.json"):
            with open("cargo_config.json", "r") as f:
                self.config = json.load(f)
        else:
            messagebox.showerror("Error", "Configuration file not found. Run the main simulator first.")
            self.root.destroy()
            return
            
    def load_cargo_data(self):
        """Load existing cargo data if available"""
        self.cargo_list = []
        
        if os.path.exists("cargo_sim_save.csv"):
            try:
                with open("cargo_sim_save.csv", "r") as file:
                    reader = csv.reader(file)
                    
                    in_cargo_section = False
                    header_row = None
                    
                    for row in reader:
                        if not row:
                            continue
                            
                        if row[0] == "CARGO_DATA":
                            in_cargo_section = True
                            continue
                        elif row[0] == "BID_DATA":
                            in_cargo_section = False
                            continue
                            
                        if in_cargo_section:
                            if header_row is None:
                                header_row = row
                                continue
                                
                            cargo = {
                                "id": int(row[0]),
                                "cargo_type": row[1],
                                "origin": row[2],
                                "destination": row[3],
                                "mass": int(row[4]),
                                "value_per_ton": int(row[5]),
                                "total_value": int(row[6]),
                                "shipping_company": row[7],
                                "posted_on": row[8],
                                "deadline": row[9],
                                "status": row[10]
                            }
                            self.cargo_list.append(cargo)
            except Exception as e:
                messagebox.showwarning("Warning", f"Error loading cargo data: {str(e)}")
                self.cargo_list = []
                
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cargo listings frame
        cargo_frame = ttk.LabelFrame(main_frame, text="Current Cargo Listings", padding="10")
        cargo_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview for cargo listings
        columns = ("ID", "Cargo Type", "Origin", "Destination", "Mass (tons)", 
                  "Value (cr/ton)", "Total Value", "Shipping Company", "Posted On", "Deadline", "Status")
        
        self.cargo_tree = ttk.Treeview(cargo_frame, columns=columns, show="headings")
        
        # Configure columns
        self.cargo_tree.column("ID", width=40, anchor=tk.CENTER)
        self.cargo_tree.column("Cargo Type", width=150)
        self.cargo_tree.column("Origin", width=100)
        self.cargo_tree.column("Destination", width=100)
        self.cargo_tree.column("Mass (tons)", width=80, anchor=tk.CENTER)
        self.cargo_tree.column("Value (cr/ton)", width=100, anchor=tk.CENTER)
        self.cargo_tree.column("Total Value", width=100, anchor=tk.CENTER)
        self.cargo_tree.column("Shipping Company", width=150)
        self.cargo_tree.column("Posted On", width=100, anchor=tk.CENTER)
        self.cargo_tree.column("Deadline", width=100, anchor=tk.CENTER)
        self.cargo_tree.column("Status", width=100, anchor=tk.CENTER)
        
        # Configure headings
        for col in columns:
            self.cargo_tree.heading(col, text=col)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(cargo_frame, orient=tk.VERTICAL, command=self.cargo_tree.yview)
        self.cargo_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cargo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control frame for buttons
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Add Cargo", command=self.add_cargo).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Edit Selected", command=self.edit_cargo).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Delete Selected", command=self.delete_cargo).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Add Special/Unusual", command=self.add_unusual_cargo).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Refresh", command=self.update_cargo_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Changes", command=self.save_changes).pack(side=tk.RIGHT, padx=5)
        
        self.update_cargo_display()
        
    def update_cargo_display(self):
        """Update the cargo treeview with all listings"""
        # Clear the existing items
        for item in self.cargo_tree.get_children():
            self.cargo_tree.delete(item)
            
        # Insert cargo listings
        for cargo in self.cargo_list:
            values = (
                cargo["id"],
                cargo["cargo_type"],
                cargo["origin"],
                cargo["destination"],
                f"{cargo['mass']:,}",
                f"{cargo['value_per_ton']:,}",
                f"{cargo['total_value']:,}",
                cargo["shipping_company"],
                cargo["posted_on"],
                cargo["deadline"],
                cargo["status"]
            )
            self.cargo_tree.insert("", tk.END, values=values)
            
    def add_cargo(self):
        """Add a new cargo listing"""
        # Create a new dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Cargo")
        dialog.geometry("500x550")
        dialog.grab_set()  # Make dialog modal
        
        # Frame for form fields
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get next available ID
        next_id = 1
        if self.cargo_list:
            next_id = max(cargo["id"] for cargo in self.cargo_list) + 1
            
        # Create form fields
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_var = tk.StringVar(value=str(next_id))
        ttk.Entry(form_frame, textvariable=id_var, state="readonly").grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Cargo Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        cargo_type_var = tk.StringVar()
        cargo_type_combo = ttk.Combobox(form_frame, textvariable=cargo_type_var, values=list(self.config["cargo_types"].keys()))
        cargo_type_combo.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        cargo_type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_mass_value_ranges(cargo_type_var.get(), mass_var, value_var))
        
        ttk.Label(form_frame, text="Origin:").grid(row=2, column=0, sticky=tk.W, pady=5)
        origin_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=origin_var, values=self.config["destinations"]).grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Destination:").grid(row=3, column=0, sticky=tk.W, pady=5)
        dest_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=dest_var, values=self.config["destinations"]).grid(row=3, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Mass (tons):").grid(row=4, column=0, sticky=tk.W, pady=5)
        mass_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=mass_var).grid(row=4, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Value (cr/ton):").grid(row=5, column=0, sticky=tk.W, pady=5)
        value_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=value_var).grid(row=5, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Shipping Company:").grid(row=6, column=0, sticky=tk.W, pady=5)
        company_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=company_var, values=self.config["shipping_companies"]).grid(row=6, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Posted On (YYYY-MM-DD):").grid(row=7, column=0, sticky=tk.W, pady=5)
        posted_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=posted_var).grid(row=7, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=8, column=0, sticky=tk.W, pady=5)
        deadline_var = tk.StringVar(value=(datetime.now() + timedelta(weeks=4)).strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=deadline_var).grid(row=8, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Status:").grid(row=9, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value="Available")
        ttk.Combobox(form_frame, textvariable=status_var, values=["Available", "Contracted", "Expired"]).grid(row=9, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Range info labels
        mass_range_label = ttk.Label(form_frame, text="")
        mass_range_label.grid(row=4, column=2, sticky=tk.W, pady=5)
        
        value_range_label = ttk.Label(form_frame, text="")
        value_range_label.grid(row=5, column=2, sticky=tk.W, pady=5)
        
        # Function to update mass and value ranges when cargo type is selected
        def update_mass_value_ranges(cargo_type, mass_var, value_var):
            if cargo_type in self.config["cargo_types"]:
                mass_range = self.config["cargo_types"][cargo_type]["mass"]
                value_range = self.config["cargo_types"][cargo_type]["value"]
                
                # Use random values within the range as defaults
                mass_var.set(str(random.randint(mass_range[0], mass_range[1])))
                value_var.set(str(random.randint(value_range[0], value_range[1])))
                
                mass_range_label.config(text=f"Range: {mass_range[0]}-{mass_range[1]}")
                value_range_label.config(text=f"Range: {value_range[0]}-{value_range[1]}")
        
        # Button frame
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X)
        
        def save_new_cargo():
            # Validate inputs
            try:
                mass = int(mass_var.get())
                value_per_ton = int(value_var.get())
                
                cargo = {
                    "id": int(id_var.get()),
                    "cargo_type": cargo_type_var.get(),
                    "origin": origin_var.get(),
                    "destination": dest_var.get(),
                    "mass": mass,
                    "value_per_ton": value_per_ton,
                    "total_value": mass * value_per_ton,
                    "shipping_company": company_var.get(),
                    "posted_on": posted_var.get(),
                    "deadline": deadline_var.get(),
                    "status": status_var.get()
                }
                
                # Validate required fields
                if not cargo["cargo_type"] or not cargo["origin"] or not cargo["destination"] or not cargo["shipping_company"]:
                    messagebox.showwarning("Missing Data", "Please fill in all required fields.")
                    return
                    
                self.cargo_list.append(cargo)
                self.update_cargo_display()
                dialog.destroy()
                
            except ValueError:
                messagebox.showwarning("Invalid Input", "Mass and value must be numbers.")
        
        ttk.Button(button_frame, text="Add", command=save_new_cargo).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
    def edit_cargo(self):
        """Edit the selected cargo listing"""
        selected_item = self.cargo_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a cargo listing to edit.")
            return
            
        # Get the cargo ID from the selected item
        cargo_id = int(self.cargo_tree.item(selected_item[0], "values")[0])
        
        # Find the cargo in our list
        cargo_index = next((i for i, cargo in enumerate(self.cargo_list) if cargo["id"] == cargo_id), None)
        if cargo_index is None:
            messagebox.showerror("Error", "Cargo not found.")
            return
            
        cargo = self.cargo_list[cargo_index]
        
        # Create a new dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Cargo")
        dialog.geometry("500x550")
        dialog.grab_set()  # Make dialog modal
        
        # Frame for form fields
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form fields with existing values
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_var = tk.StringVar(value=str(cargo["id"]))
        ttk.Entry(form_frame, textvariable=id_var, state="readonly").grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Cargo Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        cargo_type_var = tk.StringVar(value=cargo["cargo_type"])
        ttk.Combobox(form_frame, textvariable=cargo_type_var, values=list(self.config["cargo_types"].keys())).grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Origin:").grid(row=2, column=0, sticky=tk.W, pady=5)
        origin_var = tk.StringVar(value=cargo["origin"])
        ttk.Combobox(form_frame, textvariable=origin_var, values=self.config["destinations"]).grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Destination:").grid(row=3, column=0, sticky=tk.W, pady=5)
        dest_var = tk.StringVar(value=cargo["destination"])
        ttk.Combobox(form_frame, textvariable=dest_var, values=self.config["destinations"]).grid(row=3, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Mass (tons):").grid(row=4, column=0, sticky=tk.W, pady=5)
        mass_var = tk.StringVar(value=str(cargo["mass"]))
        ttk.Entry(form_frame, textvariable=mass_var).grid(row=4, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Value (cr/ton):").grid(row=5, column=0, sticky=tk.W, pady=5)
        value_var = tk.StringVar(value=str(cargo["value_per_ton"]))
        ttk.Entry(form_frame, textvariable=value_var).grid(row=5, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Shipping Company:").grid(row=6, column=0, sticky=tk.W, pady=5)
        company_var = tk.StringVar(value=cargo["shipping_company"])
        ttk.Combobox(form_frame, textvariable=company_var, values=self.config["shipping_companies"]).grid(row=6, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Posted On (YYYY-MM-DD):").grid(row=7, column=0, sticky=tk.W, pady=5)
        posted_var = tk.StringVar(value=cargo["posted_on"])
        ttk.Entry(form_frame, textvariable=posted_var).grid(row=7, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=8, column=0, sticky=tk.W, pady=5)
        deadline_var = tk.StringVar(value=cargo["deadline"])
        ttk.Entry(form_frame, textvariable=deadline_var).grid(row=8, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Status:").grid(row=9, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value=cargo["status"])
        ttk.Combobox(form_frame, textvariable=status_var, values=["Available", "Contracted", "Expired"]).grid(row=9, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X)
        
        def save_edited_cargo():
            # Validate inputs
            try:
                mass = int(mass_var.get())
                value_per_ton = int(value_var.get())
                
                self.cargo_list[cargo_index] = {
                    "id": int(id_var.get()),
                    "cargo_type": cargo_type_var.get(),
                    "origin": origin_var.get(),
                    "destination": dest_var.get(),
                    "mass": mass,
                    "value_per_ton": value_per_ton,
                    "total_value": mass * value_per_ton,
                    "shipping_company": company_var.get(),
                    "posted_on": posted_var.get(),
                    "deadline": deadline_var.get(),
                    "status": status_var.get()
                }
                
                self.update_cargo_display()
                dialog.destroy()
                
            except ValueError:
                messagebox.showwarning("Invalid Input", "Mass and value must be numbers.")
        
        ttk.Button(button_frame, text="Save", command=save_edited_cargo).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def delete_cargo(self):
        """Delete the selected cargo listing"""
        selected_item = self.cargo_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a cargo listing to delete.")
            return
            
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this cargo listing?"):
            return
            
        # Get the cargo ID from the selected item
        cargo_id = int(self.cargo_tree.item(selected_item[0], "values")[0])
        
        # Remove the cargo from our list
        self.cargo_list = [cargo for cargo in self.cargo_list if cargo["id"] != cargo_id]
        self.update_cargo_display()
        
    def add_unusual_cargo(self):
        """Add a special or unusual cargo with custom parameters"""
        # Create a dialog with more options
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Special/Unusual Cargo")
        dialog.geometry("600x700")
        dialog.grab_set()  # Make dialog modal
        
        # Frame for form fields
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get next available ID
        next_id = 1
        if self.cargo_list:
            next_id = max(cargo["id"] for cargo in self.cargo_list) + 1
            
        # Create form fields with more detailed options
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_var = tk.StringVar(value=str(next_id))
        ttk.Entry(form_frame, textvariable=id_var, state="readonly").grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Cargo Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        cargo_type_var = tk.StringVar()
        cargo_type_entry = ttk.Entry(form_frame, textvariable=cargo_type_var)
        cargo_type_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        ttk.Label(form_frame, text="(Custom type name)").grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Predefined unusual cargo types
        unusual_types = [
            "Experimental Weapon System", 
            "Diplomatic Courier Package",
            "Xeno-Archaeological Artifacts",
            "Unstable Isotopes",
            "Live Exotic Animals",
            "Political Prisoner/VIP",
            "Ancient Technology",
            "Corsair Plunder",
            "Military Prototype",
            "Black Market Biologicals"
        ]
        
        ttk.Label(form_frame, text="Quick Select:").grid(row=2, column=0, sticky=tk.W, pady=5)
        def set_unusual_type(event):
            selected = unusual_type_combo.get()
            if selected:
                cargo_type_var.set(selected)
                # Set reasonable defaults for the type
                if "Weapon" in selected or "Military" in selected:
                    mass_var.set("5")
                    value_var.set("100000")
                    risk_var.set("High")
                elif "Diplomatic" in selected or "VIP" in selected:
                    mass_var.set("1")
                    value_var.set("500000")
                    risk_var.set("Medium")
                elif "Biological" in selected or "Animals" in selected:
                    mass_var.set("10")
                    value_var.set("75000")
                    risk_var.set("Medium")
                elif "Artifact" in selected or "Ancient" in selected:
                    mass_var.set("3")
                    value_var.set("200000")
                    risk_var.set("Low")
                else:
                    mass_var.set("5")
                    value_var.set("50000")
                    risk_var.set("Medium")
        
        unusual_type_combo = ttk.Combobox(form_frame, values=unusual_types)
        unusual_type_combo.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        unusual_type_combo.bind("<<ComboboxSelected>>", set_unusual_type)
        
        ttk.Label(form_frame, text="Origin:").grid(row=3, column=0, sticky=tk.W, pady=5)
        origin_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=origin_var, values=self.config["destinations"]).grid(row=3, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Destination:").grid(row=4, column=0, sticky=tk.W, pady=5)
        dest_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=dest_var, values=self.config["destinations"]).grid(row=4, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Mass (tons):").grid(row=5, column=0, sticky=tk.W, pady=5)
        mass_var = tk.StringVar(value="5")
        ttk.Entry(form_frame, textvariable=mass_var).grid(row=5, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Value (cr/ton):").grid(row=6, column=0, sticky=tk.W, pady=5)
        value_var = tk.StringVar(value="50000")
        ttk.Entry(form_frame, textvariable=value_var).grid(row=6, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Shipping Company:").grid(row=7, column=0, sticky=tk.W, pady=5)
        company_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=company_var, values=self.config["shipping_companies"]).grid(row=7, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Posted On (YYYY-MM-DD):").grid(row=8, column=0, sticky=tk.W, pady=5)
        posted_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=posted_var).grid(row=8, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=9, column=0, sticky=tk.W, pady=5)
        deadline_var = tk.StringVar(value=(datetime.now() + timedelta(weeks=4)).strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=deadline_var).grid(row=9, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Status:").grid(row=10, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value="Available")
        ttk.Combobox(form_frame, textvariable=status_var, values=["Available", "Contracted", "Expired"]).grid(row=10, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Risk Level:").grid(row=11, column=0, sticky=tk.W, pady=5)
        risk_var = tk.StringVar(value="Medium")
        ttk.Combobox(form_frame, textvariable=risk_var, values=["Low", "Medium", "High", "Extreme"]).grid(row=11, column=1, sticky=tk.W+tk.E, pady=5)
        
        ttk.Label(form_frame, text="Special Notes:").grid(row=12, column=0, sticky=tk.W, pady=5)
        notes_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=notes_var).grid(row=12, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X)
        
        def save_unusual_cargo():
            # Validate inputs
            try:
                mass = int(mass_var.get())
                value_per_ton = int(value_var.get())
                
                cargo = {
                    "id": int(id_var.get()),
                    "cargo_type": cargo_type_var.get(),
                    "origin": origin_var.get(),
                    "destination": dest_var.get(),
                    "mass": mass,
                    "value_per_ton": value_per_ton,
                    "total_value": mass * value_per_ton,
                    "shipping_company": company_var.get(),
                    "posted_on": posted_var.get(),
                    "deadline": deadline_var.get(),
                    "status": status_var.get(),
                    "risk_level": risk_var.get(),
                    "special_notes": notes_var.get()
                }
                
                # Validate required fields
                if not cargo["cargo_type"] or not cargo["origin"] or not cargo["destination"] or not cargo["shipping_company"]:
                    messagebox.showwarning("Missing Data", "Please fill in all required fields.")
                    return
                    
                self.cargo_list.append(cargo)
                self.update_cargo_display()
                dialog.destroy()
                
            except ValueError:
                messagebox.showwarning("Invalid Input", "Mass and value must be numbers.")
        
        ttk.Button(button_frame, text="Add", command=save_unusual_cargo).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
    def save_changes(self):
        """Save all changes to the cargo save file"""
        try:
            # First, load the existing save file to preserve other sections
            player_credits = 10000
            current_bids = {}
            
            if os.path.exists("cargo_sim_save.csv"):
                with open("cargo_sim_save.csv", "r") as file:
                    reader = csv.reader(file)
                    
                    section = None
                    
                    for row in reader:
                        if not row:
                            continue
                            
                        if row[0] == "CARGO_DATA":
                            section = "cargo"
                            continue
                        elif row[0] == "BID_DATA":
                            section = "bids"
                            continue
                        elif row[0] == "PLAYER_DATA":
                            section = "player"
                            continue
                            
                        if section == "bids" and row[0] != "cargo_id":
                            cargo_id = int(row[0])
                            
                            # Find the corresponding cargo
                            cargo = next((c for c in self.cargo_list if c["id"] == cargo_id), None)
                            
                            if cargo:
                                current_bids[cargo_id] = {
                                    "amount": int(row[1]),
                                    "status": row[2],
                                    "bid_date": row[3],
                                    "cargo": cargo
                                }
                        elif section == "player" and row[0] != "credits":
                            player_credits = int(row[0])
            
            # Now write the updated file
            with open("cargo_sim_save.csv", "w", newline="") as file:
                writer = csv.writer(file)
                
                # Write header row
                writer.writerow(["CARGO_DATA"])
                writer.writerow(["id", "cargo_type", "origin", "destination", "mass", 
                                "value_per_ton", "total_value", "shipping_company", 
                                "posted_on", "deadline", "status"])
                
                # Write cargo data
                for cargo in self.cargo_list:
                    row = [
                        cargo["id"],
                        cargo["cargo_type"],
                        cargo["origin"],
                        cargo["destination"],
                        cargo["mass"],
                        cargo["value_per_ton"],
                        cargo["total_value"],
                        cargo["shipping_company"],
                        cargo["posted_on"],
                        cargo["deadline"],
                        cargo["status"]
                    ]
                    writer.writerow(row)
                    
                # Write bid data
                writer.writerow(["BID_DATA"])
                writer.writerow(["cargo_id", "amount", "status", "bid_date"])
                
                for cargo_id, bid_info in current_bids.items():
                    writer.writerow([
                        cargo_id,
                        bid_info["amount"],
                        bid_info["status"],
                        bid_info["bid_date"]
                    ])
                    
                # Write player data
                writer.writerow(["PLAYER_DATA"])
                writer.writerow(["credits"])
                writer.writerow([player_credits])
                
            messagebox.showinfo("Success", "Cargo listings saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving cargo data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CargoEditor(root)
    root.mainloop()
                                                        