#!/bin/bash

# Start local mongodb instance
service mongodb start

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

# Other unit tests
echo "Running unit tests.."
PYTHONPATH=/root/app/server/dbscripts/ python3 /root/test/unittests/ut_transactions.py -v
if [ "$?" -ne 0 ]
then
    exit -1
fi 
echo "All Unit tests passed"