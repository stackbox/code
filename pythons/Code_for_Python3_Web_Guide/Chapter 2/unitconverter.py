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
</head>
<body id="spreadsheet_example">
<div id="example">
	<form id="unitconversion">
	<input name="from" type="text" value="1" />
	<select name="fromunit">
		<option selected="true">inch</option>
		<option>cm</option>
	</select>
	<label for="to">=</label>
	<input name="to" type="text" readonly="true" />
	<select name="tounit">
		<option>inch</option>
		<option selected="true">cm</option>
	</select>
	<button name="convert" type="button">convert</button>
	</form>
</div>
<p id="logging">
</p>
<script type="text/javascript" src="unitconverter.js" ></script>
</body>
</html>
	'''
	
	@cherrypy.expose
	def index(self):
		return Root.convertor
	
if __name__ == "__main__":
	
	print(os.path.join(current_dir,"unitconverter.js"))
	cherrypy.quickstart(Root(),config={
		'/static':
		{ 'tools.staticdir.on':True,
		  'tools.staticdir.dir':os.path.join(current_dir,"static")
		},
		'/unitconverter.js':
		{ 'tools.staticfile.on':True,
		  'tools.staticfile.filename':os.path.join(current_dir,"unitconverter.js")
		}
	})
