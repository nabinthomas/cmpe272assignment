import unittest
import mongomock
import json
#import list_books
import add_customer
#import create_order
#import update_inventory

class DBTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient()['testdb']
 #       self.db.books.insert_one({'_id': '1', 'title': 'A test book'})
 #       self.db.books.insert_one({'_id': '2', 'title': 'Another test book'})
 #       self.db.books.insert_one({'_id': '3', 'title': 'A rare book'})
 #       self.db.inventory.insert_one({'_id': '1', 'id': '1', 'qty': 5})
 #       self.db.inventory.insert_one({'_id': '2', 'id': '2', 'qty': 0})
        self.customer_info = {"name" : "Mock User", "email": "mock_email@email.com"}
        
    def tearDown(self):
        pass
    '''
    def test_list_books(self):
        books = list_books.get_available_books(self.db)
        self.assertEqual(len(books), 1)
        print(books)
    '''

    def test_add_customer(self):
        customerInfo = add_customer.add_new_customer(self.db, self.customer_info)
#        self.assertEqual(len(customer_info), 1)
        self.assertEqual(customerInfo['email'], self.customer_info['email'])
        self.assertEqual(customerInfo['name'], self.customer_info['name'])
        print('\r\nCustomer info from db \r\n' + str(customerInfo))
        self.db.customers.drop()

    def test_add_customer1(self):
        customerInfo1 = add_customer.add_new_customer(self.db, self.customer_info)
        customerInfo2 = add_customer.add_new_customer(self.db, self.customer_info)
#        self.assertEqual(len(customer_info), 1)
        self.assertEqual(customerInfo2, {})
        print('\r\nCustomer1 info from db \r\n' + str(customerInfo1))
        print('Customer2 info from db \r\n' + str(customerInfo2))
        self.db.customers.drop()

    '''
    def test_create_order(self, cust_json_file):
	# Adding a new order with unique id gen: as [ "_id" : "13" ]
    	new_order_dict = { "_id": "13",  "OrderID" : 13 , "CustomerId" : 1, 
     			   "Items" : [ {"BookId": "978-1503215678", "qty" : 1, "SellingPrice": 22}, {"BookId": "9978-1503215677", "qty" : 3, "SellingPrice": 23} ],  
         		   "Shipping" : { "Address": "4321 Avery Ranch, San Mateo, CA 95123", "Status" : "InProgress", "Provider" : "UPS", "Type" : "Overnight shipping", "ShippingDate":"", "DeliveryDate":"" }, 
        		   "PaymentType": "Cash On Delivery" }

        books = create_order.create_new_order(self.db, 'orders', new_order_dict)
        # Usage: python create_order.py mongodb_uri collection_name new_order_dict")
        self.assertEqual(len(books), 1)
        print(books)

    def test_update_inventory(self, cust_json_file):
        {  "Title" : "Fundamentals of Wavelets", 
           "Author" : [ "Goswami, Jaideva", "Binu Jose" ], 
           "Genre" : "signal_processing", 
           "Page" : 228, 
           "Publisher" : "Wiley", 
           "Price" : 22.8, 
           "ISBN-13" : "978-1503215672", 
           "Inventory" : 10 }
	    book_id = 1 # Update schema to 
        books = update_inventory.update_inventory(self.db, )
		# def update_inventory(db, id, incoming_inv):
        self.assertEqual(len(books), 1)
        print(books)
    '''

if __name__ == "__main__":

    unittest.main()