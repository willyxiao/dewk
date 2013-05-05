import unittest 
import helpers
import io
import subprocess
import string
import pickle
import json
import os
 
ALG_NAME = "seq"
BYTE_SIZE = 8

# COMPRESSION

master = {}

def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)
    
    input = file_in.read()
    encoded = _encode(input)
    content = ''
    to_dump = dict((k,v) for k, v in hashed.items() if (v != 0))
    to_dump = dict((v, k) for k, v in to_dump.items())

    def conversion (id, i) :
        if len(i) == 1 :
            written = (str(id) + (helpers.to_bin(ord(i),BYTE_SIZE)) +
                       (helpers.to_bin(ord("\x00"),BYTE_SIZE)))
            file_out.write(written)
        else :
            written = (str(id))
            for j in i :
                written += (helpers.to_bin(ord(j),BYTE_SIZE))
            written += (helpers.to_bin(ord("\x00"),BYTE_SIZE))
            file_out.write(written)
        return len(written)

    def extract (input) :
        i = 0
        length = 0
        while i <= len(input) :
            new_l = 0
            if i in input :
                new_l = conversion(0,str(i)) 
                for j in input[i]:
                    if type(j) == int:
                        new_l += conversion(0,str(j))
                    else:
                        new_l += conversion(1,j)
            length += new_l
            i += 1
        return length

    print "compressing dictionary..."

    dict_size = extract(to_dump)

    print "compressing text..."
    content_size = 0
    for i in encoded :
        if type(i) == int :
            i = str(i)
            content_size += conversion(0, i)
        else :
            content_size += conversion(1, i)

    #for i in json.dumps(encoded) :
    #    content = content + (helpers.to_bin(ord(i),BYTE_SIZE))

    total_size = dict_size + content_size
    padding = (BYTE_SIZE - (total_size % BYTE_SIZE)) % BYTE_SIZE
    file_out.write(helpers.to_bin(dict_size,(BYTE_SIZE * 5)+padding))

    return helpers.end_compress(file_in,file_out)

# DECOMPRESSION

def decompress(file_name):
    
    (file_in,file_out) = helpers.start_decompress(file_name, ALG_NAME)

    def de_bin (i) :
        if i == '0' :
            key = ''
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    key = key + chr(int(i,2))
            key = int(key)
        elif i == '1' :
            key = ''
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    key = key + chr(int(i,2))
        return key

    print "decompressing dictionary"
    p = file_in.tell()
    file_in.seek(-BYTE_SIZE,2)
    insig = int(file_in.read(BYTE_SIZE),2)
    file_in.seek(-(BYTE_SIZE*6),2)
    s = file_in.read((BYTE_SIZE*5)-insig)
    dict_size = int(s,2)
    file_in.seek(p,0)
    i = file_in.read(1)
    dictionary = {}
    temp = []
    counter = 0
    while file_in.tell() <= (dict_size + p) :
        if i == '0' :
            acc = ''
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))
            if acc != '\x00' and acc != '' :
                temp.append(int(acc))
                counter += 1
            i = file_in.read(1)
        elif i == '1' :
            acc = ''
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))
            if acc != '\x00' and acc != '' :
                temp.append(acc)
                counter += 1
            i = file_in.read(1)
        else :
            raise TypeError ("must start with 0 or 1")
        if counter == 3 :
            enter = {temp[0]: (temp[1],temp[2])}
            temp = []
            counter = 0
            dictionary.update(enter)
    content = []

    print "decompressing text..."
    while file_in.tell() < helpers.size(file_in.name) - (BYTE_SIZE*5) :
        if i == '0' :
            acc = ''
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))
            if acc != '\x00' and acc != '' :
                content.append(int(acc))
            i = file_in.read(1)
        elif i == '1' :
            acc = ''
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))
            if acc != '\x00' and acc != '' :
                content.append(acc)
            i = file_in.read(1)
        else :
            raise TypeError ("must start with 0 or 1")
            
    #content = json.loads(content)    
    content = _decode(content, dictionary)

    for i in content:
        if len(i) == 1 :
            file_out.write(helpers.to_bin(ord(i),BYTE_SIZE))
        else :
            for j in i :
                file_out.write(helpers.to_bin(ord(j),BYTE_SIZE))
                
    return helpers.end_decompress(file_in,file_out)

# ESTIMATE

def estimate (file_name) :

    file_in = open(file_name, "r")
    sample_size = 2000
    file_size = os.path.getsize(file_name)
    if file_size > 500000 :
        return file_size + 1
    if file_size <= sample_size :
        input = file_in.read()
        sample_size = file_size
    else :
        input = file_in.read(sample_size)
    encoded = _encode(input)
    dictionary = ''
    content = ''
    to_dump = dict((k,v) for k, v in hashed.items() if (v != 0))

    for i in pickle.dumps(to_dump) :
        dictionary = dictionary + (helpers.to_bin(ord(i),BYTE_SIZE))

    dictionary = dictionary + (helpers.to_bin(ord("\x00"),BYTE_SIZE))

    for i in encoded :
        if type(i) == int :
            i = str(i)
            content = conversion(0, i, content)
        else :
            content = conversion(1, i, content)

    dict_len = len(dictionary) / float(BYTE_SIZE)
    con_len = len(content) / float(BYTE_SIZE)

    comp_size = (dict_len + con_len)

    return comp_size / float(sample_size)

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

def _decode (content, inv_dict) :
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
