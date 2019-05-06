import sys
import pymongo

from server.dbscripts.update_inventory import * 

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

def process_order(db, orderId):
    '''
    Process an Order and mark as shipped. ( "InProgress" to "Shipped")
    param db - reference to the db ob
    param orderId - Order to process
    return processed order when successful, {} when failed. 
    '''

    # Find Order
    order = db.orders.find_one({ "OrderID" : { "$eq": orderId }  })
    print("Order Found = ", str(order));
    
    if (order["Shipping"]["Status"] != "InProgress"):
        return {}

    book_order_list = order["Items"] 

    # TODO: Make order insertion and inventory update Atomic
    # Confirm inventory
    for items_dict in book_order_list: 
        bookId = items_dict["BookId"]
        requested_qty = items_dict["qty"]
        in_stock_count = get_available_book_count(db, bookId)
        if int(in_stock_count) < int(requested_qty): 
            print("BookId " + bookId + " Out of stock to fulfill order")           
            return order

    # Update inventory if all items are in stock, else fail.
    for items_dict in book_order_list: 
        bookId = items_dict["BookId"]
        requested_qty = items_dict["qty"]
        updated_record = update_inventory(db, bookId, -requested_qty) # Update with -ve quantity for sale.
        print (bookId, requested_qty)
        if updated_record is None:
            return {}
    
    order = db.orders.find_one({ "OrderID" : { "$eq": orderId }  })
    order = update_order(db, orderId, "Shipped")

    return order

def update_order(db, orderId, new_shipping_state):
    '''
    Update Order
    param db - reference to the database
    param orderId - Unique Order Id
    param new_shipping_state - New shipping state (InProgress/Shipped/Delivered)
    return updated record when successful, {} when failed. 
    '''

    updated_record = db.orders.find_one_and_update({'OrderID':orderId}, {"$set": { 'Shipping' : {'Status': new_shipping_state}}}, return_document=ReturnDocument.AFTER)
    if updated_record is None:
        return {}
    print("\r\nUpdated Order record:" + str(updated_record))

    return updated_record

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

