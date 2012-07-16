import gtk

class PyApp(gtk.Window):
    def __init__(self):
	super(PyApp,self).__init__()

	self.set_title("test")
	self.set_size_request(260,150)
	self.set_position(gtk.WIN_POS_CENTER)

        ok = gtk.Button("OK")
	ok.set_size_request(70,30)
	close = gtk.Button("Close")

	hbox = gtk.HBox(True,4)
	hbox.add(ok)
	hbox.add(close)

	halign = gtk.Alignment(0.5,0,0,0)
	halign.add(hbox)

	vbox = gtk.VBox(False,5)
	valign = gtk.Alignment(0,0.5,0,0)
	vbox.pack_start(valign)

	valign.add(halign)

	self.add(vbox)

	self.connect("destroy",gtk.main_quit)
	self.show_all()
PyApp()
gtk.main()
