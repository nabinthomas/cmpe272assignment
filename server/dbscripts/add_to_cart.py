import sys
import pymongo
from server.dbscripts.add_customer import *
from server.dbscripts.create_order import * 
from server.dbscripts.update_inventory import * 
from server.dbscripts.list_books import *
from server.dbscripts.process_order import *

def import_customers(db) :
    db.customers.insert_one({  "customerId" : 1, "email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas"  })
    db.customers.insert_one({  "customerId" : 2, "email" : "sandeep.panakkal@gmail.com", "name" : "Sandeep Panakkal"  })
    db.customers.insert_one({  "customerId" : 3, "email" : "ginto100@gmail.com", "name" : "Ginto George"  })
    db.customers.insert_one({  "customerId" : 4, "email" : "binu.jose@gmail.com", "name" : "Binu Jose"  })

def add_to_cart(db, customerId, cart):
    '''
    Adds book to cart
    param db - reference to the db ob
    param customerInfo - Customer Information 
        {"email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas" }
    return new_cart when successful, {} when failed. 
    '''

    print("new cart:", cart)

    # Find customer 
    customer = db.customers.find_one({ "customerId" : { "$eq": customerId }  })
    print("Customer Found = ", str(customer));

    if customer is None:
        print ("Error: add to cart,  customer id [",customerId,"] not found in db")
        return {}

    qty = cart['qty']
    bookId = cart['BookId']
    inserted_cart = db.customers.find_one_and_update({'customerId':customerId ,'cart.BookId':bookId}, { '$inc': {'cart.$.qty': qty}}, return_document=ReturnDocument.AFTER)

    if inserted_cart is None:
        print("Purchasing new book ", bookId)
        inserted_cart = db.customers.find_one_and_update({'customerId':customerId}, {'$push': {'cart': cart}}, return_document=ReturnDocument.AFTER)
    else:
        print("Updated book qty for book ", bookId)
   
    print ("Inserted cart record = ", str(inserted_cart))
    return inserted_cart['cart']

def delete_cart(db, customerId):
    '''
    Delete user's cart
    param db - reference to the db
    customerId - Customer Id
    return new_cart when successful, {} when failed.
    '''
    
    print("Customer Id:", customerId)
    # Find customer 
    customer = db.customers.find_one({ "customerId" : { "$eq": customerId }  })
    if customer is None:
        print ("Error: deleting from cart,  customer id [",customerId,"] not found in db")
        return {}

    print("Customer Found = ", str(customer));
    
    updated_customer_record = db.customers.find_one_and_update({'customerId':customerId}, {'$set': {'cart': []}}, return_document=ReturnDocument.AFTER)
        
    print ("Deleted customer record = ", str(updated_customer_record))
    return customerId

def get_cart(db, customerId):
    '''
    Get cart
    param db - reference to the db ob
    param customerId - Customer Information 
    return cart when successful, {}
    '''

    # Find customer 
    customer = db.customers.find_one({ "customerId" : { "$eq": customerId }  })
    print("Customer Found = ", str(customer));

    if customer is None:
        print ("Error: add to cart,  customer id [",customerId,"] not found in db")
        return {}

    try:
        cus_cart = db.customers.find_one({'customerId':customerId})['cart']
    except KeyError:
        print("No cart for customer ", customerId)
        return {}
   
    print ("Inserted cart record = ", str(cus_cart))
    if cus_cart is None:
        return {}
    else:
        return cus_cart

if __name__ == "__main__":
    argv = sys.argv
    '''
    if len(argv) < 2:
        print("Usage: python create_order.py mongodb_uri orderId customerId book_order_list shipping_details paymentType")
        exit(-1)
    mongodb_uri = argv[1]
    customerId = argv[2] 	
    new_cart = argv[3] 	
    '''
    mongodb_uri = "mongodb://localhost/test"
    customerId = 2
    new_cart = {"BookId": "978-1503215678", "qty" : 1, "SellingPrice": 22}
    db = pymongo.MongoClient(mongodb_uri).get_database()

    import_customers(db) # Temporary import code

    inserted_record = add_to_cart(db, customerId, new_cart)
    
    if (inserted_record != {}):
        print("add cart successfully:")
        print("cart:" + str(inserted_record))
    else:
       print("Add cart failed")
       exit(-1) 

    exit(0)
