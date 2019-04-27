#!/bin/bash


#Test import scripts
cd test/unittests
bash ./test_import_books.sh
if [ "$?" -ne 0 ]
then
    exit -1
fi 

cd test/unittests
bash ./test_import_orders.sh
if [ "$?" -ne 0 ]
then
    exit -1
fi 

cd test/unittests
bash ./test_import_customers.sh
if [ "$?" -ne 0 ]
then
    exit -1
fi 

echo "Running unit tests.."
python3 /root/app/server/dbscripts/ut.py -v
if [ "$?" -ne 0 ]
then
    exit -1
fi 
echo "All Unit tests passed"