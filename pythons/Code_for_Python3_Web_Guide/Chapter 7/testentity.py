from entity import *

class Entity(AbstractEntity):
	database="/tmp/abc.db"
	
class MyEntity(Entity):
	a=Attribute(unique=True, notnull=True, affinity='float',
		displayname='Attribute A', validate=lambda x:x<5)

a=MyEntity(a=3.14)
print(MyEntity.list())

e=MyEntity.list(pattern=[('a',3.14)])[0]
print(e)

e.delete()

a=MyEntity(a=2.71)
print([str(e) for e in MyEntity.list()])

a.a=1
a.update()
print([str(e) for e in MyEntity.list()])

a.a=9
