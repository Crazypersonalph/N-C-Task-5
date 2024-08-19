import yahtzo.utils.read_config
import yahtzo.utils.roll_dice
import yahtzo.utils.calculate

held_numbers: list = []

config_file, num_dice = yahtzo.utils.read_config.read_config('config.json')

number_of_dice = num_dice


print("Welcome to Yahtzo! Let's begin!")

def ask_for_hold(rolled_list: list):
    held_order = int(input('Which number (in its order) do you want to hold? '))
    try:
        if held_order > 0:
            held_numbers.append(rolled_list[abs(held_order-1)])
        else:
            raise
    except:
        print('Invalid number. Please try again.')
        ask_for_hold(rolled_list)

i = 0

while i < num_dice:
    rolled_list = yahtzo.utils.roll_dice.roll_dice(number_of_dice)
    try:
        rolled_list.append(held_numbers.pop(0))
    except:
        pass

    if i == num_dice-1:
        break

    print(f'You rolled {rolled_list}')

    ask_for_hold(rolled_list)

    i+=1
    if i == 1:
        number_of_dice -= 1

print(f'You scored {rolled_list} last!')
score = yahtzo.utils.calculate.calculate(rolled_list)
print(score)

