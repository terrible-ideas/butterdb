fuckitdb
========

| Master: |Build Status|
| Develop: |Build Status|

`Documentation`_

`fuckitdb on PyPi`_

fuckitdb is a Python ORM for Google Drive Spreadsheets. Never use this for anything important, it's an experiment.

Installation
------------

``pip install fuckitdb``

Usage
-----

::

   import fuckitdb
   
   database = fuckitdb.Database("MyDatabaseSheet", "foo@google.com", "password")
   
   
   @fuckitdb.register(database)
   class User(fuckitdb.Model):
       def __init__(self, name, password):
           self.name = self.field(name)
           self.password = self.field(password)
   
   
   barry = User("Barry", "hunter2")
   barry.name = "Steve"
   barry.commit()
   
   users = User.get_instances()
   
Tests
-----
`nosetests`

What works?
----------
* Store data in Google Spreadsheets (the cloud!!!)
* Models from classes
* Fields as attributes. decimals, ints and strings only (as far as I know)
* Commits
* Mocked unit tests, mock database
* Arbitrary cell execution with `=blah()` (free stored procedures?)
* Auto backup/bad patch control

What's missing?
---------------
* Spreadsheets must exist before connecting
* References
* Collections
* Customizable fields
* Customizable table size (arbitrarily hardcoded)

Feedback
--------
Comments, concerns, issues and pull requests welcomed. Reddit /u/Widdershiny or email me at ncwjohnstone@gmail.com.

License
-------

MIT License. See LICENSE file for full text.

.. _Documentation: http://fuckitdb.readthedocs.org
.. _fuckitdb on PyPi: https://pypi.python.org/pypi/fuckitdb

.. |Build Status| image:: https://travis-ci.org/Widdershin/fuckitdb.png?branch=master
   :target: https://travis-ci.org/Widdershin/fuckitdb
.. |Build Status| image:: https://travis-ci.org/Widdershin/fuckitdb.png?branch=develop
   :target: https://travis-ci.org/Widdershin/fuckitdb
