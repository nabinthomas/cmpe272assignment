
## Python test code for experimentation. This will need to be deleted later during deployment.

import sys
import csv
import json
import pymongo

if(len(sys.argv) == 2):
    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader.keys)
        for row in reader:
            #print (json.dumps(row ))
            for x in row:
                print(x.key, x.value);