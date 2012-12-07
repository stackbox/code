from operator import attrgetter
import re
from urllib.parse import urlparse,urlunparse
from html.parser import HTMLParser

import wikidb

# represent domain specific functionality

def gettopiclist():
	return wikidb.Topic.getcolumnvalues('title')

def gettopic(topic,revision=None):
	t=list(wikidb.Topic.list(title=topic))
	if len(t):
		topic = wikidb.Topic(id=t[0])
		pages=[ wikidb.Page(id=p.b_id) 
				for p in wikidb.TopicPage.list(topic) ]
		
		pages = sorted(pages,key=attrgetter('modified'),
						reverse=True)
		
		tags = [ wikidb.Tag(id=t.b_id).tag 
				 for t in wikidb.TopicTag.list(topic) ]
		return pages[0].content,tags
	else:
		return '''no such topic (yet).
				  If you edit this topic it will be created.''',[]

class Scrubber(HTMLParser):
	def __init__(self,allowed_tags=[]):
		super().__init__()
		self.result = []
		self.allowed_tags = set(allowed_tags)
		
	def handle_starttag(self, tag, attrs):
		if tag in self.allowed_tags:
			self.result.append('<%s %s>'%(tag,
							" ".join('%s="%s"'%a for a in attrs)))
		
	def handle_endtag(self, tag):
		if tag in self.allowed_tags:
			self.result.append('</'+tag+'>')

	def handle_data(self,data):
		self.result.append(data)

def scrub(content):
	parser = Scrubber(('ul','ol','li','b','i','u','em','code',
						'pre','h1','h2','h3','h4'))
	parser.feed(content)
	return "".join(parser.result)

topicref = re.compile(r'\[\s*([^,\]]+?)(\s*,\s*([^\]]+))?\s*\]')
linkref  = re.compile(r'\{\s*([^,\}]+?)(\s*,\s*([^\}]+))?\s*\}')
imgref   = re.compile(r'\<\s*(\d+?)(\s*,\s*([^\>]*))?\s*\>')

def topicrefreplace(matchobj):
	ref=matchobj.group(1)
	txt=matchobj.group(3) if (not matchobj.group(3)
								is None) else matchobj.group(1)
	nonexist = ""
	if(len(list(wikidb.Topic.list(title=ref)))==0):
		nonexist = " nonexisting"
	return '<a href="show?topic=%s" class="topicref%s">%s</a>'%(
				ref,nonexist,txt)
	
def linkrefreplace(matchobj):
	ref=matchobj.group(1)
	txt=matchobj.group(3) if (not matchobj.group(3)
								is None) else matchobj.group(1)
	ref=urlunparse(urlparse(ref,'http'))
	return '<a href="%s" class="externalref">%s</a>'%(ref,txt)
	
def imgrefreplace(matchobj):
	ref=matchobj.group(1)
	txt=matchobj.group(3) if (not matchobj.group(3)
								is None) else matchobj.group(1)
	return '''<img src="showimage?id=%s" alt="%s"
				class="wikiimage">'''%(ref,txt)
	
def render(content):
	yield '<p>\n'
	for line in content.splitlines(True):
		line = re.sub(imgref  ,imgrefreplace  ,line) #first otherwise replace tags
		line = re.sub(topicref,topicrefreplace,line)
		line = re.sub(linkref ,linkrefreplace ,line)
		if len(line.strip())==0 : line = '</p>\n<p>'
		yield line
	yield '</p>\n'
	
def splitwords(content):
	for word in content.split():
		word=word.strip('.,:;!?').lower()
		if word.isalnum():
			yield word

def updateitemrelation(p,itemmap,newitems,Entity,attr,Relation):
	"""
	p			the primary Entity whose relation with items will be updated, e.g. an instance of Topic
	itemmap 	maps current items (strings) to Entity instances
	newitems	a set of new items (strings)
	Entity		class (e.g. Word)
	attr		the Entity attribute representing a item (e.g. 'word')
	Relation    class of the relation we want update (e.g. TopicWord)
	"""
	olditems = set()
	for item in itemmap:
		if not item in newitems:
			itemmap[item].delete()
			# this changes the size of the dict: del topicwords[word]
		else:
			olditems.add(item)
	for item in newitems - olditems:
		if not item in itemmap:
			ilist = list(Entity.list(**{attr:item}))
			if (len(ilist)):
				i = Entity(id=ilist[0])
			else:
				i = Entity(**{attr:item})
			Relation.add(p,i)
	
def updatetopic(originaltopic,topic,content,tags):
	t=list(wikidb.Topic.list(title=originaltopic))
	if len(t) == 0 :
		t=wikidb.Topic(title=topic)
	else:
		t=wikidb.Topic(id=t[0])
		t.update(title=topic)
	content=scrub(content)
	p=wikidb.Page(content=content)
	wikidb.TopicPage(t.id,p.id)
	# update word index
	newwords = set(splitwords(content))
	wordlist = wikidb.TopicWord.list(t)
	topicwords = { wikidb.Word(id=w.b_id).word:w 
					for w in wordlist }
	updateitemrelation(t,topicwords,newwords,
		wikidb.Word,'word',wikidb.TopicWord)
	# update tags
	newtags = set(t.capitalize() 
					for t in [t.strip() 
						for t in tags.split(',')] if t.isalnum())
	taglist = wikidb.TopicTag.list(t)
	topictags = { wikidb.Tag(id=t.b_id).tag:t 
					for t in taglist }
	updateitemrelation(t,topictags,newtags,
		wikidb.Tag,'tag',wikidb.TopicTag)
	
def searchwords(words):
	topics = None
	for word in words.split(','):
		word = word.strip('.,:;!? ').lower() # a list with a final comma will yield an empty last term
		if word.isalnum():
			w = list(wikidb.Word.list(word=word))
			if len(w):
				ww = wikidb.Word(id=w[0])
				wtopic = set( w.a_id 
					for w in wikidb.TopicWord.list(ww) )
				if topics is None :
					topics = wtopic
				else:
					topics &= wtopic
				if len(topics) == 0 :
					break
	if not topics is None:
		for t in topics:
			yield wikidb.Topic(id=t).title

def searchtags(tags):
	topics = None
	for tag in tags.split(','):
		tag = tag.strip('.,:;!? ').capitalize()
		if tag.isalnum():
			w = list(wikidb.Tag.list(tag=tag))
			if len(w):
				ww = wikidb.Tag(id=w[0])
				wtopic = set( w.a_id 
					for w in wikidb.TopicTag.list(ww) )
				if topics is None :
					topics = wtopic
				else:
					topics &= wtopic
				if len(topics) == 0 :
					break
	if not topics is None:
		for t in topics:
			yield wikidb.Topic(id=t).title

def tagcloud():
	tags = sorted([wikidb.Tag(id=t) for t in wikidb.Tag.list()],
					key=attrgetter('tag'))
	totaltopics=0
	tagrank = []
	for t in tags:
		topics = wikidb.TopicTag.list(t)
		if len(topics):
			totaltopics += len(topics) # there migh be tags wo. topics, cleaning is for heros
			tagrank.append((t.tag,len(topics)))
	maxtopics = max(topics for tag,topics in tagrank)
	for tag,topics in tagrank:
		yield tag, int(5.0*topics/(maxtopics+1)) # map to 0 - 4

def getimages():
	imglist = [wikidb.Image(id=id) for id in wikidb.Image.list()]
	imglist = sorted(imglist,key=attrgetter('modified'),
						reverse=True)
	return imglist
