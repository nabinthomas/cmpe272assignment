import sys
import csv
import json

if(len(sys.argv) == 3):
    with open(sys.argv[1], 'r') as csvfile:
        with open(sys.argv[2], 'w') as jsonfile:
            reader = csv.DictReader(csvfile)
            print(reader.keys)
            for row in reader:
                #print (json.dumps(row ))
                for x in row:
                    print(x.key, x.value);
                #jsonfile.write(json.dumps(row ))

else :
    print ('Usage: ' + sys.argv[0] + ' input.csv output.jason ' + str(len(sys.argv)));
