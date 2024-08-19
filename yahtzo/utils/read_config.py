import json

def read_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            num_dice = int(config['num_dice'])
    except:
        config = None
        num_dice = 3
    return config, num_dice