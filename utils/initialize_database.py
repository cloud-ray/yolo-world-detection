# utils/initialize_database.py
import sqlite3
import os
from config import SQLITE_DATABASE_PATH

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
        x1 REAL,
        y1 REAL,
        x2 REAL,
        y2 REAL,
        orig_shape TEXT,
        frame_count INTEGER,
        frames_since_last_screenshot INTEGER,
        resized_screenshot_path TEXT,
        resized_x1 REAL,
        resized_y1 REAL,
        resized_x2 REAL,
        resized_y2 REAL,
        resized_shape TEXT,
        orig_x_center REAL,
        orig_y_center REAL,
        orig_width REAL,
        orig_height REAL,
        resized_x_center REAL,
        resized_y_center REAL,
        resized_width REAL,
        resized_height REAL
    );
    """)

    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == '__main__':
    initialize_database()
