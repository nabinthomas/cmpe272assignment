import sys
import csv
import json
import pymongo 

if(len(sys.argv) == 2):
    db = pymongo.MongoClient()['test']
    cname = sys.argv[1].replace(".csv","")
    col = db[cname] 
    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            data = {}
            for x in row:
                if(row[x].find(",") != -1) :
                    data[x] = row[x].split(',')
                else:      
                    data[x] = row[x]
            col.insert_one(data) 
        #q = json.dumps(data)
            
        #q = q.replace("\"","\'");
        #print (q)   
                #db.books.insert_one(data)
        #db.books.insert_one({'Title': '3', 'title': 'A rare book'})

else :
    print ('Usage: ' + sys.argv[0] + ' input.csv ' );
