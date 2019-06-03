#-*- coding:utf-8 -*-

import json
import os
from collections import OrderedDict


file = open("../박진석/sql_inject_msg.txt", "r")

contents = file.readlines()
case = []
for line in contents:
    case.append(line.rstrip())
    
file.close()


dname = "json"
fnames = os.listdir(dname)

sqljson = open("sqldata.json", "w", encoding="utf-8")
sqljson.write("[\n")
flag = 0
for fname in fnames:
    jsonfile = open("json/" + fname, 'r', encoding="utf-8")
    json_data = json.load(jsonfile)

    file_data = OrderedDict()
    
    print("processing: " + fname)
    check =0
    for data in json_data:
        msg = data['MSG']
        if msg in case:
            if flag == 1 and check ==0:
                sqljson.write(",\n")
            if check !=0:
                sqljson.write(",\n")
            file_data["FILE"] = fname
            file_data["MSG"] = data["MSG"]
            file_data["RES"] = data["RES"]
            tmp = []
            for payload in data["PAYLOAD"]:
                tempdata = []
                for innerdata in payload["DATA"]:
                    tempdata.append(innerdata)
                tmp.append(tempdata)
            file_data["DATA"] = tmp
            json.dump(file_data, sqljson, indent=4)
            check +=1
            flag =1
    jsonfile.close()
sqljson.write("\n]")
sqljson.close()
