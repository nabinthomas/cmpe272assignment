#!/bin/bash


#Test to Import Books
cd test/unittests
echo "Running unit tests.."
/bin/bash test_import_books.sh
if [ "$?" -ne 0 ]
then
    echo "Importing Books failed"
    exit -1
fi 
echo "All Unit tests passed"