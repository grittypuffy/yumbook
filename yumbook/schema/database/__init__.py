import sqlite3
conn = sqlite3.connect("pancakes.db")
cur = conn.execute("select * from recipe")
for i in cur.fetchall():
    for j in i:
        print(j)
conn.close()
