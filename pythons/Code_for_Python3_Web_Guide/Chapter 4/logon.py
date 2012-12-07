import cherrypy
import urllib.parse

import logging

class Logon:
	base_page = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<script type="text/javascript" src="/jquery.js" ></script>
<script type="text/javascript" src="/jquery-ui.js" ></script>
<style type="text/css" title="currentStyle">
	@import "/jquerytheme.css";
	@import "/static/css/logon.css";
</style>
</head>
<body id="logonscreen">
<div id="content">
%s
</div>
<script type="text/javascript">$("button").button({icons: {primary: 'ui-icon-power'}})</script>
</body>
</html>
'''

	# change the GET once in production: otherwise passwords may end up in the access log!
	
	# use <button> NOT <input> for submit and reset otherwise icons won't show!
	logon_screen = base_page % '''
<form class="login" action="%s/logon" method="GET">
<fieldset>
<label for="username">Username</label><input id="username" type="text" name="username" />
<script type="text/javascript">$("#username").focus()</script>
<label for="password">Password</label><input id="password" type="password" name="password" />
<input type="hidden" name="returnpage" value="%s" />
<button type="submit" class="login-button" value="Log in">Log in</button>
</fieldset>
</form>
'''

	not_authenticated = base_page % '''<h1>Login or password not correct</h1>'''

	def __init__(self,path="/logon",authenticated="/",not_authenticated="/"):
		self.path=path
		self.authenticated=authenticated
		self.not_authenticated=not_authenticated
		
	# change this to a proper check in a production environment
	@staticmethod
	def checkpass(username,password):
		if username=='user' and password=='secret': return True
		return False

	@cherrypy.expose
	def index(self,returnpage=None):
		if returnpage is None : returnpage = '' 
		return Logon.logon_screen % (self.path,urllib.parse.quote(returnpage))
	index._cp_config = {'tools.expires.on':True,'tools.expires.secs':0,'tools.expires.force':True}
	
	@cherrypy.expose
	def logon(self,username,password,returnpage='',db=':memory:'):
		returnpage = urllib.parse.unquote(returnpage)
		#logging.error("####"+returnpage+"####")
		if self.checkpass(username,password):
			cherrypy.session['authenticated']=username
			if returnpage != '':
				raise cherrypy.InternalRedirect(returnpage)
			else:
				raise cherrypy.InternalRedirect(self.authenticated)
		raise cherrypy.InternalRedirect(self.not_authenticated)
	
	@cherrypy.expose
	def logoff(self,logoffurl=None):
		cherrypy.session.delete()
		cherrypy.lib.sessions.expire()
		#cherrypy.session['authenticated']=None
		if logoffurl is None :
			raise cherrypy.InternalRedirect(self.not_authenticated)
		raise cherrypy.InternalRedirect(logoffurl)

	@staticmethod
	def checkauth(logonurl="/", returntopage=False):
		returnpage=''
		if returntopage:
			returnpage='?returnpage='+cherrypy.request.script_name+cherrypy.request.path_info
			#returnpage='?returnpage='+cherrypy.request.base+cherrypy.request.script_name+cherrypy.request.path_info
			#returnpage='?returnpage='+cherrypy.request.path_info
		
		auth = cherrypy.session.get('authenticated',None)
		if auth == None : raise cherrypy.HTTPRedirect(logonurl+returnpage)
		return auth

