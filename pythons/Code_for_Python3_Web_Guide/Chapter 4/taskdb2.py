# taskdb1.py 
#
# (c) 2010 Michel J. Anders (varkenvarken)
#
# all rights reserved
#
# an sample program to illustrate working with the databases needed for tasklist II 

import sqlite3

database=':memory:'

connection = sqlite3.connect(database)
connection.row_factory = sqlite3.Row

cursor=connection.executescript('''
create table if not exists task (
	task_id integer primary key autoincrement,
	description,
	duedate,
	completed,
	user_id
);
''')
connection.commit()

sql = '''insert into task (description,duedate,completed,user_id) values(?,?,?,?)'''
cursor.execute(sql,('work'          ,'2010-01-01',None,'alice'))
cursor.execute(sql,('more work'     ,'2010-02-01',None,'alice'))
cursor.execute(sql,('work'          ,'2010-03-01',None,'john'))
cursor.execute(sql,('even more work','2010-04-01',None,'john'))

connection.commit()

sql = """select * from task where user_id = 'john'"""
cursor.execute(sql)
tasks = cursor.fetchall()
for t in tasks:
	print(t['duedate'],t['description'])

connection.close()
