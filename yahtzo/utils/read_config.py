import json

class Config:
    def __init__(self, num_dice: int, db_name: str, scoring: dict, config):
        self.config = config
        self.num_dice = num_dice
        self.db_name = db_name
        self.scoring = scoring

def read_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            return Config(int(config['num_dice']), str(config['db_name']), config['scoring'], config)
    except:
        config = None
        num_dice = 3
        db_name = 'yahtzo.db'
        scoring = {'all-six': 100, 'all-of-kind': 70, 'straight': 50, 'full-house': 50}
        with open(config_file, 'w') as f:
            json.dump({'num_dice': num_dice, 'db_name': db_name, 'scoring': scoring}, f, indent=4)
        return Config(num_dice, db_name, scoring, None)