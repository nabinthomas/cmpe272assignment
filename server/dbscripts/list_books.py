import sys
import pymongo

    
'''
    Function to fetch books
        db: Database
        page_index: Record Page number to return
            0 : ALL books
        books_per_index: Number of books per index

    Invoke as get_all_books(db, 0, 0) for all books
'''
def get_all_books(db, page_index, books_per_index ):
    if page_index is 0:
        return db.books.find()
    else:
        total_book_count = db.books.count()
        if total_book_count is 0:
            print("No books available in inventory")
            return None
        total_indices = total_book_count / books_per_index
        if (total_book_count % books_per_index) is not 0:
            total_indices = total_indices  + 1
        if page_index > total_indices:
            print("Fewer indices available")
            return {}
        start = (page_index -1) * books_per_index
        end = page_index * books_per_index
        db_booklist = db.books.find()
        booklist = []
        for i in range(start,end):
            booklist.append(db_booklist[i])
        return booklist

def get_available_books(db):
    return db.books.find({ "Inventory" : { "$gt": 0 }  })

def get_bookdata(db, isbn13):
    return db.books.find_one({ "ISBN-13" : { "$eq": isbn13 } })

def get_bookcount(db, isbn13):
    book =  db.books.find_one({ "ISBN-13" : { "$eq": isbn13 } })
    return book['Inventory']

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
