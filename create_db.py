import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE events(
id INTEGER PRIMARY KEY AUTOINCREMENT,
event_name TEXT,
event_date TEXT,
event_description TEXT
)
""")

cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
branch TEXT
)
""")

cursor.execute("""
CREATE TABLE registrations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
event_id INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")