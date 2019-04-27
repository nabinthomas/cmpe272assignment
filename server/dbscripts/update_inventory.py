import sys
import pymongo
from bson.objectid import ObjectId
from pymongo import ReturnDocument

def get_available_book_count(db, in_book_id):
    '''
    Fetch number of book available in inventory
    param db: reference to the database
    param in_book_id: ISBN-13 value of Book 
    return updated record when successful, {} when failed. 
    '''
    book_count = db.books.find_one({"ISBN-13" : in_book_id})['Inventory']

    return book_count


def update_inventory(db, isbn, incoming_inv):
    '''
    Update Inventory
    param db - reference to the database
    param customerInfo - Inventory update value (-/+)
    return updated record when successful, {} when failed. 
    '''
    current_inv = get_available_book_count(db, isbn)
    new_inv = current_inv + incoming_inv

    if current_inv < 0 or new_inv < 0:
        return {}

    #TODO: replace id with Unique key combinations?
    #updated_record = db.books.find_one_and_update({"ISBN-13": isbn}, { '$set': {'Inventory': new_inv }}, return_document=ReturnDocument.AFTER)
    updated_record = db.books.find_one_and_update({'ISBN-13':isbn}, {"$set": {'Inventory': new_inv}}, return_document=ReturnDocument.AFTER)
    if updated_record is None:
        return {}
    print("\r\nUpdated record:" + str(updated_record))

    return updated_record

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 4:
        print("Usage: python update_inventory.py mongodb_uri book_id incoming_quantity")
        exit(-1)

    mongodb_uri = argv[1]
    book_id = argv[2]
    incoming_quantity = argv[3]
    
    db = pymongo.MongoClient(mongodb_uri).get_database()
    ret_val = update_inventory(db, book_id, incoming_quantity)
    print("update_inventory operation " + ret_val)

'''
	# Books Entry for ref:
	{  "Title" : "Fundamentals of Wavelets", 
	   "Author" : [ "Goswami, Jaideva", "Binu Jose" ], 
	   "Genre" : "signal_processing", 
	   "Page" : 228, 
	   "Publisher" : "Wiley", 
	   "Price" : 22.8, 
	   "ISBN-13" : "978-1503215672", 
	   "Inventory" : 10 }
'''

