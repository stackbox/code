import cherrypy

import logon

class Root(object):

	logon = logon.Logon(path="/logon", authenticated="/", not_authenticated="/goaway")
	
	@cherrypy.expose
	def index(self):
		username=logon.checkauth('/logon')
		return '<html><body><p>Hello user <b>%s</b></p></body></html>'%username
	
	@cherrypy.expose
	def goaway(self):
		return '<html><body><h1>Not authenticated, please go away.</h1></body></html>'
	goaway._cp_config = {'tools.expires.on':True,'tools.expires.secs':0,'tools.expires.force':True}
	
	@cherrypy.expose
	def somepage(self):
		username=logon.checkauth('/logon',returntopage=True)
		return '<html><body><h1>This is some page.</h1></body></html>'
		
if __name__ == "__main__":

	import os.path
	current_dir = os.path.dirname(os.path.abspath(__file__))
	
	cherrypy.quickstart(Root(),config={
		'/': { 'log.access_file' : os.path.join(current_dir,"access.log"), 'tools.sessions.on': True },
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
		'tools.staticfile.filename':os.path.join(current_dir,"static","jquery","css","redmond","jquery-ui-1.8.1.custom.css")
		}
		}
		)
