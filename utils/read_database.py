import sqlite3
from config import SQLITE_DATABASE_PATH

def print_last_two_rows(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM screenshots ORDER BY id DESC LIMIT 2")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

# Usage
print_last_two_rows(SQLITE_DATABASE_PATH)



# def print_schema(db_path):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
#     tables = cursor.fetchall()

#     for table in tables:
#         print(f"Table: {table[0].split('(')[0].split()[-1]}")
#         cursor.execute(f"PRAGMA table_info({table[0].split('(')[0].split()[-1]})")
#         columns = cursor.fetchall()
#         for column in columns:
#             print(f"  {column[1]} {column[2]}")

#     conn.close()

# # Usage
# print_schema(SQLITE_DATABASE_PATH)