import os
import cherrypy

from rbacentity import AbstractEntity, Attribute, Picklist, AbstractRelation

from browse import Browse
from display import Display

from logondb import LogonDB

db="/tmp/crm5.db"

class Entity(AbstractEntity):
	database = db

class Relation(AbstractRelation):
	database = db

class User(Entity):
	name = Attribute(notnull=True, unique=True, displayname="Name", primary=True)

class Account(Entity):
	name = Attribute(notnull=True, displayname="Name", primary=True)
	created = Attribute(notnull=True, default="CURRENT_DATE", displayclass="mb-date")
	
class Contact(Entity):
	firstname = Attribute(displayname="First Name")
	lastname = Attribute(displayname="Last Name", notnull=True, primary=True)
	gender = Attribute(displayname="Gender", notnull=True, validate=Picklist(Male=1,Female=2,Unknown=0))
	telephone = Attribute(displayname="Telephone")

class Address(Entity):
	address = Attribute(displayname="Address", notnull=True, primary=True)
	city = Attribute(displayname="City")
	zipcode = Attribute(displayname="Zip")
	country = Attribute(displayname="Country")
	telephone = Attribute(displayname="Telephone")

class OwnerShip(Relation):
	a = User
	b = Account

class Contacts(Relation):
	a = Account
	b = Contact

class AccountAddress(Relation):
	a = Account
	b = Address
	relation_type = 'N:N'
	
class ContactAddress(Relation):
	a = Contact
	b = Address
	relation_type = 'N:N'
	
logon = LogonDB()
	
class AccountBrowser(Browse):
	display = Display(Account)
	edit = Display(Account, edit=True, logon=logon, columns=Account.columns+[Address,User])
	add = Display(Account, add=True, logon=logon, columns=Account.columns+[Address,User])
	
class UserBrowser(Browse):
	display = Display(User)
	edit = Display(User, edit=True, logon=logon)
	add = Display(User, add=True, logon=logon)
	
class ContactBrowser(Browse):
	display = Display(Contact)
	edit = Display(Contact, edit=True, logon=logon, columns=Contact.columns+[Account,Address])
	add = Display(Contact, add=True, logon=logon, columns=Contact.columns+[Account,Address])

class AddressBrowser(Browse):
	display = Display(Address)
	edit = Display(Address, edit=True, logon=logon)
	add = Display(Address, add=True, logon=logon)

displaycustom = User._custom().getDisplayCustomization()
browsecustom = User._custom().getBrowseCustomization()

class DisplayCustomizationBrowser(Browse):
	edit = Display(displaycustom, edit=True, logon=logon)
	add = Display(displaycustom, add=True, logon=logon)

class BrowseCustomizationBrowser(Browse):
	edit = Display(browsecustom, edit=True, logon=logon)
	add = Display(browsecustom, add=True, logon=logon)
	
with open('basepage.html') as f:
	basepage=f.read(-1)

class Root():
	logon   = logon
	user    = UserBrowser(User)
	account = AccountBrowser(Account,columns=Account.columns+[User,Address,Contact])
	contact = ContactBrowser(Contact,columns=Contact.columns+[Address,Account])
	address = AddressBrowser(Address)
	displaycustomization = DisplayCustomizationBrowser(displaycustom,columns=['entity','description'])
	browsecustomization = BrowseCustomizationBrowser(browsecustom,columns=['entity','description'])
	
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
		<a href="user">Users</a>
		<a href="displaycustomization">Customize Item</a>
		<a href="browsecustomization">Customize List</a>
		<a href="account">Accounts</a>
		<a href="contact">Contacts</a>
		<a href="address">Addresses</a>
		</div><div class="content">
		</div>
		<script src="/browse.js" type="text/javascript"></script>
		'''

cherrypy.config.update({'server.thread_pool':1})

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
		'/display.js':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/display.js"
		},
		'/base.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/base.css"
		}
	})
		