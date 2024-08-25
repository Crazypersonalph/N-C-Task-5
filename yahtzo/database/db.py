import sqlite3
import datetime
con: sqlite3.Connection

def grab_db(database: str): # Define a function to grab the database, else create it.
    global con
    con = sqlite3.connect(database)
    cur = con.cursor()
    if not check_if_table_exists(cur, 'history'):
        cur.execute('CREATE TABLE history (id INTEGER PRIMARY KEY, score INTEGER, date TEXT, rolls TEXT, holds TEXT, current_config TEXT)')

    return cur

def check_if_table_exists(cur: sqlite3.Cursor, table_name: str): # Define a function to check if a table exists
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cur.fetchone():
        return True
    return False

def store_game(cur: sqlite3.Cursor, score: int, rolls: list, holds: list, current_config: str): # Define a function to store the game in the database
    cur.execute(f"""
    INSERT INTO history (score, date, rolls, holds, current_config) VALUES
        (?, ?, ?, ?, ?)
""", (score, datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(), str(rolls), str(holds), current_config))

def get_last_result(cur: sqlite3.Cursor): # Define a function to get the last result from the database
    cur.execute('SELECT * FROM history ORDER BY id DESC LIMIT 1')
    return cur.fetchone()

def clean(): # Define a function to clean up the database connection
    con.commit()
    con.close()