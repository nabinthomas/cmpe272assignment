#!/bin/bash

data_dir=/root/test/unittests/data
scripts_dir=/root/test/unittests/

echo "Running Test: $0"

python3 ${scripts_dir}/csvTojson.py ${data_dir}/books.csv ${data_dir}/books.schema.json ${data_dir}/books.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/books.csv"
    exit -1
fi 
mongoimport -d test --drop ${data_dir}/books.json
if [ "$?" -ne 0 ]
then
    echo "import failed for ./data/books.json"
    exit -1
fi 
rm -rf ${data_dir}/books.json
echo "Test $0 completed successfully"