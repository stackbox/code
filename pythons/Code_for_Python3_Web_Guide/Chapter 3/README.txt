This directory contains source code and other resources for the examples in chapter 3.

The python files marked with an * are actual applications that may be started either by double clicking the file or by starting it from the command line by changin to this directory and issueing a command like 

c:\python32\python.exe application.py

This will start up a CherryPy webserver accessible on http://localhost:8080/ or http://127.0.0.1:8080/

All applications require the user to authenticate and are preconfigured to accept 'user' and 'secret' (both without the quotes) as valid credentials.

All applications require Python 3 and a properly installed CherryPy distribution. All neccessary jQuery libraries are provided in the static directory.

static              directory containing all static resources
  css               contains stylesheets specific to our applications
    logon.css       stylesheet for the logon screen
    tasklist.css    stylesheet for the tasklist application
  jquery            directory containing all jQuery and jQueryUI libraries and stylesheets
  js                directory containing plugins and application specific javascript libraries
    jeditable.js    the jeditble plugin used by spreadheet.js
    sort.js         the sort plugin used by tasklist.js
    tasklist.js     application specific javascript used by tasklist.py
    tasklist2.js    application specific javascript used by tasklist2.py (a sample implementation for a hero assignement)
    tooltip.js      functions to create inline labels in input elements

logon.py            file for the logon module
* logonapp.py       sample application to show off the logon module

spreadsheet.js      the actual spreadsheet application from chapter 2 (unchanged)
* spreadsheet3.py   the application serving the spreadsheet but uses the logon module to restrict access

task.py             the task module
* tasklist.py       the tasklist application. Uses the logon and task modules.

task2.py            another implementation of the task module. Uses tasklist2.js instead of tasklist.js (a hero assignment)
* tasklist2.py      the tasklist application but uses task2.py instaed of task.py

* tasklistapp.py    serving the tasklist application from a different url (a hero assignment)



Any .svn or __pycache__ directories present may be ignored.