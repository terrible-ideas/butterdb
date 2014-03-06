.. fuckitdb documentation master file, created by
   sphinx-quickstart on Thu Mar  6 22:51:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fuckitdb's documentation!
====================================

Api reference:

.. toctree::
   :maxdepth: 2
   
fuckitdb is a database ORM for Google Drive Spreadsheets.

   import fuckitdb
   
   database = fuckitdb.Database("MyDatabaseSheet", "foo@google.com", "password")
   
   
   @fuckitdb.register(database)
   class User(fuckitdb.Mode):
       def __init__(self, name, password, id=None):
           super(User, self).__init__(id)
           self.name = self.field("name", name)
           self.password = self.field("password", password)
   
   
   barry = User("Barry", "hunter2")
   barry.name = "Steve"
   barry.commit()
   
   users = User.get_instances()

API Reference:
==============

.. automodule:: fuckitdb.fuckit
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
