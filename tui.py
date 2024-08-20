from yahtzo.utils.read_config import read_config
from yahtzo.utils.roll_dice import roll_dice
from yahtzo.utils.calculate import calculate

from yahtzo.database.db import get_last_result, grab_db, store_game

class StopAdv(Exception):
    pass

held_numbers: list = []

rolls: list = []
holds: list = []

config_file, num_dice, db_name = read_config('config.json')

db = grab_db(db_name)

number_of_dice = num_dice


print("Welcome to Yahtzo! Let's begin!")
try:
    print(f'You scored {get_last_result(db)[1]} points last time!')
except:
    pass

def ask_for_hold(rolled_list: list):
    held_order = int(input('Which number (in its order) do you want to hold? '))
    try:
        if held_order > 0:
            held_numbers.append(rolled_list[abs(held_order-1)])
            holds.append(rolled_list[abs(held_order-1)])
        else:
            raise
    except:
        print('Invalid number. Please try again.')
        ask_for_hold(rolled_list)

def play_game():
    i = 0
    global rolled_list
    global number_of_dice
    while i < num_dice:
        rolled_list = roll_dice(number_of_dice)
        try:
            rolled_list.append(held_numbers.pop(0))
        except:
            pass

        rolls.append(rolled_list)

        if i == num_dice-1:
            break

        print(f'You rolled {rolled_list}')

        ask_for_hold(rolled_list)

        i+=1
        if i == 1:
            number_of_dice -= 1

def start_menu():
    try:
        menu_1 = int(input('Would you like to play a game (1), see your past games (2) or exit (3)? '))
        if menu_1 == 1:
            play_game()
            print(f'You rolled {rolled_list} last!')
            score = calculate(rolled_list)
            print(f'You scored {score} points!')

            store_game(db, score, rolls, holds)
        elif menu_1 == 2:
            for i in db.execute('SELECT * FROM history').fetchall():
                print(f'Game {i[0]}: {i}')

        elif menu_1 == 3:
            raise StopAdv
        else:
            raise
    except StopAdv:
        raise StopAdv

    except:   
        print('Invalid input. Please try again.')
        start_menu()

try:
    while True:        
        start_menu()
except StopAdv:
    pass
