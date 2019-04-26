import sys
import pymongo


def add_new_customer(db, cust_json_file):
    available_books = []
    for record in db.inventory.find({}):
        book_id = record['id']
        qty = record['qty']
        if qty <= 0:
            continue
        book = db.books.find_one({'_id': book_id})
        book['qty'] = qty
        available_books.append(book)
    return available_books

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 3:
        print("Usage: python add_customer.py mongodb_uri customer.json")
        exit(-1)

    mongodb_uri = argv[1]
    cust_json_file = argv[2]
    
    db = pymongo.MongoClient(mongodb_uri).get_database()
    add_new_customer(db, cust_json_file)

{ "customerId" : 1, "email" : "nabin.thomas@gmail.com", "name" : "Nabin Thomas" }

