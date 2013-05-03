import unittest 
import helpers
import io
import subprocess
import string
import pickle
import json
 
ALG_NAME = "seq"
BYTE_SIZE = 8

# COMPRESSION

def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)
    
    input = file_in.read()
    encoded = _encode(input)
    dictionary = ''
    content = ''
    to_dump = dict((k,v) for k, v in hashed.items() if (v != 0))

    for i in pickle.dumps(to_dump) :
        dictionary = dictionary + (helpers.to_bin(ord(i),BYTE_SIZE))

    file_out.write(dictionary)
    file_out.write(helpers.to_bin(ord("\x00"),BYTE_SIZE))

    for i in json.dumps(encoded) :
        content = content + (helpers.to_bin(ord(i),BYTE_SIZE))

    file_out.write(content)

    return helpers.end_compress(file_in,file_out)

# DECOMPRESSION

def decompress(file_name):
    
    (file_in,file_out) = helpers.start_decompress(file_name, ALG_NAME)
    
    i = file_in.read(BYTE_SIZE)
    i = file_in.read(BYTE_SIZE)
    dictionary = '('

    while i != '00000000' :
        dictionary = dictionary + chr(int(i,2))
        i = file_in.read(BYTE_SIZE)

    dictionary = pickle.loads(dictionary)

    i = file_in.read(BYTE_SIZE)
    content = ''

    while i != '' :
        content = content + chr(int(i,2))
        i = file_in.read(BYTE_SIZE)

    content = json.loads(content)
    content = _decode(content, dictionary)

    for i in content:
        file_out.write(helpers.to_bin(ord(i),BYTE_SIZE))

    return helpers.end_decompress(file_in,file_out)

# ENCODE

hashed = {}
used_rules = []

def single_list (input) :
    sl = []
    for i in input :
        sl.append(i)
    return sl

def two_list (input) :
    tl = []
    i = 0
    length = len(input) - 1 
    while i <= length :
        if i < length :
            tl.append((input[i], input[i+1]))
        else : tl.append((input[i], ''))
        i += 1
    return tl

def hash_it (tl) :
    new_dict = {}
    for i in tl :
        if i in new_dict :
            entry = new_dict.get(i)
            if entry == 0 :
                if used_rules == [] :
                    new_dict[i] = 1
                    used_rules.insert(0,1)
                else :
                    new_dict[i] = (used_rules[0] + 1)
                    used_rules.insert(0,(used_rules[0] + 1))
            else :
                new_dict[i] = new_dict[i]
        else :
            new_dict[i] = 0
    hashed.update(new_dict)
    return hashed

def replace (sl, hashed) :
    replaced = []
    i = 0
    while i < len(sl) - 1:
        digram = (sl[i], sl[i+1])
        if digram not in hashed :
            raise NameError ("dictionary not full")
        else :
            if hashed.get(digram) == 0 :
                replaced.append(digram[0])
                i += 1
                if len(sl) - i < 2 :
                    replaced.append(digram[1])
            else :
                replaced.append(hashed.get(digram))
                if i <= len(sl) - 2 :
                    i += 2
                else :
                    i += 1
    return replaced

def _encode (input) :
    sl = single_list(input)
    tl = two_list(input)
    dic = hash_it(tl)
    while len(tl) > len(set(tl)) :
        replaced = replace(sl, dic)
        sl = single_list(replaced)
        tl = two_list(replaced)
        dic = hash_it(tl)
    return replaced

# DECODE

def _decode (content, dictionary) :
    inv_dict = dict((v, k) for k, v in dictionary.items())
    while any(type(n) == int for n in content) :
        i = 0
        for i, v in enumerate(content) :
            if v in inv_dict :
                tup = inv_dict.get(v)
                content.pop(i)
                content.insert(i,tup[0])
                content.insert(i+1,tup[1])
    return content

#compress("../tests/ps7.txt")
#decompress("../tests/ps7.seq")

#compress("../tests/st.txt")
#decompress("../tests/st.seq")

compress("../tests/small3.bmp")
decompress("../tests/small3.bmp")
