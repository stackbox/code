# -*- coding: utf-8 -*-
# FileName: helloworld.py

import pygtk
pygtk.require( '2.0' )
import gtk

class HelloWorld:
    '''helloworld use pygtk'''
    
    def hello( self, widget, data=None ):
        
        print 'Hello World!'
        
    def delete_event( self, widget, event, data=None ):
        '''If you return FALSE in the 'delete_event' signal
        handler, GTK will emit the 'destroy' signal. Return TRUE
        means you don't want the window to be destroyed.
        This is useful for popping up 'are you sure you want to
        quit?' type dialogs.'''
        
        print 'delete event occurred'
        
        return False
        
    def destroy( self, widget, data=None ):
        '''Another callback'''
        
        gtk.main_quit()
        
    def __init__( self ):
        '''Create a new window'''
        
        self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
        self.window.connect( 'delete_event', self.delete_event )
        self.window.connect( 'destroy', self.destroy )
        self.window.set_border_width( 10 )
        self.button = gtk.Button( 'Hello World' )
        self.button.connect( 'clicked', self.hello, None )
        self.button.connect_object( 'clicked', gtk.Widget.destroy, self.window )
        self.window.add( self.button )
        self.button.show()
        self.window.show()
        
    def main( self ):
        gtk.main()
        
if __name__ == '__main__':
    hello = HelloWorld()
    hello.main()