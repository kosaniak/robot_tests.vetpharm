VetDoc
====

This directory contains Robot tests and Python unittests for VetDoc home page, Search results page and Clinic/Veterinary profile page.

How to run tests
--------------------

1. Ensure you have phantomjs installed properly on your system.
1. Create a virtual environment, then
1. `pip install robotframework-pageobjects`
1. `$ pybot -vbrowser:firefox -vbaseurl:http://vet-directory.devel.vetopharm.quintagroup.com/`

To run the Python unittest example:

1. `$ export PO_BASEURL=http://vet-directory.devel.vetopharm.quintagroup.com/`
1. `$ python test_vetdoc.py`

By default tests will run in PhantomJS unless you specify otherwise.