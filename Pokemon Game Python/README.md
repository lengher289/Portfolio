# Safari Zone Simulator

This is a Python program that simulates a Safari Zone adventure. It uses the Tkinter library for creating a graphical user interface. The objective of the game is to catch wild Pokémon using Safari Balls.

## Instructions

1. Run the program using Python.
2. A window titled "Safari Zone Simulator" will open.
3. The window contains the following elements:
   - A label indicating the Pokémon encountered.
   - An image of the Pokémon.
   - A label indicating the catch probability of the Pokémon.
   - Two buttons: "Throw Safari Ball" and "Run Away."
   - A label for status messages.

## Game Screenshots

### Startup Image
![Startup Image](startup.png)
*Figure 1: The game interface when it starts up.*

### Game End Image
![Game End Image](game_end.png)
*Figure 2: The game interface when the game ends.*

## Pokemon Class

The `Pokemon` class represents a Pokémon with its attributes. The attributes include the Pokémon's name, number, catch rate, and speed.

## SafariSimulator Class

The `SafariSimulator` class is responsible for managing the game's logic and user interface. It contains the following methods:

### `__init__(self, master=None)`

This method initializes the Safari Simulator. It sets up the window, reads data from the "pokedex.csv" file, and initializes instance variables. It also calls the `createWidgets()` method to create the user interface.

### `createWidgets(self)`

This method creates the widgets for the user interface. It creates buttons, labels, and an image label to display the Pokémon. It also calculates and displays the catch probability of the Pokémon.

### `nextPokemon(self)`

This method is called when a Pokémon is caught or when the user clicks the "Run Away" button. It selects a new random Pokémon, updates the instance variables, and refreshes the user interface.

### `throwBall(self)`

This method is called when the user clicks the "Throw Safari Ball" button. It decrements the number of remaining Safari Balls and determines if the Pokémon is caught based on its catch rate. It updates the user interface accordingly and calls the `nextPokemon()` method.

### `endAdventure(self)`

This method is called when the user runs out of Safari Balls. It displays a message indicating the end of the adventure and lists the Pokémon caught during the game.

## Additional Notes

- The Pokémon data is stored in a CSV file named "pokedex.csv." It contains information such as the Pokémon's name, number, catch rate, and speed.
- The Pokémon sprites are stored in the "sprites" folder and are displayed using the `PhotoImage` class from the Tkinter library.

Enjoy your Safari Zone adventure and try to catch as many Pokémon as possible!
