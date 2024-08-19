def calculate(score_list: list):
    if score_list.count(6) == len(score_list):
        return 100
    
    elif score_list.count(score_list[0]) == len(score_list):
        return 70
    
    elif sorted(score_list) == list(range(min(score_list), max(score_list)+1)):
        return 50
    
    elif score_list.count(score_list[0]) == len(score_list)-1 or score_list.count(score_list[1]) == len(score_list)-1:
        return 50
    
    else:
        return 0

