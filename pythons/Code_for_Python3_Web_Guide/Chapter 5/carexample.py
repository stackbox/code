from entity import Entity

class Car(Entity): pass

Car.threadinit('c:/tmp/cardatabase.db')
Car.inittable(make="",model="",licenseplate="unique")

mycar = Car(make="Volvo",model="C30",licenseplate="12-abc-3")
yourcar = Car(make="Renault",model="Twingo",licenseplate="ab-cd-12")

allcars = Car.list()

for id in allcars:
	car=Car(id=id)
	print(car.make, car.model, car.licenseplate)
