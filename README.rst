butterdb
========

| Master: |Build Status Master|
| Develop: |Build Status Develop|

`Documentation`_ | `butterdb on PyPi`_

butterdb is a library to help you work with Google Spreadsheet data. It lets you model your data as Python objects, to be easily manipulated or created.

How do I use it?
-----
.. image:: http://i.imgur.com/h75z1k6.png

::

   import butterdb
   import json

   # For getting OAuth Credential JSON file see http://gspread.readthedocs.org/en/latest/oauth2.html
   # Ensure that the client_email has been granted privileges to any workbooks you wish to access.

   with open('SomeGoogleProject-2a31d827b2a9.json') as credentials_file:
      json_key = json.load(credentials_file)

   client_email = json_key['client_email']
   private_key = str(json_key['private_key']).encode('utf-8')
   
   database = butterdb.Database(name="MyDatabaseSheet", client_email=client_email, private_key=private_key)
   
   @butterdb.register(database)
   class User(butterdb.Model):
       def __init__(self, name, password):
           self.name = self.field(name)
           self.password = self.field(password)
   
   users = User.get_instances()
   
   marianne = users[1]
   
   print(marianne.password) # rainbow_trout
   
   marianne.password = "hunter2"
   marianne.commit()


How do I make instances?
=================

::

   bob = User("bob", "BestPassword!")
   bob.commit()


Where do I get it?
------------

``pip install butterdb``

Simple as that?
---------------
Yep! butterdb is a simple interface around `gspread`_. Just .commit() your objects when you want to update the spreadsheet!

How do I run the tests?
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

.. _Documentation: http://butterdb.readthedocs.org
.. _butterdb on PyPi: https://pypi.python.org/pypi/butterdb
.. _gspread: https://github.com/burnash/gspread

.. |Build Status Master| image:: https://travis-ci.org/Widdershin/butterdb.png?branch=master
   :target: https://travis-ci.org/Widdershin/butterdb
.. |Build Status Develop| image:: https://travis-ci.org/Widdershin/butterdb.png?branch=develop
   :target: https://travis-ci.org/Widdershin/butterdb
