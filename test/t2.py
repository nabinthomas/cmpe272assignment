
## Python test code for experimentation. This will need to be deleted later during deployment.

import sys
import csv
import json
import pymongo

if(len(sys.argv) == 3):
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