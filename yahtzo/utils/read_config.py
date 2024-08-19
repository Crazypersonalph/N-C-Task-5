import json

def read_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            num_dice = int(config['num_dice'])
            db_name = str(config['db_name'])
    except:
        config = None
        num_dice = 3
        db_name = 'yahtzo.db'
    return config, num_dice, db_name