from tempfile import mkstemp
from os import unlink,close
import unittest
from sqlite3 import IntegrityError

from rbacentity import Attribute,Picklist,AbstractEntity,AbstractRelation

class TestPicklist(unittest.TestCase):

	def test_create(self):
		p = Picklist(one=1,two=2)
		self.assertEqual(p['one'],1)
		self.assertEqual(p['two'],2)
		# ordered list should retain order
		p = Picklist([('one',1),('two',2)])
		self.assertEqual(p['one'],1)
		self.assertEqual(p['two'],2)
		self.assertListEqual(list(p.list.keys()),['one','two'])
		# empty picklist not allowed
		with self.assertRaises(AttributeError):
			p = Picklist()
		
class TestAttribute(unittest.TestCase):

	def test_create(self):
		a = Attribute()
		self.assertEqual(a.coldef,'')
		self.assertEqual(a.validate,None)
		self.assertEqual(a.displayname,None)
		self.assertEqual(a.primary,False)
		self.assertEqual(a.displayclass,None)
		self.assertEqual(a.htmlescape,False)
		
		def f(x):return x
		
		a = Attribute(affinity='float',unique=True,notnull=True,default=0.1,validate=f,displayname='A',primary=True,displayclass='a b',htmlescape=True)
		self.assertEqual(a.coldef,'float unique not null default 0.1 ')
		self.assertEqual(a.validate,f)
		self.assertEqual(a.displayname,'A')
		self.assertEqual(a.primary,True)
		self.assertEqual(a.displayclass,'a b')
		self.assertEqual(a.htmlescape,True)
		
		a = Attribute(validate=Picklist(one=1,two=2))
		self.assertEqual(a.validate['one'],1)

class TestAbstractEntity(unittest.TestCase):
	
	def test_create(self):
		class Entity(AbstractEntity):
			database=name
		# creation should only be possible for derived classes
		with self.assertRaises(NotImplementedError):
			e=Entity()
		# class methods should only be callable fir derived classes
		with self.assertRaises(NotImplementedError):
			ids=Entity.listids()
		with self.assertRaises(NotImplementedError):
			es=Entity.list()
		with self.assertRaises(NotImplementedError):
			cvs=Entity.getcolumnvalues('col')

class TestEntity(unittest.TestCase):

	"""
	Test the various aspects of concrete implementations of the AbstractEntity class.
	
	Note that each test_ method should define its own concrete entity because defining an
	Entity twice with different attributes will not alter the first implementation!
	"""
	
	def setUp(self):
		class Entity(AbstractEntity):
			database=name
		self.e=Entity
	
	def test_create(self):
		class ConcreteEntity(self.e):
			a = Attribute()
		ce = ConcreteEntity(a='oink')
		self.assertEqual(ce.id,1)
		self.assertEqual(ce.a,'oink')
		ce = ConcreteEntity(id=1)
		self.assertEqual(ce.a,'oink')
		self.assertListEqual(ConcreteEntity.listids(),[1])

	def test_delete(self):
		class ConcreteEntityA(self.e):
			a = Attribute()
		ce = ConcreteEntityA(a='oink')
		le = ConcreteEntityA.listids()
		id = ce.id
		self.assertIn(id,le)
		ce.delete()
		le = ConcreteEntityA.listids()
		self.assertNotIn(id,le)
	
	def test_update(self):
		class ConcreteEntityB(self.e):
			a = Attribute()
		ce = ConcreteEntityB(a='oink')
		id = ce.id
		ce.a = 'oink oink'
		c2 = ConcreteEntityB(id=id)
		self.assertEqual(c2.a,'oink')
		ce.update()
		c2 = ConcreteEntityB(id=id)
		self.assertEqual(c2.a,'oink oink')
		ce.update(a='pig')
		c2 = ConcreteEntityB(id=id)
		self.assertEqual(c2.a,'pig')
	
	def test_validate(self):
		class ConcreteEntity2(self.e):
			a = Attribute(validate=lambda x:x>0)
			b = Attribute(validate=Picklist(one=1,two=2))
			
		ce = ConcreteEntity2(a=4,b='one')
		ce = ConcreteEntity2(a=4,b=1)
		with self.assertRaises(AttributeError):
			ce = ConcreteEntity2(a=4,b='three')
		with self.assertRaises(AttributeError):
			ce = ConcreteEntity2(a=4,b=3)
		with self.assertRaises(AttributeError):
			ce = ConcreteEntity2(a=0,b='one')
		
		ce.update(a=5)
		ce.update(b='two')
		ce.update(b=1)
		with self.assertRaises(AttributeError):
			ce.update(a=-1)
		with self.assertRaises(AttributeError):
			ce.update(b='three')
		with self.assertRaises(AttributeError):
			ce.update(b=3)

	def test_default(self):
		class ConcreteEntity3(self.e):
			a = Attribute(default='oink')
			b = Attribute(default=0.3)
			c = Attribute(affinity='float',default=0.4)
			d = Attribute(affinity='text',default=0.4)
		
		ce = ConcreteEntity3()
		self.assertEqual(ce.a,'oink')
		self.assertEqual(ce.b,0.3)
		self.assertEqual(ce.c,0.4)
		self.assertEqual(ce.d,'0.4')

	def test_unique(self):
		class ConcreteEntity4(self.e):
			a = Attribute(unique=True)
		
		c1 = ConcreteEntity4(a=1)
		c2 = ConcreteEntity4(a=2)
		cn1 = ConcreteEntity4()
		cn2 = ConcreteEntity4() # should work: None or NULL cannot violate a unique constraint
		self.assertEqual(cn1.a,cn2.a)
		self.assertIsNone(cn1.a)
		with self.assertRaises(IntegrityError):
			cd = ConcreteEntity4(a=2)

	def test_notnull(self):
		class ConcreteEntity5(self.e):
			a = Attribute(notnull=True)
		
		ce = ConcreteEntity5(a=3)
		with self.assertRaises(IntegrityError):
			ce = ConcreteEntity5()
	
	def test_list(self):
		class ConcreteEntity6(self.e):
			a = Attribute()
		
		l=[]
		v=(1,3,5,7,2,4,44,444,6)
		for i in v:
			l.append(ConcreteEntity6(a=i))
		
		l2=ConcreteEntity6.listids()
		self.assertSameElements([e.id for e in l],[e for e in l2])
		l3=[ConcreteEntity6(id=id) for id in l2]
		self.assertSameElements(v,[e.a for e in l3])
		l4=ConcreteEntity6.list()
		self.assertSameElements([e.id for e in l3],[e.id for e in l4])
		
		# note that ints are converted to strings and then patterned w. like %x%
		l5=ConcreteEntity6.list(pattern=[('a',4)])
		self.assertEqual(len(l5),3)
		self.assertSameElements([4,44,444],[e.a for e in l5])
		
		l5=ConcreteEntity6.list(sortorder=[('a','asc')])
		self.assertListEqual(sorted(v),[e.a for e in l5])
		
		l5=ConcreteEntity6.list(pattern=[('a',4)],sortorder=[('a','desc')])
		self.assertListEqual([444,44,4],[e.a for e in l5])
	
class TestRbacEntity(unittest.TestCase):

	"""
	Test the various aspects of concrete implementations of the AbstractEntity class with Role Based Access Control enabled.
	
	Note that each test_ method should define its own concrete entity because defining an
	Entity twice with different attributes will not alter the first implementation!
	"""
	
	def setUp(self):
		class Entity(AbstractEntity):
			database=name
		
		self.e=Entity
		
		class User(Entity):
			name=Attribute(unique=True,notnull=True)
		
		Entity._rbac().setOn(User)
		
		self.u=User
		try:
			self.userlist=[User(name='admin'),User(name='jane'),User(name='john')]
		except IntegrityError: # if setUp runs more than once
			pass
			
		class ConcreteEntity1(self.e):
			a = Attribute()
		self.ce1 = ConcreteEntity1
		
		class ConcreteEntity2(self.e):
			a = Attribute()
		self.ce2 = ConcreteEntity2
		
	def test_rbac(self):
		self.assertEqual(self.ce1._rbac().on,self.u)
		self.assertEqual(self.ce2._rbac().on,self.u)
		self.assertIs(self.ce1._rbac(),self.ce2._rbac())
	
	@unittest.expectedFailure
	def test_rbacdefaults(self):
		Role = self.ce1._rbac().getRole()
		Permission = self.ce1._rbac().getPermission()
		
		r=Role.list(pattern=[('name','Administrator')])
		self.assertEqual(len(r),1)
		
		p=Permission.list(pattern=[('entity','Role')])
		self.assertEqual(len(p),4) # 

class TestRbacRelation(unittest.TestCase):

	def setUp(self):
		class Relation(AbstractRelation):
			database=name
		self.r=Relation
		
		class Entity(AbstractEntity):
			database=name
		self.e=Entity
		
	def test_create(self):
		class A(self.e):
			a = Attribute()
			
		class B(self.e):
			b = Attribute()
		
		class R(self.r):
			a = A
			b = B
		
		self.assertEqual(R.relation_type,'1:N')
		self.assertTrue(hasattr(A,'getB'))
		self.assertTrue(hasattr(A,'get'))
		self.assertTrue(hasattr(B,'getA'))
		self.assertTrue(hasattr(B,'get'))
		self.assertDictEqual(A.reltype,{'B':'1:N'})
		self.assertDictEqual(A.relclass,{'B':B})
		self.assertDictEqual(A.joins,{'B':'R'})
		self.assertDictEqual(B.reltype,{'A':'N:1'})
		self.assertDictEqual(B.relclass,{'A':A})
		self.assertDictEqual(B.joins,{'A':'R'})
		
		class R2(self.r):
			relation_type='N:1'
			a = A
			b = B
		self.assertEqual(R2.relation_type,'N:1')
		
		class R3(self.r):
			relation_type='N:N'
			a = A
			b = B
		self.assertEqual(R3.relation_type,'N:N')
		
		with self.assertRaises(KeyError):
			class R4(self.r):
				relation_type='2:2'
				a = A
				b = B
		
	def test_1n(self):
		class A1N(self.e): pass
		class B1N(self.e): pass
		class R1N(self.r):
			a=A1N
			b=B1N
		a=A1N()
		alist=[a.id]
		b1=B1N()
		b2=B1N()
		blist=[b1.id,b2.id]
		a.add(b1)
		a.add(b2)
		self.assertSameElements(blist,[e.id for e in a.get(B1N)])
		self.assertSameElements(alist,[e.id for e in b1.get(A1N)])
		self.assertSameElements(alist,[e.id for e in b2.get(A1N)])
		# A -(1:N)-> B implies B -(N:1)-> A, adding to b *replaces* references to a
		a=A1N()
		alist=[a.id]
		b1.add(a)
		self.assertSameElements(alist,[e.id for e in b1.get(A1N)])
		# adding the same element twice should have no effect
		b1.add(a)
		self.assertSameElements(alist,[e.id for e in b1.get(A1N)])
		
	def test_nn(self):
		class ANN(self.e): pass
		class BNN(self.e): pass
		class RNN(self.r):
			relation_type='N:N'
			a=ANN
			b=BNN
		a1=ANN()
		a2=ANN()
		alist=[a1.id,a2.id]
		b1=BNN()
		b2=BNN()
		blist=[b1.id,b2.id]
		a1.add(b1)
		a1.add(b2)
		a2.add(b1)
		a2.add(b2)
		self.assertSameElements(alist,[e.id for e in b1.get(ANN)])
		self.assertSameElements(alist,[e.id for e in b2.get(ANN)])
		self.assertSameElements(blist,[e.id for e in a1.get(BNN)])
		self.assertSameElements(blist,[e.id for e in a2.get(BNN)])
		# adding the same element twice should have no effect
		a1.add(b1)
		self.assertSameElements(alist,[e.id for e in b1.get(ANN)])
		self.assertSameElements(blist,[e.id for e in a1.get(BNN)])
		
if __name__ == '__main__':

	global name
	# create a file to be used as a sqlite dbstore
	file,name = mkstemp()
	close(file)
    
	unittest.main()
	try: # remove any lingering database
		unlink(name)
	except Exception as e:
		print(e,name)
