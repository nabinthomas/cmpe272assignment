#!/bin/bash

# Central place to start processes/services for the Web app.

#Start Mongodb database server
service mongodb start

## Import books
python3 ./test/unittests/csvTojson.py ./test/unittests/data/books.csv ./test/unittests/data/books.schema.json ./test/unittests/data/books.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/books.csv"
    exit -1
fi 
mongoimport -d test --drop ./test/unittests/data/books.json

##Import orders
python3 ./test/unittests/csvTojson.py ./test/unittests/data/orders.csv ./test/unittests/data/orders.schema.json ./test/unittests/data/orders.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/orders.csv"
    exit -1
fi 
mongoimport -d test --drop ./test/unittests/data/orders.json

##Import customers
python3 ./test/unittests/csvTojson.py ./test/unittests/data/customers.csv ./test/unittests/data/customers.schema.json ./test/unittests/data/customers.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/orders.csv"
    exit -1
fi 
mongoimport -d test --drop ./test/unittests/data/customers.json

#Start the web server
#This should be started at the end
PYTHONPATH=/root/app/ python3 app/server/main.py  mongodb://localhost/test &
bash 
