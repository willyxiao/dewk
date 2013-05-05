"""
CS51 Final Project
Eamon, David, Kevin, Willy

seq.py by David Herman
davidherman@college.harvard.edu

seq.py is a module that implements the Sequitur compression algorithm: 
http://www.cs.waikato.ac.nz/ml/publications/1997/NM-IHW-Compress97.pdf
http://sequitur.info/

1. seq.compress compresses a file outputting FileName.seq to disk. 
2. seq.decompress takes in a file outputting FileName.FileType to disk. 
"""

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

### COMPRESS ###

# compress(file_in_name) outputs a compressed .seq file to disk
def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)

    # read in whole file
    input = file_in.read()

    # replace repeated digrams with rules and create dictionary
    encoded = _encode(input)
    content = ''

    # remove non-repeated digrams from dictionary and invert keys and values
    to_dump = dict((k,v) for k, v in hashed.items() if (v != 0))
    to_dump = dict((v, k) for k, v in to_dump.items())

    # write rule (id = 0) or digram (id = 1) to .seq file
    def conversion (id, i) :

        # if rule or string of length 1, write id as bit and rest as byte
        if len(i) == 1 :
            written = (str(id) + (helpers.to_bin(ord(i),BYTE_SIZE)) +
                       (helpers.to_bin(ord("\x00"),BYTE_SIZE)))
            file_out.write(written)

        # otherwise, write id as bit and rest as bytes
        else :
            written = (str(id))
            for j in i :
                written += (helpers.to_bin(ord(j),BYTE_SIZE))
            written += (helpers.to_bin(ord("\x00"),BYTE_SIZE))
            file_out.write(written)
            
        # return length of whatever was written
        return len(written)

    # write dictionary to .seq file but maintain structure/track length
    def extract (input) :
        i = 0
        length = 0
        while i <= len(input) :
            new_l = 0
            
            # call conversion on key (rule)
            if i in input :
                new_l = conversion(0,str(i)) 

                # then call conversion on each half of value (digram)
                for j in input[i]:
                    if type(j) == int:
                        new_l += conversion(0,str(j))
                    else:
                        new_l += conversion(1,j)
            length += new_l
            i += 1

        # return dictionary length
        return length

    # write size of dictionary to .seq and remove padding at end
    dict_size = extract(to_dump)

    content_size = 0
    for i in encoded :

        # if its a rule, mark as an int, then write as a string to .seq file
        if type(i) == int :
            i = str(i)
            content_size += conversion(0, i)

        # otherwise, mark as string and write as string to .seq file
        else :
            content_size += conversion(1, i)

    # track total size and ensure it's a multiple of BYTE_SIZE
    total_size = dict_size + content_size
    padding = (BYTE_SIZE - (total_size % BYTE_SIZE)) % BYTE_SIZE
    file_out.write(helpers.to_bin(dict_size,(BYTE_SIZE * 5)+padding))

    # done with compression!
    return helpers.end_compress(file_in,file_out)

### DECOMPRESS ###

# decompress(file_name) takes in .seq and outputs uncompressed file to disk
def decompress(file_name):
    
    (file_in,file_out) = helpers.start_decompress(file_name, ALG_NAME)

    # convert single element (in dict or content) from binary form
    def de_bin (i) :

        # if its an int
        if i == '0' :
            key = ''

            # until hit a null byte, convert to string form
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    key = key + chr(int(i,2))

            # convert back to int
            key = int(key)

        # if its a string
        elif i == '1' :
            key = ''

            # until hit a null byte, convert to string form
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    key = key + chr(int(i,2))

        # return decoded element
        return key

    # find and remove any padding at end of file
    p = file_in.tell()
    #file_in.seek(-BYTE_SIZE,2)
    #insig = int(file_in.read(BYTE_SIZE),2)

    # find length of dictionary
    file_in.seek(-(BYTE_SIZE*5),2) #6
    s = file_in.read((BYTE_SIZE*5))#-insig)
    dict_size = int(s,2)
    file_in.seek(p,0)

    # read first id in dictionary
    i = file_in.read(1)
    print i

    # decoded dictionary
    dictionary = {}
    temp = []
    counter = 0

    # read until end of dictionary
    while file_in.tell() <= (dict_size + p) :

        # if element is marked as an int
        if i == '0' :
            acc = ''

            # read until end of element (marked by nul)
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                print i
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))

            # create whole element from individual strings
            if acc != '\x00' and acc != '' :
                temp.append(int(acc))
                counter += 1

            # read next id
            i = file_in.read(1)
            print i

        # if element is marked as a string
        elif i == '1' :
            acc = ''

            # read until end of element (marked by nul)
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                print i
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))

            # create whole element from individual strings
            if acc != '\x00' and acc != '' :
                temp.append(acc)
                counter += 1

            # read next id
            i = file_in.read(1)
            print i

        # otherwise raise an error if id isn't 1 or 0
        else :
            raise TypeError ("must start with 0 or 1")

        # if 3 elements read, you have a dictionary entry
        if counter == 3 :

            # the first is the key, the next two are the value (a tuple)
            enter = {temp[0]: (temp[1],temp[2])}
            temp = []
            counter = 0

            # add new entry to finished dictionary
            dictionary.update(enter)

    # list of decoded content
    content = []

    # read until end of content
    while file_in.tell() < helpers.size(file_in.name) - (BYTE_SIZE*5) :

        # if element is marked as an int
        if i == '0' :
            acc = ''
            
            # read until end of element (marked by nul)
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))

            # create whole element from individual strings
            if acc != '\x00' and acc != '' :
                content.append(int(acc))

            # read next id
            i = file_in.read(1)

        # if element is marked as a string
        elif i == '1' :
            acc = ''

            # read until end of element (marked by nul)
            while i != "00000000" and i != '' :
                i = file_in.read(BYTE_SIZE)
                if i != "00000000" and i != '' :
                    acc = acc + chr(int(i,2))

            # create whole element from individual strings
            if acc != '\x00' and acc != '' :
                content.append(acc)

            # read next id
            i = file_in.read(1)

        # otherwise raise an error if id isn't 1 or 0            
        else :
            raise TypeError ("must start with 0 or 1")
            
    # replace rules with original digrams to decompress 
    content = _decode(content, dictionary)

    # write out the finished, decoded file
    for i in content:
        if len(i) == 1 :
            file_out.write(helpers.to_bin(ord(i),BYTE_SIZE))
        else :
            for j in i :
                file_out.write(helpers.to_bin(ord(j),BYTE_SIZE))

    # now you're done!
    return helpers.end_decompress(file_in,file_out)

# ENCODE

# dictionary of rules
hashed = {}

# list of used rules
used_rules = []


# create a list of single char strings from input
def single_list (input) :
    sl = []
    for i in input :
        sl.append(i)
    return sl

# create a list of all possible digrams (2 char pairs) in input
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

# enter all digrams into dictionary (non-repeated ones will be removed)
def hash_it (tl) :
    new_dict = {}
    for i in tl :
        # if its in the dictionary already...
        if i in new_dict :
            entry = new_dict.get(i)

            # if its 0 (no repetition), update to reflect repetition
            if entry == 0 :

                # if no used rules, make it one and update used_rules
                if used_rules == [] :
                    new_dict[i] = 1
                    used_rules.insert(0,1)

                # otherwise make it 1 + last used rule
                else :
                    new_dict[i] = (used_rules[0] + 1)
                    used_rules.insert(0,(used_rules[0] + 1))

            # if its already been repeated, don't change it
            else :
                new_dict[i] = new_dict[i]

        # otherwise, add to dictionary with 0 (no repetition yet)
        else :
            new_dict[i] = 0

    # add to master dictionary
    hashed.update(new_dict)
    return hashed

# replace digrams with corresponding rules
def replace (sl, hashed) :

    # list of single elements (post-replacement) to write in compressed file
    replaced = []
    i = 0

    # go through whole file
    while i < len(sl) - 1:
        digram = (sl[i], sl[i+1])

        # if digram isn't in dictionary, something is wrong with dictionary
        if digram not in hashed :
            raise NameError ("dictionary not full")
        else :

            # if no repetition, just add digram
            if hashed.get(digram) == 0 :
                replaced.append(digram[0])
                i += 1
                if len(sl) - i < 2 :
                    replaced.append(digram[1])

            # otherwise add the rule corresponding to the digram
            else :
                replaced.append(hashed.get(digram))
                if i <= len(sl) - 2 :
                    i += 2
                else :
                    i += 1
    return replaced

# call replace on file until no more repetitions
def _encode (input) :
    sl = single_list(input)
    tl = two_list(input)
    dic = hash_it(tl)

    replaced = []
    # when len of the file = len of the set version, there're no repetitions
    while len(tl) > len(set(tl)) :
        replaced = replace(sl, dic)
        sl = single_list(replaced)
        tl = two_list(replaced)
        dic = hash_it(tl)
    return replaced

###DECODE###

# NOTE: We didn't have time to write a version of this that didn't require
# the whole file as an input (although we believe it is possible).  This is
# the primary bottleneck in terms of efficiency (we got the rest of the
# program to run pretty quickly on pretty big files.

# replace rules with corresponding digrams to recreate original file
def _decode (content, inv_dict) :

    # while there are still ints in the file... 
    while any(type(n) == int for n in content) :
        i = 0
        for i, v in enumerate(content) :
            if v in inv_dict :
                # get the digram (as a tuple)
                tup = inv_dict.get(v)

                # remove the rule
                content.pop(i)

                # add elements in the tuple as the original digram
                content.insert(i,tup[0])
                content.insert(i+1,tup[1])

                print tup

    # woot you're done!
    return content

###ESTIMATE###
import math

def estimate(file_name):
    # assuming compresion ratio gets better by log(size of file / sample size)
    return helpers.estimate_cr(file_name, compress, math.log, sample_size)

# NOTE: Originally testing was done in each file but then was
# abstracted out into another file for the final version.
