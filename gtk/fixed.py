import gtk
import sys

class PyApp(gtk.Window):
    def __init__(self):
	super(PyApp,self).__init__()

	self.set_title("Fixed")
	self.set_size_request(300,280)
	self.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(6400,6400,6400))
	self.set_position(gtk.WIN_POS_CENTER)

	try:
	    self.bardejov = gtk.gdk.pixbuf_new_from_file("1.jpg")
	    self.rotunda = gtk.gdk.pixbuf_new_from_file("2.jpg")
	    self.mincol = gtk.gdk.pixbuf_new_from_file("3.jpg")

	except Exception,e:
	    print e.message
	    sys.exit(1)

	image1 = gtk.Image()
	image2 = gtk.Image()
	image3 = gtk.Image()

	image1.set_from_pixbuf(self.bardejov)
	image2.set_from_pixbuf(self.rotunda)
	image3.set_from_pixbuf(self.mincol)

	fix = gtk.Fixed()
	fix.put(image1,20,20)
	fix.put(image2,40,160)
	fix.put(image3,170,50)

	self.add(fix)
	self.connect("destroy",gtk.main_quit)
	self.show_all()
PyApp()
gtk.main()
