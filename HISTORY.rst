.. :changelog:

History
-------

0.1.0 7/3/14
++++++++++++++++++

* First release on PyPI.

0.1.1 7/3/14
++++++++++++++++++

* Converted readme to rst from md

0.1.2 7/3/14
++++++++++++++++++

* Included HISTORY.rst in package build

0.1.3 7/3/14
++++++++++++++++++

* Model.field no longer requires name to be specified. Attribute name will be used if none is provided.
* Model no longer needs to have id as a keyword argument, or call super in init
* Tests now use pep8 asserts

0.1.4 7/4/14
++++++++++++++++++

* Renamed project to butterdb

0.1.5 12/6/15
++++++++++++++++++

* Use OAuth instead of now deprecated simple login (thanks to @julierae!)
* Fix a bug in get_instance that broke modifying fields (thanks to @dequis!)
