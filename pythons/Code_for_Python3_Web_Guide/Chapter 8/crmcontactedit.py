import os
import cherrypy

from entity import AbstractEntity, Attribute, Picklist

from browse import Browse
from display import Display

from logondb import LogonDB

db="/tmp/contactedit.db"

class Entity(AbstractEntity):
	database = db

class Contact(Entity):
	firstname = Attribute(displayname="First Name")
	lastname  = Attribute(displayname="Last Name",
							notnull=True, primary=True)
	gender    = Attribute(displayname="Gender", 
							notnull=True, validate=Picklist(
									Male=1,Female=2,Unknown=0))
	telephone = Attribute(displayname="Telephone")

with open('basepage.html') as f:
	basepage=f.read(-1)

class ContactBrowser(Browse):
	edit = Display(Contact, edit=True)
	add  = Display(Contact, add=True)
	
	@cherrypy.expose
	def index(self, _=None,
		start=0, pattern=None, sortorder=None, cacheid=None,
		next=None, previous=None, first=None, last=None,
		clear=None):
		s="".join(super().index(_, start, pattern, sortorder,
					cacheid, next,previous, first, last, clear))
		s+='''
		<script>
		$("table.entitylist tr").dblclick(function(){
				var id=$(this).attr('id');
				$("body").load('edit/?id='+id);
			});
		</script>
		'''
		return basepage%s
		
current_dir = os.path.dirname(os.path.abspath(__file__))

cherrypy.quickstart(ContactBrowser(Contact),config={
		'/':
		{ 'log.access_file' :
			os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		}
})
