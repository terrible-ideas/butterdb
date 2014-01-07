fuckitdb
========

Master: [![Build Status](https://travis-ci.org/Widdershin/fuckitdb.png?branch=master)](https://travis-ci.org/Widdershin/fuckitdb)  
Develop: [![Build Status](https://travis-ci.org/Widdershin/fuckitdb.png?branch=develop)](https://travis-ci.org/Widdershin/fuckitdb)

FuckIt.db is a Python ORM for Google Drive Spreadsheets. Yep. Sorry. Never use this in production, ever (or at all).

Usage
-----
    import fuckitdb
    
    database = fuckitdb.Database('TestDatabase', google_username, google_password)
    
    @fuckitdb.register(database)
    class Foo(fuckitdb.Model):
      def __init__(self, bar, id=None):
        self.bar = self.field("bar", bar)

    a = Foo('test')
    a.commit()

Installation
------------
`pip install -r requirements.txt`

License
-------
MIT License. See LICENSE file for full text.
