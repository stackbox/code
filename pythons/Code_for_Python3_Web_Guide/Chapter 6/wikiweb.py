import wiki
import wikidb

# implements the web application

import cherrypy
import json
import os

from logondb import LogonDB

with open('basepage.html') as f:
	basepage=f.read(-1)

class Wiki():
	def __init__(self,logon,logoffpath):
		self.logon=logon
		self.logoffpath=logoffpath

	@cherrypy.expose
	def index(self):
		item = '<li><a href="show?topic=%s">%s</a></li>'
		topiclist = "\n".join(
			[item%(t,t)for t in wiki.gettopiclist()])
		content = '<div id="wikihome"><ul>%s</ul></div>'%(
			topiclist,)
		return basepage % content
	
	@cherrypy.expose
	def show(self,topic):
		topic = topic.capitalize()
		currentcontent,tags = wiki.gettopic(topic)
		currentcontent = "".join(wiki.render(currentcontent))
		tags = ['<li><a href="searchtags?tags=%s">%s</a></li>'%(
					t,t) for t in tags]
		content = '''
		<div>
			<h1>%s</h1><a href="edit?topic=%s">Edit</a>
		</div>
		<div id="wikitopic">%s</div>
		<div id="wikitags"><ul>%s</ul></div>
		<div id="revisions">revisions</div>
		''' % ( topic, topic, currentcontent,"\n".join(tags))
		return basepage % content

	@cherrypy.expose
	def edit(self,topic,
				content=None,tags=None,originaltopic=None):
				
		user = self.logon.checkauth(
			logonurl=self.logon.path, returntopage=True)
		
		if content is None :
			currentcontent,tags = wiki.gettopic(topic)
			html = '''
			<div id="editarea">
				<form id="edittopic" action="edit" 
					method="GET">
					<label for="topic"></label>
					<input name="originaltopic" 
						type="hidden" value="%s">
					<input name="topic" type="text"
						value="%s">
					<div id="buttonbar">
						<button type="button" id="insertlink">
							External link
						</button>
						<button type="button" id="inserttopic">
							Wiki page
						</button>
						<button type="button" id="insertimage">
							Image
						</button>
					</div>
					<label for="content"></label>
					<textarea name="content"
						cols="72" rows="24" >
						%s
					</textarea>
					<label for="tags"></label>
					<input name="tags" type="text" value="%s">
					<button type="submit">Save</button>
					<button type="button">Cancel</button>
					<button type="button">Preview</button>
				</form>
			</div>
			<div id="previewarea">preview</div>
			<div id="imagedialog">%s</div>
			<script>
				$("#imagedialog").dialog(
					{autoOpen:false,
					 width:600,
					 height:600});
			</script>
			'''%(topic, topic, currentcontent,
					", ".join(tags),
					"".join(self.images()))
			return basepage % html
		else :
			wiki.updatetopic(originaltopic,topic,content,tags)
			raise cherrypy.HTTPRedirect('show?topic='+topic)

	@cherrypy.expose
	def searchwords(self,words):
		yield '<ul>\n'
		for topic in sorted(wiki.searchwords(words)):
			yield '<li><a href="show?topic=%s">%s</a></li>'%(
				topic,topic)
		yield '</ul>\n'
	
	@cherrypy.expose
	def searchtags(self,tags):
		yield '<ul>\n'
		for topic in sorted(wiki.searchtags(tags)):
			yield '<li><a href="show?topic=%s">%s</a></li>'%(
				topic,topic)
		yield '</ul>\n'
	
	@cherrypy.expose
	def tagcloud(self,_=None):
		for tag,weight in wiki.tagcloud():
			yield '''
			<span class="weight%s">
				<a href="searchtags?tags=%s">%s</a>
			</span>'''%(weight,tag,tag)

	@cherrypy.expose
	def images(self,title=None,description=None,file=None):
		if not file is None:
			data = file.file.read()
			#yield '%s %d %s\n'%(file.filename,len(data),file.content_type)
			wikidb.Image(title=title,description=description,
				data=data,type=str(file.content_type))
		yield '''
		<div>
			<form>
				<label for="title">select a title</label>
				<input name="title" type="text">
				<button type="submit">Search</button>
			</form>
			<form method="post" action="./images" 
				enctype="multipart/form-data">
				<label for="file">New image</label>
				<input type="file" name="file">
				<label for="title">Title</label>
				<input type="text" name="title">
				<label for="description">Description</label>
				<textarea name="description"
					cols="48" rows="3"></textarea>
				<button type="submit">Upload</button>
			</form>
		</div>
		'''
		yield '<div id="imagelist">\n'
		for img in self.getimages():
			yield img
		yield '</div>'

	@cherrypy.expose
	def getimages(self,title=None,_=None):
		for img in wiki.getimages():
			yield '''
			<div>
				<img src="showimage?id=%s" id="img%s"
				class="selectable-image"
				alt="%s">
				<p>%s</p>
				<p>%s</p>
			</div>\n''' % (img.id,img.id,img.description,
							img.title,img.modified)
	
	@cherrypy.expose
	def showimage(self,id):
		return wikidb.Image(id=id).data
		
	@cherrypy.expose
	def gettopics(self,term,_=None):
		term = term.lower()
		# the square brackets [] are needed here because we cannot json serialize a generator
		# topic title may contain upper and lower case
		return json.dumps(
			[t for t in wikidb.Topic.getcolumnvalues('title')
				if t.lower().startswith(term)])

	@cherrypy.expose
	def getwords(self,term,_=None):
		term = term.lower()
		# the square brackets [] are needed here because we cannot json serialize a generator
		# words are stored all lowercase
		return json.dumps(
			[t for t in wikidb.Word.getcolumnvalues('word')
				if t.startswith(term)])

	@cherrypy.expose
	def gettags(self,term,_=None):
		term = term.capitalize()
		# the square brackets [] are needed here because we cannot json serialize a generator
		# tags are stored capitalized
		return json.dumps(
			[t for t in wikidb.Tag.getcolumnvalues('tag')
				if t.startswith(term)])

class Root(object):
	logon = LogonDB()
	wiki = Wiki(logon=logon,logoffpath="/logon/logoff")
	
	@cherrypy.expose
	def index(self):
		raise cherrypy.HTTPRedirect("/wiki")

if __name__ == "__main__":
	
	current_dir = os.path.dirname(os.path.abspath(__file__))

	db='/tmp/wikiweb.db'
	
	# we can subscribe more than one function
	cherrypy.engine.subscribe('start_thread',
			lambda thread_index: wikidb.threadinit(db))
	cherrypy.engine.subscribe('start_thread',
			lambda thread_index: Root.logon.connect())
	
	wikidb.threadinit(db)
	wikidb.inittable()
	
	cherrypy.quickstart(Root(),config={
		'/':
		{ 'log.access_file' : 
				os.path.join(current_dir,"access.log"),
		'log.screen': False,
		'tools.sessions.on': True
		},
		'/wikiweb.js':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/wikiweb.js"
		},
		'/logon.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/logon.css"
		},
		'/wiki.css':
		{ 'tools.staticfile.on':True,
		'tools.staticfile.filename':current_dir+"/wiki.css"
		}
	})
