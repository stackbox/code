'''
spreadsheet3.py is adapted to present the user with a logon screen first, before serving the spreadsheet.

it uses the default implementation of the Logon class, so the only user that will be authenticated will
be the user 'user' with the password 'secret'.

The few lines of code that had to be added are marked with the sting CHANGED
'''

import cherrypy

import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))

# CHANGED, we need to import the logon module
import logon

class Root(object):
	
	spreadsheet = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<link rel="stylesheet" href="/jquerytheme.css" type="text/css" media="screen, projection" />
<script type="text/javascript" src="/jquery.js" ></script>
<script type="text/javascript" src="/jquery-ui.js" ></script>
<script type="text/javascript" src="/static/js/jeditable.js" ></script>
<script type="text/javascript" src="/spreadsheet.js" ></script>
</head>
<body id="spreadsheet_example">
<div id="example"></div>
<p id="logging">
</p>
<script type="text/javascript">
$("#example").sheet({cols:8,rows:10});
</script>
</body>
</html>
	'''

	# CHANGED, we mount an instance of the Logon class
	logon = logon.Logon(path='/logon')
	
	@cherrypy.expose
	def index(self):
		# CHANGED, before serving the sheet, we authenticate the user. No returnpage argument is needed
		# as the defautl one is / 
		username=logon.checkauth('/logon')
		return Root.spreadsheet
	
if __name__ == "__main__":
	
	cherrypy.quickstart(Root(),config={
		# CHANGED, enable sessions
		'/': 
		{ 'tools.sessions.on': True },
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
		},
		'/spreadsheet.js':
		{ 'tools.staticfile.on':True,
		  'tools.staticfile.filename':os.path.join(current_dir,"spreadsheet.js")
		}
	})
