import sqlite3
from config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS namu_hot_posts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        url TEXT,
        date DATE
        new_title TEXT,
        status TEXT
        video_id TEXT
    )
    """)
    conn.commit()
    conn.close()

create_tables()