import sqlite3

con = sqlite3.connect("database.db")

cur = con.cursor()

cur.execute("SELECT * FROM users")

rows = cur.fetchall()

# cur.execute("delete from users")

# con.commit()


print(len(rows))
for row in rows:
    print(row)
