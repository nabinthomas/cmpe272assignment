import unittest
import os
#import mongomock
import pymongo
import json
from flask import jsonify
from server.dbscripts.add_customer import *
from server.dbscripts.create_order import * 
from server.dbscripts.update_inventory import * 
from server.dbscripts.list_books import *
from server.dbscripts.process_order import *
from server import main


class RESTTests(unittest.TestCase):
    # Each of the test case should have a fresh dtabase
    # Test cases may run in parallel so need to give unique name.
    test_case_number = 133; 
        
    def setUp(self):
        
        print ("SETUP BEGIN")
        #self.mongo_client = mongomock.MongoClient() 
        #self.db = self.mongo_client['testdb']
        RESTTests.test_case_number = RESTTests.test_case_number + 1; 
        self.testname =  str(RESTTests.test_case_number)
        print ("testcase  name = ", self.testname)
        mongodb_uri = "mongodb://localhost/" + self.testname  
        self.mongo_client  = pymongo.MongoClient(mongodb_uri)
        self.db = self.mongo_client.get_database()
   
        self.db.books.insert_one({'_id': '1', "Title" : "Integration of the Indian States", "Author" : [ "Menon, V P" ], "Genre" : "history", "Page" : 217, "Publisher" : "Orient Blackswan", "Price" : 21.7, "ISBN-13" : "978-1503215678", "Inventory" : 90 })
        self.db.books.insert_one({'_id': '2', "Title" : "God Created the Integers", "Author" : [ "Hawking, Stephen" ], "Genre" : "mathematics", "Page" : 197, "Publisher" : "Penguin", "Price" : 19.7, "ISBN-13" : "978-1503215674", "Inventory" : 40 }) 
        self.db.books.insert_one({'_id': '3', "Title" : "Superfreakonomics", "Author" : [ "Dubner, Stephen" ], "Genre" : "economics", "Page" : 179, "Publisher" : "HarperCollins", "Price" : 17.9, "ISBN-13" : "978-1503215675", "Inventory" : 60 })
        self.db.books.insert_one({'_id': '4', "Title" : "Fundamentals of Wavelets", "Author" : [ "Goswami, Jaideva", "Binu Jose" ], "Genre" : "signal_processing", "Page" : 228, "Publisher" : "Wiley", "Price" : 22.8, "ISBN-13" : "978-1503215672", "Inventory" : 10 })
        self.db.books.insert_one({'_id': '5', "Title" : "Nature of Statistical Learning Theory, The", "Author" : [ "Vapnik, Vladimir" ], "Genre" : "data_science", "Page" : 230, "Publisher" : "Springer", "Price" : 23, "ISBN-13" : "978-1503215677", "Inventory" : 80 })
        self.db.books.insert_one({'_id': '6', "Title" : "The Jungle Book", "Author" : [ "Kipling, Rudyard" ], "Genre" : "fiction", "Page" : 92, "Publisher" : "CreateSpace Independent Publishing Platform", "Price" : 6.89, "ISBN-13" : "978-1503332546", "Inventory" : 0 })
        self.db.books.insert_one({'_id': '7', "Title" : "The Jungle Book(Paperback)", "Author" : [ "Kipling, Rudyard" ], "Genre" : "fiction", "Page" : 94, "Publisher" : "CreateSpace Independent Publishing Platform", "Price" : 6.89, "ISBN-13" : "978-1505332546", "Inventory" : 1 })
        self.db.books.insert_one({'_id': '8', "Title" : "New Book", "Author" : [ "New, Author" ], "Genre" : "fiction", "Page" : 94, "Publisher" : "CreateSpace Independent Publishing Platform", "Price" : 6.89, "ISBN-13" : "123-1234567890", "Inventory" : 1 })

        self.db.orders.insert_one({"OrderID": "33", "CustomerId": 2, "Items": [{"BookId": "978-1503215677", "qty": 30, "SellingPrice": 24.0}], "Shipping": {"Address": "100 W Tasman Dr, San Jose, 95134", "Status": "InProgress", "Provider": "Fedex", "Type": "2 day shipping", "ShippingDate": "4/12/2019", "DeliveryDate": "4/14/2019 "}, "PaymentType": "Cash On Delivery"})
        self.db.orders.insert_one({"OrderID": "44", "CustomerId": 2, "Items": [{"BookId": "978-1503215677", "qty": 300, "SellingPrice": 24.0}], "Shipping": {"Address": "100 W Tasman Dr, San Jose, 95134", "Status": "InProgress", "Provider": "Fedex", "Type": "2 day shipping", "ShippingDate": "4/12/2019", "DeliveryDate": "4/14/2019 "}, "PaymentType": "Cash On Delivery"})
       
        # Create a dummy customer and session for that 
        self.db.customers.insert_one({ "customerId" : 1, "email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas", "accessToken" : "DUMMY_TEST_TOCKEN_NABIN" })
        self.db.customers.insert_one({ "customerId" : 2, "email" : "ginto100@gmail.com", "name" : "Ginto George", "accessToken" : "DUMMY_TEST_TOCKEN_GINTO" })
        self.app = main.app.test_client()
        main.db = self.db
        main.mongo_client = self.mongo_client
        print ("SETUP END")
        
    def tearDown(self):
        print ("tearDown Start : " , self.testname)
        self.db.books.drop() ;
        self.db.orders.drop() ;
        print ("Collections Dropped  tearDown END :",self.testname)

    def test_api(self):
        """
        Test REST API /api 
        """
        resp = self.app.get('/api')
        reply_from_server = json.loads(resp.data)
        print ("Reply from Server was :\n", reply_from_server)
        print ("api help message was :\n", main.api_help_message)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.SUCCESS)
        self.assertEqual(reply_from_server, {
            "response": main.api_help_message,
            "status": main.ReturnCodes.SUCCESS
        })
    
    def test_api_book(self):
        """
        Test REST API /api/book/
        """
        resp = self.app.get('/api/book', headers={'Authorization': 'Bearer DUMMY_TEST_TOCKEN_GINTO'})
        reply_from_server = json.loads(resp.data)
        print (reply_from_server)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.ERROR_INVALID_PARAM)
        self.assertEqual(reply_from_server, {
            "response": {
                
            },
            "status": main.ReturnCodes.ERROR_INVALID_PARAM
        })
    
    def test_api_book_details(self):
        """
        Test REST API /api/book/<isbn13>
        """
        resp = self.app.get('/api/book/123-1234567890', headers={'Authorization': 'Bearer DUMMY_TEST_TOCKEN_GINTO'})
        reply_from_server = json.loads(resp.data)
        print (reply_from_server)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.SUCCESS)
        self.assertEqual(reply_from_server, {
            "response": { 
                "book_details": {"Title" : "New Book", "Author" : [ "New, Author" ], "Genre" : "fiction", "Page" : 94, "Publisher" : "CreateSpace Independent Publishing Platform", "Price" : 6.89, "ISBN-13" : "123-1234567890", "Inventory" : 1 },
                'requested_book': '123-1234567890'
                },
            "status": main.ReturnCodes.SUCCESS
        })
        
    def test_api_books(self):
        """
        Test REST API /api/books>
        """
        resp = self.app.get('/api/books', headers={'Authorization': 'Bearer DUMMY_TEST_TOCKEN_GINTO'})

        reply_from_server = json.loads(resp.data)
        print("----------------------GET api/books response----------------------------")
        print (reply_from_server)
        print("----------------------GET api/books response----------------------------")

        expected_json_file = "/root/test/unittests/data/books_ut_cmp.json"

        vdata = {}
        with open(expected_json_file) as f:
            vdata = json.load(f)
        print("------------------Expected response--------------------------------")
        print(vdata)
        print("------------------Expected response--------------------------------")

        self.assertEqual(reply_from_server['status'], main.ReturnCodes.SUCCESS)
        self.assertEqual(reply_from_server, vdata)

    def test_api_fulfill_order(self):
        """
        Test REST API /api/fulfillorder/<orderid>
        """
        print("------------------test_api_fulfill_order enter--------------------------------")
       
        resp = self.app.put('/api/fulfillorder/33', headers={'Authorization': 'Bearer DUMMY_TEST_TOCKEN_GINTO'})
        reply_from_server = json.loads(resp.data)
        print (reply_from_server)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.SUCCESS)
        self.assertEqual(reply_from_server['response']['Status'], True)
        print("------------------test_api_fulfill_order exit--------------------------------")
       

    def test_api_fulfill_order_fail(self):
        """
        Test REST API /api/fulfillorder/<orderid>
        """
        print("------------------test_api_fulfill_order_fail enter--------------------------------")
       
        resp = self.app.put('/api/fulfillorder/987', headers={'Authorization': 'Bearer DUMMY_TEST_TOCKEN_GINTO'})
        reply_from_server = json.loads(resp.data)
        print (reply_from_server)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.ERROR_OBJECT_NOT_FOUND)
        self.assertEqual(reply_from_server['response']['Status'], False)
             
        print("------------------test_api_fulfill_order_fail exit--------------------------------")
        
    def test_api_create_order(self):
        """
        Test REST API /api/neworder
        """
        new_order = {"CustomerId" : 2, "Items" : [ {"BookId": "978-1503215678", "qty" : 1} ] }
        response = self.app.post('/api/neworder', data = json.dumps(new_order), content_type='application/json', headers={'Authorization': 'Bearer DUMMY_TEST_TOCKEN_GINTO'})
        print ("Response status ", response)
        resp_from_server = json.loads(response.data)
        print ("Response data ", resp_from_server)
        self.assertEqual(resp_from_server['status'],"Success")
        del resp_from_server['response']['order_request']['OrderID']  #orderid is dynamically created, cannot compare with static info
        self.assertEqual(resp_from_server, { 
            "response": { 
                "order_request": {
                    "CustomerId": 2,
                    "Items": [ 
                        { 
                            "BookId": "978-1503215678",
                            "qty": 1 
                        } 
                    ], 
                    "PaymentType": "Cash On Delivery", 
                    "Shipping": { 
                        "Status": "InProgress" 
                    } 
                } 
            }, 
            "status": "Success"
        })

if __name__ == "__main__":
    unittest.main()
