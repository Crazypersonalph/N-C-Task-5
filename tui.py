from yahtzo.utils.read_config import read_config
from yahtzo.utils.roll_dice import roll_dice
from yahtzo.utils.calculate import calculate

from yahtzo.database.db import get_high_score, get_last_result, grab_db, store_game, clean

import base64

# Import required libraries

class StopAdv(Exception): # Define a custom exception to stop the game
    pass

held_numbers: list = [] # Define a list to hold the numbers that the player wants to hold

rolls: list = [] # Define a list to hold the rolls (for the db)
holds: list = [] # Define a list to hold the holds (for the db)

configuration = read_config('config.json') # Read the configuration file

db = grab_db(configuration.db_name) # Grab the database

num_dice = configuration.num_dice # Get the number of dice from the configuration file of dice (config file)


print("Welcome to Yahtzo! Let's begin!")
try:
    print(f'You scored {get_last_result(db)[1]} points last time!') # Print the last score from the database
except:
    pass

try:
    print(f'Your all-time high score is {get_high_score(db)[1]}!') # Print the highest score from the database
except:
    pass

def ask_for_hold(rolled_list: list): # Define a function to ask the player which numbers they want to hold
    held_real = []
    held_order = input('Which number(s) (in its order) do you want to hold (separated by a comma)? ')
    try:
        held_order_list = [int(i) for i in held_order.split(',')] # Split the input by commas and convert it to a list of integers
        if len(held_order_list) > 0 and all(i > 0 for i in held_order_list): # Check if the input is valid
            for i in held_order_list: # Append the numbers to the held_numbers list
                held_numbers.append(rolled_list[i-1])

            for i in held_order_list: # Append the numbers to the held_real list (database concatenation)
                held_real.append(rolled_list[i-1])
                
            holds.append(held_real) # Append the held numbers to the holds list (database)
        else:
            raise
    except:
        print('Invalid number(s). Please try again.') # If the input is invalid, print an error message and ask again
        ask_for_hold(rolled_list)

def play_game(): # Define a function to play the game
    i = 0
    global rolled_list # Reference the global variable to hold the rolled numbers
    
    while i < num_dice: # Loop through the number of dice
        number_of_dice = num_dice - len(held_numbers) # Set the number of dice to the number of dice minus the held numbers
        rolled_list = roll_dice(number_of_dice) # Roll the dice

        try: # Try to append the held numbers to the rolled list. If there are no held numbers, pass
            for x in held_numbers:
                rolled_list.append(x)
        except:
            pass

        held_numbers.clear() # Clear the held numbers list for the next round of rolling
        rolls.append(rolled_list) # Append the rolled numbers to the rolls list (database), for saving

        print(f'You rolled {rolled_list}')
        if i < num_dice-1: # If the player has not rolled all the dice, ask if they want to hold any numbers
            ask_for_hold(rolled_list)

        i+=1

def start_menu(): # Define a function to show the start menu
    try:
        menu_1 = int(input('Would you like to play a game (1), see your past games (2) or exit (3)? '))
        if menu_1 == 1:
            # If '1' is selected, play the game, and calculate a score
            play_game()
            print(f'You rolled {rolled_list} last!')
            score = calculate(rolled_list)
            print(f'You scored {score} points!')
            # Store the game in the database at the end
            store_game(db, score, rolls, holds, base64.b64encode(str(configuration.config).encode()).decode())
        elif menu_1 == 2:
            # If '2' is selected, show the past games
            hist_exists: bool = False 
            for i in db.execute('SELECT * FROM history').fetchall(): # Loop through the database and print the games
                print()
                print(f'Game {i[0]}: {i}')
                print()
                hist_exists = True
            if not hist_exists: # If there are no games, print a message
                print('Nothing to see here.')
            

        elif menu_1 == 3: # If '3' is selected, raise the StopAdv exception to stop the game
            raise StopAdv
        else:
            raise
    except StopAdv:
        raise StopAdv

    except:   
        print('Invalid input. Please try again.')
        start_menu()

# Where the magic happens
# The start of the actual game

try:
    while True:       
        start_menu()
except StopAdv:
    pass

# Clean up all the database stuff at the end
clean()