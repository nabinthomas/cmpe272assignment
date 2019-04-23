# Guidelines for directory structure of unit tests:
under test, there is a new dir "unittests"
 and a "data" dir under that
 keep all the CSVs to import for unit tests under that data folder, with proper names
and create one shell script for each set of unit tests
 running that shell script should do the unit tests.
 Any .py scripts can be in the same folder as needed.
 eg: test_import_books.sh will run the test to import all books from a csv file and report a PASS fail (via return code to shell).
 and print a message alsop
 test_run_all.sh will run each of these individual test scripts
 it will be used from the continuous integration