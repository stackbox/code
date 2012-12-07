import cherrypy

import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))

from time import asctime

class Root(object):
	
	content_first = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
	'''
	content_last = '''<link rel="stylesheet" href="static/css/smoothness/jquery-ui-1.8.4.custom.css" type="text/css" media="screen, projection" />
<script type="text/javascript" src="static/jquery-1.4.2.js" ></script>
<script type="text/javascript" src="static/jquery-ui-1.8.4.custom.min.js" ></script>
</head>
<body id="spreadsheet_example">
<div id="example">
	an empty div
</div>
</body>
</html>
	'''
	
	@cherrypy.expose
	def index(self):
		title = '<title>'+asctime()+'</title>'
		return Root.content_first+title+Root.content_last
	
if __name__ == "__main__":
	
	cherrypy.quickstart(Root(),config={
		'/static':
		{ 'tools.staticdir.on':True,
		  'tools.staticdir.dir':current_dir+"/static"
		}
	})
