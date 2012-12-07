# tasklistdb.py 
#
# (c) 2010 Michel J. Anders (varkenvarken)
#
# all rights reserved
#
# tasklistdb.py implements the low level database interactions of the tasklist II app
# and provides a Task class 

import sqlite3
import threading
from datetime import date

debug = lambda *args,**kw: None
#debug = print

class Task:
	
	def __init__(self,taskdb,user,id=None,description='',duedate=None,completed=None):
		self.taskdb=taskdb
		self.user=user
		self.id=id
		self.description=description
		self.completed=completed
		self.duedate=duedate if duedate != None else date.today().isoformat()
		if id == None:
			cursor = self.taskdb.conn.cursor()
			sql = '''insert into task (description,duedate,completed,user_id) values(?,?,?,?)'''
			cursor.execute(sql,(self.description,self.duedate,self.completed,self.user))
			self.id = cursor.lastrowid
			self.taskdb.conn.commit()

	def update(self,user):
		params= []
		params.append('description = ?')
		params.append('duedate = ?')
		params.append('completed = ?')
		sql = '''update task set %s where task_id = ? and user_id = ?'''
		sql = sql%(",".join(params))
		conn = self.taskdb.conn
		cursor = conn.cursor()
		cursor.execute(sql,(self.description,self.duedate,self.completed,self.id,user))
		if cursor.rowcount != 1 :
			debug('updated',cursor.rowcount)
			debug(sql)
			conn.rollback()
			raise DatabaseError('update failed')
		conn.commit()
		
	def delete(self,user):
		sql = '''delete from task where task_id = ? and user_id = ?'''
		conn = self.taskdb.conn
		cursor = conn.cursor()
		cursor.execute(sql,(self.id,user))
		if cursor.rowcount != 1:
			conn.rollback()
			raise DatabaseError('no such task')
		conn.commit()
			
class DatabaseError(Exception): pass
class AuthenticationError(Exception): pass

class TaskDB:

	def __init__(self,db):
		self.data = threading.local()
		self.db = db
		self._initdb()
		
	def connect(self):
		'''call once for every thread'''
		self.data.conn = sqlite3.connect(self.db)
		self.data.conn.row_factory = sqlite3.Row
	
	def _initdb(self):
		'''call once to initialize the metabase tables'''
		conn = sqlite3.connect(self.db)
		#conn.cursor().execute('pragma foreign_keys = 1')
		#conn.commit()

		conn.cursor().executescript('''
		create table if not exists task (
			task_id integer primary key autoincrement,
			description,
			duedate,
			completed,
			user_id
		);
		'''
		)
		conn.commit()
		conn.close()
		
	def close(self):
		self.data.conn.close()

	def create(self,user=None,id=None,description='',duedate=None,completed=None):
		return Task(self.data,user=user,id=id,description=description,duedate=duedate,completed=completed)
		
	def retrieve(self,user,id):
		sql = """select * from task where task_id = ? and user_id = ?"""
		cursor = self.data.conn.cursor()
		cursor.execute(sql,(id,user))
		tasks = cursor.fetchall()
		if len(tasks):
			return self.create(user,tasks[0]['task_id'],tasks[0]['description'],tasks[0]['duedate'],tasks[0]['completed'])
		raise KeyError('no such task')
		
	def list(self,user):
		sql = '''select task_id from task where user_id = ?'''
		cursor = self.data.conn.cursor()
		cursor.execute(sql,(user,))
		return [row[0] for row in cursor.fetchall()]

if __name__ == "__main__":
	print('ok');
	
