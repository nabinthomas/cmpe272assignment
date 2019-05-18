""" @package Main entry point for Web server.
"""
  
import datetime
import pytz
from flask import Flask, render_template, jsonify, request, redirect
import pymongo  
from pymongo import MongoClient
from server.dbscripts.list_books import *
from server.dbscripts.create_order import *
from server.dbscripts.fulfill_order import *
from server.dbscripts.add_to_cart import *
import sys
import http.client
from jose import jwt
from six.moves.urllib.request import urlopen
import json

## Create the App
app = Flask(__name__)
db = None;
mongo_client = None;

'''
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

'''

@app.route('/')
def mainPage():
    """ Handle request for default page. 
    """
    now = datetime.datetime.now(pytz.timezone('US/Pacific'));

    return render_template('default.html', 
			serverTime=now, 
			pageWelcomeMessage="Welcome aMAZE.com Online Book Store", 
			pageTitle="aMAZE.com Online Book Store",
            teamMembers=["Binu Jose", "Ginto George", "Nabin Thomas", "Sandeep Panakkal"]);

@app.route('/books')
def page_books():
    """ Handle request for /books page. 
    """
    return render_template('books.html');

@app.route('/cart')
def page_cart():
    """ Handle request for /cart page. 
    """
    return render_template('cart.html');

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 0 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.context_processor
def override_url_for():
    """
    Generate a new token on every request to prevent the browser from
    caching static files.
    From : https://gist.github.com/itsnauman/b3d386e4cecf97d59c94
    """
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

########################################################################
# REST API Implementation
########################################################################
api_help_message = { "message":
    [
    "API Usage:",
    "    - GET    /api/books",
    "    - GET    /api/book/<isbn13>",
    "    - POST   /api/neworder data={'key': 'value'}",
    "    - PUT    /api/update/<orderid> data={'key': 'value_to_replace'}",
    "    - DELETE is not supported"
    ]
}

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

@app.route('/logout', methods=['GET'])
def logout():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index )  
    response.set_cookie('auth_token',value='', expires=0)
    ## TODO Clear all cookies here. 
    return response

@app.route('/cookie', methods=['GET'])
def create_cookie():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index)  
    restrictTo = request.host
    if (restrictTo == "localhost"):
        restrictTo= None
    # TODO change value to setup the Auth token and move this to loginsuccess handler
    response.set_cookie('auth_token',value='Nabin', domain=restrictTo)
    return response

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

@app.route('/api/loginsuccess', methods=['GET'])
def loginSuccess():
    """
    API To pass successful user auth from auth0. 
    This gets the response "code" from the auth0 server and issue a redirect to locahost/api/loginsuccess

    open in browser: https://nthomas.auth0.com/authorize?response_type=code&client_id=QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG&redirect_uri=http://localhost/api/loginsuccess&scope=openid%20profile%20email&state=xyzABC123
    then login. and then this will be called with code and state as params. 
    """
    print ("Enter /api/loginsuccess");
    app.logger.info("Enter /api/loginsuccess")
    
    response = {};
    payload = request.args;
    print ("Client login request: [", payload, "]")

    try:
        code = request.args['code']
        state = request.args['state']
        print ("Client Code received:", code)
        print ("Client State received:", state)

        conn = http.client.HTTPSConnection("nthomas.auth0.com")

        #payload = "{\"code\":str(code),\"client_id\":\"QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG\",\"client_secret\":\"aDoe0md20-pFTGP6_XmoazFiUZdYN1Ze5CwxX21qDl1U_MaYbasmuJ4fjb7fDNlZ\",\"audience\":\"http://localhost/login\",\"grant_type\":\"client_credentials\"}"
        #payload = "grant_type=authorization_code&client_id=%24%7Baccount.clientId%7D&client_secret=YOUR_CLIENT_SECRET&code=YOUR_AUTHORIZATION_CODE&redirect_ui=https%3A%2F%2F%24%7Baccount.callback%7D"
        CLIENT_ID = 'QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG'
        CLIENT_SECRET = 'aDoe0md20-pFTGP6_XmoazFiUZdYN1Ze5CwxX21qDl1U_MaYbasmuJ4fjb7fDNlZ' 
        AUTHORIZATION_CODE = code
        payload = 'grant_type=authorization_code&client_id=' + CLIENT_ID + \
                    '&client_secret=' + CLIENT_SECRET + \
                    '&code=' + AUTHORIZATION_CODE + \
                    '&redirect_uri=http://localhost/api/loginsuccess'

        fullurl = "https://nthomas.auth0.com/oauth/token" + payload
        print (fullurl)

        headers = { 'content-type': 'application/x-www-form-urlencoded' }

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        data_str = (str(data.decode("utf-8").replace('"',"'")))
        data_json = json.loads(data.decode("utf-8"))

        jsonurl = urlopen("https://"+ "nthomas.auth0.com" +"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read().decode("utf8"))

        response = {
            "Received" : {
                "code" : code,
                "state" : state,
                "token_data" : data_json,
                "jwks" : jwks # This should be removed once everything is working. 
            }
        }

        
        return encodeJsonResponse(response, ReturnCodes.SUCCESS);
    except Exception as e:
        print ('Failed : '+ str(e))
        return encodeJsonResponse(response, ReturnCodes.ERROR_INVALID_PARAM);


@app.route('/api/neworder', methods=['POST'])
def newOrder():
    """
    API To create a new order
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' http://localhost/api/neworder -d '{"CustomerId" : 2, "Items" : [ {"BookId": "978-1503215678", "qty" : 1} ] }'
    """
    response = {}
    payload = request.json;
    print ("new order:", payload)

    try:
        customerId = request.json['CustomerId']
        book_order_list = request.json['Items']
    except:
        return encodeJsonResponse(response, ReturnCodes.ERROR_INVALID_PARAM);

    new_order = create_new_order(db, 0, customerId, book_order_list, "none", "none")

    if new_order is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        del new_order['_id']
        new_order['OrderID'] = str(new_order['OrderID'])
        response["order_request"] = new_order
        returnCode = ReturnCodes.SUCCESS
    return encodeJsonResponse(response, returnCode);
    
@app.route('/api/fulfillorder', methods=['PUT'])
def fulfillorder_default():
    """
    API To update an order
    Order Id is a mandatory argument .    
    """
    return encodeJsonResponse({}, ReturnCodes.ERROR_INVALID_PARAM)

@app.route('/api/fulfillorder/<string:orderid>', methods=['PUT'])
def fulfillorder_orderid(orderid):
    """
    API To update an order
    @param orderid -> ID of the order to modify
    TODO Document the payload format and process it
    eg: curl -XPUT -H 'Content-Type: application/json' http://localhost/api/fulfillorder/1234 -d '{"book" : "12314", "copies" : 3}'
    """
    #make sure the oder id is an integer.
    try:
        OrderId= int (orderid)
    except:
        return encodeJsonResponse({}, ReturnCodes.ERROR_INVALID_PARAM)

    with  mongo_client.start_session() as s:
        s.start_transaction()
        status = fulfill_order(db,OrderId)
        s.commit_transaction()
    if (status == True) :
        returnCode = ReturnCodes.SUCCESS;
    else :
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    return encodeJsonResponse({"Status" : status }, returnCode);

@app.route('/api/books', methods=['GET'])
def books():
    """
    Handle API to request details of all books
    eg: curl -XGET http://localhost/api/books
    """
    response = {}
    books,total_book_count,page_count = get_all_books(db, 0, 0)
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

'''
def is_valid_json(func):
    def wrapper():
        print("Something is happening before the function is X called.")
        response = {}
        if request == None :
            print("Returning ERROR_INVALID_PARAM.")
            raise Exception("Both x and y have to be positive")
        else :
            print(" request is not non.  .", str(request))
            #return encodeJsonResponse(response, ReturnCodes.ERROR_INVALID_PARAM);
        return func()
    return wrapper
'''
@app.route('/api/addtocart', methods=['POST'])
#@is_valid_json
def addToCart():
    """
    API To add book to cart
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' http://localhost/api/addtocart -d '{"CustomerId" : 2, "Items" : {"BookId": "978-1503215678", "qty" : 1} }'
    """
    print("Inside  addToCart  .")
    response = {}
    try :
        customerId = request.json['CustomerId']
        cart_item = request.json['Items']
    except :
        return encodeJsonResponse(response, ReturnCodes.ERROR_INVALID_PARAM);
    payload = request.json;
    print ("add to cart:", payload)
    new_cart = add_to_cart(db, customerId, cart_item)

    if new_cart is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        response["cart_item"] = new_cart
        returnCode = ReturnCodes.SUCCESS
    return encodeJsonResponse(response, returnCode);

@app.route('/api/deletecart', methods=['DELETE'])
def deleteCart():
    """
    API To delete user's cart
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' http://localhost/api/deletecart -d '{"CustomerId" : 2} }'
    """
    response = {}

    try:
        customerId = request.json['CustomerId']
        deleted_cart = delete_cart(db, customerId)
    except:
        return encodeJsonResponse(response, ReturnCodes.ERROR_INVALID_PARAM)

    payload = request.json;
    print ("delete cart:", payload)
   

    if deleted_cart is {}:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        response["CustomerId"] = customerId
        returnCode = ReturnCodes.SUCCESS
    return encodeJsonResponse(response, returnCode);

@app.route('/api/placeorder', methods=['POST'])
def placeOrder():
    """
    API To place order from customer cart
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' http://localhost/api/placeorder -d '{"CustomerId" : 2} }'
    """
    response = {}
    try:
        customerId = request.json['CustomerId']
        
    except:
        return encodeJsonResponse(response, ReturnCodes.ERROR_INVALID_PARAM)

    # Fetch customer cart
    customer_cart = get_cart(db, customerId)
    print("Customer's cart: ", str(customer_cart))

    if len(customer_cart) is 0:
        return encodeJsonResponse({"Reason" : "Cart was empty"}, ReturnCodes.ERROR_OBJECT_NOT_FOUND)
    #place order
    new_order = create_new_order(db, 0, customerId, customer_cart, "none", "none")

    if new_order is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
        reason = "Customer ID was invalid"
        response["Reason": reason]
        print("create_new_order FAILED")
    else:
        del new_order['_id']
        new_order['OrderID'] = str(new_order['OrderID'])
        response["order_request"] = new_order
        
        returnCode = ReturnCodes.SUCCESS
        cid = delete_cart(db, customerId)
        
        if cid is not customerId:
            returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
            response = {}
            print("delete_cart FAILED")
            
    return encodeJsonResponse(response, returnCode);

@app.route('/api/cart/<int:customerId>', methods=['GET'])
def customer_cart(customerId):
    """
    Get the details about a customer's cart. 
    @param - customerId
    TODO get real data from the database
    curl -XGET http://localhost/api/cart/2
    """
    cart = get_cart(db, customerId)
    response = {"requested_cart": customerId}

    if cart is None:
        returnCode = ReturnCodes.ERROR_OBJECT_NOT_FOUND;
    else:
        for item in cart:
            book = get_bookdata(db, item['BookId'])
            item['Title'] = book ['Title']
        response["cart_details"] = cart
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
    mongo_client = pymongo.MongoClient(mongodb_uri);
    db = mongo_client.get_database()
    
    ## Start the http server
    app.run(host='0.0.0.0', port=80);
