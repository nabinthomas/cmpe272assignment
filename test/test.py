
## Python test code for experimentation. This will need to be deleted later during deployment.

import json

array = [
        {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": "false"
        },
        {
            "userId": 2,
            "id": 2,
            "title": "Title 2",
            "completed": "false"
        },
    ]

for x in array:
    header = ""
    for key in x.keys():
        header = header + key + " | " 
    header = header + "\n"
    print (header);
    line = ""
    for key in x.keys():
        line = line + str(x[key]) + " | "
    line = line + "\n"
    print(line);