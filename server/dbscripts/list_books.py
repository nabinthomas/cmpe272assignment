import sys
import pymongo


def get_available_books(db):
    return db.books.find({ "Inventory" : { "$gt": 0 }  })

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python list_books.py mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]
    
    db = pymongo.MongoClient(mongodb_uri).get_database()
    available_books = get_available_books(db)
    print("List of Available Books")
    print("************************")
    for book in available_books:
        print("Title: ", book['Title'])
        print("Author(s) :", end='')
        for author in book["Author"]:
            print(author, "\n          :", end='')
        print("\r", end='')
        print("Available Copies :", book['Inventory'])
        print("Genre", book['Genre'])
        print("Publisher", book['Publisher'])
        print("Current Price", book['Price'])
        print("ISBN-13 : ", book['ISBN-13'])
        print("*************************")
        print()
        

'''
{ "Title" : "How to Think Like Sherlock Holmes", "Author" : [ "Konnikova, Maria" ], 
"Genre" : "psychology", "Page" : 240, "Publisher" : "Penguin", "Price" : 24, 
"ISBN-13" : "978-1503215681", "Inventory" : 30 }
'''