from yahtzo.utils.read_config import read_config
from yahtzo.utils.roll_dice import roll_dice
from yahtzo.utils.calculate import calculate

from yahtzo.database.db import get_last_result, grab_db, store_game, clean

class StopAdv(Exception):
    pass

held_numbers: list = []

rolls: list = []
holds: list = []

configuration = read_config('config.json')

db = grab_db(configuration.db_name)

num_dice = configuration.num_dice
number_of_dice = num_dice


print("Welcome to Yahtzo! Let's begin!")
try:
    print(f'You scored {get_last_result(db)[1]} points last time!')
except:
    pass

def ask_for_hold(rolled_list: list):
    held_real = []
    held_order = input('Which number(s) (in its order) do you want to hold (separated by a comma)? ')
    try:
        held_order_list = [int(i) for i in held_order.split(',')]
        if len(held_order_list) > 0 and all(i > 0 for i in held_order_list):
            for i in held_order_list:
                held_numbers.append(rolled_list[i-1])

            for i in held_order_list:
                held_real.append(rolled_list[i-1])
                
            holds.append(held_real)
        else:
            raise
    except:
        print('Invalid number(s). Please try again.')
        ask_for_hold(rolled_list)

def play_game():
    i = 0
    global rolled_list
    global number_of_dice
    while i < num_dice:
        number_of_dice = num_dice - len(held_numbers)
        rolled_list = roll_dice(number_of_dice)

        try:
            for x in held_numbers:
                rolled_list.append(x)
        except:
            pass

        held_numbers.clear()
        rolls.append(rolled_list)

        print(f'You rolled {rolled_list}')
        if i < num_dice-1:
            ask_for_hold(rolled_list)

        i+=1

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
            hist_exists: bool = False
            for i in db.execute('SELECT * FROM history').fetchall():
                print(f'Game {i[0]}: {i}')
                hist_exists = True
            if not hist_exists:
                print('Nothing to see here.')
            

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

clean()