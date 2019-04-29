#!/bin/bash

echo "Running Test: $0"

python3 csvTojson.py ./data/orders.csv ./data/orders.schema.json ./data/orders.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/orders.csv"
    exit -1
fi 
mongoimport -d test  --drop ./data/orders.json
if [ "$?" -ne 0 ]
then
    echo "import failed for ./data/orders.json"
    exit -1
fi 
rm -rf ./data/orders.json
echo "Test $0 completed successfully"