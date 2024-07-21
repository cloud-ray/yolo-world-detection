import sqlite3
import os
from utils.config import SQLITE_DATABASE_PATH

def initialize_database():
    # Get the directory path from the database file path
    db_dir = os.path.dirname(SQLITE_DATABASE_PATH)

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(SQLITE_DATABASE_PATH)
    cursor = conn.cursor()

    # Create the screenshots table with all required columns
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS screenshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT,
        class_id INTEGER,
        confidence REAL,
        obj_id INTEGER,
        timestamp INTEGER,
        screenshot_path TEXT,
        x1 INTEGER,
        y1 INTEGER,
        x2 INTEGER,
        y2 INTEGER,
        orig_shape TEXT,
        frame_count INTEGER,
        frames_since_last_screenshot INTEGER,
        resized_screenshot_path TEXT,
        resized_x1 INTEGER,
        resized_y1 INTEGER,
        resized_x2 INTEGER,
        resized_y2 INTEGER,
        resized_shape TEXT
    );
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()