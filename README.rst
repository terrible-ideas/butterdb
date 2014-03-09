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


License
-------

MIT License. See LICENSE file for full text.

.. _Documentation: http://fuckitdb.readthedocs.org
.. _fuckitdb on PyPi: https://pypi.python.org/pypi/fuckitdb

.. |Build Status| image:: https://travis-ci.org/Widdershin/fuckitdb.png?branch=master
   :target: https://travis-ci.org/Widdershin/fuckitdb
.. |Build Status| image:: https://travis-ci.org/Widdershin/fuckitdb.png?branch=develop
   :target: https://travis-ci.org/Widdershin/fuckitdb
