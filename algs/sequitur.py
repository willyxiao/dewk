# my old imports
import sys
import random

# start of willy's stuff
import unittest 
import helpers
import io
import subprocess
import string

READ_IN_SIZE = 1 
ALG_NAME = "seq"
BYTE_SIZE = 8
TOO_MUCH = 100
    
###COMPRESS###

# compress takes in a string of the file name to compress 
# and outputs a compressed file to disk
def compress(file_in_name):

    # opens output file and signs it 
    (file_out_name, sign) = helpers.ensign(file_in_name, ALG_NAME)  
    file_out = io.open(file_out_name, "wb") 
    file_out.write(sign)
        
    file_in = io.FileIO(file_in_name, "r")
    i = file_in.read(READ_IN_SIZE)
    
    while (i != ''):
        enc = _encode(ord(i)) 
        file_out.write(enc)
        i = file_in.read(READ_IN_SIZE)
        
    file_in.close(); 
    file_out.close();
    
    subprocess.call(["./writer", file_out_name, file_out_name[:-1], "e"])

# list of used rules
used_list = []

# dictionary to send for decoding
hash = {}

def single_list (s) :
    l1 = []
    c = 0
    while c < len(s) :
        if s[c] == "/" and c < len(s) - 3:
            second = s.find("/", c+1)
            if second == (c+2) :
                l1.append(s[c+1])
                c += 2
            elif second == (c+3) :
                l1.append(s[c+1] + s[c+2])
                c += 3
            else :
                l1.append(s[c+1] + s[c+2] + s[c+3])
                c += 4
        elif s[c] == "/" and c > len(s) - 3:
            c += 1
        else :
            l1.append(s[c])
            c+=1
    return l1

def tuple_list (s) :
    l2 = []
    i = 0
    length = len(s) - 1 
    while i <= length :
        if i < length :
            l2.append(str(s[i]) + str(s[i+1]))
        else : l2.append(str(s[i]))
        i += 1
    return l2

def hash_it (tl) :
    for i in range (0, len(tl)) :
        if tl[i] in hash :
            fst = hash.get(tl[i])
            if fst == 0 : 
                if used_list == [] :
                    hash[tl[i]] = 1
                    used_list.insert(0,1)
                else :
                    hash[tl[i]] = (used_list[0] + 1)
                    used_list.insert(0,(used_list[0] + 1))
            else :
                hash[tl[i]] = hash[tl[i]]
        else :
            hash[tl[i]] = 0
    return hash

def replace_helper (digram, sl, sym) :
    for i, v in enumerate(sl) :
        if i < len(sl) - 1 :
            if (str(sl[i]) + str(sl[i+1])) == digram :
                sl.pop(i)
                sl.pop(i)
                sl.insert(i, sym)
    return sl

def count_helper (digram, sl) :
    counter = 0
    for i, v in enumerate(sl) :
        if i < len(sl) - 1 :
            if (str(sl[i]) + str(sl[i+1])) == digram :
                counter += 1
    return counter

def replace (tl, sl) :
    hashed = hash_it (tl)
    for i, v in enumerate(sl) :
        if i < len(sl) - 1 :
            old = str(sl[i]) + str(sl[i+1])
            new = hashed.get(old)
            if old in hashed and new != 0 and count_helper(old, sl) > 1:
                sl = replace_helper(old, sl, new)
    return sl

def string_it (sl) :
    new_string = ''
    for i,v in enumerate(sl) :
        new_string = new_string + str(v)
    return new_string

def _encode (input) :
    sl = single_list(input)
    tl = tuple_list(input)
    while len(set(tl)) != len(tl) :
        subst = replace(tl, sl)
        tl = tuple_list(subst)
        sl = subst
        print sl
    return sl

compress("../tests/ps7.txt")
