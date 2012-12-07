# wikidb.py 
#
# (c) 2010 Michel J. Anders (varkenvarken)
# wikidb.py implements the object abstraction of the wiki

from entity import Entity
from relation import Relation

class User(Entity): pass
class Topic(Entity): pass
class Page(Entity): pass
class Tag(Entity): pass
class Word(Entity): pass
class Image(Entity): pass

class UserPage(Relation): pass
class TopicPage(Relation): pass
class TopicTag(Relation): pass
class ImagePage(Relation): pass
class TopicWord(Relation): pass

def threadinit(db):
	User.threadinit(db)
	Topic.threadinit(db)
	Page.threadinit(db)
	Tag.threadinit(db)
	Word.threadinit(db)
	Image.threadinit(db)
	UserPage.threadinit(db)
	TopicPage.threadinit(db)
	TopicTag.threadinit(db)
	ImagePage.threadinit(db)
	TopicWord.threadinit(db)

def threadexit(db):
	User.threadexit(db)
	Topic.threadexit(db)
	Page.threadexit(db)
	Tag.threadexit(db)
	Word.threadexit(db)
	Image.threadexit(db)
	UserPage.threadexit(db)
	TopicPage.threadexit(db)
	TopicTag.threadexit(db)
	TopicWord.threadexit(db)

def inittable():
	User.inittable(userid="unique not null")
	Topic.inittable(title="unique not null")
	Page.inittable(content="",
				modified="not null default CURRENT_TIMESTAMP")
	Tag.inittable(tag="unique not null")
	Word.inittable(word="unique not null")
	Image.inittable(type="",data="blob",title="",
				modified="not null default CURRENT_TIMESTAMP",
				description="")
	
	UserPage.inittable(User,Page)
	TopicPage.inittable(Topic,Page)
	TopicTag.inittable(Topic,Tag)
	TopicWord.inittable(Topic,Word)
