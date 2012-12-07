import cherrypy

import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))

class Root(object):
	
	convertor = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<link rel="stylesheet" href="static/css/smoothness/jquery-ui-1.8.4.custom.css" type="text/css" media="screen, projection" />
<script type="text/javascript" src="static/jquery-1.4.2.js" ></script>
<script type="text/javascript" src="static/jquery-ui-1.8.4.custom.min.js" ></script>
<script type="text/javascript" src="unitconverter2.js" ></script>
</head>
<body id="spreadsheet_example">
<div id="example"></div>
<script type="text/javascript">
$("#example").unitconverter({'km_mile':1.0/0.621371192,'mile_km':0.621371192});
</script>
</body>
</html>
	'''
	
	@cherrypy.expose
	def index(self):
		return Root.convertor
	
if __name__ == "__main__":
	
	cherrypy.quickstart(Root(),config={
		'/static':
		{ 'tools.staticdir.on':True,
		  'tools.staticdir.dir':os.path.join(current_dir,"static")
		},
		'/unitconverter2.js':
		{ 'tools.staticfile.on':True,
		  'tools.staticfile.filename':os.path.join(current_dir,"unitconverter2.js")
		}
	})
