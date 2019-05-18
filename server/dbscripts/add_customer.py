import sys
import pymongo
import bson
from bson.objectid import ObjectId



def find_customer_email(db, accessToken):
    '''
    Find the customer email id 
    param db - reference to the db ob
    param accessToken - Access Token 
    returns en=mail id when success 
    {} on fail  {"email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas" }
    '''
     
    # Created or Switched to collection name: customers 
    customer_collection = db['customers'] 
    dbReturn = customer_collection.find_one ({'accessToken': accessToken}) 
    if (dbReturn is None) :
        print ("find_customer_email fail")
        return None
    else :
        print(dbReturn)
        return dbReturn["email"]



def update_customer_session_data(db, customerEmail, customerName, accessToken):
    '''
    Update session data for customer
    param db - reference to the db ob
    param customerEmail - Customer Email 
    param customerName - Customer Name 
    param accessToken - Access Token 
        {"email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas" }
    return 0 when successful, -1 when failed. 
    '''
    print("update_customer_session_data " + customerEmail +" "+ customerName+" " + accessToken )
    # Created or Switched to collection name: customers 
    customer_collection = db['customers'] 
    dbReturn = customer_collection.find_one_and_update({'email':customerEmail,'name':customerName},
                                                        {'$set': {'accessToken': accessToken}},
                                                        return_document=pymongo.ReturnDocument.AFTER) 
    if dbReturn is None:
        customerInfo = {"email" : customerEmail, "name" : customerName }
        add_new_customer(db, customerInfo)
        dbReturn = customer_collection.find_one_and_update({'email':customerEmail,'name':customerName},
                                                        {'$set': {'accessToken': accessToken}},
                                                        return_document=pymongo.ReturnDocument.AFTER) 

    upserted_record = customer_collection.find_one({'email':customerEmail,'name':customerName}) 
    print(upserted_record)

    return upserted_record

def add_new_customer(db, customerInfo):
    '''
    Adds a new Customer
    param db - reference to the db ob
    param customerInfo - Customer Information 
        {"email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas" }
    return 0 when successful, -1 when failed. 
    '''
     
    # Created or Switched to collection name: customers 
    collection = db['customers'] 

    
    name = customerInfo["name"]
    email = customerInfo["email"]
    print ("\r\nCustomer name : " + name)
    print ("EMAIL id : " + email)
        
    
    collection.create_index( [("email", pymongo.ASCENDING) ], unique = True )
    customerInfo["customerId"] = ObjectId();
    
    try:
        dbReturn = collection.insert_one(customerInfo)
    except pymongo.errors.DuplicateKeyError:
        print("User with this email id already exist")
        return ({}) 

    inserted_record = collection.find_one({"_id" : ObjectId(str(dbReturn.inserted_id))}) 
    print(dbReturn.inserted_id)

    return inserted_record 

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 4:
        print("Usage: python add_customer.py mongodb_uri customername email")
        exit(-1)

    mongodb_uri = argv[1]
    customername = argv[2]
    email = argv[3]

    customerInfo = {
        "name" : customername,
        "email": email
    }
    
    db = pymongo.MongoClient(mongodb_uri).get_database()

    customers=db["customers"]
    
    retval = add_new_customer(db, customerInfo)
    if (retval != {}):
        print ("Successfully added Customer:" + str(customerInfo))
    else:
        print ("Failed to add Customer  :" + str(customerInfo))
        exit (-1)

    exit (0)