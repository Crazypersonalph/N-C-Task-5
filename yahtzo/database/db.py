import sqlite3
import datetime
con = any

def grab_db(database: str):
    global con
    con = sqlite3.connect(database)
    cur = con.cursor()
    if not check_if_table_exists(cur, 'history'):
        cur.execute('CREATE TABLE history (id INTEGER PRIMARY KEY, score INTEGER, date TEXT, rolls TEXT, holds TEXT)')

    return cur

def check_if_table_exists(cur: sqlite3.Cursor, table_name: str):
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cur.fetchone():
        return True
    return False

def store_game(cur: sqlite3.Cursor, score: int, rolls: list, holds: list):
    cur.execute(f"""
    INSERT INTO history (score, date, rolls, holds) VALUES
        (?, ?, ?, ?)
""", (score, datetime.datetime.now(datetime.timezone.utc).isoformat(), str(rolls), str(holds)))
    clean()
    
def clean():
    con.commit()
    con.close()