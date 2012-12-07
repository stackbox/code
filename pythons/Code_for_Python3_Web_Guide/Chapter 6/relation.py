import sqlite3 as sqlite
import threading
from entity import Entity
	
class Relation:

	threadlocal = threading.local()
	
	def __init__(self,a_id,b_id,stub=False):
		self.a_id=a_id
		self.b_id=b_id
		if stub : return
		cols=self.columns[0]+"_id,"+self.columns[1]+"_id"
		sql='insert or replace into %s (%s) values(?,?)'%(self.__class__.__name__,cols)
		#print(sql)
		with self.threadlocal.connection as conn:
			cursor=conn.cursor()
			#print("\n".join(conn.iterdump()))
			cursor.execute(sql,(a_id,b_id))
			if cursor.rowcount!=1: raise ValueError()
			
	@classmethod
	def add(cls,instance_a,instance_b):
		#print("add",cls.__name__,instance_a,instance_b)
		if instance_a.__class__.__name__ != cls.columns[0] : raise ValueError("instance a, wrong class")
		if instance_b.__class__.__name__ != cls.columns[1] : raise ValueError("instance b, wrong class")
		return cls(instance_a.id,instance_b.id)
	
	def delete(self):
		sql='delete from %s where %s_id = ? and %s_id = ?'%(self.__class__.__name__,self.columns[0],self.columns[1])
		#print(sql,self.a_id,self.b_id)
		with self.threadlocal.connection as conn:
			#print("\n".join(conn.iterdump()))
			cursor=conn.cursor()
			cursor.execute(sql,(self.a_id,self.b_id))
			if cursor.rowcount!=1: raise ValueError()
		
	@classmethod
	def list(cls,instance):
		sql='select %s_id,%s_id from %s where %s_id = ?'%(cls.columns[0],cls.columns[1],cls.__name__,instance.__class__.__name__)
		#print(sql,instance.id)
		#print("\n".join(cls.threadlocal.connection.iterdump()))
		with cls.threadlocal.connection as conn:
			cursor=conn.cursor()
			cursor.execute(sql,(instance.id,))
			return [cls(r[0],r[1],stub=True) for r in cursor.fetchall()]

	@classmethod
	def inittable(cls,entity_a, entity_b, reltype="N:N", cascade=None):
		sql='''create table if not exists %(table)s (
			%(a)s_id references %(a)s on delete cascade,
			%(b)s_id references %(b)s on delete cascade,
			unique(%(a)s_id,%(b)s_id)
		);
		'''%{'table':cls.__name__,'a':entity_a.__name__,'b':entity_b.__name__}
		#print(sql)
		with cls.threadlocal.connection as conn:
			cursor=conn.cursor()
			cursor.execute(sql)
		cls.columns=[entity_a.__name__,entity_b.__name__]
	
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
	
	def __eq__(self,other):
		return self.a_id == other.a_id and self.b_id == other.b_id
	
	def __str__(self): return "<%s:%s>"%(self.a_id,self.b_id)
	
if __name__ == "__main__":
	import unittest
	import os
	
	class A(Entity): pass
	class B(Entity): pass
	
	class ABRelation(Relation): pass
			
	class TestRelation(unittest.TestCase):
		def setUp(self):
			self.db='/tmp/relationtest.db'  # :memory: not thread safe and no mulitple conns possible at all
			try:
				os.unlink(self.db)
			except:
				pass
			A.threadinit(self.db)
			A.inittable(a="",b="")
			B.threadinit(self.db)
			B.inittable(a="",b="")
			ABRelation.threadinit(self.db)
			ABRelation.inittable(A,B)
			self.a1=A(a=1,b=1)
			self.a2=A(a=2,b=2)
			self.b1=B(a=3,b=3)
			self.b2=B(a=4,b=4)
			self.b3=B(a=5,b=5)
			self.b4=B(a=6,b=6)
			ABRelation.add(self.a1,self.b1)
		
		def tearDown(self):
			A.threadexit()
			B.threadexit()
			ABRelation.threadexit()
			os.unlink(self.db)
			
		def test_create(self):
			ABRelation.threadinit(':memory:')
			ABRelation.inittable(A,B)
			r11=ABRelation.add(self.a1,self.b1)
			r12=ABRelation.add(self.a1,self.b2)
			r23=ABRelation.add(self.a2,self.b3)
			blist1=ABRelation.list(self.a1)
			blist2=ABRelation.list(self.a2)
			alist1=ABRelation.list(self.b1)
			alist2=ABRelation.list(self.b2)
			self.assertListEqual([r11,r12],blist1)
			self.assertListEqual([r23],blist2)
			self.assertListEqual([r11],alist1)
			self.assertListEqual([r12],alist2)
			ABRelation.threadexit()
		
		def test_delete(self):
			ABRelation.threadinit(':memory:')
			ABRelation.inittable(A,B)
			ABRelation.add(self.a1,self.b1)
			ABRelation.add(self.a1,self.b2)
			ABRelation.add(self.a2,self.b3)
			ABRelation.add(self.a2,self.b4)
			blist=ABRelation.list(self.a1)
			# remove relation, nothing should change for a and b entities
			blist[0].delete()
			self.assertItemsEqual([self.a1.id,self.a2.id],A.list())
			self.assertItemsEqual([self.b1.id,self.b2.id,self.b3.id,self.b4.id],B.list())
			# remove b 
			self.b3.delete()
			blist=ABRelation.list(self.a2)
			self.assertListEqual([self.b4.id],[ab.b_id for ab in blist])
			self.assertItemsEqual([self.b1.id,self.b2.id,self.b4.id],B.list())
			
			ABRelation.threadexit()

		def test_delete_cascade(self):
			ABRelation.threadinit(':memory:')
			ABRelation.inittable(A,B,cascade=B)
			r11=ABRelation.add(self.a1,self.b1)
			r12=ABRelation.add(self.a1,self.b2)
			r22=ABRelation.add(self.a2,self.b2)
			r23=ABRelation.add(self.a2,self.b3)
			blist=ABRelation.list(self.a1)
			# remove relation, nothing should change for a and b entities
			r12.delete()
			self.assertItemsEqual([self.a1.id,self.a2.id],A.list())
			self.assertItemsEqual([self.b1.id,self.b2.id,self.b3.id,self.b4.id],B.list())
			# remove relation, nothing should change for a and b entities
			r11.delete()
			self.assertItemsEqual([self.a1.id,self.a2.id],A.list())
			self.assertItemsEqual([self.b1.id,self.b2.id,self.b3.id,self.b4.id],B.list())
			
			ABRelation.threadexit()

	unittest.main()
	