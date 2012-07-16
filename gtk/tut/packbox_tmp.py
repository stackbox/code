#!/usr/bin/env python


import pygtk
pygtk.require('2.0')
import gtk
import sys, string

def make_box(homogeneous, spacing, expand, fill, padding):
    box = gtk.HBox(homogeneous, spacing)
    button = gtk.Button("box.pack")
    box.pack_start(button, expand, fill, padding)
    button.show()
    button = gtk.Button("(button,")
    box.pack_start(button, expand, fill, padding)
    button.show()
    if expand == True:
        button = gtk.Button("True,")
    else:
        button = gtk.Button("False,")
    box.pack_start(button, expand, fill, padding)
    button.show()
    button = gtk.Button(("False,", "True,")[fill==True])
    box.pack_start(button, expand, fill, padding)
    button.show()
    padstr = "%d)" % padding
    button = gtk.Button(padstr)
    box.pack_start(button, expand, fill, padding)
    button.show()
    return box

class PackBox1:
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, which):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)
    
        box1 = gtk.VBox(False, 0)
    
        if which == 1:
            label = gtk.Label("HBox(False, 0)")
            label.set_alignment(0, 0)
            box1.pack_start(label, False, False, 0)
            label.show()
            box2 = make_box(False, 0, False, False, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
            box2 = make_box(False, 0, True, False, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
            box2 = make_box(False, 0, True, True, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
            separator = gtk.HSeparator()
            box1.pack_start(separator, False, True, 5)
            separator.show()
            label = gtk.Label("HBox(True, 0)")
            label.set_alignment(0, 0)
            box1.pack_start(label, False, False, 0)
            label.show()
            box2 = make_box(True, 0, True, False, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
            box2 = make_box(True, 0, True, True, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
            separator = gtk.HSeparator()
            box1.pack_start(separator, False, True, 5)
            separator.show()
        elif which == 2:
            label = gtk.Label("HBox(False, 10)")
            label.set_alignment( 0, 0)
            box1.pack_start(label, False, False, 0)
            label.show()
            box2 = make_box(False, 10, True, False, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
            box2 = make_box(False, 10, True, True, 0)
            box1.pack_start(box2, False, False, 0)
            box2.show()
	
            separator = gtk.HSeparator()
            box1.pack_start(separator, False, True, 5)
            separator.show()
	
            label = gtk.Label("HBox(False, 0)")
            label.set_alignment(0, 0)
            box1.pack_start(label, False, False, 0)
            label.show()
	
            # Args are: homogeneous, spacing, expand, fill, padding
            box2 = make_box(False, 0, True, False, 10)
            box1.pack_start(box2, False, False, 0)
            box2.show()
	
            # Args are: homogeneous, spacing, expand, fill, padding
            box2 = make_box(False, 0, True, True, 10)
            box1.pack_start(box2, False, False, 0)
            box2.show()
	
            separator = gtk.HSeparator()
            # The last 3 arguments to pack_start are:
            # expand, fill, padding.
            box1.pack_start(separator, False, True, 5)
            separator.show()

        elif which == 3:

            # This demonstrates the ability to use pack_end() to
            # right justify widgets. First, we create a new box as before.
            box2 = make_box(False, 0, False, False, 0)

            # Create the label that will be put at the end.
            label = gtk.Label("end")
            # Pack it using pack_end(), so it is put on the right
            # side of the hbox created in the make_box() call.
            box2.pack_end(label, False, False, 0)
            # Show the label.
            label.show()
	
            # Pack box2 into box1
            box1.pack_start(box2, False, False, 0)
            box2.show()
	
            # A separator for the bottom.
            separator = gtk.HSeparator()
            
            # This explicitly sets the separator to 400 pixels wide by 5
            # pixels high. This is so the hbox we created will also be 400
            # pixels wide, and the "end" label will be separated from the
            # other labels in the hbox. Otherwise, all the widgets in the
            # hbox would be packed as close together as possible.
            separator.set_size_request(400, 5)
            # pack the separator into the vbox (box1) created near the start 
            # of __init__()
            box1.pack_start(separator, False, True, 5)
            separator.show()
    
        # Create another new hbox.. remember we can use as many as we need!
        quitbox = gtk.HBox(False, 0)
    
        # Our quit button.
        button = gtk.Button("Quit")
    
        # Setup the signal to terminate the program when the button is clicked
        button.connect("clicked", lambda w: gtk.main_quit())
        # Pack the button into the quitbox.
        # The last 3 arguments to pack_start are:
        # expand, fill, padding.
        quitbox.pack_start(button, True, False, 0)
        # pack the quitbox into the vbox (box1)
        box1.pack_start(quitbox, False, False, 0)
    
        # Pack the vbox (box1) which now contains all our widgets, into the
        # main window.
        self.window.add(box1)
    
        # And show everything left
        button.show()
        quitbox.show()
    
        box1.show()
        # Showing the window last so everything pops up at once.
        self.window.show()

def main():
    # And of course, our main loop.
    gtk.main()
    # Control returns here when main_quit() is called
    return 0         

if __name__ =="__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("usage: packbox.py num, where num is 1, 2, or 3.\n")
        sys.exit(1)
    PackBox1(string.atoi(sys.argv[1]))
    main()
