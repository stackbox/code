import os
import cherrypy

from entity import AbstractEntity, Attribute
from relation import AbstractRelation

from browse import Browse
from display import Display
from editor import Editor

from logondb import LogonDB

db="/tmp/book2.db"

class Entity(AbstractEntity):
	database = db

class Relation(AbstractRelation):
	database = db

class User(Entity):
	name = Attribute(notnull=True, unique=True, displayname="Name")

class Book(Entity):
	title = Attribute(notnull=True, displayname="Title")
	isbn  = Attribute(displayname="Isbn")
	published = Attribute(displayname="Published")

class Author(Entity):
	name = Attribute(notnull=True, unique=True, displayname="Name", primary=True)

class OwnerShip(Relation):
	a = User
	b = Book

class Writer(Relation):
	a = Book
	b = Author


logon = LogonDB()
	
class AuthorBrowser(Browse):
	display = Display(Author)
	edit = Display(Author, edit=True, logon=logon)
	add = Display(Author, add=True, logon=logon)
	
class BookBrowser(Browse):
	display = Display(Book)
	edit = Display(Book, edit=True, logon=logon)
	add = Display(Book, add=True, logon=logon)

with open('basepage.html') as f:
	basepage=f.read(-1)

class Root():
	logon = logon
	books = BookBrowser(Book,columns=['title','isbn','published',Author])
	authors = AuthorBrowser(Author)
	
	@cherrypy.expose
	def index(self):
		return Root.logon.index(returnpage='../entities')
	
	@cherrypy.expose
	def entities(self):
		username = self.logon.checkauth()
		if username is None : raise HTTPRedirect('.')
		user=User.list(pattern=[('name',username)])
		if len(user) < 1 : User(name=username)
		
		return basepage%'''<div class="navigation">
		<a href="books">Books</a>
		<a href="authors">Authors</a>
		</div><div class="content">
		</div>
		<script>
		$.ajaxSetup({cache:false,type:"GET"});
		$(".navigation a").click(function (){
			//alert('click on entity');
			var rel = $(this).attr('href');
			function shiftforms(){
				//alert('shiftforms called');
				$(".content form").each(function(i,e){
					$(e).attr('action',rel+'/'+$(e).attr('action'));
					$('[type=submit]',e).bind('click',function(event){
						var f = $(this).parents('form');
						var n = $(this).attr('name');
						if (n != ''){ n = '&'+n+'='+$(this).attr('value');}
						$(".content").load(f.attr('action'), f.serialize()+n,shiftforms);
						return false;
					});
				});
			};
			// change action attributes of form elements
			$(".content").load($(this).attr('href'),shiftforms);
			return false;
		});
		</script>
		'''
cherrypy.engine.subscribe('start_thread', lambda thread_index: Root.logon.connect())
	
current_dir = os.path.dirname(os.path.abspath(__file__))

cherrypy.quickstart(Root(),config={
		'/':
		{ 'log.access_file' : os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		}
	})
		