#!/bin/bash


#Test to Import Books
cd test/unittests

/bin/bash test_import_books.sh
if [ "$?" -ne 0 ]
then
    echo "Importing Books failed"
    exit -1
fi 