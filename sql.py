import sqlite3

conn = sqlite3.connect("cs50 project//submissions.db")

db = conn.cursor()

db.execute("""CREATE TABLE entries(
                id INTEGER,
                entry TEXT,
                date TEXT,
                time TEXT,
                postid INTEGER PRIMARY KEY AUTOINCREMENT 
                )""")

conn.commit()
conn.close