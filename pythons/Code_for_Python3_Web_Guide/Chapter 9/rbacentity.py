import threading
import collections
import sqlite3 as sqlite

import logging
sqllogger = logging.getLogger('SQLLogger')
sqllogger.setLevel(logging.DEBUG)
sqllogger.addHandler(logging.FileHandler('sql.log'))

class rbac:
	
	def __init__(self,db):
		class RBACEntity(AbstractEntity):
			database=db
		
		class RBACRelation(AbstractRelation):
			database=db
	
		class Role(RBACEntity):
			name = Attribute(notnull=True,displayname="Name",primary=True)
		
		self.Role = Role
		
		class Permission(RBACEntity):
			entity = Attribute(notnull= True, displayname = "Entity")
			# can't have an <input name="action">
			operation = Attribute(notnull= True, displayname = "Action")
			level = Attribute(notnull= True, default=0, displayname = "Level", validate=Picklist(all=0,owner=1,none=2))
		
		self.Permission = Permission
		
		# for k,v in globals().items():
			# if k.endswith('Entity') :
				# print (k)
		
		class RolePermission(RBACRelation):
			a= Role
			b = Permission
		
	def allowed(self,entity,user,action):
		return False
	
	def getRole(self):
		return self.Role
	
	def getPermission(self):
		return self.Permission

class custom:
	
	def __init__(self,db):
		class CustomEntity(AbstractEntity):
			database=db
		
		class DisplayCustomization(CustomEntity):
			entity = Attribute(notnull= True, displayname = "Entity")
			description = Attribute(displayname = "Description")
			customhtml = Attribute(displayname = "Custom HTML", htmlescape=True, displayclass="mb-textarea")
			
		self.DisplayCustomization = DisplayCustomization

		class BrowseCustomization(CustomEntity):
			entity = Attribute(notnull= True, displayname = "Entity")
			description = Attribute(displayname = "Description")
			customhtml = Attribute(displayname = "Custom HTML", htmlescape=True, displayclass="mb-textarea")
			
		self.BrowseCustomization = BrowseCustomization
		
		
	def getDisplayCustomization(self):
		return self.DisplayCustomization
	
	def getDisplayCustomHTML(self,entity):
		return "".join(dc.customhtml for dc in self.DisplayCustomization.list(pattern=[('entity',entity)]))
		
	def getBrowseCustomization(self):
		return self.BrowseCustomization
	
	def getBrowseCustomHTML(self,entity):
		return "".join(dc.customhtml for dc in self.BrowseCustomization.list(pattern=[('entity',entity)]))
				
# TODO: a Picklist attr *must* have a default! (otherwise the default is None and that might bot be in the picklist)

class Picklist:
	def __init__(self,list=None,**kw):
		self.list = collections.OrderedDict(list) if not list is None else collections.OrderedDict()
		self.list.update(kw)
		if len(self.list)==0 : raise AttributeError("empty Picklist")
	
	def __getitem__(self,key):
		return self.list[key]
		
class Attribute:
	def __init__(self,
		unique		=False,
		notnull		=False,
		default		=None,
		affinity	=None,
		validate	=None,
		displayname	=None,
		primary		=False,
		displayclass=None,
		htmlescape  =False):
		
		self.unique = unique
		self.notnull= notnull
		self.default= default
		self.affinity=affinity
		
		self.coldef = (affinity+' ' if not affinity is None else '') + ('unique ' if unique else '') + ('not null ' if notnull else '') + ('default %s '%default if not default is None else '')
		self.validate = validate # check whether this is a function w. 1 arg?
		self.displayname = displayname
		self.primary = primary
		self.displayclass = displayclass
		self.htmlescape = htmlescape
		
#print('def ME')		
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
		#print('ME in',classname,metaclass.__name__,baseclasses)
		def connect(cls):
			"""create a thread local connection if there isn't one yet"""
			#print('@@@@@@@@ connect',cls,cls._database,'thread',threading.current_thread().ident)
			##print('connect',cls)
			if not hasattr(cls._local,'conn'):
				#print('!!!!!!!!!!!!!!!!!!new connection for thread',threading.current_thread().ident)
				cls._local.conn=sqlite.connect(cls._database)
				cls._local.conn.execute('pragma foreign_keys = 1')
				cls._local.conn.row_factory = sqlite.Row
				# check if rbac tables are defined, if not, initialize them
				cls._local.rbac=rbac(cls._database)
				# check if we have a display customization table, if not, initialize it
				cls._local.custom=custom(cls._database)
			#print(cls._local.conn)
			return cls._local.conn
		
		def getrbac(cls):
			cls._connect()
			return cls._local.rbac
			
		def getcustom(cls):
			cls._connect()
			return cls._local.custom
			
		entitydefinition = False
		if len(baseclasses):
			# these test ensure we only take special actions for
			# classes derived from Entity ( we cannot check that directly 
			# because forward references are not allowed
			#print('ME baseclasses nonzero')
			if not 'database' in classdict and not '_database' in classdict:
				classdict['_database']=MetaEntity.findattr(baseclasses,'database')
				#print('ME no database',classdict['_database'])
				if classdict['_database'] is None:
					raise AttributeError('subclass of AbstractEntity has no database class variable')
				entitydefinition=True
			
			# copy reference to thread local storage
			if not '_local' in classdict:
				classdict['_local']=MetaEntity.findattr(baseclasses,'_local')
				
			classdict['_connect']=classmethod(connect)
			classdict['_rbac']=classmethod(getrbac)
			classdict['_custom']=classmethod(getcustom)
			classdict['columns']=[k for k,v in classdict.items() if type(v) == Attribute]
			classdict['sortorder']=[]
			classdict['displaynames']={k:v.displayname if v.displayname else k for k,v in classdict.items() if type(v) == Attribute}
			classdict['validators']={k:v.validate for k,v in classdict.items() if type(v) == Attribute and not v.validate is None}
			classdict['displaynames']['id']='id'
			classdict['displayclasses']={k:v.displayclass for k,v in classdict.items() if type(v) == Attribute}
			classdict['htmlescape']={k:v.htmlescape for k,v in classdict.items() if type(v) == Attribute}
			PrimaryKey = Attribute()
			PrimaryKey.coldef = 'integer primary key autoincrement'
			#print('ME entitydefinition',entitydefinition)
			if entitydefinition or '_meta' in classdict:
				sql = 'create table if not exists "' + classname +'" (' + ", ".join(['"'+k+'" '+v.coldef for k,v in [('id',PrimaryKey)]+list(classdict.items()) if type(v) == Attribute]) + ')'
				# we cannot use connect yet
				conn = sqlite.connect(classdict['_database'])
				sqllogger.debug(sql)
				conn.execute(sql)
				conn.commit()
				conn.close()

			for k,v in classdict.items():
				if type(v) == Attribute:
					if v.primary:
						classdict['primary']=property(lambda self:getattr(self,k))
						classdict['primaryname']=k
						break # absolutely necessary otherwise infinite recursion!
			if not 'primary' in classdict:
				classdict['primary']=property(lambda self:getattr(self,'id'))
				classdict['primaryname']='id'
				
		return type.__new__(metaclass,classname,baseclasses,classdict)

#print('def MME')		
class MetaMetaEntity(MetaEntity):
	
	@classmethod
	def __prepare__(metaclass, classname, baseclasses, **kwds):
		return collections.OrderedDict()

	def __new__(metaclass,classname,baseclasses,classdict):
		#print('MME in',classname,metaclass.__name__,baseclasses)
		cls = MetaEntity.__new__(metaclass,classname,baseclasses,classdict)
		#print('MME out')
		if not classname.startswith('MD_') and False:
			#print('meta')
			if not 'database' in classdict and  len(baseclasses)>0  :
				if not 'MD_entities' in globals():
					#if '_database' in classdict:
					mddict = collections.OrderedDict()
					mddict['name']=Attribute(notnull=True,unique=True)
					#print('MME w db', classname)
					mddict['_database']=cls._database
					mddict['_meta']=True
					globals()['MD_entities']=MetaMetaEntity.__new__(MetaMetaEntity,'MD_entities',(AbstractEntity,),mddict)
				#print('adding metainfo',classname,baseclasses)
				el=MD_entities.list(pattern=[('name',classname)])
				if len(el)<1 :
					e=MD_entities(name=classname)
				else:
					e=el[0]
				# attributes
				if not 'MD_attributes' in globals():
					mddict = collections.OrderedDict()
					mddict['name']=Attribute(notnull=True)
					mddict['notnull']=Attribute(affinity='bool',default=False)
					mddict['unique']=Attribute()
					mddict['displayname']=Attribute()
					mddict['affinity']=Attribute()
					
					mddict['_database']=cls._database
					mddict['_meta']=True
					globals()['MD_attributes']=MetaMetaEntity.__new__(MetaMetaEntity,'MD_attributes',(AbstractEntity,),mddict)

				if not 'MD_entity_attributes' in globals():
						print(']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]] creating MD_entity_attributes')
						mddict={'a':MD_entities, 'b':MD_attributes,
						'_database':cls._database,
						'_meta':True}
						globals()['MD_entity_attributes']=MetaMetaRelation.__new__(MetaMetaRelation,'MD_entity_attributes',(AbstractRelation,),mddict)
						
						
				# picklist items
				if not 'MD_picklistitem' in globals():
					mddict = collections.OrderedDict()
					mddict['key']=Attribute(notnull=True)
					mddict['value']=Attribute(notnull=True)
					
					mddict['_database']=cls._database
					mddict['_meta']=True
					globals()['MD_picklistitem']=MetaMetaEntity.__new__(MetaMetaEntity,'MD_picklistitem',(AbstractEntity,),mddict)

				if not 'MD_attribute_picklistitems' in globals():
						mddict={'a':MD_attributes, 'b':MD_picklistitem,
						'_database':cls._database,
						'_meta':True}
						globals()['MD_attribute_picklistitems']=MetaMetaRelation.__new__(MetaMetaRelation,'MD_attribute_picklistitems',(AbstractRelation,),mddict)
				
				print('>>>>>>>>>>>>>>>>>>>>>>>>>>>',e)
				attrs=e.get(MD_attributes)
				print('>>>>>>>>>>>>>>>>>>>>>>>>>>>',attrs)
				for a in attrs:
					a.delete()
					
				for k,v in classdict.items():
					print("ME kv",k,v)
					if type(v)==Attribute:
						if not k in [ a.name for a in attrs ]:
							a=MD_attributes(name=k,notnull=v.notnull,unique=v.unique,affinity=v.affinity,displayname=v.displayname)
							print("MEA",e,a)
							e.add(a)
							if type(v.validate) == Picklist:
								for kk,vv in v.validate.list.items():
									p=MD_picklistitem(key=kk,value=vv)
									a.add(p)
							
		return cls

#print('def AE')		
class AbstractEntity(metaclass=MetaMetaEntity):
	_local = threading.local()
	
	@classmethod
	def listids(cls,pattern=None,sortorder=None):
		if cls.__name__ == 'Entity' : raise NotImplementedError('Entity classmethod may only be called on a derived class')

		sql = 'select id from "%s" '%(cls.__name__,)
		
		args = []
		joins = []
		patternattrs = []
		
		if not pattern is None and len(pattern)>0:
			for s in pattern:
				if not (s[0] in cls.columns or s[0]=='id'):
					# it's probably another entity so we have to construct a join
					#print('pattern',pattern,'\nRELTYPE',cls.reltype)
					if not s[0] in cls.reltype:
						raise TypeError('unknown column '+s[0])
					else:
						joins.append((s,cls.joins[s[0]]))
				else:
					patternattrs.append(s)
			#if len(joins):
				#print('JOIN', " ".join(["join %s on %s.id = %s.%s_id"%(j[1],cls.__name__,j[1],cls.__name__) for j in joins]))
				#print('JWHERE',["%s.%s_id = ?"%(j[1],j[0][0]) for j in joins])
				#print('JWHEREARGS',[int(j[0][1]) for j in joins])
			if len(joins):
				sql += " ".join(["join %s on %s.id = %s.%s_id"%(j[1],cls.__name__,j[1],cls.__name__) for j in joins])
			if len(patternattrs) or len(joins):
				sql += " where "
			if len(patternattrs):
				sql += " and ".join("%s like ?"%s[0] for s in patternattrs)
				args += ['%'+str(s[1])+'%' for s in patternattrs]
			if len(joins):
				sql += " "
				if len(patternattrs): sql += "and "
				sql += " and ".join(["%s.%s_id = ?"%(j[1],j[0][0]) for j in joins])
				args += [int(j[0][1]) for j in joins]
		
		if sortorder is None:
			if not cls.sortorder is None :
				sortorder = cls.sortorder
		else:
			##print('SORTORDER',sortorder)
			for s in sortorder:
				if not (s[0] in cls.columns or s[0]=='id'): raise TypeError('unknown column '+s[0])
				if not s[1] in ('asc', 'desc') : raise TypeError('illegal sort argument'+s[1])
		if not (sortorder is None or len(sortorder) == 0):
			sql += ' order by ' + ','.join(s[0]+' '+s[1] for s in sortorder)
		cursor=cls._connect().cursor()
		sqllogger.debug(sql+str(args))
		cursor.execute(sql,args)
		return [r['id'] for r in cursor]
	
	@classmethod
	def list(cls,pattern=None,sortorder=None):
		if cls.__name__ == 'Entity' : raise NotImplementedError('Entity classmethod may only be called on a derived class')
		return [cls(id=id) for id in cls.listids(sortorder=sortorder,pattern=pattern)]
	
	@classmethod
	def getcolumnvalues(cls,column):
		if cls.__name__ == 'Entity' : raise NotImplementedError('Entity classmethod may only be called on a derived class')
		if not column in cls.columns : raise KeyError('unknown column '+column)
		sql='select "%s" from "%s" order by lower("%s")'%(column,cls.__name__,column)
		cursor=cls._connect().cursor()
		sqllogger.debug(sql)
		cursor.execute(sql)
		return [r[0] for r in cursor.fetchall()]
		
	
	def __str__(self):
		return '<'+self.__class__.__name__+': '+", ".join(["%s=%s"%(displayname, getattr(self,column)) for column,displayname in self.displaynames.items()])+'>'
	
	def __repr__(self):
		return self.__class__.__name__+"(id="+str(self.id)+")"
		
	def __setattr__(self,name,value):
		if name in self.validators :
			if type(self.validators[name])==Picklist:
				try:
					value=self.validators[name].list[value]
				except:
					# key not known, try value directly
					if not value in list(self.validators[name].list.values()):
						raise AttributeError("assignment to "+name+" fails, "+str(value)+" not in picklist")
			elif not self.validators[name](value):
				raise AttributeError("assignment to "+name+" does not validate")
		object.__setattr__(self,name,value)
		
	def __init__(self,**kw):
		if self.__class__.__name__ == 'Entity' : raise NotImplementedError('instantiation only allowed for derived classes')
		if 'id' in kw:
			if len(kw)>1 : raise ArgumentError()
			sql = 'select * from "%s" where id = ?'%self.__class__.__name__
			cursor = self._connect().cursor()
			sqllogger.debug(sql+str(kw['id']))
			cursor.execute(sql,(kw['id'],))
			r=cursor.fetchone()
			for c in self.columns:
				setattr(self,c,r[c])
			self.id = kw['id']
		else:
			rels={}
			attr={} # we store but ignore: entity has no knowlegde of relation
			for col in kw:
				#print(col)
				if not col in self.columns:
					rels[col]=kw[col]
				else:
					attr[col]=kw[col]
					setattr(self,col,kw[col])
					
			name = self.__class__.__name__
			cols = ",".join(['"'+k+'"' for k in attr.keys()])
			qmarks = ",".join(['?']*len(attr))
			if len(cols):
				sql = 'insert into "%s" (%s) values (%s)'%(name,cols,qmarks)
			else:
				sql = 'insert into "%s" default values'%name
			sqllogger.debug(sql+str(attr.values()))
			with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,tuple(attr.values()))
				self.id = cursor.lastrowid
				# retrieve resultant values (inclusive defaults)
				sql = 'select * from "%s" where id = ?'%self.__class__.__name__
				sqllogger.debug(sql+str(self.id))
				cursor.execute(sql,(self.id,))
				r=cursor.fetchone()
				for c in self.columns:
					setattr(self,c,r[c])
				
	def delete(self):
		sql = 'delete from "%s" where id = ?'%self.__class__.__name__
		with self._connect() as conn:
				cursor = conn.cursor()
				sqllogger.debug(sql+str(self.id))
				cursor.execute(sql,(self.id,))
	
	def update(self,**kw):
		for k,v in kw.items():
			setattr(self,k,v)
		sets = []
		vals = []
		for c in self.columns:
			if not c == 'id':
				sets.append('"'+c+'"=?')
				vals.append(getattr(self,c))
		table = self.__class__.__name__
		sql = 'update "%s" set %s where id = ?'%(table,",".join(sets))
		vals.append(self.id)
		sqllogger.debug(sql+str(vals))
		with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,vals)

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
		# print(classdict)
		def connect(cls):
			"""create a thread local connection if there isn't one yet"""
			#print('@@@@@@@@ connect',cls,cls._database,'thread',threading.current_thread().ident)
			if not hasattr(cls._local,'conn'):
				cls._local.conn=sqlite.connect(cls._database)
				cls._local.conn.execute('pragma foreign_keys = 1')
				cls._local.conn.row_factory = sqlite.Row
			#print(cls._local.conn)
			return cls._local.conn
		
		def get(self,cls):
			return getattr(self,'get'+cls.__name__)()
		
		def getclass(self,cls,relname):
			clsname = cls.__name__
			sql = 'select %s_id from %s where %s_id = ?'%(clsname,relname,self.__class__.__name__)
			sqllogger.debug(sql+str(self.id))
			result = 'no result'
			with self._connect() as conn:
				#print("\n".join(conn.iterdump()))
				cursor=conn.cursor()
				cursor.execute(sql,(self.id,))
				result = [cls(id=r[0]) for r in cursor]
			# print(result)
			return result
	
		def add(self,entity):
			return getattr(self,'add'+entity.__class__.__name__)(entity)
		
		def addclass(self,entity,Entity,relname,reltype='N:1'):
			if not entity.__class__ == Entity : raise TypeError('entity not of the required class')
			sql = 'insert or replace into %(rel)s (%(a)s_id,%(b)s_id) values (?,?)'%{'rel':relname,'a':self.__class__.__name__,'b':entity.__class__.__name__} 
			sqllogger.debug(sql+str(self.id)+str(entity.id))
			with self._connect() as conn:
				cursor = conn.cursor()
				cursor.execute(sql,(self.id,entity.id))
				
		relationdefinition = False
		if len(baseclasses):
			# these test ensure we only take special actions for
			# classes derived from Relation ( we cannot check that directly 
			# because forward references are not allowed
			if not 'database' in classdict and not '_database' in classdict:
				classdict['_database']=MetaRelation.findattr(baseclasses,'database')
				if classdict['_database'] is None:
					raise AttributeError('subclass of AbstractRelation has no database class variable')
				relationdefinition=True
			# copy reference to thread local storage
			if not '_local' in classdict:
				classdict['_local']=MetaRelation.findattr(baseclasses,'_local')
				
			classdict['_connect']=classmethod(connect)
			
			if relationdefinition or '_meta' in classdict:
				a = classdict['a']
				b = classdict['b']
				r = '1:N'
				if 'relation_type' in classdict: r = classdict['relation_type']
				if not r in ('N:1','1:N','N:N'): raise KeyError("unknown relation_type %s"%r)
				classdict['relation_type'] = r
				
				if not issubclass(a,AbstractEntity) : raise TypeError('a not an AbstractEntity')
				if not issubclass(a,AbstractEntity) : raise TypeError('b not an AbstractEntity')
				
				runique = ''
				if r == 'N:1' : runique = ' ,unique(%s_id)'%a.__name__
				if r == '1:N' : runique = ' ,unique(%s_id)'%b.__name__
				
				sql = 'create table if not exists %(rel)s ( %(a)s_id references %(a)s on delete cascade, %(b)s_id references %(b)s on delete cascade, unique(%(a)s_id,%(b)s_id)%(ru)s)'%{'rel':classname,'a':a.__name__,'b':b.__name__,'ru':runique}
				# we cannot use connect yet
				conn = sqlite.connect(classdict['_database'])
				sqllogger.debug(sql)
				conn.execute(sql)
				conn.commit()
				conn.close()
				
				setattr(a,'get'+b.__name__,lambda self:getclass(self,b,classname))
				setattr(a,'get',get)
				setattr(b,'get'+a.__name__,lambda self:getclass(self,a,classname))
				setattr(b,'get',get)
				setattr(a,'add'+b.__name__,lambda self,entity:addclass(self,entity,b,classname))
				setattr(a,'add',add)
				setattr(b,'add'+a.__name__,lambda self,entity:addclass(self,entity,a,classname))
				setattr(b,'add',add)
				
				reltypes = getattr(a,'reltype',{})
				reltypes[b.__name__]=r
				setattr(a,'reltype',reltypes)
				reltypes = getattr(b,'reltype',{})
				reltypes[a.__name__]={'1:N':'N:1','N:N':'N:N','N:1':'1:N'}[r]
				setattr(b,'reltype',reltypes)
				
				relclasses = getattr(a,'relclass',{})
				relclasses[b.__name__]=b
				setattr(a,'relclass',relclasses)
				relclasses = getattr(b,'relclass',{})
				relclasses[a.__name__]=a
				setattr(b,'relclass',relclasses)
				
				joins = getattr(a,'joins',{})
				joins[b.__name__]=classname
				setattr(a,'joins',joins)
				joins = getattr(b,'joins',{})
				joins[a.__name__]=classname
				setattr(b,'joins',joins)
				
		return type.__new__(metaclass,classname,baseclasses,classdict)

class MetaMetaRelation(MetaRelation):
	def __new__(metaclass,classname,baseclasses,classdict):
		cls = MetaRelation.__new__(metaclass,classname,baseclasses,classdict)

		if not classname.startswith('MD_') and False:
			#print('meta')
			if not 'database' in classdict and  len(baseclasses)>0  :
				if not 'MD_relations' in globals():
					#if '_database' in classdict:
					mddict = collections.OrderedDict()
					mddict['name']=Attribute(notnull=True,unique=True)
					mddict['a']=Attribute(notnull=True)
					mddict['b']=Attribute(notnull=True)
					mddict['relation_type']=Attribute(notnull=True)
					#print('MME w db', classname)
					mddict['_database']=cls._database
					mddict['_meta']=True
					globals()['MD_relations']=MetaMetaEntity.__new__(MetaMetaEntity,'MD_relations',(AbstractEntity,),mddict)
				#print('adding metainfo',classname,baseclasses)
				try:
					r=MD_relations(name=classname,a=classdict['a'].__name__,b=classdict['b'].__name__,relation_type=classdict['relation_type'])
				except Exception as e:
					print('ignored',e)
		return cls

class AbstractRelation(metaclass=MetaMetaRelation):
	_local = threading.local()
	
				
if __name__ == "__main__":
	
	db="/tmp/abc.db"
	import os
	try:
		os.unlink(db)
	except:
		pass
		
	class Entity(AbstractEntity):
		database=db
	
	class MyEntity(Entity):
		a=Attribute(unique=True,notnull=True,affinity='float',displayname='Atrribute A',validate=lambda x:x<5)
	
	class OtherEntity(Entity):
		b=Attribute(validate=Picklist(one=1,two=2,three=3),default=3)
		
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
	
	p=MyEntity(a=123)
	q=OtherEntity()
	q2=OtherEntity()
	
	class Relation(AbstractRelation):
		database=db
		
	class MyOther(Relation):
		a=MyEntity
		b=OtherEntity
		relation_type='1:N'
		
	p.add(q)
	p.add(q2)
	print('='*40)
	print(p.getOtherEntity())
	print(p.__class__.reltype)
	print(q.__class__.reltype)
	print('='*40)
	
	try:
		q.b='four'
	except AttributeError as e:
		print(e)
	
	for m in MD_entities.list():
		print(m.name)
		for a in m.get(MD_attributes):
			print(a.name,a.displayname,a.notnull,a.unique,a.affinity)
		
	for r in MD_relations.list():
		print(r.name,r.a,r.b)
	