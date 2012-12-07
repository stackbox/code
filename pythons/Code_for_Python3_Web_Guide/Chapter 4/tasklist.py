import cherrypy

from taskapp import TaskApp
from logondb import LogonDB

import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))

theme = "smoothness"

class Root(object):
	logon = LogonDB()
	task = TaskApp(dbpath='/tmp/taskdb.db',logon=logon,logoffpath="/logon/logoff")
	
	@cherrypy.expose
	def index(self):
		return Root.logon.index(returnpage='/task')
	
if __name__ == "__main__":

	Root.logon.initdb()
	
	def connect(thread_index): 
		Root.task.connect()
		Root.logon.connect()
		
	# Tell CherryPy to call "connect" for each thread, when it starts up 
	cherrypy.engine.subscribe('start_thread', connect)

	cherrypy.quickstart(Root(),config={
		'/':
		{ 'log.access_file' : os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		},
		'/static':
		{ 'tools.staticdir.on':True,
		'tools.staticdir.dir':os.path.join(current_dir,"static")
		},
		'/jquery.js':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':os.path.join(current_dir,"static","jquery","jquery-1.4.2.js")
		},
		'/jquery-ui.js':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':os.path.join(current_dir,"static","jquery","jquery-ui-1.8.1.custom.min.js")
		},
		'/jquerytheme.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':os.path.join(current_dir,"static","jquery","css",theme,"jquery-ui-1.8.4.custom.css")
		},
		'/images':
		{ 'tools.staticdir.on':True,
		'tools.staticdir.dir':os.path.join(current_dir,"static","jquery","css",theme,"images")
		}
	})
