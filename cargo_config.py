import json
import os

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

def load_config():
    """Load configuration from file or create default if not exists"""
    if os.path.exists("cargo_config.json"):
        with open("cargo_config.json", "r") as f:
            config = json.load(f)
    else:
        config = create_default_config()
        
    # Convert lists to tuples where needed for compatibility with original code
    for cargo_type in config["cargo_types"]:
        config["cargo_types"][cargo_type]["mass"] = tuple(config["cargo_types"][cargo_type]["mass"])
        config["cargo_types"][cargo_type]["value"] = tuple(config["cargo_types"][cargo_type]["value"])
    
    return config

if __name__ == "__main__":
    # If run directly, create/reset the config file
    create_default_config()
    print("Default configuration file created: cargo_config.json")
    print("You can now edit this file to customize cargo types, destinations, and other settings.")