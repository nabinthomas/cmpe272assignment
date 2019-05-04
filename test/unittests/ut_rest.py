import unittest
import mongomock
import json
from flask import jsonify
from server.dbscripts.add_customer import *
from server.dbscripts.create_order import * 
from server.dbscripts.update_inventory import * 
from server.dbscripts.list_books import *
from server.dbscripts.process_order import *
from server import main

class RESTTests(unittest.TestCase):
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


        self.app = main.app.test_client()
        print ("SETUP END")
        
    def tearDown(self):
        print ("tearDown")
        pass

    def test_api(self):
        """
        Test REST API /api 
        """
        resp = self.app.get('/api')
        reply_from_server = json.loads(resp.data)
        print (reply_from_server)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.SUCCESS)
        self.assertEqual(reply_from_server, {
            "response": {
                "message": "\n    API Usage:\n \n        - GET    /api/books\n        - GET    /api/book/<isbn13>\n        - POST   /api/neworder data={\"key\": \"value\"}\n        - PUT    /api/update/<orderid> data={\"key\": \"value_to_replace\"}\n        - DELETE is not supported\n\n"
            },
            "status": main.ReturnCodes.SUCCESS
        })
    
    def test_api_book(self):
        """
        Test REST API /api/book/
        """
        resp = self.app.get('/api/book')
        reply_from_server = json.loads(resp.data)
        print (reply_from_server)
        self.assertEqual(reply_from_server['status'], main.ReturnCodes.ERROR_INVALID_PARAM)
        self.assertEqual(reply_from_server, {
            "response": {
                
            },
            "status": main.ReturnCodes.ERROR_INVALID_PARAM
        })
        
if __name__ == "__main__":
    unittest.main()