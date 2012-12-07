from collections import OrderedDict
from itertools import takewhile,dropwhile
from re import compile,sub,IGNORECASE
import json
from xml.sax.saxutils import escape,unescape
import cherrypy
from rbacentity import AbstractEntity,Picklist


class Display():
	
	finaladd = compile(r'/?add/?$')
	
	def __init__(self, entity, edit=False, add=False, logon=None, columns=None):
		self.entity = entity
		self.edit = edit
		self.add = add
		self.logon = logon
		if columns is None:
			self.columns = entity.columns
		else:
			self.columns = columns
	
	@cherrypy.expose
	def index(self,id=None,_=None,add=None,edit=None,related=None,**kw):
		mount = cherrypy.request.path_info
		# print('MMMMMMM',mount)
		if not id is None : id = int(id) # the only attr that must be an integer!
		kv=[]
		submitbutton=""
		if edit or add:
			if (edit and add):
				raise HTTPError(500)
			if not self.logon is None:
				username=self.logon.checkauth()
				# print(username)
				if username is None:
					raise HTTPRedirect('/')
			if add:
				# print('add add add add')
				attr={}
				cols={}
				relations={c.__name__:c for c in self.columns if type(c)!=str}
				# print('related',related)
				for k,v in kw.items():
					# print('>>>',k,v)
					if not k in self.entity.columns:
						attr[k]=v
						if not k in relations :
							raise KeyError(k,'not a defined relation')
					else:
						cols[k]=v
				# print(attr,cols)
				e=self.entity(**cols)
				for k,v in attr.items():
					if v != None and v != '':  #only take action for non empty relations arguments
						relentity = relations[k]
						primary = relentity.primaryname
						rels = relentity.listids(pattern=[(primary,v)])
						if len(rels):
							r = relentity(id=rels[0])
						else:
							r = relentity(**{primary:v})
						# print('ADDING %s to %s'%(str(r),str(e)))
						e.add(r)
				#yield '<div class="addresult" id="%s">%s</div>'%(str(e.id),str(e.id))
				#return
				if not related is None and related != '':
					r=related.split(',')
					print('>>>>>>>>>',r[0],e.relclass[r[0]])
					re=e.relclass[r[0]](id=int(r[1]))
					e.add(re)
					
				redit = sub(Display.finaladd,'',mount)
				print('NNNNNNNNNNNNNN',redit,related)
				raise cherrypy.HTTPRedirect(redit)
			elif edit:
				e=self.entity(id=id)
				e.update(**kw)
				#yield '<div class="editresult" id="%s">%s</div>'%(str(e.id),str(e.id))
				#return
				raise cherrypy.HTTPRedirect(mount.replace('edit','').replace('//','/'))
		action="display"
		autocomplete=''
		if not id is None:
			e=self.entity(id=id)
			# conn = e.__class__._connect()
			# cursor = conn.cursor()
			# cursor.execute('select Account_id from Contacts where Contact_id = ?',(e.id,))
			# print(e.id,type(e.id),[d[0] for d in cursor.description])
			# for r in cursor:
				# print(list(r))
			
			# print(e,e.get(self.columns[-1]))
			for c in self.columns:
				# if hasattr(c,'__name__'):
				# 	print('DISPLAY',c,c.__name__,issubclass(c,AbstractEntity))
				if c in self.entity.columns:
					kv.append('<label for="%s">%s</label>'%(c,self.entity.displaynames[c]))
					displayclass=""
					print(self.entity.displayclasses)
					try:
						displayclass = self.entity.displayclasses[c]
					except KeyError:
						pass
					if c in self.entity.validators and type(self.entity.validators[c])==Picklist:
						kv.append('<select name="%s" class="%s">'%(c,displayclass))
						kv.extend(['<option %s>%s</option>'%("selected" if v==getattr(e,c) else "",k) for k,v in self.entity.validators[c].list.items()])
						kv.append('</select>')
					else:
						val=getattr(e,c)
						if self.entity.htmlescape[c] :
							val=escape(val,{'"':'&quot;','\n':'&#xa;'})
						line='<input type="text" name="%s" value="%s" class="%s">'%(c,val,displayclass)
						print(line)
						kv.append(line)
				elif issubclass(c,AbstractEntity):
					kv.append('<label for="%s">%s</label>'%(c.__name__,c.__name__))
					# conn = e.__class__._connect()
					# cursor = conn.cursor()
					# cursor.execute('select Account_id from Contacts where Contact_id = ?',(e.id,))
					# print('aaaa',e.id,[r[0] for r in cursor])
					v=",".join([r.primary for r in e.get(c)])
					kv.append('<input type="text" name="%s" value="%s">'%(c.__name__,v))
					autocomplete += '$("input[name=%s]").autocomplete({source:"%s",minLength:2});'%(c.__name__,mount+'autocomplete?entity='+c.__name__)
			yield self.related_entities(e)
			if self.edit:
				action='edit'
				submitbutton='<input type="hidden" name="id" value="%s"><input type="hidden" name="related" value="%s,%s"><input type="submit" name="edit" value="Edit">'%(id,self.entity.__name__,id)
		elif self.add:
			action='add'
			for c in self.columns:
				print(']]]]',c,self.entity.columns)
				if c in self.entity.columns:
					displayclass=""
					print(self.entity.displayclasses)
					try:
						displayclass = self.entity.displayclasses[c]
					except KeyError:
						pass
					kv.append('<label for="%s">%s</label>'%(c,self.entity.displaynames[c]))
					if c in self.entity.validators and type(self.entity.validators[c])==Picklist:
						kv.append('<select name="%s" class="%s">'%(c,displayclass))
						kv.extend(['<option>%s</option>'%v for v in self.entity.validators[c].list.keys()])
						kv.append('</select>')
					else: # some way to set a default here?	
						kv.append('<input type="text" name="%s" class="%s">'%(c,displayclass))
				elif c=="related":
					pass
				elif issubclass(c,AbstractEntity):
					kv.append('<label for="%s">%s</label>'%(c.__name__,c.__name__))
					kv.append('<input type="text" name="%s">'%c.__name__)
					autocomplete += '$("input[name=%s]").autocomplete({source:"%s",minLength:2});'%(c.__name__,mount+'autocomplete?entity='+c.__name__)
			submitbutton='<input type="hidden" name="related" value="%s"><input type="submit" name="add" value="Add">'%(related if not related is None else '')
		else:
			yield "cannot happen id=%s, edit=%s, add=%s, self.edit=%s, self.add=%s"%(id,edit,add,self.edit,self.add)
		yield '<form action="%s">'%action
		for k in kv:
			yield k
		yield submitbutton
		yield "</form>"
		yield '<script>'+autocomplete+'</script>'
		yield '<script src="/display.js"></script>'
		yield self.entity._custom().getDisplayCustomHTML('*')
		yield self.entity._custom().getDisplayCustomHTML(self.entity.__name__)
		
	@cherrypy.expose
	def autocomplete(self,entity,term,_=None):
		entity={c.__name__:c for c in self.columns if type(c)!=str}[entity]
		names=entity.getcolumnvalues(entity.primaryname)
		pat=compile(term,IGNORECASE)
		return json.dumps(list(takewhile(lambda x:pat.match(x),dropwhile(lambda x:not pat.match(x),names))))

	@staticmethod
	def related_link(re,e):
		return '<li id="%s" class="%s" ref="%s">%s</li>'%(
			e.id,e.__class__.__name__,re.lower(),re)
	
	def related_entities(self,e):
		r=['<div class="related_entities"><h3>Related</h3><ul>']
		if hasattr(e.__class__,'reltype'):
			r.extend([self.related_link(re,e) 
				for re,rt in e.__class__.reltype.items() 
				if (rt == '1:N' or rt == 'N:N')])
		r.append('</ul></div>')
		# .param() is used to pass arguments as a string to prevent POST
		r.append('''
		<script>
			$('div.related_entities li').click(function(){
				var rel=$(this).attr("ref");
				var related=$("input[name=related]").val();
				$(".content").load(rel,
					$.param({
						"pattern" : $(this).attr("class") +
									"," + $(this).attr("id"),
						"related": related}),
					function(){shiftforms(rel)});
			});
		</script>''')
		return "\n".join(r)
	
	@cherrypy.expose
	def delete(self,id=None,_=None):
		if not self.logon is None:
			username=self.logon.checkauth()
			if not username is None:
				e=self.entity(id=id);
				print('DELETE',e)
				e.delete();
		return 'ok'