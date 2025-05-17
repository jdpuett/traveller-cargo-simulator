# Traveller Free Trader Cargo Simulator

A Python-based cargo trading simulator for the Mongoose Traveller RPG. This application simulates how cargo is moved in the open shipping market, allowing players to bid on cargo contracts in a realistic trading environment.


## Features

- **Realistic Cargo Trading System**: Simulates the open shipping market with various cargo types, destinations, and shipping companies
- **Bidding Mechanics**: Players can place bids on available cargo and compete with other traders
- **Time Progression**: Advance game time to simulate market changes and cargo deadlines
- **Customizable Data**: All cargo types, destinations, and shipping companies can be easily modified
- **Special Cargo Editor**: Create unusual or high-value cargo with custom parameters
- **Save/Load System**: Save your game progress and resume later

## Installation

1. Ensure you have Python 3.6+ installed on your system
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/traveller-cargo-simulator.git
   cd traveller-cargo-simulator
   ```
3. The application uses only standard libraries (tkinter), so no additional installation is required

## Usage

The application consists of three main components:

### Main Simulator (`cargo_simulator.py`)

Run the main simulator with:
```
python cargo_simulator.py
```

This launches the main interface where players can:
- View available cargo listings
- Place bids on cargo
- Advance game time
- Refresh cargo listings
- Save/load game progress

### Cargo Configuration (`cargo_config.py`)

To create or reset the configuration to defaults:
```
python cargo_config.py
```

This generates the `cargo_config.json` file which controls:
- Cargo types with mass and value ranges
- Available destinations
- Shipping companies
- Simulation settings (bid acceptance chances, etc.)

### Cargo Editor (`cargo_editor.py`)

For game masters who want to create custom cargo listings:
```
python cargo_editor.py
```

The editor allows you to:
- Add regular cargo listings
- Create special or unusual cargo with custom parameters
- Edit existing cargo
- Delete cargo listings

## Game Mechanics

- **Bidding System**: The acceptance of bids depends on how much you offer relative to the cargo's value
  - 80%+ of cargo value: 70% chance of acceptance
  - 60-80% of cargo value: 40% chance of acceptance
  - Below 60% of cargo value: 20% chance of acceptance

- **Time System**: Each advance of time progresses the game by one week, with cargo having deadlines between 2-6 weeks

## Customization

You can customize almost every aspect of the simulation:

1. Edit `cargo_config.json` directly (automatically created on first run)
2. Use the Cargo Editor to add special cargo listings
3. Modify the code to add additional features or change game mechanics

## Development

This project is structured into three main Python files:

- `cargo_simulator.py`: The main application
- `cargo_config.py`: Configuration management
- `cargo_editor.py`: Custom cargo creation tool

The game data is stored in:
- `cargo_config.json`: Configuration settings
- `cargo_sim_save.csv`: Game save data

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests with your improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the Mongoose Traveller RPG trading mechanics
- Designed to simulate realistic cargo shipping markets
- Created for enhancing the trading experience in Traveller campaigns

---

*Note: This is not an official Mongoose Publishing product and is not affiliated with the Traveller RPG. This is a fan-made tool for enhancing gameplay.*