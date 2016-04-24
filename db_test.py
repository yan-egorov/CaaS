import sqlite3

db_conn = sqlite3.connect('sins.db')
print("1")
c = db_conn.cursor()
print("2")
for row in c.execute('SELECT sin_action FROM sins ORDER BY sin_id'):
    print(row)
print("3")
db_conn.close()
