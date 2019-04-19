## @package Main entry point for Web server.
  
import datetime
import pytz
from flask import Flask, render_template
import pymongo  
from pymongo import MongoClient

## Create the App
app = Flask(__name__)

@app.route('/mongo')
## Handle request for default page. 
def mongo():
    myclient = MongoClient()
    mydb = myclient["test"]

    ret = "<html>"

    ret = ret + "<h1> Books </h1>"
    mycol = mydb["books"]
    for x in mycol.find():
        print(x)
        ret = ret + str(x)

    ret = ret + "<h1> Customers </h1>"
    mycol = mydb["customers"]
    for x in mycol.find():
        print(x)
        ret = ret + str(x)

    mycol = mydb["orders"]
    ret = ret + "<h1> Orders </h1>"
    for x in mycol.find():
        print(x)
        ret = ret + str(x)
    
    ret = ret + "<html>"
    return ret

    

@app.route('/')
## Handle request for default page. 
def mainPage():
    now = datetime.datetime.now(pytz.timezone('US/Pacific'));

    return render_template('template.html', 
			serverTime=now, 
			pageWelcomeMessage="Welcome to Team aMAZE!", 
			pageTitle="aMAZE.com Online Book Store",
            teamMembers=["Binu Jose", "Ginto George", "Nabin Thomas", "Sandeep Panakkal"]);

if __name__ == '__main__':
        ## Start the http server
        app.run(host='0.0.0.0', port=80);

