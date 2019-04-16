#!/bin/bash

# Central place to start processes/services for the Web app.

#Start Mongodb database server
service mongodb start

#Start the web server
#This should be started at the end
python3 app/server/main.py