import cherrypy
import json

import os
import os.path
import glob
from configparser import RawConfigParser as configparser
from uuid import uuid4 as uuid
from datetime import date

import logon

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
<script type="text/javascript" src="/static/js/tasklist2.js" ></script>
</head>
<body id="%s">
<div id="content">
%s
</div>
</body>
</html>
'''


current_dir = os.path.dirname(os.path.abspath(__file__))

def gettaskdir(username):
	"""create a directory for the given username if it does not yet exists"""
	taskdir = os.path.join(current_dir,'taskdir',username)
	# fails if name exists but is a file instead of a directory
	if not os.path.exists(taskdir):
		os.makedirs(taskdir)
	return taskdir

class Task(object):

	def __init__(self,logoffpath="/logoff"):
		self.logoffpath=logoffpath

	@cherrypy.expose
	def index(self):
		username = logon.checkauth()
		taskdir = gettaskdir(username)
		tasklist = glob.glob(os.path.join(taskdir,'*.task'))
		tasks = ['<div class="header">Tasklist for user : <span class="highlight">%s</span><form class="logoff" action="%s" method="GET"><button type="submit" name="logoffurl" class="logoff-button" value="/">Log off</button></form></div>'%(username,self.logoffpath),
				'<div class="taskheader"><div class="left">Due date</div><div class="middle">Description</div><div class="right">Completed</div></div>',
				'<div id="items" class="ui-widget-content">']
		for filename in tasklist:
			d = configparser(defaults={'description':'','duedate':'','completed':None})
			id = os.path.splitext(os.path.basename(filename))[0]
			d.readfp(open(filename))
			description = d.get('task','description')
			duedate = d.get('task','duedate')
			completed = d.get('task','completed')
			tasks.append('''<form class="%s" action="mark" method="GET">
			<input type="text" class="duedate left" name="duedate" value="%s" readonly="readonly" />
			<input type="text" class="description middle" name="description" value="%s" readonly="readonly" />
			<input type="text" class="completed right editable-date tooltip" title="click to select a date, then click done" name="completed" value="%s" />
			<input type="hidden" name="id" value="%s" />
			<button type="submit" class="done-button" name="done" value="Done" >Done</button>
			<button type="submit" class="del-button" name="delete" value="Del" >Del</button>
			</form>
			'''%('notdone' if completed==None else 'done',duedate,description,completed,id))
		tasks.append('''<form class="add" action="add" method="GET">
			<input type="text" class="duedate left editable-date tooltip" name="duedate" title="click for a date" />
			<input type="text" class="description middle tooltip" title="click to enter a description" name="description"/>
			<button type="submit" class="add-button" name="add" value="Add" >Add</button>
			</form></div>
			''')
		return base_page%('itemlist',"".join(tasks))

	@cherrypy.expose
	def add(self,add,description,duedate):
		username = logon.checkauth()
		taskdir = gettaskdir(username)
		filename = os.path.join(taskdir,uuid().hex+'.task')
		d=configparser()
		d.add_section('task')
		d.set('task','description',description)
		d.set('task','duedate',duedate)
		with open(filename,"w") as file:
			d.write(file)
		raise cherrypy.InternalRedirect(".")

	@cherrypy.expose
	def mark(self,id,duedate,description,completed,done=None,delete=None):
		username = logon.checkauth()
		taskdir = gettaskdir(username)
		filename = os.path.join(taskdir,id+'.task')
		if done=="Done":
			print('####',id,duedate,description,completed,done,delete)
			d=configparser()
			with open(filename,"r") as file:
				d.readfp(file)
			if completed == ""  or completed == "None": completed = date.today().isoformat()
			d.set('task','completed',completed)
			with open(filename,"w") as file:
				d.write(file)
		elif delete=="Del":
			os.unlink(filename)
		raise cherrypy.InternalRedirect(".")
