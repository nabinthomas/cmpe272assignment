import sys
import pymongo

def get_available_book_count(db, in_book_id):
    book_count = -1
    for record in db.books.find({}):
        book_id = record['ISBN-13']
        if book_id != in_book_id:
            continue

        book_count = record['Inventory']

    return book_count


def update_inventory(db, isbn, incoming_inv):
    update_status = "failed"

    current_inv = get_available_book_count(db, isbn)
    new_inv = current_inv + incoming_inv

    if current_inv < 0 or new_inv < 0:
        return update_status

    #TODO: replace id with Unique key combinations?
    record = db.inventory.find_one_and_update({"ISBN-13": isbn}, { '$set': {'Inventory': incoming_inv }})

    update_status = "success" # TODO: detect update success/failure
    return update_status

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

