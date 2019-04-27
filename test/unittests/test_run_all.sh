#!/bin/bash


#Test to Import Books
cd test/unittests
echo "Running unit tests.."
python3 /root/app/server/dbscripts/ut.py -v
if [ "$?" -ne 0 ]
then
    echo "Add customer failed"
    exit -1
fi 
echo "All Unit tests passed"