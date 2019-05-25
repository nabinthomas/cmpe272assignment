""" @package Main entry point for Web server.
"""
import json
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
from functools import wraps
from six.moves.urllib.request import urlopen


## Create the App
app = Flask(__name__)
db = None;
mongo_client = None;
app.config.from_envvar('SERVER_CONFIG');

AUTH0_DOMAIN = "nthomas.auth0.com"
ALGORITHMS = ["RS256"]
API_IDENTIFIER = "https://0.0.0.0:3010/api/private"
CLIENT_ID = 'QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG'
CLIENT_SECRET = app.config['CLIENT_SECRET']

token = ""
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
    
    loggedinUser='Guest'

    print ("Base url with port",request.host_url)

    # TODO: Validate the auth_token and Get the Users full name from the session information. 
    if (request.cookies.get('auth_token') is not None):
        loggedinUser = request.cookies.get('userFullName')

    rendered_page = render_template('default.html', 
			            serverTime=now, 
			            pageWelcomeMessage="Welcome to aMAZE.com Online Book Store", 
                        userFullName=loggedinUser,
			            pageTitle="aMAZE.com Online Book Store",
                        teamMembers=["Binu Jose", "Ginto George", "Nabin Thomas", "Sandeep Panakkal"]);
    response = app.make_response(rendered_page);
    response.set_cookie('base_url', request.host_url);
    return response;

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

@app.route('/api', methods=['GET'])
def help():
    """
    Default API handler. Returns the API documentation
    eg:  curl -XGET https://localhost/api
    """
    return encodeJsonResponse(api_help_message, ReturnCodes.SUCCESS);

@app.route('/api/deleteuser', methods=['DELETE'])
def deleteUser():
    """
    API Handler for deleting a user. 
    This will not be implemented and is just a placeholder as an example in case we need this later.
    eg: curl -XDELETE -H 'Content-Type: application/json' https://localhost/api/deleteuser
    """
    return encodeJsonResponse({}, ReturnCodes.ERROR_NOT_IMPLEMENTED);

def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    print (request.headers)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        print ("Enter requires_auth  ")
        #validate email-id and access_token 
        token = get_token_auth_header() #get access token 
        print ("Token recieved : " + token)
        customerEmail = find_customer_email(db, token)
        if(customerEmail is None) :
            print ("Exit requires_auth : Error : customer email not found")
            raise AuthError({"code": "invalid_header",
                        "description": "Invalid header. "
                        "Incorrect Access Token"}, 401) 
        return f(*args, **kwargs)
    return decorated

def get_id_token_payload(token):
    """Determines if the access token is valid
    """
     
    print ("Enter get_id_token_payload")
 
    print ("requires_auth token = " + token )
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read().decode("utf8"))
    print ("jwks" + jsonurl.read().decode("utf8"))

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "description":
                        "Invalid header. "
                        "Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header HS",
                        "description":
                        "Invalid header. "
                        "Use an HS S256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    print("rsa_key =", rsa_key)
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience="QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG",
                issuer="https://"+AUTH0_DOMAIN+"/"
                
            )

            print( "payload :" , json.dumps(payload, indent=2))
            #return json.dumps(payload, indent=2)
            return  payload 
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError as e:
            print(e)
            #print(API_IDENTIFIER)
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                " please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

def clear_all_cookies(response):
    """
    Helper function to clear Cookies set by this application. 
    Add Any additional cookies if set anywhere else to the end of the list
    """
    restrictTo = request.host
    if (restrictTo == "localhost"):
        restrictTo= None
        
    response.set_cookie('auth_token', value='', expires=0, domain=restrictTo)
    response.set_cookie('userFullName', value='', expires=0, domain=restrictTo)
    response.set_cookie('userEmailId', value='', expires=0, domain=restrictTo)
    response.set_cookie('customerId', value='', expires=0, domain=restrictTo)
    response.set_cookie('userPicture', value='', expires=0, domain=restrictTo)
    return response

@app.route('/logout', methods=['GET'])
def page_logout():
    accessToken = request.cookies.get('auth_token')
    if (accessToken is not None):
        customer = find_customer_with_token(db, accessToken)
        if (customer is not None):
            update_customer_session_data(db, customer['email'], customer['name'], '', '')

    rendered_page = render_template('logout.html', 
                LogoutMessage="You have been Logged out sucessfully",
                ExtraDetails=''
			);
    response = app.make_response(rendered_page )  
    response = clear_all_cookies(response)

    return response

@app.route('/loginfailed/<string:errorCode>', methods=['GET'])
def page_loginFailed(errorCode):
    rendered_page = render_template('logout.html', 
            LogoutMessage="Login Failed !!!",
            ExtraDetails=errorCode
        );
    response = app.make_response(rendered_page)  
    response = clear_all_cookies(response)
    return response

@app.route('/api/loginsuccess', methods=['GET'])
def loginSuccess():
    """
    API To pass successful user auth from auth0. 
    This gets the response "code" from the auth0 server and issue a redirect to locahost/api/loginsuccess

    open in browser: https://nthomas.auth0.com/authorize?response_type=code&client_id=QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG&redirect_uri=https://localhost/api/loginsuccess&scope=openid%20profile%20email&state=xyzABC123
    then login. and then this will be called with code and state as params. 
    """
    
    print ("Enter /api/loginsuccess");
    app.logger.info("Enter /api/loginsuccess")
    customerEmail = ''
    customerName = ''
    accessToken = ''
    
    loginStatus = ReturnCodes.ERROR_AUTHENTICATE;
    payload = request.args;
    print ("Client login request: [", payload, "]")

    try:
        code = request.args['code']
        state = request.args['state']
        print ("Client Code received:", code)
        print ("Client State received:", state)

        conn = http.client.HTTPSConnection("nthomas.auth0.com")

        #payload = "{\"code\":str(code),\"client_id\":\"QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG\",\"client_secret\":\"aDoe0md20-pFTGP6_XmoazFiUZdYN1Ze5CwxX21qDl1U_MaYbasmuJ4fjb7fDNlZ\",\"audience\":\"https://localhost/login\",\"grant_type\":\"client_credentials\"}"
        #payload = "grant_type=authorization_code&client_id=%24%7Baccount.clientId%7D&client_secret=YOUR_CLIENT_SECRET&code=YOUR_AUTHORIZATION_CODE&redirect_ui=https%3A%2F%2F%24%7Baccount.callback%7D"
    
        host_base_url = request.base_url
        print ("Host Base URL Was : " + host_base_url);
    
        payload = 'grant_type=authorization_code&client_id=' + CLIENT_ID + \
                    '&client_secret=' + CLIENT_SECRET + \
                    '&code=' + code + \
                    '&redirect_uri=' + host_base_url 

        fullurl = "https://" + AUTH0_DOMAIN + "/oauth/token" + payload
        print (fullurl)

        headers = { 'content-type': 'application/x-www-form-urlencoded' }

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        datareceived = res.read()
        print("Data is = " , datareceived.decode("utf-8"))
        data = json.loads(datareceived.decode("utf-8"))
        print("Data was = " , datareceived.decode("utf-8"))
        try:
            id_token_payload = get_id_token_payload(data["id_token"]) 
            print("id_token_payload got  ")
            print("id_token_payload got" + json.dumps(id_token_payload) )
            customerEmail = id_token_payload ['email']
            customerName = id_token_payload['name']
            customerPicture = id_token_payload['picture']
            accessToken = data["access_token"]
            print("calling update_customer_session_data")
            update_customer_session_data(db, customerEmail, customerName, customerPicture, accessToken)
            print("calling Done update_customer_session_data")
            extraData = {
                "Received" : {
                    "code" : code,
                    "state" : state
                },
                "access_token" : data["access_token"]
            }
            loginStatus = ReturnCodes.SUCCESS;
        except Exception as e:
            print ('get_id_token_payload Failed : '+ str(e))
            loginStatus = ReturnCodes.ERROR_AUTHENTICATE;
        loginStatus = ReturnCodes.SUCCESS;
    except Exception as e:
        print ('Failed : '+ str(e))
        loginStatus = ReturnCodes.ERROR_AUTHENTICATE;

    if (loginStatus == ReturnCodes.SUCCESS):
        customer = find_customer_with_token(db, accessToken)
        if customer is None: 
            loginStatus = ReturnCodes.ERROR_AUTHENTICATE

    if (loginStatus == ReturnCodes.SUCCESS):
        redirect_to_index = redirect('/')
        response = app.make_response(redirect_to_index)  
        restrictTo = request.host
        if (restrictTo == "localhost"):
            restrictTo= None
        
        response.set_cookie('auth_token',value=accessToken, domain=restrictTo)
        response.set_cookie('userFullName',value=customer['name'], domain=restrictTo)
        response.set_cookie('customerId',value=str(customer['customerId']), domain=restrictTo)
        response.set_cookie('userEmailId',value=str(customer['email']), domain=restrictTo)
        response.set_cookie('userPicture',value=customer['picture'], domain=restrictTo)
        return response
    else:
        redirect_url = '/loginfailed/' + loginStatus
        redirect_to_index = redirect(redirect_url)
        response = app.make_response(redirect_to_index)  
        return response


@app.route('/api/neworder', methods=['POST'])
def newOrder():
    """
    API To create a new order
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' https://localhost/api/neworder -d '{"CustomerId" : 2, "Items" : [ {"BookId": "978-1503215678", "qty" : 1} ] }'
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
    eg: curl -XPUT -H 'Content-Type: application/json' https://localhost/api/fulfillorder/1234 -d '{"book" : "12314", "copies" : 3}'
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
@requires_auth
def books():
    """
    Handle API to request details of all books
    eg: curl -XGET https://localhost/api/books
    """
    print( "Entering  books")

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
@requires_auth
def book_default():
    """
    Handle and error out case when book detail is requested without a book isbn number
    eg: curl -XGET https://localhost/api/book
    """
    return encodeJsonResponse({}, ReturnCodes.ERROR_INVALID_PARAM)



@app.route('/api/book/<string:isbn13>', methods=['GET'])
@requires_auth
def book_isbn(isbn13):
    """
    Get the details about a book. 
    @param - isbn13 - ISBN 13 value as a string for the book.
    TODO get real data from the database
    curl -XGET https://localhost/api/book/13455
    curl -XGET https://localhost/api/book/978-1503215680
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


@app.route('/api/addtocart', methods=['POST'])
@requires_auth
def addToCart():
    """
    API To add book to cart
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' https://localhost/api/addtocart -d '{"CustomerId" : 2, "Items" : {"BookId": "978-1503215678", "qty" : 1} }'
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
@requires_auth
def deleteCart():
    """
    API To delete user's cart
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' https://localhost/api/deletecart -d '{"CustomerId" : 2} }'
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
@requires_auth
def placeOrder():
    """
    API To place order from customer cart
    TODO Document the payload format and process it
    eg: curl -XPOST -H 'Content-Type: application/json' https://localhost/api/placeorder -d '{"CustomerId" : 2} }'
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

@app.route('/api/cart/<string:customerId>', methods=['GET'])
@requires_auth
def customer_cart(customerId):
    """
    Get the details about a customer's cart. 
    @param - customerId
    TODO get real data from the database
    curl -XGET https://localhost/api/cart/2
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
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc');
