import os
import cherrypy

from entity1 import AbstractEntity, Attribute, Picklist, AbstractRelation

from browse1 import Browse
from display1 import Display

from logondb import LogonDB

db="/tmp/access1.db"

logon = LogonDB()

from permissions1 import isallowed

class Entity(AbstractEntity):
	database = db
	
	def update(self,**kw):
		if isallowed('update', self, logon.checkauth(),
						self.getUser()):
			super().update(**kw)
		else:
			print('access violation')

class Relation(AbstractRelation):
	database = db

class User(Entity):
	name = Attribute(notnull=True, unique=True,
		displayname="Name", primary=True)

class Account(Entity):
	name = Attribute(notnull=True, displayname="Name",
		primary=True)
	
class OwnerShip(Relation):
	a = User
	b = Account
	
class AccountBrowser(Browse):
	edit = Display(Account, edit=True, logon=logon,
		columns=Account.columns+[User])
	add  = Display(Account, add=True, logon=logon, 
		columns=Account.columns+[User])
	
class UserBrowser(Browse):
	edit = Display(User, edit=True, logon=logon)
	add = Display(User, add=True, logon=logon)
	
with open('basepage.html') as f:
		basepage=f.read(-1)

class Root():
	logon = logon
	account = AccountBrowser(Account,columns=Account.columns+[User])
	user = UserBrowser(User)
	

	@cherrypy.expose
	def index(self):
		return Root.logon.index(returnpage='../entities')
	
	@cherrypy.expose
	def entities(self):
		username = self.logon.checkauth()
		if username is None : raise HTTPRedirect('.')
		user=User.list(pattern=[('name',username)])
		if len(user) < 1 : User(name=username) # may raise an exception here?
		
		return basepage%'''<div class="navigation">
		<a href="account">Accounts</a>
		<a href="user">Users</a>
		</div><div class="content">
		</div>
		<script src="/browse.js"></script>
		'''
cherrypy.engine.subscribe('start_thread', lambda thread_index: Root.logon.connect())
	
current_dir = os.path.dirname(os.path.abspath(__file__))

cherrypy.quickstart(Root(),config={
		'/':
		{ 'log.access_file' : os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		},
		'/browse.js':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/browse.js"
		},
		'/base.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/base.css"
		}
	})
		