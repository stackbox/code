# test_tasklistdb.py 
#
# (c) 2010 Michel J. Anders (varkenvarken)
#
# all rights reserved
#
# test_tasklistdb.py performs a series of unit tests on tasklistdb.py

from tasklistdb import TaskDB, Task, AuthenticationError, DatabaseError
import unittest
from os import unlink,close
from tempfile import mkstemp

(fileno,database) = mkstemp()
close(fileno)

class BaseTest(unittest.TestCase):
	
	def setUp(self):
		try:
			unlink(database)
		except:
			pass
		self.t=TaskDB(database)
		self.t.connect()

	def tearDown(self):
		self.t.close()
		try:
			unlink(database)
		except:
			pass
		
	def test_connect(self):
		pass # just exercises setUp/tearDown
				
class DBTest(unittest.TestCase):
	
	def setUp(self):
		try:
			unlink(database)
		except:
			pass
		self.t=TaskDB(database)
		self.t.connect()

	def tearDown(self):
		self.t.close()
		try:
			unlink(database)
		except:
			pass
		
	def test_create(self):
		description='testtask'
		self.task = self.t.create(user='testuser',description=description)
		self.assertIsNot(self.task.id,None)
		self.assertEqual(self.task.description,description)

class DBentityTest(unittest.TestCase):
	
	def setUp(self):
		try:
			unlink(database)
		except:
			pass
		self.t=TaskDB(database)
		self.t.connect()
		self.description='testtask'
		self.task = self.t.create(user='testuser',description=self.description)
		
	def tearDown(self):
		self.t.close()
		try:
			unlink(database)
		except:
			pass
		
	def test_retrieve(self):
		task = self.t.retrieve('testuser',self.task.id)
		self.assertEqual(task.id,self.task.id)
		self.assertEqual(task.description,self.task.description)
		self.assertEqual(task.user,self.task.user)

	def test_list(self):
		ids = self.t.list('testuser')
		self.assertListEqual(ids,[self.task.id])

	def test_update(self):
		newdescription='updated description'
		self.task.description=newdescription
		self.task.update('testuser')
		task = self.t.retrieve('testuser',self.task.id)
		self.assertEqual(task.id,self.task.id)
		self.assertEqual(task.duedate,self.task.duedate)
		self.assertEqual(task.completed,self.task.completed)
		self.assertEqual(task.description,newdescription)

	def test_delete(self):
		task = self.t.create('testuser',description='second task')
		ids = self.t.list('testuser')
		self.assertListEqual(sorted(ids),sorted([self.task.id,task.id]))
		task.delete('testuser')
		ids = self.t.list('testuser')
		self.assertListEqual(sorted(ids),sorted([self.task.id]))
		with self.assertRaises(DatabaseError):
			task = self.t.create('testuser',id='short')
			task.delete('testuser')
		
if __name__ == '__main__':
	unittest.main(exit=False)
