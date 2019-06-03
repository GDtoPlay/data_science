import json
import base64
from string import ascii_lowercase, ascii_uppercase

with open('sqldata.json') as sql_injection_json:

    json_data = json.load(sql_injection_json)


def safeword_split(string, save_list):
    letter_start = 0
    letter_end = 0
    cutting = 0
    for idx, letter in enumerate(string):
        
        if letter in safe_word_list and cutting == 0 and idx != len(string) - 1:
            letter_start = idx
            cutting = 1

        elif letter in safe_word_list and cutting == 0 and idx == len(string) - 1:
            letter_start = idx
            save_list.append(string[letter_start])

        elif letter not in safe_word_list and cutting == 1:
            letter_end = idx
            save_list.append(string[letter_start:letter_end])
            cutting = 0

        elif  idx == len(string) - 1 and cutting == 1:
            letter_end = idx
            save_list.append(string[letter_start:letter_end + 1])
            cutting = 0
            


safe_word_list = list(ascii_lowercase) + list(ascii_uppercase) +["_", "."] +["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


for sql_json in json_data:
    if "DATA" in sql_json:
        for DATA in sql_json["DATA"]:
            char_list  = []
            for base64_data in DATA:
                if base64_data != "":
                    decoded = str(base64.b64decode(base64_data), encoding='utf-8')
                    space_split = decoded.split(" ")

                    for string in space_split:
                        safeword_split(string, char_list)

            print(char_list)



            
