import sqlite3

conn=sqlite3.connect("data.sqlite")
c=conn.cursor()
conn.commit()
c.execute('DELETE FROM people WHERE ID >= 0')
conn.commit()