import sqlite3
from pathlib import Path
from flask import g

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / 'censoescolar.db'

def get_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()