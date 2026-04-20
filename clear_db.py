import sqlite3

conn = sqlite3.connect("news.db")
conn.execute("DELETE FROM articles")
conn.commit()
conn.close()
print("Database cleared")