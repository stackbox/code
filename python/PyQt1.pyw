#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys  
from PyQt4 import QtGui,QtWebKit  
  
app = QtGui.QApplication(sys.argv)  
view = QtWebKit.QWebView()  
frame = view.page().mainFrame()  
frame.setHtml("hello world")  
str = frame.toPlainText()  
print str.toUtf8()  
view.show()  
app.exec_() 