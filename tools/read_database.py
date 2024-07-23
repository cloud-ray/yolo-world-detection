# tools/read_database.py
import sqlite3
import os
import sys

# Add the utils directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../utils'))

from config import SQLITE_DATABASE_PATH

def print_last_two_rows(db_path):
    """
    Print the last two rows from the 'screenshots' table.

    Args:
        db_path (str): The path to the SQLite database file.

    This function connects to the database specified by db_path and retrieves the last
    two entries from the 'screenshots' table, printing them to the console.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM screenshots ORDER BY id DESC LIMIT 2")
            rows = cursor.fetchall()

            for row in rows:
                print(row)
    except sqlite3.Error as e:
        print(f"An error occurred while fetching rows: {e}")

# def print_schema(db_path):
#     """
#     Print the schema of all tables in the database.

#     Args:
#         db_path (str): The path to the SQLite database file.

#     This function connects to the database specified by db_path and retrieves the schema
#     information for all tables, printing each table's name and its columns with their types.
#     """
#     try:
#         with sqlite3.connect(db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
#             tables = cursor.fetchall()

#             for table in tables:
#                 table_name = table[0].split('(')[0].split()[-1]
#                 print(f"Table: {table_name}")
#                 cursor.execute(f"PRAGMA table_info({table_name})")
#                 columns = cursor.fetchall()
#                 for column in columns:
#                     print(f"  {column[1]} {column[2]}")
#     except sqlite3.Error as e:
#         print(f"An error occurred while fetching the schema: {e}")

# Usage
print_last_two_rows(SQLITE_DATABASE_PATH)
# print_schema(SQLITE_DATABASE_PATH)
