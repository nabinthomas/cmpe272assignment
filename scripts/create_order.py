import sys
import pymongo
import update_inventory


# TODO:Fix CASING
def create_new_order(db, orderId, customerId, book_order_list, shipping_details, paymentType):
    ret_status = 'failed'

    # Confirm inventory
    for items_dict in book_order_list: 
        for bookId, requested_qty, sell_price in items_dict.items():
            in_stock_count = get_available_book_count(db, bookId)
	    if in_stock_count <  requested_qty:
                return ret_status

    # Create Order
    new_order = {}
    new_order.append({"OrderID":orderId})
    new_order.append({"CustomerId":customerId})
    new_order["Items"] = book_order_list
    new_order["Shipping"] = shipping_details
    new_order.append({""PaymentType":"Cash On Delivery"})

    # TODO: Make order insertion and inventory update Atomic
    order_col = db['orders']] 
    order_col.insert_one(new_order) 
    # TODO: ERROR handling, exit on failure
    
    # Update inventory if all items are in stock, else fail.
    update_inventory(db, id, incoming_inv):
    for items_dict in book_order_list: 
        for bookId, requested_qty, sell_price in items_dict.items():
            update_inventory(db, bookId, -requested_qty) # Update with -ve quantity for sale.

    ret_status = 'success'
    return ret_status


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python create_order.py mongodb_uri orderId customerId book_order_list shipping_details paymentType")
        exit(-1)

    mongodb_uri = argv[1]
    orderId = argv[2] 	
    customerId = argv[3] 	
    book_order_list = argv[4] 	
    shipping_details = argv[5] 	
    paymentType = argv[6] 	
    
    db = pymongo.MongoClient(mongodb_uri).get_database()

    ret_status = create_new_order(db, orderId, customerId, book_order_list, shipping_details, paymentType)
    print("New order creation " ret_status)

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

