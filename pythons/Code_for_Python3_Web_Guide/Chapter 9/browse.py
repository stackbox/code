import threading
from uuid import uuid4 as uuid
from time import time
import cherrypy
from rbacentity import *

class Browse:
	def __init__(self,entity,columns=None,sortorder=None,pattern=None,page=10,show="show"):
		
		print(entity)
		if not issubclass(entity,AbstractEntity) : raise TypeError()
		
		self.entity = entity
		self.columns = entity.columns if columns is None else columns
		self.sortorder = [] if sortorder is None else sortorder
		self.pattern = [] if pattern is None else pattern
		self.page = page
		self.show = show

		# the cache should be thread safe, hence the lock
		self.cache= {}
		self.cachelock=threading.Lock()
		self.cachesize=3
		
		# print(self,dir(self))
		for c in self.columns:
			if not (c in entity.columns or c == 'id') and not (hasattr(self.entity,'get'+c.__name__)) :
				raise ValueError('column %s not defined'%c)
		if len(self.sortorder)>len(self.columns) :
			raise ValueError()
		for s in self.sortorder:
			if s[0] not in self.columns and s[0]!='id':
				raise ValueError('sorting on column %s not possible'%s[0])
			if s[1] not in ('asc','desc'):
				raise ValueError('column %s, %s is not a valid sort order'%s)
		
		for s in self.pattern:
			if s[0] not in self.columns and s[0]!='id':
				raise ValueError('patterning on column %s not possible'%s[0])
			
		if self.page < 5 :
				raise ValueError()
	
	def chash(self,cacheid,sortorder,pattern):
		# print(cacheid,str(sortorder),str(pattern))
		return cacheid+'-'+hex(hash(str(sortorder)))+'-'+hex(hash(str(pattern)))
		
	def iscached(self,cacheid,sortorder,pattern):
		if cacheid is None: return None
		h=self.chash(cacheid,sortorder,pattern)
		t=False
		with self.cachelock:
			t = h in self.cache
			if t :
				self.cache[h]=(time(),self.cache[h][1])
		# print(t,h)
		return cacheid if t else None
	
	def cleancache(self):
		t={}
		with self.cachelock:
			t={v[0]:k for k,v in self.cache.items()}
		if len(t) == 0 :
			return
		# print('cleancache length',len(t))	
		limit  = time()
		oldest = limit
		limit -= 3600
		key=None
		# print(t)
		for tt,k in t.items():
			if tt<limit:
				with self.cachelock:
					del self.cache[k]
					# print('delete',k)
			else:
				if tt<oldest:
					oldest = tt
					key = k
		if key:
			with self.cachelock:
				del self.cache[key]
				# print('delete oldest',k)
				
	def storeincache(self,ids,sortorder,pattern):
		cacheid=uuid().hex
		h=self.chash(cacheid,sortorder,pattern)
		if len(self.cache)>self.cachesize :
			self.cleancache()
		with self.cachelock:
			self.cache[h]=(time(),ids)
		# print('cached',h)
		return cacheid
		
	def getfromcache(self,cacheid,sortorder,pattern):
		# print('retrieving from cache')
		ids=None
		h=self.chash(cacheid,sortorder,pattern)
		with self.cachelock:
			try:
				ids=self.cache[h][1]
			except KeyError:
				# print(h,'not present, expired?')
				pass
		return ids
			
	@cherrypy.expose
	def index(self, _=None, start=0, pattern=None, sortorder=None, cacheid=None, next=None,previous=None, first=None, last=None, clear=None, related=None):
		#print(cherrypy.serving.request.headers)
		
		if not clear is None: # present but with empty string as value
			pattern=None
			sortorder=None
		if sortorder is None : sortorder = self.sortorder
		elif type(sortorder)==str:
			sortorder=[tuple(sortorder.split(','))]
		elif type(sortorder)==list:
			sortorder=[tuple(s.split(',')) for s in sortorder]
		else:
			sortorder=None

		# splitting pattern is too naive as pattern may contain commas
		if pattern is None : pattern = self.pattern
		elif type(pattern)==str:
			pattern=[tuple(pattern.split(','))]
		elif type(pattern)==list:
			pattern=[tuple(s.split(',',1)) for s in pattern]
		else:
			pattern=None
		
		if not next is None or not previous is None or not first is None or not last is None:
			cacheid=self.iscached(cacheid,sortorder,pattern)
		else:
			cacheid=None
		# print('CACHEID',cacheid)
		if cacheid is None:
			ids = self.entity.listids(pattern=pattern,sortorder=sortorder)
			cacheid = self.storeincache(ids,sortorder,pattern)
		else:
			ids = self.getfromcache(cacheid,sortorder,pattern)
			if ids == None:
				ids = self.entity.listids(pattern=pattern,sortorder=sortorder)
				cacheid = self.storeincache(ids,sortorder,pattern)
		
		start=int(start)
		if not next is None : start+=self.page
		elif not previous is None : start-=self.page
		elif not first is None : start=0
		elif not last is None : start=len(ids)-self.page
		if start >= len(ids) : start=len(ids)-1
		if start<0 : start = 0
		
		yield '<table class="entitylist" start="%d" page="%d">\n'%(start,self.page)
		yield '<thead><tr>'
		# print(self.columns)
		for col in self.columns:
			if type(col) == str :
				sortclass="notsorted"
				iconclass="ui-icon ui-icon-triangle-2-n-s"
				for s in sortorder:
					if s[0]==col :
						sortclass='sorted-'+s[1]
						iconclass=' ui-icon ui-icon-triangle-1-%s'%({'asc':'n','desc':'s'}[s[1]])
						break
				yield '<th class="%s"><div class="colname" style="display:none">%s</div>'%(sortclass,col)+self.entity.displaynames[col]+'<span class="%s"><span></th>'%iconclass
			else :
				yield '<th>'+col.__name__+'</th>'
		yield '</tr></thead>\n<tbody>\n'
		entities = [self.entity(id=i) for i in ids[start:start+self.page]]
		even=True
		for e in entities:
			even = not even
			vals=[]
			for col in self.columns:
				if not type(col) == str:
					vals.append("".join(['<span class="related" entity="%s" >%s</span> '%(r.__class__.__name__, r.primary) for r in e.get(col)]))
				else:
					if col in self.entity.validators:
						# reverse map the picklist
						vals.append({v:k for k,v in self.entity.validators[col].list.items()}[getattr(e,col)])
					else:
						vals.append(str(getattr(e,col)))
			# print(vals)
			# print(e,e.get(self.columns[-1]))
			yield ('<tr id="%d" class="%s"><td>'+'</td><td>'.join(vals)+'</td></tr>\n')%(e.id,"even" if even else "odd")
		yield '</tbody>\n'
		yield '<tfoot><tr>'
		for col in self.columns:
			if type(col)==str:
				patternvalue=dict(pattern).get(col,'')
				yield '<td><input name="pattern" value="%s"><span style="display:none">%s</span></td>'%(patternvalue,col)
		yield '</tr></tfoot>\n'
		yield '</table>\n'
		# yield nav buttons 
		yield '<form method="GET" action=".">'
		yield '<div class="buttonbar">'
		yield '<input name="start" type="hidden" value="%d">\n'%start
		for s in sortorder:
			yield '<input name="sortorder" type="hidden" value="%s,%s">\n'%s
		for f in pattern:
			yield '<input name="pattern" type="hidden" value="%s,%s">\n'%f
		yield '<input name="cacheid" type="hidden" value="%s">'%cacheid
		yield '<input name="related" type="hidden" value="%s"'%related if not related is None else ''
		yield '<p class="info">items %d-%d/%d</p>'%(start+1,start+len(entities),len(ids))
		yield '<button name="first" type="submit">First</button>\n'
		yield '<button name="previous" type="submit">Previous</button>\n'
		yield '<button name="next" type="submit">Next</button>\n'
		yield '<button name="last" type="submit">Last</button>\n'
		yield '<button name="search" type="button">Search</button>\n'
		yield '<button name="clear" type="submit">Clear</button>\n'
		yield '</div>'
		yield '</form>'
		# no name attr on the following button otherwise it may be sent as an argument!
		yield '<form method="GET" action="add">'
		yield '<input name="related" type="hidden" value="%s">'%related if not related is None else ''
		yield '<button type="submit" name="addnew">Add new</button>'
		yield '</form>'
		yield self.entity._custom().getBrowseCustomHTML('*')
		yield self.entity._custom().getBrowseCustomHTML(self.entity.__name__)
		

if __name__ == "__main__":
	
	from random import randint
	import os
	
	current_dir = os.path.dirname(os.path.abspath(__file__))

	class Entity(AbstractEntity):
		database='/tmp/browsetest.db'

	class Number(Entity):
		n = Attribute(displayname="Size")
	
	n=len(Number.listids())
	if n<100:
		for i in range(100-n):
			Number(n=randint(0,1000000))
		
	root = Browse(Number,columns=['id','n'],sortorder=[('n','asc'),('id','desc')])
	
	cherrypy.quickstart(root,config={
		'/':
		{ 'log.access_file' : os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		}
	})
		