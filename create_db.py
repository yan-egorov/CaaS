import sqlite3

db_conn = sqlite3.connect('sins.db')

c = db_conn.cursor()
c.execute('''DROP TABLE sins''')
c.execute('''CREATE TABLE sins
             (sin_id integer, sin_name text, sin_action text, sin_fee integer)''')
c.execute("INSERT INTO sins VALUES ('1','чревоугодие','Обожрался',100), ('2','блуд','Распустился',100)")
db_conn.close()