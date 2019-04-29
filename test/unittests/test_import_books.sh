#!/bin/bash

echo "Running Test: $0"

python3 csvTojson.py ./data/books.csv ./data/books.schema.json ./data/books.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/books.csv"
    exit -1
fi 
mongoimport -d test --drop ./data/books.json
if [ "$?" -ne 0 ]
then
    echo "import failed for ./data/books.json"
    exit -1
fi 
rm -rf ./data/books.json
echo "Test $0 completed successfully"