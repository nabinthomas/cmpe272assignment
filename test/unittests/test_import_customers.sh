#!/bin/bash

data_dir=/root/test/unittests/data
scripts_dir=/root/test/unittests/

echo "Running Test: $0"

python3 ${scripts_dir}/csvTojson.py ${data_dir}/customers.csv ${data_dir}/customers.schema.json ${data_dir}/customers.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/customers.csv"
    exit -1
fi 
mongoimport -d test --drop ${data_dir}/customers.json
if [ "$?" -ne 0 ]
then
    echo "import failed for ${data_dir}/customers.json"
    exit -1
fi 
rm -rf ${data_dir}/customers.json
echo "Test $0 completed successfully"