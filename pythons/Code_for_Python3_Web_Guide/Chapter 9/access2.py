import os
import cherrypy

from rbacentity import AbstractEntity, Attribute, Picklist, AbstractRelation

from browse import Browse
from display import Display

from logondb import LogonDB

db="/tmp/access2.db"

class Entity(AbstractEntity):
	database = db
	
	userentity = None
	logon = None
	
	@classmethod
	def setUserEntity(cls,entity):
		cls.userentity = entity
	
	@classmethod
	def getUserEntity(cls):
		return cls.userentity
	
	@classmethod
	def setLogon(cls,logon):
		cls.logon = logon
	
	@classmethod
	def getAuthenticatedUsername(cls):
		if cls.logon :
			return cls.logon.checkauth()
		return None
	
	def isallowed(self,operation):
		user = self.getUserEntity().list(
			pattern=[('name',self.getAuthenticatedUsername())])[0]
		entity = self.__class__.__name__
		print(operation,user,entity)
		if user.name == 'admin' :
			return True
		roles = user.getRole()
		if len(roles):
			role = roles[0]
			permissions = role.getPermission()
			for p in permissions :
				print(p)
				if p.entity == entity:
					print('>>>',p.operation,p.level)
					if p.operation=='*' or p.operation==operation:
						print('>>> operation match')
						if p.level == 0 :
							print('>>> all')
							return True
						elif p.level == 1:
							print('>>> owner')
							# hard coded Owner === User
							for owner in self.getUser():
								if user.id == owner.id :
									return True
			print('end of permissions for',user)
		else:
			print('no roles for',user)
		return False
		
	def update(self,**kw):
		if self.isallowed('update'):
			super().update(**kw)
			print('--- updated')
		else:
			print('!!!not updated')
			
class Relation(AbstractRelation):
	database = db

class User(Entity):
	name = Attribute(notnull=True, unique=True, displayname="Name", primary=True)

class Account(Entity):
	name = Attribute(notnull=True, displayname="Name", primary=True)
	
class OwnerShip(Relation):
	a = User
	b = Account

class UserRoles(Relation):
	a = User
	b = User._rbac().getRole()
	relation_type = "N:1"

logon = LogonDB()

Entity.setUserEntity(User)
Entity.setLogon(logon)	
	
class AccountBrowser(Browse):
	edit = Display(Account, edit=True, logon=logon, columns=Account.columns+[User])
	add = Display(Account, add=True, logon=logon, columns=Account.columns+[User])
	
class UserBrowser(Browse):
	edit = Display(User, edit=True, logon=logon, columns=User.columns+[User._rbac().getRole()])
	add = Display(User, add=True, logon=logon, columns=User.columns+[User._rbac().getRole()])

class RoleBrowser(Browse):
	edit = Display(User._rbac().getRole(), edit=True, logon=logon)
	add = Display(User._rbac().getRole(), add=True, logon=logon)

class PermissionBrowser(Browse):
	edit = Display(User._rbac().getPermission(), edit=True, logon=logon, columns=User._rbac().getPermission().columns+[User._rbac().getRole()])
	add = Display(User._rbac().getPermission(), add=True, logon=logon, columns=User._rbac().getPermission().columns+[User._rbac().getRole()])

with open('basepage.html') as f:
		basepage=f.read(-1)

class Root():
	logon = logon
	user = UserBrowser(User, columns=User.columns+[User._rbac().getRole()])
	account = AccountBrowser(Account,columns=Account.columns+[User])
	role = RoleBrowser(User._local.rbac.getRole())
	permission = PermissionBrowser(User._local.rbac.getPermission(), columns=User._rbac().getPermission().columns+[User._rbac().getRole()])
	
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
		<a href="role">Roles</a>
		<a href="permission">Permissions</a>
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
		