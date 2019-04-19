#!/bin/bash

# Central place to start processes/services for the Web app.

#Start Mongodb database server
service mongodb start

#import test data to mongodb from csv after converting to json
cd test
python3 csvTojson.py books.csv books.json
python3 csvTojson.py customers.csv customers.json
python3 csvTojson.py orders.csv orders.json  
mongoimport books.json
mongoimport customers.json 
mongoimport orders.json 

cd ..
#Start the web server
#This should be started at the end
python3 app/server/main.py 
