import logon
import sqlite3
from hashlib import sha1 as hash
import threading
import cherrypy

class LogonDB(logon.Logon):
	def __init__(self,path="/logon",authenticated="/",not_authenticated="/",db="/tmp/pwd.db"):
		super().__init__(path,authenticated,not_authenticated)
		self.db=db
		self.initdb()
		
	@staticmethod
	def _dohash(s):
		h = hash()
		h.update(s.encode())
		return h.hexdigest()
	
	def checkpass(self,username,password):
		password = LogonDB._dohash(password)
		c = self.data.conn.cursor()
		c.execute("SELECT count(*) FROM pwdb WHERE username = ? AND password = ?",(username,password))
		if c.fetchone()[0]==1 :return True
		return False

	def initdb(self):
		conn=sqlite3.connect(self.db)
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS pwdb(username unique not null,password not null);")
		c.execute('INSERT OR IGNORE INTO pwdb VALUES("admin",?)',(LogonDB._dohash("admin"),))
		c.execute('INSERT OR IGNORE INTO pwdb VALUES("eve",?)',(LogonDB._dohash("eve"),))
		c.execute('INSERT OR IGNORE INTO pwdb VALUES("john",?)',(LogonDB._dohash("john"),))
		c.execute('INSERT OR IGNORE INTO pwdb VALUES("mike",?)',(LogonDB._dohash("mike"),))
		conn.commit()
		conn.close()
		self.data=threading.local()
		
	def connect(self):
		'''call once for every thread as sqlite connection objects cannot be shared among threads.'''
		self.data.conn = sqlite3.connect(self.db)
		
	def close(self):
		'''call once for every thread.'''
		self.data.conn.close()
	
	@cherrypy.expose
	def adduserform(self):
		if self.checkauth(returntopage=True) != 'admin':
			raise cherrypy.HTTPError("403 Forbidden", "Only admin allowed to access this resource.")

		return logon.Logon.base_page % '''
		<form action="./adduser" method="GET"><fieldset>
		<label for="username">New username</label><input id="username" name="username" type="text" />
		<label for="password">New password</label><input id="password" name="password" type="password" />
		<button type="submit" class="add-button" value="Add">Add</button>>
		</fieldset></form>
		'''

	@cherrypy.expose
	def adduser(self,username,password):
		if self.checkauth(returntopage=True) != 'admin':
			raise cherrypy.HTTPError("403 Forbidden", "Only admin allowed to access this resource.")

		password = LogonDB._dohash(password)
		try:
			c = self.data.conn.cursor()
			c.execute("INSERT INTO pwdb (username,password) VALUES (?,?)",(username,password))
			self.data.conn.commit()
		except sqlite3.IntegrityError:
			raise cherrypy.HTTPError("403 Forbidden","username %s already exists"%username)
		return '''<html>
		<head>
		<meta http-equiv="refresh" content="5; url=/">
		</head>
		<body><h1>%s successfully added.</h1></body>
		</html>
		''' % username

if __name__ == "__main__":
	import unittest
	import os
	
	class LogonDBTest(unittest.TestCase):
	
		def setUp(self):
			self.logon = LogonDB(db='/tmp/pwd.db')
			self.logon.connect()

		def tearDown(self):
			self.logon.close()
			os.unlink('/tmp/pwd.db')

		def test_checkpass(self):
			self.assertTrue(self.logon.checkpass('admin','admin'))
			self.assertFalse(self.logon.checkpass('admin','qadmin'))
			self.assertFalse(self.logon.checkpass('nadmin','admin'))
	
	class ThreadLogonDBTest(unittest.TestCase):

		def tearDown(self):
			os.unlink('/tmp/pwd.db')

		def run_check(self):
			logon=LogonDB(db='/tmp/pwd.db')
			logon.connect()
			self.assertTrue(logon.checkpass('admin','admin'))
			self.assertFalse(logon.checkpass('admin','qadmin'))
			self.assertFalse(logon.checkpass('nadmin','admin'))
			logon.close()
	
		def test_threads(self):
			n=2
			threads=[]
			for t in range(n):
				thread=threading.Thread(target=self.run_check)
				threads.append(thread)
			for thread in threads:
				thread.start()
			for thread in threads:
				thread.join(timeout=5.0)
				
	unittest.main(exit=False)
	