""" @package Main entry point for Web server.
"""
  
import datetime
import pytz
from flask import Flask, render_template
import pymongo  
from pymongo import MongoClient

## Create the App
app = Flask(__name__)

@app.route('/mongo')
def mongo():
    """ Handle request for page to dump mongodb. 
    @todo This need to be restricted to unit tests. 
    @todo Formatting to be changed to use template
    """
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
    ret = ret + ("<table border=2>")
    for row in mycol.find({}, {"_id":0}):
        ret = ret + ("<tr>")
        for key in row.keys():
            if (key != "_id"):
                header = "<th>" + key + "</th>"
                ret = ret + (header)
        ret = ret + ("</tr>")
        break;

    for row in mycol.find({}, {"_id":0}):
        ret = ret + ("<tr>")
        for key in row.keys():
            dataline = "<td>" + str(row[key]) + "</td>"
            ret = ret + (dataline)
        ret = ret + ("</tr>")
    ret = ret + "</table>"


    mycol = mydb["orders"]
    ret = ret + "<h1> Orders </h1>"
    for x in mycol.find():
        print(x)
        ret = ret + str(x)
    
    ret = ret + "<html>"
    return ret

    

@app.route('/')
def mainPage():
    """ Handle request for default page. 
    """
    now = datetime.datetime.now(pytz.timezone('US/Pacific'));

    return render_template('default.html', 
			serverTime=now, 
			pageWelcomeMessage="Welcome to Team aMAZE!", 
			pageTitle="aMAZE.com Online Book Store",
            teamMembers=["Binu Jose", "Ginto George", "Nabin Thomas", "Sandeep Panakkal"]);

if __name__ == '__main__':
        ## Start the http server
        app.run(host='0.0.0.0', port=80);

