from yahtzo.utils.read_config import read_config
config = read_config('config.json')

def calculate(score_list: list): # Define a function to calculate the score
    if score_list.count(6) == len(score_list): # Check if all the numbers are 6
        return config.scoring['all-six']
    
    elif score_list.count(score_list[0]) == len(score_list): # Check if all the numbers are the same
        return config.scoring['all-of-kind']
    
    elif sorted(score_list) == list(range(min(score_list), max(score_list)+1)): # Check if the numbers are in order
        return config.scoring['straight']
    
    elif score_list.count(score_list[0]) == len(score_list)-1 or score_list.count(score_list[1]) == len(score_list)-1: # Check if the numbers are a full house
        return config.scoring['full-house']
    
    else: # If none of the above conditions are met, return no-points, due to no conditions being met for a score.
        return config.scoring['no-score']

