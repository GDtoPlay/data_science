def msg_check(msg,key_list,nkey_list):
    ret= True
    msg = msg.lower()
    msg_key = msg.split(" ")

    for key in key_list:
        ret = ret and key.lower() in msg_key

    for nkey in nkey_list:
        ret = ret and nkey.lower() not in msg_key

    return ret


def msg_simple_check(msg,word):
    msg_word = msg[:len(word)].lower()
    
    if msg_word == word.lower():
        return True

    else:
        return False
