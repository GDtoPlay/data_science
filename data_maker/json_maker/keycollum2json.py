#-*- coding:utf-8 -*-

import os
import csv
import json
import codecs
from collections import OrderedDict

dname = "../utf8"
fnames = os.listdir(dname)
for fname in fnames:
    jname = "../json_raw/" + fname[:-4] + ".json"
    cname = dname + "/" + fname
    
    jsonfile = open(jname, 'w', encoding="utf-8")
    file_data = OrderedDict()

    print("processing : " + jname)
    with open(cname, 'r', encoding="utf-8-sig", newline='') as csvFile:
        jsonfile.write("[\n")
        
        reader = csv.DictReader(csvFile)
        first_in = 0
        for row in reader:
            if first_in == 0:
                first_in = 1
            else:
                jsonfile.write(',\n')
            file_data["TIME"] = row["장비발생시간"]
            file_data["SIP"] = row['출발지IP']
            file_data["SPORT"] = row['출발지포트']
            file_data["DIP"] = row['목적지IP']
            file_data["DPORT"] = row['목적지포트']
            file_data["MSG"] = row['공격명']

            payload = row['페이로드']

            while '\r' in payload:
                payload = payload.replace('\r', '')

            while '\n' in payload:
                payload = payload.replace('\n', '')
                
            file_data["PAYLOAD"] = payload
            
            try:
                file_data["RES"] = row['결과']
            except:
                file_data["RES"] = row['정오탐']
            file_data["PROTO"] = row['프로토콜']
            json.dump(file_data, jsonfile, indent = 4)
        jsonfile.write('\n]')
        jsonfile.close()

print("done")
