import sqlite3
from flask import g
from config import DATABASE_FILE

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        first_name TEXT,
        last_name TEXT,
        profile_picture TEXT,
        has_profile_picture INTEGER DEFAULT 0
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS BannerImages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image TEXT NOT NULL,  -- You can use TEXT for file or URL
        status INTEGER DEFAULT 1  -- 1 for active, 0 for inactive
    )''')
    conn.commit()
