# setup/initialize_database.py
import sqlite3
import os
import sys

# Add the utils directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.config import SQLITE_DATABASE_PATH

def initialize_database():
    """
    Initialize the SQLite database.

    This function checks if the directory for the SQLite database exists and creates it if necessary. 
    It then initializes the database with a table named 'screenshots' containing all required columns 
    for storing information about screenshots and their respective metadata.
    """
    # Get the directory path from the database file path
    db_dir = os.path.dirname(SQLITE_DATABASE_PATH)

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    try:
        # Use a context manager to handle the database connection
        with sqlite3.connect(SQLITE_DATABASE_PATH) as conn:
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
                orig_shape_height INTEGER,
                orig_shape_width INTEGER,
                frame_count INTEGER,
                frames_since_last_screenshot INTEGER,
                resized_screenshot_path TEXT,
                resized_x1 REAL,
                resized_y1 REAL,
                resized_x2 REAL,
                resized_y2 REAL,
                resized_shape_height INTEGER,
                resized_shape_width INTEGER,
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
        print("Database created successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

if __name__ == '__main__':
    initialize_database()
