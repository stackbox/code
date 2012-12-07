import os
import cherrypy

from entity import AbstractEntity, Attribute, Picklist, AbstractRelation

from browse import Browse
from display import Display

from logondb import LogonDB

db="/tmp/crm1.db"

class Entity(AbstractEntity):
	database = db

class Relation(AbstractRelation):
	database = db

class User(Entity):
	name = Attribute(notnull=True, unique=True,
						displayname="Name", primary=True)

class Account(Entity):
	name = Attribute(notnull=True,
						displayname="Name", primary=True)
	
class Contact(Entity):
	firstname = Attribute(displayname="First Name")
	lastname  = Attribute(displayname="Last Name",
							notnull=True, primary=True)
	gender    = Attribute(displayname="Gender",
							notnull=True,
							validate=Picklist(
											Male=1,
											Female=2,
											Unknown=0))
	telephone = Attribute(displayname="Telephone")

class Address(Entity):
	address   = Attribute(displayname="Address",
							notnull=True, primary=True)
	city      = Attribute(displayname="City")
	zipcode   = Attribute(displayname="Zip")
	country   = Attribute(displayname="Country")
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
	
class ContactAddress(Relation):
	a = Contact
	b = Address
	
logon = LogonDB()
	
class AccountBrowser(Browse):
	display = Display(Account)
	edit = Display(Account, edit=True, logon=logon,
					columns=Account.columns+[Address,User])
	add = Display(Account, add=True, logon=logon,
					columns=Account.columns+[Address,User])
	
class UserBrowser(Browse):
	display = Display(User)
	edit = Display(User, edit=True, logon=logon)
	add = Display(User, add=True, logon=logon)
	
class ContactBrowser(Browse):
	display = Display(Contact)
	edit = Display(Contact, edit=True, logon=logon,
					columns=Contact.columns+[Account,Address])
	add = Display(Contact, add=True, logon=logon,
					columns=Contact.columns+[Account,Address])

class AddressBrowser(Browse):
	display = Display(Address)
	edit = Display(Address, edit=True, logon=logon)
	add = Display(Address, add=True, logon=logon)
	
with open('basepage.html') as f:
	basepage=f.read(-1)

class Root():
	logon   = logon
	user    = UserBrowser(User)
	account = AccountBrowser(Account,
				columns=Account.columns+[User,Address,Contact])
	contact = ContactBrowser(Contact,
				columns=Contact.columns+[Address,Account])
	address = AddressBrowser(Address)
	
	@cherrypy.expose
	def index(self):
		return Root.logon.index(returnpage='../entities')
	
	@cherrypy.expose
	def entities(self):
		username = self.logon.checkauth()
		if username is None :
			raise HTTPRedirect('.')
		
		user=User.list(pattern=[('name',username)])
		if len(user) < 1 :
			User(name=username)
		
		return basepage%'''
		<div class="navigation">
			<a href="user">Users</a>
			<a href="account">Accounts</a>
			<a href="contact">Contacts</a>
			<a href="address">Addresses</a>
		</div>
		<div class="content">
		</div>
		<script>
		$.ajaxSetup({cache:false,type:"GET"});
		
		function shiftforms(rel){
				//alert('shiftforms called '+rel);
				$(".content form").each(function(i,e){
					$(e).attr('action',rel+'/'+$(e).attr('action'));
					$('[type=submit]',e).bind('click',function(event){
						var f = $(this).parents('form');
						var n = $(this).attr('name');
						if (n != ''){ n = '&'+n+'='+$(this).attr('value');}
						$(".content").load(f.attr('action'), f.serialize()+n,function(){shiftforms(rel)});
						return false;
					});
				});
			};
		
		function edit(rel,t){
				var id=$(t).attr('id');
				// this one points to the corrected relative url, e.g.  contacts/.
				var act=$(".content form").first().attr('action');
				act=act.replace(/\/\.$/,'/edit?id=')
				//alert('oink2!'+act+id);
				$(".content").load(act+id,function(){shiftforms(rel)});
			};
			
		$(".navigation a").click(function (){
			//alert('click on entity');
			var rel = $(this).attr('href');
			
			// change action attributes of form elements
			$(".content").load($(this).attr('href'),function(){shiftforms(rel)});
			
			// create a named function in order to be able to remove it again by name
			function reledit(){edit(rel,this)};
			
			$("table.entitylist tr").die('dblclick');
			$("table.entitylist tr").live('dblclick',reledit);
			
			$("table.entitylist tr").live('click',function(){
				$(this).toggleClass("ui-state-highlight").toggleClass("selected");
			});
			
			return false;
		});
		</script>
		'''

cherrypy.config.update({'server.thread_pool':1})

cherrypy.engine.subscribe('start_thread',
	lambda thread_index: Root.logon.connect())
	
current_dir = os.path.dirname(os.path.abspath(__file__))

cherrypy.quickstart(Root(),config={
		'/':
		{ 'log.access_file' :
			os.path.join(current_dir,"access.log"),
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
		