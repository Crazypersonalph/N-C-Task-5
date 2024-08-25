import secrets

def roll_dice(num_dice: int): # Define a function to roll the dice
    returned_nums = []
    for i in range(num_dice):
        returned_nums.append(secrets.randbelow(6) + 1) # Append a random number between 1 and 6 to the rolled numbers list
    return returned_nums


