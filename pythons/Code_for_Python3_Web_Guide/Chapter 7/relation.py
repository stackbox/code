import threading
import collections
import sqlite3 as sqlite
from entity import AbstractEntity
	
class MetaRelation(type):
	
	@staticmethod
	def findattr(classes,attribute):
		a=None
		for c in classes:
			if hasattr(c,attribute):
				a=getattr(c,attribute)
				break
		if a is None:
			for c in classes:
				a = MetaRelation.findattr(c.__bases__,attribute)
				if not a is None:
					break
		return a
	
	
	def __new__(metaclass,classname,baseclasses,classdict):
		print(classdict)
		def connect(cls):
			"""create a thread local connection if there isn't one yet"""
			#print('connect',cls)
			if not hasattr(cls._local,'conn'):
				cls._local.conn=sqlite.connect(cls._database)
				cls._local.conn.execute('pragma foreign_keys = 1')
				cls._local.conn.row_factory = sqlite.Row
			return cls._local.conn
		
		def get(self,cls):
			return getattr(self,'get'+cls.__name__)()
		
		def getclass(self,cls,relname):
			clsname = cls.__name__
			sql = 'select %s_id from %s where %s_id = ?'%(clsname,relname,self.__class__.__name__)
			print(sql,self.id)
			cursor=self._connect().cursor()
			cursor.execute(sql,(self.id,))
			return [cls(id=r[clsname+'_id']) for r in cursor]
	
		def add(self,entity):
			return getattr(self,'add'+entity.__class__.__name__)(entity)
		
		def addclass(self,entity,Entity,relname):
			if not entity.__class__ == Entity : raise TypeError('entity not of the required class')
			sql = 'insert or replace into %(rel)s (%(a)s_id,%(b)s_id) values (?,?)'%{'rel':relname,'a':self.__class__.__name__,'b':entity.__class__.__name__} 
			print(sql,self.id,entity.id)
			with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,(self.id,entity.id))
				
		relationdefinition = False
		if len(baseclasses):
			# these test ensure we only take special actions for
			# classes derived from Relation ( we cannot check that directly 
			# because forward references are not allowed
			if not 'database' in classdict:
				classdict['_database']=MetaRelation.findattr(baseclasses,'database')
				if classdict['_database'] is None:
					raise AttributeError('subclass of AbstractRelation has no database class variable')
				relationdefinition=True
			# copy reference to thread local storage
			if not '_local' in classdict:
				classdict['_local']=MetaRelation.findattr(baseclasses,'_local')
				
			classdict['_connect']=classmethod(connect)
			
			if relationdefinition:
				a = classdict['a']
				b = classdict['b']
				if not issubclass(a,AbstractEntity) : raise TypeError('a not an AbstractEntity')
				if not issubclass(a,AbstractEntity) : raise TypeError('b not an AbstractEntity')
			
				sql = 'create table if not exists %(rel)s ( %(a)s_id references %(a)s on delete cascade, %(b)s_id references %(b)s on delete cascade, unique(%(a)s_id,%(b)s_id))'%{'rel':classname,'a':a.__name__,'b':b.__name__}
				# we cannot use connect yet
				conn = sqlite.connect(classdict['_database'])
				print(sql)
				conn.execute(sql)
				
				setattr(a,'get'+b.__name__,lambda self:getclass(self,b,classname))
				setattr(a,'get',get)
				setattr(b,'get'+a.__name__,lambda self:getclass(self,a,classname))
				setattr(b,'get',get)
				setattr(a,'add'+b.__name__,lambda self,entity:addclass(self,entity,b,classname))
				setattr(a,'add',add)
				setattr(b,'add'+a.__name__,lambda self,entity:addclass(self,entity,a,classname))
				setattr(b,'add',add)
				
		return type.__new__(metaclass,classname,baseclasses,classdict)

class AbstractRelation(metaclass=MetaRelation):
	_local = threading.local()
	
if __name__ == "__main__":
	
	from os import unlink
	db="/tmp/abcr.db"
	try:
		unlink(db)
	except:
		pass
	
	class Entity(AbstractEntity):
		database=db

	class Relation(AbstractRelation):
		database=db

	class A(Entity): pass
	
	class B(Entity): pass
	
	class AB(Relation):
		a=A
		b=B
	
	a1=A()
	a2=A()
	b1=B()
	b2=B()
	
	a1.add(b1)
	a1.add(b2)
	print(a1.get(B))
	print(b1.get(A))