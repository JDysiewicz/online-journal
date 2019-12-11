import sqlite3

conn = sqlite3.connect("submissions.db")

db = conn.cursor()

db.execute("""DELETE FROM entries""")

conn.commit()
conn.close