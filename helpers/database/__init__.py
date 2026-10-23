import sqlite3
from pathlib import Path
from flask import g
from helpers.application import app

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE = BASE_DIR / 'censoescolar.db'

def get_connexao():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)  
    return conn
 
@app.teardown_appcontext
def close_db(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()
