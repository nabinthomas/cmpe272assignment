import sys
import pymongo
from  update_inventory import *


def import_books_inventory(db) :
    db.books.insert_one({  "Title" : "Fundamentals of Wavelets", "Author" : [ "Goswami, Jaideva", "Binu Jose" ], "Genre" : "signal_processing", "Page" : 228, "Publisher" : "Wiley", "Price" : 22.8, "ISBN-13" : "978-1503215672", "Inventory" : 10 })
    db.books.insert_one({  "Title" : "Data Smart", "Author" : [ "Foreman, John" ], "Genre" : "data_science", "Page" : 235, "Publisher" : "Wiley", "Price" : 23.5, "ISBN-13" : "978-1503215673", "Inventory" : 20 })
    db.books.insert_one({  "Title" : "God Created the Integers", "Author" : [ "Hawking, Stephen" ], "Genre" : "mathematics", "Page" : 197, "Publisher" : "Penguin", "Price" : 19.7, "ISBN-13" : "978-1503215674", "Inventory" : 40 })
    db.books.insert_one({ "Title" : "Superfreakonomics", "Author" : [ "Dubner, Stephen" ], "Genre" : "economics", "Page" : 179, "Publisher" : "HarperCollins", "Price" : 17.9, "ISBN-13" : "978-1503215675", "Inventory" : 60 })
    db.books.insert_one({ "Title" : "Orientalism", "Author" : [ "Said, Edward" ], "Genre" : "history", "Page" : 197, "Publisher" : "Penguin", "Price" : 19.7, "ISBN-13" : "978-1503215676", "Inventory" : 69 })
    db.books.insert_one({ "Title" : "Nature of Statistical Learning Theory, The", "Author" : [ "Vapnik, Vladimir" ], "Genre" : "data_science", "Page" : 230, "Publisher" : "Springer", "Price" : 23, "ISBN-13" : "978-1503215677", "Inventory" : 80 }) 
    db.books.insert_one({ "Title" : "Integration of the Indian States", "Author" : [ "Menon, V P" ], "Genre" : "history", "Page" : 217, "Publisher" : "Orient Blackswan", "Price" : 21.7, "ISBN-13" : "978-1503215678", "Inventory" : 90 })
    db.books.insert_one({ "Title" : "The Drunkard's Walk", "Author" : [ "Mlodinow, Leonard" ], "Genre" : "science", "Page" : 197, "Publisher" : "Penguin", "Price" : 19.7, "ISBN-13" : "978-1503215679", "Inventory" : 50 })
    db.books.insert_one({ "Title" : "Image Processing & Mathematical Morphology", "Author" : [ "Shih, Frank" ], "Genre" : "signal_processing", "Page" : 241, "Publisher" : "CRC", "Price" : 24.1, "ISBN-13" : "978-1503215680", "Inventory" : 49 })
    db.books.insert_one({ "Title" : "How to Think Like Sherlock Holmes", "Author" : [ "Konnikova, Maria" ], "Genre" : "psychology", "Page" : 240, "Publisher" : "Penguin", "Price" : 24, "ISBN-13" : "978-1503215681", "Inventory" : 30 })


# TODO:Fix CASING
def create_new_order(db, orderId, customerId, book_order_list, shipping_details, paymentType):
    '''
    Creates a new Order
    param db - reference to the db ob
    param customerInfo - Customer Information 
        {"email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas" }
    return 0 when successful, -1 when failed. 
    '''

    # Create Order
    new_order = {}
    new_order.update({"OrderID":orderId})
    new_order.update({"CustomerId":customerId})
    new_order["Items"] = book_order_list
    new_order["Shipping"] = shipping_details
    new_order.update({"PaymentType":"Cash On Delivery"})

    # TODO: Make order insertion and inventory update Atomic
    # Confirm inventory
    for items_dict in book_order_list: 
        bookId = items_dict["BookId"]
        requested_qty = items_dict["qty"]
        in_stock_count = get_available_book_count(db, bookId)
        if int(in_stock_count) < int(requested_qty):
            print("BookId " + bookId + "Out of stock to fulfill order")           
            return {}

    orders_coll = db['orders'] 
    dbReturn = orders_coll.insert_one(new_order)
    if dbReturn is None:
        return {}

    # Update inventory if all items are in stock, else fail.
    for items_dict in book_order_list: 
        bookId = items_dict["BookId"]
        requested_qty = items_dict["qty"]
        updated_record = update_inventory(db, bookId, -requested_qty) # Update with -ve quantity for sale.
        if updated_record is None:
            return {}

    inserted_record = orders_coll.find_one({"_id" : ObjectId(str(dbReturn.inserted_id))}) 
    
    return inserted_record


if __name__ == "__main__":
    argv = sys.argv
    '''
    if len(argv) < 2:
        print("Usage: python create_order.py mongodb_uri orderId customerId book_order_list shipping_details paymentType")
        exit(-1)
    mongodb_uri = argv[1]
    orderId = argv[2] 	
    customerId = argv[3] 	
    book_order_list = argv[4] 	
    shipping_details = argv[5] 	
    paymentType = argv[6] 	
    '''
    mongodb_uri = "mongodb://localhost/test"
    orderId = 2
    customerId = 2
    book_order_list = [{"BookId": "978-1503215678", "qty" : 1, "SellingPrice": 22},{"BookId": "978-1503215675", "qty" : 3, "SellingPrice": 23}]
    shipping_details = {"Address": "4321 Avery Ranch, San Mateo, CA 95123","Status" : "InProgress","Provider" : "UPS","Type" : "Overnight shipping","ShippingDate":"","DeliveryDate":""}
    paymentType = "Cash On Delivery" 
    db = pymongo.MongoClient(mongodb_uri).get_database()

    import_books_inventory(db) # Temporary import code

    in_stock_count = get_available_book_count(db, "978-1503215678")
    in_stock_count1 = get_available_book_count(db, "978-1503215675")
    print("Inventory before Order creation: ")
    print("978-1503215678 : " + str(in_stock_count)) 
    print("978-1503215675 : " + str(in_stock_count1)+ "\r\n") 

    inserted_record = create_new_order(db, orderId, customerId, book_order_list, shipping_details, paymentType)
    
    if (inserted_record != {}):
        print("New Order created successfully:")
        print("Order created:" + str(inserted_record))
    else:
       print("New Order creation failed")
       exit(-1) 

    in_stock_count = get_available_book_count(db, "978-1503215678")
    in_stock_count1 = get_available_book_count(db, "978-1503215675")
    print("\r\n\r\nInventory after Order creation: ")
    print("978-1503215678 : " + str(in_stock_count)) 
    print("978-1503215675 : " + str(in_stock_count1)) 
     
    exit(0)
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

