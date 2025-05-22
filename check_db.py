import sqlite3
conn = sqlite3.connect("applicants.db")
print(conn.execute("SELECT * FROM applicants").fetchall())
conn.close()