import sqlite3 as sqlite
import threading

class Entity:
	
	threadlocal = threading.local()
	
	def __init__(self,id=None,**kw):
		for k in kw:
			if not k in self.__class__.columns :
				raise KeyError("unknown column")
		cursor=self.threadlocal.connection.cursor()
		if id:
			if len(kw):
				raise KeyError("columns specified on retrieval")
			sql="select * from %s where %s_id = ?"%(self.__class__.__name__,self.__class__.__name__)
			#print(sql)
			cursor.execute(sql,(id,))
			entities=cursor.fetchall()
			if len(entities)!=1 : raise ValueError("not a unique entity/unknown entity")
			self.id=id
			for k in self.__class__.columns:
				setattr(self,k,entities[0][k])
		else:
			cols=[]
			vals=[]
			for c,v in kw.items():
				cols.append(c)
				vals.append(v)
				setattr(self,c,v)
			cols=",".join(cols)
			nvals=",".join(["?"]*len(vals))
			sql="insert into %s (%s) values(%s)"%(self.__class__.__name__,cols,nvals)
			print(sql)
			print([type(v) for v in vals])
			try:
				with self.threadlocal.connection as conn:
					cursor=conn.cursor()
					cursor.execute(sql,vals)
					self.id=cursor.lastrowid
			except sqlite.IntegrityError:
				raise ValueError("duplicate value for unique column")
				
	def update(self,**kw):
		for k in kw:
			if not k in self.__class__.columns :
				raise KeyError("unknown column")
		for k,v in kw.items():
			setattr(self,k,v)
		updates=[]
		values=[]
		for k in self.columns:
			updates.append("%s=?"%k)
			values.append(getattr(self,k))
		updates=",".join(updates)
		values.append(self.id)
		sql="update %s set %s where %s_id = ?"%(self.__class__.__name__, updates, self.__class__.__name__)
		with self.threadlocal.connection as conn:
			cursor=conn.cursor()
			cursor.execute(sql, values)
			if cursor.rowcount != 1 :
				raise ValueError("number of updated entities not 1 (%d)"%cursor.rowcount)

	def delete(self):
		sql="delete from %s where %s_id = ?"%(self.__class__.__name__,self.__class__.__name__)
		with self.threadlocal.connection as conn:
			cursor=conn.cursor()
			cursor.execute(sql,(self.id,))
			if cursor.rowcount != 1 :
				raise ValueError("number of deleted entities not 1 (%d)"%cursor.rowcount)
	@classmethod
	def list(cls,**kw):
		sql="select %s_id from %s"%(cls.__name__,cls.__name__)
		cursor=cls.threadlocal.connection.cursor()
		if len(kw):
			cols=[]
			values=[]
			for k,v in kw.items():
				cols.append(k)
				values.append(v)
			whereclause = " where "+",".join(c+"=?" for c in cols)
			sql += whereclause
			cursor.execute(sql,values)
		else:
			cursor.execute(sql)
		for row in cursor.fetchall():
			yield row[0]
			
	@classmethod
	def inittable(cls,**kw):
		# not neccessary to run this for every thread, once is enough
		cls.columns=kw
		connection=cls.threadlocal.connection
		coldefs=",".join(k+' '+v for k,v in kw.items())
		sql="create table if not exists %s (%s_id integer primary key autoincrement, %s);"%(cls.__name__,cls.__name__,coldefs)
		connection.execute(sql)
		connection.commit()

	@classmethod
	def getcolumnvalues(cls,column):
		if not column in cls.columns : raise KeyError('unknown column '+column)
		sql="select %s from %s order by lower(%s)"%(column,cls.__name__,column)
		cursor=cls.threadlocal.connection.cursor()
		cursor.execute(sql)
		return [r[0] for r in cursor.fetchall()]
		
	@classmethod
	def threadinit(cls,db):
		if not hasattr(cls.threadlocal,'connection') or cls.threadlocal.connection is None:
			cls.threadlocal.connection=sqlite.connect(db)
			cls.threadlocal.connection.row_factory = sqlite.Row
			cls.threadlocal.connection.execute("pragma foreign_keys=1")
		else:
			pass #print('threadinit thread has a connection object already')
	
	@classmethod
	def threadexit(cls):
		if hasattr(cls.threadlocal,'connection') and not cls.threadlocal.connection is None:
			cls.threadlocal.connection.close()
		cls.threadlocal.connection=None
		
if __name__ == "__main__" :
	
	import unittest
	import threading
	import os
	
	def dump(c): print("\n".join(c.iterdump()))
		
	class Test(Entity): pass
	class Test2(Entity): pass

	class EntityTest(unittest.TestCase):
		def setUp(self):
			Entity.threadinit(':memory:')
			Test.inittable(a="",b="unique")
			
		def tearDown(self):
			Entity.threadexit()
		
		def test_create(self):
			# test creating a new entity
			t1 = Test(a=1,b=2)
			self.assertEqual(1,t1.a)
			self.assertEqual(2,t1.b)
			# retrieve existing entity from database (the one just created) 
			t2 = Test(id=t1.id)
			self.assertEqual(t1.id,t2.id)
			self.assertEqual(t1.a,t2.a)
			self.assertEqual(t1.b,t2.b)
			
			# create, retrieve but with different types of values
			t1 = Test(a="one",b=None)
			self.assertEqual("one",t1.a)
			self.assertEqual(None,t1.b)
			t2 = Test(id=t1.id)
			self.assertEqual(t1.id,t2.id)
			self.assertEqual(t1.a,t2.a)
			self.assertEqual(t1.b,t2.b)
			
			# check if unique constraint is enforced
			with self.assertRaises(ValueError):
				t1 = Test(a=1,b=2)
		
		def test_list(self):
			# test listing all entities
			l1 = [Test(a=n,b=n) for n in range(5)]
			l2 = [Test(id=n) for n in Test.list()]
			self.assertItemsEqual([t.id for t in l1],[t.id for t in l2])
		
			# test listing entities matching an selection
			l2 = [Test(id=n) for n in Test.list(a=3)]
			self.assertEqual(1,len(l2))
			for t in l2:
				self.assertEqual(t.a,3)
		
		def test_delete(self):
			# test deletion of an existing item
			l1 = [Test(a=n,b=n) for n in range(5)]
			id=l1[2].id
			l1[2].delete()
			del l1[2]
			l2 = [Test(id=n) for n in Test.list()]
			self.assertItemsEqual([t.id for t in l1],[t.id for t in l2])
			
			# test deletion of a non existing item
			with self.assertRaises(ValueError):
				l1[0].delete()
				l1[0].delete()
		
		def test_update(self):
			# test update by passing values to update()
			t1 = Test(a=1,b=2)
			t1.update(a=3)
			t2 = Test(id=t1.id)
			self.assertEqual(t2.a,3)
			self.assertEqual(t2.b,2)
			self.assertEqual(t2.a,t1.a)
			self.assertEqual(t2.b,t1.b)
			
			# test update by calling update() after altering attributes
			t1 = Test(a=5,b=6)
			t1.b=7
			t1.update()
			t2 = Test(id=t1.id)
			self.assertEqual(t2.a,5)
			self.assertEqual(t2.b,7)
			self.assertEqual(t2.a,t1.a)
			self.assertEqual(t2.b,t1.b)
			
			# test update on non existing entity
			t1 = Test(a=100,b=200)
			t1.delete()
			with self.assertRaises(ValueError):
				t1.update()
			
			#dump(self.connection)
	
		def test_threadlocal(self):
			# test that threadlocal storage is shared by all entity derived classes
			self.assertEqual(Test.threadlocal,Test2.threadlocal)
	
	class ThreadedEntityTest(unittest.TestCase):
		def test_threads(self):
			db='/tmp/threadedentitytest.db'
			try:
				os.unlink(db)
			except:
				pass

			def run():
				Entity.threadinit(db)
				l=[Test(id=id) for id in Test.list()]
				self.assertEqual(1,len(l))
				self.assertEqual(l[0].a,100)
				self.assertEqual(l[0].b,200)
				Entity.threadexit()
				
			threads = [threading.Thread(target=run) for i in range(5)]

			Entity.threadinit(db)  # :memory: not valid in multithreaded environment
			Test.inittable(a="",b="unique")
			
			t1=Test(a=100,b=200)	# executed in main thread
			for t in threads:
				t.start()
			for t in threads:
				t.join()
			
			Entity.threadexit()
			os.unlink(db)
	
	unittest.main()
