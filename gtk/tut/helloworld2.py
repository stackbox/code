import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld2:
    def callback(self,widget,data):
	print "Hello again - %s was pressed" % data

    def delete_event(self,widget,event,data=None):
	print "quit"
	gtk.main_quit()
	return False 
    def quit(self,widget,data):
	gtk.main_quit()
    def __init__(self):
	self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.set_title("Hello Buttons!")
	self.window.connect("delete_event",self.delete_event)
	self.window.set_border_width(10)

	self.box1 = gtk.HBox(False,0)
	self.window.add(self.box1)

	self.button1 = gtk.Button("Button1")
	self.button1.connect("clicked",self.callback,"Button 1")
	self.box1.pack_start(self.button1,True,True,0)
	self.button1.show()

	self.button2 = gtk.Button("Button2")
	self.button2.connect("clicked",self.callback,"Button 2")
	self.box1.pack_start(self.button2,True,True,0)
	self.button2.show()

	self.button3 = gtk.Button("quit")
	self.button3.connect("clicked",self.quit,None)
	self.box1.pack_start(self.button3,True,True,0)
	self.button3.show()
	self.box1.show()
	self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    hello = HelloWorld2()
    main()
