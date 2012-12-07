import threading
import collections
import sqlite3 as sqlite

class Attribute:
	def __init__(self,unique=False,notnull=False,default=None,affinity=None,validate=None,displayname=None, primary=False):
		self.coldef = (affinity+' ' if not affinity is None else '') + ('unique ' if unique else '') + ('not null ' if notnull else '') + ('default %s '%default if not default is None else '')
		self.validate = validate # check whether this is a function w. 1 arg?
		self.displayname = displayname
		self.primary = primary
	
class MetaEntity(type):
	
	@classmethod
	def __prepare__(metaclass, classname, baseclasses, **kwds):
		return collections.OrderedDict()

	@staticmethod
	def findattr(classes,attribute):
		a=None
		for c in classes:
			if hasattr(c,attribute):
				a=getattr(c,attribute)
				break
		if a is None:
			for c in classes:
				a = MetaEntity.findattr(c.__bases__,attribute)
				if not a is None:
					break
		return a
	
	
	def __new__(metaclass,classname,baseclasses,classdict):
		def connect(cls):
			"""create a thread local connection if there isn't one yet"""
			#print('connect',cls)
			if not hasattr(cls._local,'conn'):
				cls._local.conn=sqlite.connect(cls._database)
				cls._local.conn.execute('pragma foreign_keys = 1')
				cls._local.conn.row_factory = sqlite.Row
			return cls._local.conn
			
		entitydefinition = False
		if len(baseclasses):
			# these test ensure we only take special actions for
			# classes derived from Entity ( we cannot check that directly 
			# because forward references are not allowed
			if not 'database' in classdict:
				classdict['_database']=MetaEntity.findattr(baseclasses,'database')
				if classdict['_database'] is None:
					raise AttributeError('subclass of AbstractEntity has no database class variable')
				entitydefinition=True
			# copy reference to thread local storage
			if not '_local' in classdict:
				classdict['_local']=MetaEntity.findattr(baseclasses,'_local')
				
			classdict['_connect']=classmethod(connect)
			classdict['columns']=[k for k,v in classdict.items() if type(v) == Attribute]
			classdict['sortorder']=[]
			classdict['displaynames']={k:v.displayname if v.displayname else k for k,v in classdict.items() if type(v) == Attribute}
			classdict['validators']={k:v.validate for k,v in classdict.items() if type(v) == Attribute and not v.validate is None}
			classdict['displaynames']['id']='id'
			PrimaryKey = Attribute()
			PrimaryKey.coldef = 'integer primary key autoincrement'
			if entitydefinition:
				sql = 'create table if not exists ' + classname +' (' + ", ".join([k+' '+v.coldef for k,v in [('id',PrimaryKey)]+list(classdict.items()) if type(v) == Attribute]) + ')'
				# we cannot use connect yet
				conn = sqlite.connect(classdict['_database'])
				print(sql)
				conn.execute(sql)

			for k,v in classdict.items():
				if type(v) == Attribute:
					if v.primary:
						classdict['primary']=property(lambda self:getattr(self,k))
						break # absolutely necessary otherwise infinite recursion!
			if not 'primary' in classdict:
				classdict['primary']=property(lambda self:getattr(self,'id'))
				
		return type.__new__(metaclass,classname,baseclasses,classdict)

class AbstractEntity(metaclass=MetaEntity):
	_local = threading.local()
	
	@classmethod
	def listids(cls,pattern=None,sortorder=None):
		sql = 'select id from %s'%(cls.__name__,)
		
		args = []
		
		if not pattern is None and len(pattern)>0:
			for s in pattern:
				if not (s[0] in cls.columns or s[0]=='id'): raise TypeError('unknown column '+s[0])
			sql += " where " + " and ".join("%s like ?"%s[0] for s in pattern)
			args += [s[1] for s in pattern]
			
		if sortorder is None:
			if not cls.sortorder is None :
				sortorder = cls.sortorder
		else:
			#print('SORTORDER',sortorder)
			for s in sortorder:
				if not (s[0] in cls.columns or s[0]=='id'): raise TypeError('unknown column '+s[0])
				if not s[1] in ('asc', 'desc') : raise TypeError('illegal sort argument'+s[1])
		if not (sortorder is None or len(sortorder) == 0):
			sql += ' order by ' + ','.join(s[0]+' '+s[1] for s in sortorder)
		cursor=cls._connect().cursor()
		print(sql,args)
		cursor.execute(sql,args)
		return [r['id'] for r in cursor]
	
	@classmethod
	def list(cls,pattern=None,sortorder=None):
		return [cls(id=id) for id in cls.listids(sortorder=sortorder,pattern=pattern)]
	
	def __str__(self):
		return '<'+self.__class__.__name__+': '+", ".join(["%s=%s"%(displayname, getattr(self,column)) for column,displayname in self.displaynames.items()])+'>'
	
	def __repr__(self):
		return self.__class__.__name__+"(id="+str(self.id)+")"
		
	def __setattr__(self,name,value):
		if name in self.validators :
			if not self.validators[name](value):
				raise AttributeError("assignment to "+name+" does not validate")
		object.__setattr__(self,name,value)
		
	def __init__(self,**kw):
		print(kw)
		if 'id' in kw:
			if len(kw)>1 : raise ArgumentError()
			sql = 'select * from %s where id = ?'%self.__class__.__name__
			cursor = self._connect().cursor()
			cursor.execute(sql,(kw['id'],))
			r=cursor.fetchone()
			for c in self.columns:
				setattr(self,c,r[c])
			self.id = kw['id']
		else:
			for col in kw:
				if not col in self.columns:
					raise KeyError(col+' is not a valid column')
			name = self.__class__.__name__
			cols = ",".join(kw.keys())
			qmarks = ",".join(['?']*len(kw))
			if len(cols):
				sql = 'insert into %s (%s) values (%s)'%(name,cols,qmarks)
			else:
				sql = 'insert into %s default values'%name
			print(sql)
			with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,tuple(kw.values()))
				self.id = cursor.lastrowid
	
	def delete(self):
		sql = 'delete from %s where id = ?'%self.__class__.__name__
		with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,(self.id,))
	
	def update(self,**kw):
		for k,v in kw.items():
			setattr(self,k,v)
		sets = []
		vals = []
		for c in self.columns:
			if not c == 'id':
				sets.append(c+'=?')
				vals.append(getattr(self,c))
		table = self.__class__.__name__
		sql = 'update %s set %s where id = ?'%(table,",".join(sets))
		print(sql)
		vals.append(self.id)
		with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,vals)
	
if __name__ == "__main__":
	
	class Entity(AbstractEntity):
		database="/tmp/abc.db"
	
	class MyEntity(Entity):
		a=Attribute(unique=True,notnull=True,affinity='float',displayname='Atrribute A',validate=lambda x:x<5)
	
	a=MyEntity(a=3.14)
	
	print(MyEntity.list())
	
	e=MyEntity.list(pattern=[('a',3.14)])[0]
	
	print(e)
	
	e.delete()
	
	a=MyEntity(a=2.71)
	print([str(e) for e in MyEntity.list()])
	
	a.a=1
	a.update()
	print([str(e) for e in MyEntity.list()])
	
	try:
		a.a=9
	except AttributeError as e:
		print(e)
		
	a.delete()
	
	