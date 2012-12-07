from entity import Entity
from relation import Relation

class Book(Entity):
	pass

class Author(Entity):
	pass
	
class User(Entity):
	pass

class BookAuthor(Relation):
	pass

class UserBook(Relation):
	pass

def threadinit(db):
	Book.threadinit(db)
	Author.threadinit(db)
	User.threadinit(db)
	BookAuthor.threadinit(db)
	UserBook.threadinit(db)

def threadexit():
	Book.threadexit()
	Author.threadexit()
	User.threadexit()
	BookAuthor.threadexit()
	UserBook.threadexit()

def inittable():
	Book.inittable(title="",isbn="unique",publisher="")
	Author.inittable(name="")
	User.inittable(userid="unique not null")
	BookAuthor.inittable(Book,Author)
	UserBook.inittable(User,Book)

def newbook(title,authors,**kw):
	if not isinstance(title,str) :
		raise TypeError("title is not a str")
	if len(title)<1 :
		raise ValueError("title is empty")
	for a in authors :
		if not isinstance(a,Author) :
			raise TypeError("authors should be of type Author")
		
	bl=list(Book.list(title=title,**kw))
	if len(bl) == 0:
			b=Book(title=title,**kw)
	elif len(bl) == 1:
			b=Book(id=bl[0])
	else:
		raise ValueError("multiple books match criteria")
	
	lba=list(BookAuthor.list(b))
	if len(authors):
		lba=[Author(id=r.b_id) for r in lba]
		for a in authors:
			known=False
			for a1 in lba:
				if a.id == a1.id :
					known=True
					break
			if not known:
				r=BookAuthor.add(b,a)
	return b
	
def newauthor(name):
	if not isinstance(name,str) :
		raise TypeError("name is not a str")
	if len(name)<1 :
		raise ValueError("name is empty")
	
	al=list(Author.list(name=name))
	if len(al) == 0:
			a=Author(name=name)
	elif len(al) == 1:
			a=Author(id=al[0])
	else:
		raise ValueError("multiple authors match criteria")
	return a
	
def listbooks(user=None,author=None,offset=0,limit=-1,pattern=""):
	lba={}
	lbu={}
	if not user is None:
		if not isinstance(user,User):
			raise TypeError("user argument not a User")
		lbu={r.b_id for r in UserBook.list(user)}

	if not author is None:
		if not isinstance(author,Author):
			raise TypeError("author argument not an Author")
		lba={r.a_id for r in BookAuthor.list(author)}

	if user is None and author is None:
		lb={b for b in Book.list()}
	else:
		if len(lbu)==0 : lb=lba
		elif len(lba)==0 : lb=lbu
		else : lb = lba & lbu
	# note that the following might be terribly inefficient and probably should
	# be implemented as a proper sql query. However, this way we seperate hi/lo level interactions
	
	books = [Book(id=id) for id in lb]
	books = sorted(books,key=lambda book:book.title.lower())
	if pattern != "" :
		pattern = pattern.lower()
		books = [b for b in books 
					if b.title.lower().find(pattern)>=0 ]
	if limit<0 :
		limit=len(books)
	else:
		limit=offset+limit
	return len(books),books[offset:limit]
	
def listauthors(book=None):
	if not book is None:
		if not isinstance(book,Book):
			raise TypeError("book argument not a Book")
		la=[r.b_id for r in BookAuthor.list(book)]
	else:
		la=Author.list()
	return [Author(id=id) for id in la]

from itertools import takewhile,dropwhile
from re import compile,IGNORECASE

def gettitles(term):
	# here we might implement caching (should be invalidated 
	# by newbook/newauthor and be thread safe)
	titles=Book.getcolumnvalues('title')
	re=compile(term,IGNORECASE)
	return list(takewhile(lambda x:re.match(x),
				dropwhile(lambda x:not re.match(x),titles)))
	
def getauthors(term):
	# here we might implement caching (should be invalidated
	# by newbook/newauthor and be thread safe)
	names=Author.getcolumnvalues('name')
	re=compile(term,IGNORECASE)
	return list(takewhile(lambda x:re.match(x),
				dropwhile(lambda x:not re.match(x),names)))
	
def checkuser(username):
	users=list(User.list(userid=username))
	if len(users):
		return User(id=users[0])
	return User(userid=username)
	
def addowner(book,user):
	if not isinstance(book,Book):
		raise TypeError("book argument not a Book")
	if not isinstance(user,User):
		raise TypeError("user argument not a User")
	return UserBook.add(user,book)
	
def delowner(book,user):
	if not isinstance(book,Book):
		raise TypeError("book argument not a Book")
	if not isinstance(user,User):
		raise TypeError("user argument not a User")
	UserBook(user.id,book.id,stub=True).delete()

def adduser(userid):
	return User(userid=userid)
	
if __name__ == "__main__":
	import unittest
	import os
				
	class TestBooksDB(unittest.TestCase):
		def setUp(self):
			self.db='/tmp/booksdbtest.db'  # :memory: not thread safe and no multiple conns possible at all
			try:
				os.unlink(self.db)
			except:
				pass
			threadinit(self.db)
			inittable()
			self.u1=adduser("me")
			self.u2=adduser("you")
			
		def tearDown(self):
			threadexit()
			os.unlink(self.db)
		
		def test_create(self):
			# create an author
			a=newauthor(name="A.U. Thor")
			la=listauthors()
			self.assertEqual(1,len(la))
			self.assertEqual(a.name,la[0].name)
			self.assertEqual(a.id,la[0].id)
			
			# create a book
			b=newbook(title="A Book",authors=[a])
			n,lb=listbooks()
			self.assertEqual(1,len(lb))
			self.assertEqual(b.title,lb[0].title)
			self.assertEqual(b.id,lb[0].id)
			
			# create another book by the same author
			b2=newbook(title="Another Book",authors=[a])
			# give each book different owners
			addowner(b,self.u1)
			addowner(b2,self.u2)
			n,lb=listbooks(user=self.u1)
			self.assertEqual(1,len(lb))
			self.assertEqual(b.id,lb[0].id)
			n,lb=listbooks()
			self.assertEqual(2,len(lb))
			
			# b owned by more than one user
			addowner(b,self.u2)
			n,lb=listbooks(user=self.u1)
			self.assertEqual(1,len(lb))
			self.assertEqual(b.id,lb[0].id)
			n,lb=listbooks(user=self.u2)
			self.assertEqual(2,len(lb))
			n,lb=listbooks()
			self.assertEqual(2,len(lb))
			
			# create another author
			a2=newauthor(name="W. Riter")
			la=listauthors()
			self.assertEqual(2,len(la))
			
			# create yet another book
			b3=newbook(title="A New Book",authors=[a2])
			n,lb=listbooks()
			self.assertEqual(3,len(lb))
			n,lb=listbooks(user=self.u2)
			self.assertEqual(2,len(lb))
			n,lb=listbooks(author=a)
			self.assertEqual(2,len(lb))
			n,lb=listbooks(user=self.u2,author=a2)
			self.assertEqual(0,len(lb))
			
			#remove ownership
			delowner(b,self.u2)
			n,lb=listbooks(user=self.u2)
			self.assertEqual(1,len(lb))
			
		def test_list(self):
			from random import shuffle
			a=newauthor(name="A.U. Thor")
			titles="aaa BBB ccc DDD eee FFF ggg HHH iii JJJ kkk LLL".split()
			rtitles=titles[:]
			shuffle(rtitles)
			for i,t in enumerate(rtitles):
				b=newbook(title=t,authors=[a])
				addowner(b,self.u1 if i%2 else self.u2)
			n,full=listbooks()
			self.assertEqual(12,len(full))
			n,auth=listbooks(author=a)
			self.assertEqual(12,len(auth))
			n,user=listbooks(user=self.u1)
			self.assertEqual(6,len(user))
			n,first=listbooks(offset=0,limit=5)
			self.assertEqual(5,len(first))
			self.assertListEqual([b.title for b in first],titles[0:5])
			n,second=listbooks(offset=5,limit=5)
			self.assertEqual(5,len(second))
			self.assertListEqual([b.title for b in second],titles[5:10])
			n,pattern=listbooks(pattern="j")
			self.assertEqual(1,len(pattern))
			self.assertListEqual([b.title for b in pattern],["JJJ"])
			
			
	unittest.main()
	