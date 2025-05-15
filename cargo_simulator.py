import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import csv
import os
import json
from datetime import datetime, timedelta

class CargoTradingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Trader Cargo Simulator")
        self.root.geometry("1300x700")
        
        # Load configuration
        self.load_config()
        
        # Data structures
        self.cargo_list = []
        self.player_credits = self.config["simulation_settings"]["player_starting_credits"]
        self.current_bids = {}
        
        self.create_gui()
        self.generate_cargo(self.config["simulation_settings"]["initial_cargo_listings"])
        
    def load_config(self):
        """Load configuration from file or create default if not exists"""
        if os.path.exists("cargo_config.json"):
            with open("cargo_config.json", "r") as f:
                self.config = json.load(f)
        else:
            self.config = create_default_config()
            
        # Convert lists to tuples where needed for compatibility with original code
        for cargo_type in self.config["cargo_types"]:
            self.config["cargo_types"][cargo_type]["mass"] = tuple(self.config["cargo_types"][cargo_type]["mass"])
            self.config["cargo_types"][cargo_type]["value"] = tuple(self.config["cargo_types"][cargo_type]["value"])
        
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top information bar
        info_frame = ttk.Frame(main_frame, padding="5")
        info_frame.pack(fill=tk.X)
        
        ttk.Label(info_frame, text="Current Date:").pack(side=tk.LEFT, padx=5)
        self.date_label = ttk.Label(info_frame, text=self.get_game_date())
        self.date_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(info_frame, text="Credits:").pack(side=tk.LEFT, padx=20)
        self.credits_label = ttk.Label(info_frame, text=f"{self.player_credits:,}")
        self.credits_label.pack(side=tk.LEFT, padx=5)
        
        # Cargo listings frame
        cargo_frame = ttk.LabelFrame(main_frame, text="Available Cargo Contracts", padding="10")
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
            self.cargo_tree.heading(col, text=col, command=lambda c=col: self.sort_cargo_by_column(c))
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(cargo_frame, orient=tk.VERTICAL, command=self.cargo_tree.yview)
        self.cargo_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cargo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bottom control frame
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Place Bid", command=self.place_bid).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="View My Bids", command=self.view_bids).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Refresh Listings", command=self.refresh_listings).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Advance Time (1 Week)", command=self.advance_time).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Edit Config", command=self.edit_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Game", command=self.save_game).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Load Game", command=self.load_game).pack(side=tk.RIGHT, padx=5)
        
    def generate_cargo(self, count=5):
        """Generate random cargo listings"""
        current_ids = [cargo["id"] for cargo in self.cargo_list]
        next_id = 1
        if current_ids:
            next_id = max(current_ids) + 1
            
        new_cargo = []
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for _ in range(count):
            cargo_types = list(self.config["cargo_types"].keys())
            cargo_type = random.choice(cargo_types)
            mass_range = self.config["cargo_types"][cargo_type]["mass"]
            value_range = self.config["cargo_types"][cargo_type]["value"]
            
            mass = random.randint(mass_range[0], mass_range[1])
            value_per_ton = random.randint(value_range[0], value_range[1])
            
            # Origin and destination should be different
            origin = random.choice(self.config["destinations"])
            destination = random.choice([d for d in self.config["destinations"] if d != origin])
            
            # Random deadline between configured weeks from now
            weeks_range = self.config["simulation_settings"]["cargo_deadline_range_weeks"]
            weeks = random.randint(weeks_range[0], weeks_range[1])
            deadline_date = (datetime.now() + timedelta(weeks=weeks)).strftime("%Y-%m-%d")
            
            cargo = {
                "id": next_id,
                "cargo_type": cargo_type,
                "origin": origin,
                "destination": destination,
                "mass": mass,
                "value_per_ton": value_per_ton,
                "total_value": mass * value_per_ton,
                "shipping_company": random.choice(self.config["shipping_companies"]),
                "posted_on": current_date,
                "deadline": deadline_date,
                "status": "Available"
            }
            
            new_cargo.append(cargo)
            next_id += 1
            
        self.cargo_list.extend(new_cargo)
        self.update_cargo_display()
        
    def update_cargo_display(self):
        """Update the cargo treeview with current listings"""
        # Clear the existing items
        for item in self.cargo_tree.get_children():
            self.cargo_tree.delete(item)
            
        # Insert cargo listings
        for cargo in self.cargo_list:
            if cargo["status"] == "Available":  # Only show available cargo
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
                
    def place_bid(self):
        """Place a bid on selected cargo"""
        selected_item = self.cargo_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a cargo listing to bid on.")
            return
            
        # Get the cargo ID from the selected item
        cargo_id = int(self.cargo_tree.item(selected_item[0], "values")[0])
        
        # Find the cargo in our list
        cargo = next((c for c in self.cargo_list if c["id"] == cargo_id), None)
        if not cargo:
            messagebox.showerror("Error", "Cargo not found.")
            return
            
        # Ask for bid amount
        suggested_bid = int(cargo["total_value"] * 0.85)  # 85% of total value as suggestion
        bid_prompt = f"Enter your bid amount for {cargo['cargo_type']} to {cargo['destination']}:\n"
        bid_prompt += f"(Suggested bid: {suggested_bid:,} credits)"
        
        bid_amount = simpledialog.askinteger("Place Bid", bid_prompt, 
                                            initialvalue=suggested_bid,
                                            minvalue=1, 
                                            maxvalue=cargo["total_value"] * 2)
        
        if bid_amount is None:  # User cancelled
            return
            
        # Record the bid
        self.current_bids[cargo_id] = {
            "amount": bid_amount,
            "cargo": cargo,
            "status": "Pending",
            "bid_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        messagebox.showinfo("Bid Placed", f"Your bid of {bid_amount:,} credits has been submitted. "
                            f"Check 'View My Bids' to see the status.")
                            
    def view_bids(self):
        """View the player's current bids"""
        if not self.current_bids:
            messagebox.showinfo("No Bids", "You haven't placed any bids yet.")
            return
            
        # Create a new window to show bids
        bid_window = tk.Toplevel(self.root)
        bid_window.title("My Cargo Bids")
        bid_window.geometry("800x400")
        
        # Create treeview for bids
        columns = ("Cargo ID", "Cargo Type", "Destination", "Bid Amount", "Status", "Date")
        bid_tree = ttk.Treeview(bid_window, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            bid_tree.heading(col, text=col)
            if col == "Bid Amount":
                bid_tree.column(col, width=100, anchor=tk.CENTER)
            elif col in ["Cargo ID", "Date", "Status"]:
                bid_tree.column(col, width=80, anchor=tk.CENTER)
            else:
                bid_tree.column(col, width=150)
                
        # Add scrollbar
        scrollbar = ttk.Scrollbar(bid_window, orient=tk.VERTICAL, command=bid_tree.yview)
        bid_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        bid_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Insert bid data
        for cargo_id, bid_info in self.current_bids.items():
            cargo = bid_info["cargo"]
            values = (
                cargo_id,
                cargo["cargo_type"],
                cargo["destination"],
                f"{bid_info['amount']:,}",
                bid_info["status"],
                bid_info["bid_date"]
            )
            bid_tree.insert("", tk.END, values=values)
            
    def refresh_listings(self):
        """Refresh cargo listings - remove old ones and add new ones"""
        # Remove expired listings
        today = datetime.now()
        self.cargo_list = [cargo for cargo in self.cargo_list if 
                          cargo["status"] == "Available" and 
                          datetime.strptime(cargo["deadline"], "%Y-%m-%d") > today]
        
        # Generate new cargo
        new_cargo_range = self.config["simulation_settings"]["new_cargo_per_refresh"]
        self.generate_cargo(random.randint(new_cargo_range[0], new_cargo_range[1]))
        
    def advance_time(self):
        """Advance game time by one week and process pending bids"""
        # Process bids
        thresholds = self.config["simulation_settings"]["cargo_acceptance_thresholds"]
        
        for cargo_id, bid_info in list(self.current_bids.items()):
            if bid_info["status"] == "Pending":
                # Determine win chance based on bid amount
                cargo_value = bid_info["cargo"]["total_value"]
                if bid_info["amount"] >= cargo_value * thresholds["high_chance"]:
                    win_chance = self.config["simulation_settings"]["high_win_chance"]
                elif bid_info["amount"] >= cargo_value * thresholds["medium_chance"]:
                    win_chance = self.config["simulation_settings"]["medium_win_chance"]
                else:
                    win_chance = self.config["simulation_settings"]["low_win_chance"]
                    
                if random.random() < win_chance:
                    self.current_bids[cargo_id]["status"] = "Accepted"
                    
                    # Remove the cargo from available listings
                    for cargo in self.cargo_list:
                        if cargo["id"] == cargo_id:
                            cargo["status"] = "Contracted"
                            break
                            
                    messagebox.showinfo("Bid Accepted", 
                                       f"Your bid of {bid_info['amount']:,} credits for the "
                                       f"{bid_info['cargo']['cargo_type']} cargo to "
                                       f"{bid_info['cargo']['destination']} has been accepted!")
                else:
                    self.current_bids[cargo_id]["status"] = "Rejected"
        
        # Update the display
        self.update_cargo_display()
        
        # Update date display (advance by 1 week)
        self.date_label.config(text=self.get_game_date(7))
        
    def get_game_date(self, days_to_add=0):
        """Get the current game date, optionally adding days"""
        game_date = datetime.now() + timedelta(days=days_to_add)
        # Format in Traveller style date: year-day (out of 365)
        year = game_date.year
        day_of_year = game_date.timetuple().tm_yday
        return f"{year}-{day_of_year:03d}"
    
    def edit_config(self):
        """Open a simple editor for the configuration file"""
        messagebox.showinfo("Edit Configuration", 
                           "The configuration file will open in your default text editor. "
                           "After saving changes, restart the application for them to take effect.")
        
        # Open the config file in the default editor
        os.system(f"start cargo_config.json" if os.name == "nt" else f"open cargo_config.json")
        
    def sort_cargo_by_column(self, column):
        """Sort the cargo listings by the selected column"""
        column_index = self.cargo_tree["columns"].index(column)
        
        # Get all items with their values
        items_with_values = [(self.cargo_tree.item(item, "values"), item) for item in self.cargo_tree.get_children()]
        
        # Sort based on the column type
        if column in ["Mass (tons)", "Value (cr/ton)", "Total Value", "ID"]:
            # Sort numerically after removing commas and converting to int
            items_with_values.sort(key=lambda x: int(x[0][column_index].replace(",", "")))
        else:
            # Sort alphabetically
            items_with_values.sort(key=lambda x: x[0][column_index])
            
        # Rearrange items in the treeview
        for index, (values, item) in enumerate(items_with_values):
            self.cargo_tree.move(item, "", index)
            
    def save_game(self):
        """Save the current game state"""
        try:
            with open("cargo_sim_save.csv", "w", newline="") as file:
                writer = csv.writer(file)
                
                # Write header row
                writer.writerow(["CARGO_DATA"])
                writer.writerow(["id", "cargo_type", "origin", "destination", "mass", 
                                "value_per_ton", "total_value", "shipping_company", 
                                "posted_on", "deadline", "status"])
                
                # Write cargo data
                for cargo in self.cargo_list:
                    writer.writerow([
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
                    ])
                    
                # Write bid data
                writer.writerow(["BID_DATA"])
                writer.writerow(["cargo_id", "amount", "status", "bid_date"])
                
                for cargo_id, bid_info in self.current_bids.items():
                    writer.writerow([
                        cargo_id,
                        bid_info["amount"],
                        bid_info["status"],
                        bid_info["bid_date"]
                    ])
                    
                # Write player data
                writer.writerow(["PLAYER_DATA"])
                writer.writerow(["credits"])
                writer.writerow([self.player_credits])
                
            messagebox.showinfo("Game Saved", "Game saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving game: {str(e)}")
            
    def load_game(self):
        """Load a saved game state"""
        if not os.path.exists("cargo_sim_save.csv"):
            messagebox.showerror("Load Error", "No saved game found.")
            return
            
        try:
            with open("cargo_sim_save.csv", "r") as file:
                reader = csv.reader(file)
                
                section = None
                self.cargo_list = []
                self.current_bids = {}
                
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
                        
                    if section == "cargo" and row[0] != "id":
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
                    elif section == "bids" and row[0] != "cargo_id":
                        cargo_id = int(row[0])
                        # Find the corresponding cargo
                        cargo = next((c for c in self.cargo_list if c["id"] == cargo_id), None)
                        
                        if cargo:
                            self.current_bids[cargo_id] = {
                                "amount": int(row[1]),
                                "status": row[2],
                                "bid_date": row[3],
                                "cargo": cargo
                            }
                    elif section == "player" and row[0] != "credits":
                        self.player_credits = int(row[0])
                        self.credits_label.config(text=f"{self.player_credits:,}")
                        
            self.update_cargo_display()
            messagebox.showinfo("Game Loaded", "Game loaded successfully.")
        except Exception as e:
            messagebox.showerror("Load Error", f"Error loading game: {str(e)}")

def create_default_config():
    """Create default configuration file if none exists"""
    config = {
        "cargo_types": {
            "Agricultural Products": {"mass": [5, 200], "value": [500, 2000]},
            "Refined Metals": {"mass": [10, 100], "value": [2000, 8000]},
            "Luxury Goods": {"mass": [1, 20], "value": [10000, 50000]},
            "Medical Supplies": {"mass": [2, 30], "value": [5000, 15000]},
            "Industrial Equipment": {"mass": [20, 150], "value": [3000, 12000]},
            "Consumer Electronics": {"mass": [5, 50], "value": [4000, 12000]},
            "Processed Food": {"mass": [10, 100], "value": [800, 2500]},
            "Textiles": {"mass": [5, 60], "value": [1000, 3000]},
            "Construction Materials": {"mass": [50, 300], "value": [600, 2000]},
            "Pharmaceuticals": {"mass": [1, 15], "value": [20000, 80000]},
            "Hazardous Materials": {"mass": [10, 80], "value": [3000, 15000]},
            "Research Equipment": {"mass": [1, 10], "value": [25000, 100000]}
        },
        "shipping_companies": [
            "Interstellar Logistics", "Orion Freight Ltd.", "Nova Express",
            "Stellar Shipping Co.", "Artemis Cargo Systems", "Cygnus Transport",
            "Phoenix Carriers", "Meridian Trade Alliance", "Eclipse Haulers",
            "Vega Commercial Lines", "Antares Shipping Guild", "Frontier Movers",
            "Imperial Haulage", "Zhodani Consulate Shipping", "Solomani Transport"
        ],
        "destinations": [
            "Regina", "Mora", "Terra", "Vland", "Deneb", "Zhodane", "Sylea",
            "Corridor", "Trojan Reach", "Spinward Marches", "Karin", "Diaspora",
            "Core", "Gateway", "Far Frontiers", "Hinterworlds", "Solomani Rim",
            "Alpha Centauri", "Riftspan Reaches", "Empty Quarter", "Ley Sector",
            "Magyar", "Verge", "Foreven", "Beyond", "Depot"
        ],
        "simulation_settings": {
            "initial_cargo_listings": 15,
            "new_cargo_per_refresh": [3, 8],
            "player_starting_credits": 10000,
            "cargo_deadline_range_weeks": [2, 6],
            "cargo_acceptance_thresholds": {
                "high_chance": 0.8,  # 80% of cargo value - 70% chance of winning
                "medium_chance": 0.6  # 60% of cargo value - 40% chance of winning
                # below medium_chance - 20% chance of winning
            },
            "high_win_chance": 0.7,
            "medium_win_chance": 0.4,
            "low_win_chance": 0.2
        }
    }
    
    with open("cargo_config.json", "w") as f:
        json.dump(config, f, indent=4)
    
    return config

if __name__ == "__main__":
    root = tk.Tk()
    app = CargoTradingSimulator(root)
    root.mainloop()