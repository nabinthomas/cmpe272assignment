import sys
import pymongo

from server.dbscripts.update_inventory import * 
from server.dbscripts.list_books import * 

def import_books_inventory(db) :
    db.books.delete_many({})
    db.books.insert_one({ "Title" : "Image Processing & Mathematical Morphology", "Author" : [ "Shih, Frank" ], "Genre" : "signal_processing", "Page" : 241, "Publisher" : "CRC", "Price" : 24.1, "ISBN-13" : "978-1503215680", "Inventory" : 40 })
     
def add_one_temp_order(db) :
    db.orders.delete_many({})
    db.orders.insert_one({"OrderID": 3, "CustomerId": 2, "Items": [{"BookId": "978-1503215680", "qty": 30, "SellingPrice": 24.0}], "Shipping": {"Address": "100 W Tasman Dr, San Jose, 95134", "Status": "InProgress", "Provider": "Fedex", "Type": "2 day shipping", "ShippingDate": "4/12/2019", "DeliveryDate": "4/14/2019 "}, "PaymentType": "Cash On Delivery"})
    #return the order Id
    return 3 

def fulfill_order(mongoClient, db, orderId):
    '''
    Update an Order   
    param db - reference to the db ob
    param orderId - order Id of the oder to be updated, canot be None
    
    example order record: 
    {"OrderID": 3, "CustomerId": 2, "Items": [{"BookId": "978-1503215680", "qty": 3, "SellingPrice": 24.0}], "Shipping": {"Address": "100 W Tasman Dr, San Jose, 95134", "Status": "InProgress", "Provider": "Fedex", "Type": "2 day shipping", "ShippingDate": "4/12/2019", "DeliveryDate": "4/14/2019 "}, "PaymentType": "Cash On Delivery"}

    return true when successful, false when failed. 
    '''

    orders_coll = db['orders'] 
    record_to_update = orders_coll.find_one({"OrderID" : orderId}) 
    if record_to_update is None:
        print ("Error: update order , order id not found in db")
        return False

    book_order_list = record_to_update["Items"]
    # verify whether the order can be fulfilled minimum verification 
    # check whether the number of books requested already present .
    #session = db.getMongo().startSession()
    with  mongoClient.start_session() as s:
        s.start_transaction()
     
        is_order_ok_to_fulfill = True;
        for book in book_order_list:
            bookId = book ['BookId']
            qty = book['qty']
            if (qty > get_bookcount(db, bookId)):
                    is_order_ok_to_fulfill = False;
                    break;
        
        print ("1 is_order_ok_to_fulfill = " , is_order_ok_to_fulfill)
        if (is_order_ok_to_fulfill == True):
            for book in book_order_list:
                bookId = book ['BookId']
                qty = book['qty'] * -1 ;
                db.books.find_one_and_update({'ISBN-13':bookId}, {"$inc": {'Inventory': qty}}, return_document=ReturnDocument.AFTER)
        print ("2 is_order_ok_to_fulfill = " , is_order_ok_to_fulfill)
        order = db.orders.find_one({ "OrderID" : { "$eq": orderId }})
        if(is_order_ok_to_fulfill == True):
            order["Shipping"]["Status"] = "Complete";
        else :
            order["Shipping"]["Status"] = "OnHold";
            
        orders_coll.find_one_and_replace({"OrderID" : orderId},order)
        s.commit_transaction()

    return  is_order_ok_to_fulfill;

if __name__ == "__main__":

    '''
    Orders schema: 
    {  
    "OrderID" : 2 , 
    "CustomerId" : 2, 
     "Items" :
        [
            {"BookId": "978-1503215678", "qty" : 1, "SellingPrice": 22},
            {"BookId": "9978-1503215677", "qty" : 3, "SellingPrice": 23}
        ], 
    "Shipping" :  
            {
            "Address": "4321 Avery Ranch, San Mateo, CA 95123",
            "Status" : "InProgress", 
            "Provider" : "UPS",
            "Type" : "Overnight shipping", 
                     "ShippingDate":"",
                    "DeliveryDate":""
             }, 
        "PaymentType": "Cash On Delivery"
    }
'''

  
    mongodb_uri = "mongodb://localhost/test"
    mongoClient = pymongo.MongoClient(mongodb_uri)
    db = mongoClient.get_database()
    import_books_inventory(db);
    orderId = add_one_temp_order(db) ;
    
    order = db.orders.find_one({ "OrderID" : { "$eq": orderId }  })
    print("Before Order update order:   ", str(order) , "\n\n\n\r" );

    print("\r\n  ");
    fulfill_order(mongoClient=mongoClient, db=db, orderId =orderId);
    order = db.orders.find_one({ "OrderID" : { "$eq": orderId }  })
    print("After  Order update order:   ", str(order));
   
    exit(0)


