
## Python test code for experimentation. This will need to be deleted later during deployment.

import sys
import csv
import json
import pymongo

client = pymongo.MongoClient()
db = client['test']

if(len(sys.argv) == 4):
    collectionname = sys.argv[3]
    db[collectionname].drop()
    with open(sys.argv[2], 'r') as schemafile:
        schema = json.load(schemafile)
        print (schema)
    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print (json.dumps(row ))
            entry = {}
            for key, value in row.items():
                #print(key, value);
                #print (schema[key])
                # if string type
                if (schema[key] == "string"):
                    entry[key] = str(value);
                elif (schema[key] == "number"):
                    entry[key] = int(value);
                elif (schema[key] == "float"):
                    entry[key] = float(value);
                elif (schema[key] == "jsonarray"):
                    entry[key] = eval(value);
                else:
                    print("Parse error ", key, value);
                # if array type. 
            print(entry)
            db[collectionname].insert_one(entry)