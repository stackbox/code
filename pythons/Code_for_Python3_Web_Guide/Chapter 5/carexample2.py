from entity import Entity
from relation import Relation

class Car(Entity): pass
class Owner(Entity): pass

Car.threadinit('c:/tmp/cardatabase2.db')
Car.inittable(make="",model="",licenseplate="unique")

Owner.threadinit('c:/tmp/cardatabase2.db')
Owner.inittable(name="")

class CarOwner(Relation): pass

CarOwner.threadinit('c:/tmp/cardatabase2.db')
CarOwner.inittable(Car,Owner)

mycar = Car(make="Volvo",model="C30",licenseplate="12-abc-3")
mycar2 = Car(make="Renault",model="Coupe",licenseplate="45-de-67")
me = Owner(name="Michel")

CarOwner.add(mycar,me)
CarOwner.add(mycar2,me)

owners = CarOwner.list(mycar)
for r in owners:
	print(Car(id=r.a_id).make,'owned by',Owner(id=r.b_id).name)

owners = CarOwner.list(me)
for r in owners:
	print(Owner(id=r.b_id).name,'owns a',Car(id=r.a_id).make)
