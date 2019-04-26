import sys
import pymongo
import bson
from bson.objectid import ObjectId

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