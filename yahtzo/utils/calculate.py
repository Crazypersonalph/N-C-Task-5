from yahtzo.utils.read_config import read_config
config = read_config('config.json')

def calculate(score_list: list):
    if score_list.count(6) == len(score_list):
        return config.scoring['all-six']
    
    elif score_list.count(score_list[0]) == len(score_list):
        return config.scoring['all-of-kind']
    
    elif sorted(score_list) == list(range(min(score_list), max(score_list)+1)):
        return config.scoring['straight']
    
    elif score_list.count(score_list[0]) == len(score_list)-1 or score_list.count(score_list[1]) == len(score_list)-1:
        return config.scoring['full-house']
    
    else:
        return 0

