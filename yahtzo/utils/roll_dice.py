import secrets

def roll_dice(num_dice: int):
    returned_nums = []
    for i in range(num_dice):
        returned_nums.append(secrets.randbelow(6) + 1)
    return returned_nums


