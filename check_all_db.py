import sqlite3

conn = sqlite3.connect("news.db")
cursor = conn.cursor()
cursor.execute("SELECT category, source, title, link, summary FROM articles")
rows = cursor.fetchall()
conn.close()

print(str(len(rows)) + " articles in database")