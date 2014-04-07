.. butterdb documentation master file, created by
   sphinx-quickstart on Thu Mar  6 22:51:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to butterdb's documentation!
====================================

.. toctree::
   :maxdepth: 2
   
butterdb is a database ORM for Google Drive Spreadsheets.

Basic usage::

   import butterdb
   
   database = butterdb.Database("MyDatabaseSheet", "foo@google.com", "password")
   
   
   @butterdb.register(database)
   class User(butterdb.Model):
       def __init__(self, name, password):
           self.name = self.field(name)
           self.password = self.field(password)
   
   
   barry = User("Barry", "hunter2")
   barry.name = "Steve"
   barry.commit()
   
   users = User.get_instances()

API Reference:
==============

.. automodule:: butterdb.fuckit
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
