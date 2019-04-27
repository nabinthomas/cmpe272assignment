import sys
import csv
import json

if(len(sys.argv) == 4):
    with open(sys.argv[2], 'r') as schemafile:
        schema = json.load(schemafile)
        print (schema)

    with open(sys.argv[3], 'w') as jsonfile:
        with open(sys.argv[1], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entry = {}
                for key, value in row.items():
                    #print(key, value);
                    #print (schema[key])
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
                jsonfile.write(json.dumps(entry )) 
                jsonfile.write("\n") 
                print  ("Entry " + str(entry) )  



else :
    print ('Usage: ' + sys.argv[0] + ' input.csv jasonschemafile output.jason ');
   
