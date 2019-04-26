import sys
import pymongo


def list_books(db):
    available_books = []
    for record in db.inventory.find({}):
        book_id = record['id']
        book_count = record['Inventory']
        if book_count <= 0:
            continue
        book = db.books.find_one({'_id': book_id})
        book['Inventory'] = book_count
        book['Author'] = record['Author'] #TODO: Authors??
        book['Genre'] = record['Genre']
        book['Publishe'] = record['Publishe']
        book['Price'] = record['Price']
        book['ISBN-13'] = record['ISBN-13']
        available_books.append(book)
    return available_books

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python list_books.py mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]
    
    db = pymongo.MongoClient(mongodb_uri).get_database()
    for book in list_books(db):
        print(book['Title'], book['Author'], book['Inventory'], book['Genre'], book['Publisher'], book['Price'], book['ISBN-13']))

