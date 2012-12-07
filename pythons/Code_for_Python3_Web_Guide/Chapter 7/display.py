from collections import OrderedDict
import cherrypy
from entity import AbstractEntity

class Display():
	
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
	def index(self,id=None,_=None,add=None,edit=None,**kw):
		kv=OrderedDict()
		submitbutton=""
		if edit or add:
			if (edit and add):
				raise HTTPError(500)
			if not self.logon is None:
				username=self.logon.checkauth()
				print(username)
				if username is None:
					raise HTTPRedirect('/')
			if edit:
				e=self.entity(id=id)
				e.update(**kw)
				yield '<div class="editresult" id="%s">%s</div>'%(str(e.id),str(e.id))
				return
			elif add:
				e=self.entity(**kw)
				yield '<div class="addresult" id="%s">%s</div>'%(str(e.id),str(e.id))
				return
		action="display"		
		if not id is None:
			e=self.entity(id=id)
			for c in self.columns:
				if c in self.entity.columns:
					kv[self.entity.displaynames[c]]=(c,getattr(e,c))
				elif issubclass(e,AbstractEntity):
					kv[c.__name__]=(c.__name__,repr(e.get(c)))
			if self.edit:
				action="edit"
				submitbutton='<input type="hidden" name="id" value="%s"><input type="submit" name="edit" value="Edit">'%id
		elif self.add:
			action="add"
			for c in self.columns:
				if c in self.entity.columns:
					kv[self.entity.displaynames[c]]=(c,"")
				elif issubclass(e,AbstractEntity):
					kv[c.__name__]=(c.__name__,"default list")
			submitbutton='<input type="submit" name="add" value="Add">'
		else:
			yield "cannot happen id=%s, edit=%s, add=%s, self.edit=%s, self.add=%s"%(id,edit,add,self.edit,self.add)
		yield '<form action="%s">'%action
		for k,v in kv.items():
			yield '<label for="%s">%s</label><input name="%s" type="text" value="%s">'%(v[0],k,v[0],v[1])
		yield submitbutton
		yield "</form>"