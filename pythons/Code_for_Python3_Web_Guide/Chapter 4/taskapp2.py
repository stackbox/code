import cherrypy
import json

import os.path
from datetime import date

import logondb
from tasklistdb import TaskDB

base_page = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<script type="text/javascript" src="/jquery.js" ></script>
<script type="text/javascript" src="/jquery-ui.js" ></script>
<style type="text/css" title="currentStyle">
	@import "/static/css/tasklist.css";
	@import "/jquerytheme.css";
</style>
<script type="text/javascript" src="/static/js/sort.js" ></script>
<script type="text/javascript" src="/static/js/tooltip.js" ></script>
<script type="text/javascript" src="/static/js/tasklistajax2.js" ></script>
</head>
<body id="%s">
<div id="content">
%s
</div>
</body>
</html>
'''

current_dir = os.path.dirname(os.path.abspath(__file__))

class TaskApp(object):

	def __init__(self,dbpath,logon,logoffpath):
		self.logon=logon
		self.logoffpath=logoffpath
		self.taskdb=TaskDB(dbpath)

	def connect(self):
		self.taskdb.connect()
		
	@cherrypy.expose
	def index(self):
		username = self.logon.checkauth()
		content = ['<div class="header">Tasklist for user <span class="highlight">%s</span><button type="submit" name="logoffurl" class="logoff-button" value="%s">Log off</button></div>'%(username,self.logoffpath),
				'<div class="taskheader"><div class="left">Due date</div><div class="middle">Description</div><div class="right">Completed</div></div>',
				'<div id="items" class="ui-widget-content">',
				'</div>',
				'<div class="item newitem">',
				'<input type="text" class="duedate left editable-date tooltip" name="duedate" title="click for a date" />',
				'<input type="text" class="description middle tooltip" title="click to enter a description" name="description"/>',
				'<button type="submit" class="add-button" name="add" value="Add" >Add</button>',
				'</div>']
		return base_page%('itemlist',"".join(content))

	@cherrypy.expose
	def list(self,_=None):
		username = self.logon.checkauth()
		tasks = []
		for t in self.taskdb.list(username):
			task=self.taskdb.retrieve(username,t)
			tasks.append('''<div class="item %s">
			<input type="text" class="duedate left" name="duedate" value="%s" readonly="readonly" />
			<input type="text" class="description middle" name="description" value="%s" readonly="readonly" />
			<input type="text" class="completed right editable-date tooltip" title="click to select a date, then click done" name="completed" value="%s" />
			<input type="hidden" name="id" value="%s" />
			<button type="submit" class="done-button" name="done" value="Done" >Done</button>
			<button type="submit" class="del-button" name="delete" value="Del" >Del</button>
			</div>'''%('notdone' if task.completed==None else 'done',task.duedate,task.description,task.completed,task.id))
		return '\n'.join(tasks)

	@cherrypy.expose
	def add(self,description,duedate,_=None):
		username = self.logon.checkauth()
		task=self.taskdb.create(user=username,description=description,duedate=duedate)
		return 'ok'

	@cherrypy.expose
	def delete(self,id,_=None):
		username = self.logon.checkauth()
		task=self.taskdb.retrieve(username,id)
		task.delete(username)
		return 'ok'

	@cherrypy.expose
	def done(self,id,completed,_=None):
		username = self.logon.checkauth()
		task=self.taskdb.retrieve(username,id)
		if completed == ""  or completed == "None":
			completed = date.today().isoformat()
		task.completed=completed
		task.update(username)
		return 'ok'
