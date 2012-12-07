This directory contains source code and other resources for the examples in chapter 4.
 
The python files marked with an * are actual applications that may be started either by double clicking the file or by starting it from the command line by changing to this directory and issueing a command like 

c:\python32\python.exe application.py

This will start up a CherryPy webserver accessible on http://localhost:8080/ or http://127.0.0.1:8080/

All applications require the user to authenticate and are preconfigured to accept 'admin' and 'admin' (both without the quotes) as valid credentials.

All applications require Python 3 and a properly installed CherryPy distribution. All neccessary jQuery libraries are provided in the static directory.

static               directory containing all static resources
  css                contains stylesheets specific to our applications
    logon.css        stylesheet for the logon screen
    tasklist.css     stylesheet for the tasklist application
  jquery             directory containing all jQuery and jQueryUI libraries and stylesheets
  js                 directory containing plugins and application specific javascript libraries
    jeditable.js     the jeditble plugin used by spreadheet.js
    sort.js          the sort plugin used by tasklist.js
    tasklistajax.js  application specific javascript used by tasklist.py
    tasklistajax2.js application specific javascript used by tasklist2.py (a sample implementation for a hero assignement)
    tooltip.js       functions to create inline labels in input elements

logon.py             file for the logon module
logondb.py			 file for the logondb modul
* logondbapp.py      sample application to show off the logon module

taskapp.py           the taskapp module, implementing the TaskApp class
taskapp2.py			 the taskapp2 module, implementing the TaskApp class, implements auto refresh (refers to static/tasklistajax2.js)
* tasklist.py        the tasklist application. Uses the logondb and taskapp modules.
* tasklist2.py       the tasklist application but uses taskapp2.py instaed of taskapp.py for auto refresh
tasklistdb.py		 module providing Task and TaskDB classes to access underlying task database
* test_tasklistdb.py test suite for tasklistdb.py

* taskdb1.py		 sample applications illustrating sqlite database access
* taskdb2.py
* taskdb3.py

factorial.py		module implementing the fac() function to calculate a factorial
* test_factorial.py test suite for factorial.py


Any .svn or __pycache__ directories present may be ignored.