import unittest
import mongomock
import json
import add_customer
import create_order
import update_inventory
import list_books

class DBTests(unittest.TestCase):
    def setUp(self):
        print ("SETUP BEGIN")
        self.db = mongomock.MongoClient()['testdb']
        self.db.books.insert_one({'_id': '1', "Title" : "Integration of the Indian States", "Author" : [ "Menon, V P" ], "Genre" : "history", "Page" : 217, "Publisher" : "Orient Blackswan", "Price" : 21.7, "ISBN-13" : "978-1503215678", "Inventory" : 90 })
        self.db.books.insert_one({'_id': '2', "Title" : "God Created the Integers", "Author" : [ "Hawking, Stephen" ], "Genre" : "mathematics", "Page" : 197, "Publisher" : "Penguin", "Price" : 19.7, "ISBN-13" : "978-1503215674", "Inventory" : 40 }) 
        self.db.books.insert_one({'_id': '3', "Title" : "Superfreakonomics", "Author" : [ "Dubner, Stephen" ], "Genre" : "economics", "Page" : 179, "Publisher" : "HarperCollins", "Price" : 17.9, "ISBN-13" : "978-1503215675", "Inventory" : 60 })
        self.db.books.insert_one({'_id': '4', "Title" : "Fundamentals of Wavelets", "Author" : [ "Goswami, Jaideva", "Binu Jose" ], "Genre" : "signal_processing", "Page" : 228, "Publisher" : "Wiley", "Price" : 22.8, "ISBN-13" : "978-1503215672", "Inventory" : 10 })
        self.db.books.insert_one({'_id': '5', "Title" : "Nature of Statistical Learning Theory, The", "Author" : [ "Vapnik, Vladimir" ], "Genre" : "data_science", "Page" : 230, "Publisher" : "Springer", "Price" : 23, "ISBN-13" : "978-1503215677", "Inventory" : 80 })
        self.db.books.insert_one({'_id': '6', "Title" : "The Jungle Book", "Author" : [ "Kipling, Rudyard" ], "Genre" : "fiction", "Page" : 92, "Publisher" : "CreateSpace Independent Publishing Platform", "Price" : 6.89, "ISBN-13" : "978-1503332546", "Inventory" : 0 })
        self.db.books.insert_one({'_id': '7', "Title" : "The Jungle Book(Paperback)", "Author" : [ "Kipling, Rudyard" ], "Genre" : "fiction", "Page" : 94, "Publisher" : "CreateSpace Independent Publishing Platform", "Price" : 6.89, "ISBN-13" : "978-1505332546", "Inventory" : 1 })
        self.customer_info = {"name" : "Mock User", "email": "mock_email@email.com"}
        print ("SETUP END")
        
    def tearDown(self):
        print ("tearDown BEGIN")
        pass
        print ("tearDown END")
    
    def test_list_books(self):
        books = list_books.get_available_books(self.db)
        self.assertEqual(books.count(), 6) # Ensure 6th book with 0 copies is not returned
        print(books)

    def test_list_books_after_order_all(self):
        '''
        Order all the copies of an available book to make it empty. And then try search to ensure that this book
        is removed from the returned test.
        This also tests for update inventory
        '''
        books = list_books.get_available_books(self.db)
        self.assertEqual(books.count(), 6) # Ensure 6th book with 0 copies is not returned
        # Place order        
        paymentType = "Cash On Delivery"
        orderId = 21
        customerId = 12
        shipping_details = {"Address": "4321 Avery Ranch, San Mateo, CA 95123","Status" : "InProgress","Provider" : "UPS","Type" : "Overnight shipping","ShippingDate":"","DeliveryDate":""}
        book_order_list = [{"BookId": "978-1505332546", "qty" : 1, "SellingPrice": 6.88}]
        ins_record = create_order.create_new_order(self.db, orderId, customerId, book_order_list, shipping_details, paymentType) 

        books = list_books.get_available_books(self.db)
        self.assertEqual(books.count(), 5) # Ensure 6th, 7th books now with 0 copies are not returned
        print(books)

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

    def test_create_order(self):
        print ("LOOK HERE")
        paymentType = "Cash On Delivery"
        orderId = 21
        customerId = 12
        shipping_details = {"Address": "4321 Avery Ranch, San Mateo, CA 95123","Status" : "InProgress","Provider" : "UPS","Type" : "Overnight shipping","ShippingDate":"","DeliveryDate":""}
        book_order_list = [{"BookId": "978-1503215678", "qty" : 1, "SellingPrice": 22},{"BookId": "978-1503215675", "qty" : 3, "SellingPrice": 23}]
        ins_record = create_order.create_new_order(self.db, orderId, customerId, book_order_list, shipping_details, paymentType)
        print(ins_record)
        # Usage: python create_order.py mongodb_uri collection_name new_order_dict")
        self.assertEqual(ins_record['OrderID'], orderId)
        self.assertEqual(ins_record['CustomerId'], customerId)
        self.db.orders.drop()

    def test_create_order1(self):
        paymentType = "Cash On Delivery"
        orderId = 21
        customerId = 12
        shipping_details = {"Address": "4321 Avery Ranch, San Mateo, CA 95123","Status" : "InProgress","Provider" : "UPS","Type" : "Overnight shipping","ShippingDate":"","DeliveryDate":""}
        book_order_list = [{"BookId": "978-1503215678", "qty" : 111, "SellingPrice": 22},{"BookId": "978-1503215675", "qty" : 3, "SellingPrice": 23}]
        ins_record = create_order.create_new_order(self.db, orderId, customerId, book_order_list, shipping_details, paymentType)

        # Usage: python create_order.py mongodb_uri collection_name new_order_dict")
        self.assertEqual(ins_record, {})
    
    def test_update_inventory(self):
        # Place order        
        paymentType = "Cash On Delivery"
        orderId = 22
        customerId = 12
        shipping_details = {"Address": "4321 Avery Ranch, San Mateo, CA 95123","Status" : "InProgress","Provider" : "UPS","Type" : "Overnight shipping","ShippingDate":"","DeliveryDate":""}
        book_order_list = [{"BookId": "978-1503215678", "qty" : 3, "SellingPrice": 22}]
        original_book_count = self.db.books.find_one({"ISBN-13" : "978-1503215678"})["Inventory"]
        ins_record = create_order.create_new_order(self.db, orderId, customerId, book_order_list, shipping_details, paymentType) 

        new_book_count = self.db.books.find_one({"ISBN-13" : "978-1503215678"})["Inventory"]
        self.assertEqual(original_book_count - new_book_count, 3) #3 books ordered

if __name__ == "__main__":
    unittest.main()