import sqlite3
def display_data(db):
    conn = sqlite3.connect(db)
    cur = conn.execute("select * from recipe")
    for i in cur.fetchall():
        for j in i:
            print(j)
    conn.close()
