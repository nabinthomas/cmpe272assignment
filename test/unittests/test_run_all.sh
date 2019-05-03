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

# DB Unit tests
echo "Running DB tests.."
PYTHONPATH=/root/app/server/dbscripts/ python3 /root/test/unittests/ut_transactions.py -v
if [ "$?" -ne 0 ]
then
    exit -1
fi 

#DB REST API Unit tests
echo "Running REST API tests.."
PYTHONPATH=/root/app/server/dbscripts/ python3 /root/test/unittests/ut_rest.py -v
if [ "$?" -ne 0 ]
then
    exit -1
fi 

echo "All Unit tests passed"