from collections import OrderedDict
from itertools import takewhile,dropwhile
from re import compile,sub,IGNORECASE
import json
import cherrypy
from entity import AbstractEntity,Picklist

class Display():
	
	finaladd = compile(r'/?add/?$')
	
	def __init__(self, entity, edit=False, add=False,
					logon=None, columns=None):
		self.entity = entity
		self.edit = edit
		self.add = add
		self.logon = logon
		if columns is None:
			self.columns = entity.columns
		else:
			self.columns = columns
	
	@cherrypy.expose
	def index(self, id=None, _=None,
				add=None, edit=None, related=None, **kw):
		mount = cherrypy.request.path_info
		if not id is None :
			id = int(id)
		kv=[]
		submitbutton=""
		if edit or add:
			if (edit and add):
				raise HTTPError(500)
			if not self.logon is None:
				username=self.logon.checkauth()
				if username is None:
					raise HTTPRedirect('/')
			if add:
				attr={}
				cols={}
				relations={c.__name__:c for c in self.columns 
							if type(c)!=str}
				for k,v in kw.items():
					if not k in self.entity.columns:
						attr[k]=v
						if not k in relations :
							raise KeyError(k,
										'not a defined relation')
					else:
						cols[k]=v
				e=self.entity(**cols)
				for k,v in attr.items():
					if v != None and v != '':
						relentity = relations[k]
						primary = relentity.primaryname
						rels = relentity.listids(
							pattern=[(primary,v)])
						if len(rels):
							r = relentity(id=rels[0])
						else:
							r = relentity(**{primary:v})
						e.add(r)
				
				if not related is None and related != '':
					r=related.split(',')
					re=e.relclass[r[0]](id=int(r[1]))
					e.add(re)
					
				redit = sub(Display.finaladd,'',mount)
				raise cherrypy.HTTPRedirect(redit)
			elif edit:
				e=self.entity(id=id)
				e.update(**kw)
				raise cherrypy.HTTPRedirect(
					mount.replace('edit','').replace('//','/'))
		
		action="display"
		autocomplete=''
		if not id is None:
			e=self.entity(id=id)
			for c in self.columns:
				if c in self.entity.columns:
					kv.append('<label for="%s">%s</label>'%
								(c,self.entity.displaynames[c]))
					if c in self.entity.validators and type(
							self.entity.validators[c])==Picklist:
						kv.append('<select name="%s">'%c)
						kv.extend(['<option %s>%s</option>'%
							("selected" if v==getattr(e,c)
								else "",k) 
							for k,v in self.entity.validators[c]
							.list.items()])
						kv.append('</select>')
					else:
						kv.append(
					'<input type="text" name="%s" value="%s">'%
						(c,getattr(e,c)))
				elif issubclass(c,AbstractEntity):
					kv.append(
					'<label for="%s">%s</label>'%
					(c.__name__,c.__name__))
					v=",".join([r.primary for r in e.get(c)])
					kv.append(
					'<input type="text" name="%s" value="%s">'%
					(c.__name__,v))
					autocomplete += '''
	$("input[name=%s]").autocomplete({source:"%s",minLength:2});
					'''%(c.__name__,
						 mount+'autocomplete?entity='+c.__name__)
			yield self.related_entities(e)
			if self.edit:
				action='edit'
				submitbutton='''
				<input type="hidden" name="id" value="%s">
				<input type="hidden" name="related" value="%s,%s">
				<input type="submit" name="edit" value="Edit">
				'''%(id,self.entity.__name__,id)
		elif self.add:
			action='add'
			for c in self.columns:
				if c in self.entity.columns:
					kv.append('<label for="%s">%s</label>'%(
						c,self.entity.displaynames[c]))
					if c in self.entity.validators and type(
							self.entity.validators[c])==Picklist:
						kv.append('<select name="%s">'%c)
						kv.extend(['<option>%s</option>'%v 
							for v in self.entity.validators[c].
								list.keys()])
						kv.append('</select>')
					else:
						kv.append('<input type="text" name="%s">'
									%c)
				elif c=="related":
					pass
				elif issubclass(c,AbstractEntity):
					kv.append('<label for="%s">%s</label>'%
						(c.__name__,c.__name__))
					kv.append('<input type="text" name="%s">'%
						c.__name__)
					autocomplete += '''
	$("input[name=%s]").autocomplete({source:"%s",minLength:2});
					'''%(c.__name__,
						 mount+'autocomplete?entity='+c.__name__)
			submitbutton='''
			<input type="hidden" name="related" value="%s">
			<input type="submit" name="add" value="Add">
			'''%related
		else:
			yield """cannot happen
			id=%s, edit=%s, add=%s, self.edit=%s, self.add=%s
			"""%(id,edit,add,self.edit,self.add)
		yield '<form action="%s">'%action
		for k in kv:
			yield k
		yield submitbutton
		yield "</form>"
		yield '<script>'+autocomplete+'</script>'
		
	@cherrypy.expose
	def autocomplete(self, entity, term, _=None):
		entity={c.__name__:c for c in self.columns 
			if type(c)!=str}[entity]
		names=entity.getcolumnvalues(entity.primaryname)
		pat=compile(term,IGNORECASE)
		return json.dumps(list(takewhile(lambda x:pat.match(x),
					dropwhile(lambda x:not pat.match(x),names))))

	@staticmethod
	def related_link(re,e):
		return '<li id="%s" class="%s" ref="%s">%s</li>'%(e.id,
							e.__class__.__name__,re.lower(),re)
	
	def related_entities(self,e):
		r=['<div class="related_entities"><h3>Related</h3><ul>']
		r.extend([self.related_link(re,e) 
			for re,rt in e.__class__.reltype.items() 
			if rt == '1:N'])
		r.append('</ul></div>')
		# .param() is used to pass arguments as a string to prevent POST
		r.append('''
		<script>
		$('div.related_entities li').click(function(){
			var rel=$(this).attr("ref");
			var related=$("input[name=related]").val();
			$(".content").load(rel,
			$.param({"pattern":
			   $(this).attr("class")+","+$(this).attr("id"),
			  "related":related}),
			function(){shiftforms(rel)});
		});
		</script>''')
		return "\n".join(r)