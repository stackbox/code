# -*- coding: utf-8 -*-
# FileName: bb.py

import pygtk
pygtk.require('2.0')
import gtk

class Ba:
	def __init__(self):
		self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
		self.window.show()
		
	def main( self ):
		gtk.main()
		
print __name__

if __name__ == '__main__':
	base = Ba()
	base.main()
	