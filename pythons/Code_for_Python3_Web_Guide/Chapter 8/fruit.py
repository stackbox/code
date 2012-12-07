import os
import cherrypy

from entity import AbstractEntity, Attribute, Picklist

from browse import Browse
from display import Display

from logondb import LogonDB

db="/tmp/fruits.db"

class Entity(AbstractEntity):
	database = db

class Fruit(Entity):
	name  = Attribute(displayname="Name")
	color = Attribute(displayname="Color",
		notnull = True,
		validate= Picklist([('Yellow',1),('Green',2),('Orange',0)]))
	taste = Attribute(displayname="Taste",
		notnull = True,
		validate= Picklist(Sweet=1,Sour=2))
	
class FruitBrowser(Browse):
	edit = Display(Fruit, edit=True)
	add  = Display(Fruit, add=True)

current_dir = os.path.dirname(os.path.abspath(__file__))

cherrypy.quickstart(FruitBrowser(Fruit),config={
		'/':
		{ 'log.access_file' : os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		}
})
		