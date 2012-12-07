import cherrypy
import json
import os
from collections import defaultdict

from logondb import LogonDB
import booksdb

# base html page is a seperate file for easy editing/ html
# syntax highlighting
with open('basepage.html') as f:
	basepage=f.read(-1)

class Books():
	def __init__(self,logon,logoffpath):
		self.logon=logon
		self.logoffpath=logoffpath

	@cherrypy.expose
	def index(self):
		username = self.logon.checkauth()
		return basepage % '<div id="booklist"></div>'
	
	@cherrypy.expose
	def list(self,offset=0,limit=10,mine=1,pattern="",_=None):
		username = self.logon.checkauth()
		userid=booksdb.checkuser(username)
		try:
			offset=int(offset)
			if offset<0 : raise ValueError("offset < 0")
		except ValueError:
			raise TypeError("offset not an integer")
		try:
			limit=int(limit)
			if limit<-1 : raise ValueError("limit < -1")
		except ValueError:
			raise TypeError("limit not an integer")
		try:
			mine=int(mine)
		except ValueError:
			raise TypeError("mine not an integer")
		if not mine in (0,1) :
			raise ValueError("mine not in (0,1)")
		if len(pattern)>100 :
			raise ValueError("length of pattern > 100")
		# show titles
		yield '<div class="columnheaders"><div class="title">Title</div><div class="author">Author</div></div>'
		# get matching books
		if mine==0 : userid=None
		n,books = booksdb.listbooks(user=userid,
			offset=offset,limit=limit,pattern=pattern)
		# yield them as a list of divs
		for b in books:
			a1=booksdb.listauthors(b)[0]
			yield '''<div id="%d" class="bookrow">
<div class="title">%s</div>
<div class="author">%s</div>
</div>'''%(b.id,b.title,a1.name)
		# yield a line of navigation buttons
		yield '''<div id="navigation">
<p id="info">Showing 
<span id="limitid">%d</span> of 
<span id="nids">%d</span> items,
 owned by <span id="owner">%s</span> starting at 
<span id="firstid">%d</span>
</p>
<div id="toolbar">
<button id="firstpage" value="First">First</button> 
<button id="previouspage" value="Previous">Prev</button>
<input id="mine" type="checkbox" %s /><label for="mine">Mine</label>
<input id="pattern" type="text" value="%s" />
<button id="nextpage" value="Next" >Next</button>
<button id="lastpage" value="Last" >Last</button>
<button id="addbook" value="Add">Add</button>
</div>
</div>'''%(limit,n,username if mine else "all",
		   offset,'checked="yes"'if mine else "", pattern)
	
	addbookform='''<div id="newbook">
<form action="addbook" method="get">
<fieldset><legend>Add new book</legend>
<input name="title" id="title" type="text" value="%(title)s" %(titleerror)s />
<label for="title">Title</label>
<input name="author" id="author" type="text" value="%(author)s" %(authorerror)s />
<label for="author">Author</label>
</fieldset>
<div class="buttonbar">
<button name="submit" type="submit" value="Add">Add</button>
<button name="cancel" type="submit" value="Cancel">Cancel</button>
</div>
</form>
<div id="errorinfo"></div>
<script>
$("#title" ).autocomplete({ source:'/books/gettitles',
							minLength:2}).focus();
$("#author").autocomplete({ source:'/books/getauthors',
							minLength:2});
</script>
</div>'''
			
	@cherrypy.expose
	def addbook(self,title=None,author=None,submit=None,cancel=None):
		username = self.logon.checkauth()
		userid=booksdb.checkuser(username)
		if not cancel is None: raise cherrypy.HTTPRedirect("/books")
		data=defaultdict(str)
		if submit is None:
			return basepage%(Books.addbookform%data)
		if title is None or author is None:
			raise cherrypy.HTTPError(400,'missing argument')
		data['title']=title
		data['author']=author
		try:
			a=booksdb.newauthor(author)
			try:
				b=booksdb.newbook(title,[a])
				booksdb.addowner(b,userid)
				raise cherrypy.HTTPRedirect("/books")
			except ValueError as e:
				data['titleerror']='class="inputerror ui-state-error" title="%s"'%str(e)
		except ValueError as e:
			data['authorerror']='class="inputerror ui-state-error" title="%s"'%str(e)
		return basepage%(Books.addbookform%data)	
			
	@cherrypy.expose
	def getauthors(self,term,_=None):
		return json.dumps(booksdb.getauthors(term))
	
	@cherrypy.expose
	def gettitles(self,term,_=None):
		titles=json.dumps(booksdb.gettitles(term))
		print('TITLES',titles)
		return titles
		
class Root(object):
	logon = LogonDB()
	books = Books(logon=logon,logoffpath="/logon/logoff")
	
	@cherrypy.expose
	def index(self):
		return Root.logon.index(returnpage='/books')

if __name__ == "__main__":
	
	current_dir = os.path.dirname(os.path.abspath(__file__))

	db='/tmp/booksweb.db'
	
	# we can subscribe more than one function
	cherrypy.engine.subscribe('start_thread', lambda thread_index: booksdb.threadinit(db))
	cherrypy.engine.subscribe('start_thread', lambda thread_index: Root.logon.connect())
	
	booksdb.threadinit(db)
	booksdb.inittable()
	
	cherrypy.quickstart(Root(),config={
		'/':
		{ 'log.access_file' : os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		},
		'/booksweb.js':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/booksweb.js"
		},
		'/logon.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/logon.css"
		},
		'/books.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/books.css"
		}
	})
		