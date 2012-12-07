import cherrypy

import os.path

import logon
import task

current_dir = os.path.dirname(os.path.abspath(__file__))

theme = "smoothness"

class Root(object):
	task = task.Task(logoffpath="/logon/logoff")

	logon = logon.Logon(path="/logon", authenticated="/task", not_authenticated="/")
	
	@cherrypy.expose
	def index(self):
		return Root.logon.index()
	
if __name__ == "__main__":

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
