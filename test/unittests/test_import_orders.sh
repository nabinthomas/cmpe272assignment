#!/bin/bash

data_dir=/root/test/unittests/data
scripts_dir=/root/test/unittests/

echo "Running Test: $0"

python3 ${scripts_dir}/csvTojson.py ${data_dir}/orders.csv ${data_dir}/orders.schema.json ${data_dir}/orders.json 

if [ "$?" -ne 0 ]
then
    echo "csv to json failed for ./data/orders.csv"
    exit -1
fi 
mongoimport -d test  --drop ${data_dir}/orders.json
if [ "$?" -ne 0 ]
then
    echo "import failed for ./data/orders.json"
    exit -1
fi 
rm -rf ${data_dir}/orders.json
echo "Test $0 completed successfully"