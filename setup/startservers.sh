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

#Start the web server
#This should be started at the end
PYTHONPATH=/root/app/ python3 app/server/main.py  mongodb://localhost/test &
bash 
