import sqlite3

con = sqlite3.connect("database.db")

cur = con.cursor()

cur.execute("SELECT * FROM users WHERE email=? AND password=?", ("v@gmail.com","visheee"))

rows = cur.fetchall()


print(len(rows))
for row in rows:
    print(row)