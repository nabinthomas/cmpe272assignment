""" @package Main entry point for Web server.
"""
  
import datetime
import pytz
from flask import Flask, render_template, jsonify, request
import pymongo  
from pymongo import MongoClient
from server.dbscripts.list_books import *
from server.dbscripts.create_order import *
import sys

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


########################################################################
# REST API Implementation
########################################################################
api_help_message = { "message":
"""
    API Usage:
 
        - GET    /api/booklist
        - GET    /api/get/<isbn13>
        - POST   /api/order data={"key": "value"}
        - PUT    /api/update/<orderid> data={"key": "value_to_replace"}
        - DELETE is not supported

"""}

class ReturnCodes:
    SUCCESS = "Success";
    ERROR_GENERIC = "ErrorGeneric";
    ERROR_AUTHENTICATE = "ErrorNotAuthenticated";
    ERROR_UNAUTHORIZED = "ErrorUnauthorized";
    ERROR_NOT_IMPLEMENTED = "ErrorNotImplemented";
    ERROR_INVALID_PARAM ="ErrorInvalidParam";
    ERROR_OBJECT_NOT_FOUND = "ErrorObjectNotFound"

def encodeJsonResponse(reply, statuscode):
    """
    Encodes a json response to send back to the client. 

    @param reply  -> this is a message or json object that is the result of the operation performed. 
    @param statuscode -> one of the values from ReturnCodes, for the status of the operation. 
    """
    return jsonify({ "status" : statuscode, "response" : reply});

@app.route('/api', methods=['GET'])
def help():
    """
    Default API handler. Returns the API documentation
    eg:  curl -XGET http://localhost/api
    """
    return encodeJsonResponse(api_help_message, ReturnCodes.SUCCESS);

@app.route('/api/deleteuser', methods=['DELETE'])
def deleteUser():
    """
    API Handler for deleting a user. 
    This will not be implemented and is just a placeholder as an example in case we need this later.
    eg: curl -XDELETE -H 'Content-Type: application/json' http://localhost/api/deleteuser
    """
    return encodeJsonResponse({}, ReturnCodes.ERROR_NOT_IMPLEMENTED);

@app.route('/api/neworder', methods=['POST'])
def newOrder():
    """
    API To create a new order
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' http://localhost/api/neworder -d '{"CustomerId" : 2, "Items" : [ {"BookId": "978-1503215678", "qty" : 1} ] }'
    """
    payload = request.json;

    print ("new order:", payload)

    customerId = request.json['CustomerId']
    book_order_list = request.json['Items']
    new_order = create_new_order(db, 0, customerId, book_order_list, "none", "none")

    response = {}

    if new_order is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        del new_order['_id']
        new_order['OrderID'] = str(new_order['OrderID'])
        response["order_request"] = new_order
        returnCode = ReturnCodes.SUCCESS
    return encodeJsonResponse(response, returnCode);
    
@app.route('/api/updateorder', methods=['PUT'])
def updateOrder_default():
    """
    API To update an order
    TODO Document the payload format and process it
    eg: curl -XPUT -H 'Content-Type: application/json' http://localhost/api/updateorder -d '{"book" : "12314", "copies" : 3}'
    """
    return encodeJsonResponse({}, ReturnCodes.ERROR_INVALID_PARAM)

@app.route('/api/updateorder/<string:orderid>', methods=['PUT'])
def updateOrder_orderid(orderid):
    """
    API To update an order
    @param orderid -> ID of the order to modify
    TODO Document the payload format and process it
    eg: curl -XPUT -H 'Content-Type: application/json' http://localhost/api/updateorder/1234 -d '{"book" : "12314", "copies" : 3}'
    """
    return encodeJsonResponse({"OrderID" : orderid, "updaterequest" : request.json}, ReturnCodes.ERROR_UNAUTHORIZED);

@app.route('/api/books', methods=['GET'])
def books():
    """
    Handle API to request details of all books
    eg: curl -XGET http://localhost/api/books
    """
    response = {}
    books = get_all_books(db)
    if books is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        json_docs = []
        for doc in books:
            del doc['_id']
            json_docs.append(doc)

        response["books"] = json_docs
        returnCode = ReturnCodes.SUCCESS

    return encodeJsonResponse(response, returnCode)

@app.route('/api/book', methods=['GET'])
def book_default():
    """
    Handle and error out case when book detail is requested without a book isbn number
    eg: curl -XGET http://localhost/api/book
    """
    return encodeJsonResponse({}, ReturnCodes.ERROR_INVALID_PARAM)

@app.route('/api/book/<string:isbn13>', methods=['GET'])
def book_isbn(isbn13):
    """
    Get the details about a book. 
    @param - isbn13 - ISBN 13 value as a string for the book.
    TODO get real data from the database
    curl -XGET http://localhost/api/book/13455
    curl -XGET http://localhost/api/book/978-1503215680
    """
    book = get_bookdata(db, isbn13)
    response = {"requested_book": isbn13}

    if book is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        del book['_id']
        response["book_details"] = book
        returnCode = ReturnCodes.SUCCESS
    return encodeJsonResponse(response, returnCode);


########################################################################
# MAIN
########################################################################
if __name__ == '__main__':
    ## Setup environment 
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python list_books.py mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]

    db = pymongo.MongoClient(mongodb_uri).get_database()
    ## Start the http server
    app.run(host='0.0.0.0', port=80);
        
