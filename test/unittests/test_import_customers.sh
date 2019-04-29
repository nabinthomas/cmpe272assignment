#!/bin/bash

echo "Running Test: $0"

python3 csvTojson.py ./data/customers.csv ./data/customers.schema.json ./data/customers.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/customers.csv"
    exit -1
fi 
mongoimport -d test --drop ./data/customers.json
if [ "$?" -ne 0 ]
then
    echo "import failed for ./data/customers.json"
    exit -1
fi 
rm -rf ./data/customers.json
echo "Test $0 completed successfully"