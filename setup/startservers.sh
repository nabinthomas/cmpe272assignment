#!/bin/bash

# Central place to start processes/services for the Web app.

#Start Mongodb database server
service mongodb start

#import test data to mongodb from csv after converting to json
cd test
python3 csvTomongo.py books.csv 
python3 csvTomongo.py customers.csv 
python3 csvTomongo.py orders.csv  


cd ..
#Start the web server
#This should be started at the end
python3 app/server/main.py 
