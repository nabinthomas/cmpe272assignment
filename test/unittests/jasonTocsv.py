import sys
import csv
import json


# The json file must be a proper jason file , not the one we use to import to mongo which has jason in each line. 
# To convert that to jason , put all of those lines under a list []

if(len(sys.argv) == 3):
    with open(sys.argv[1], 'r') as jsonfile:
        data = json.load(jsonfile)
    
    print (data[0].keys())

    

    with open(sys.argv[2], 'w') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for line in data:
            writer.writerow(line) 
else :
    print ('Usage: ' + sys.argv[0] + ' input.json output.csv ' );