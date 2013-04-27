'''
CS51 Final Project
Eamon, David, Kevin, Willy

huff.py by Kevin Eskici
keskici@college.harvard.edu
'''

import io
import helpers
import Queue

# installed bitstream for this: 
# "sudo python setup.py install" after downloading from
# http://code.google.com/p/python-bitstring/
#from bitstream import BitStream, BitArray

READ_IN_SIZE = 1
ALG_NAME = "huf"
BYTE_SIZE = 8

### COMPRESS ###

# compress(file_in_name) outputs a compressed .huf file to disk
def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)
    
    # get dictionary of codes for given bytes
    codes = _add_codes(_build_tree(_build_freq_list(file_in)),{},'')
    
    # read the first integer into file
    i = file_in.read(READ_IN_SIZE)
    
    # while the integer isn't end of file, encode and write to file
    while (i != ''):
        enc = ord(i) 
        file_out.write(codes[enc])
        i = file_in.read(READ_IN_SIZE)
    
    #now you're done!
    return helpers.end_compress(file_in,file_out)

####DECROMPRESS###

# decompress(file_name) takes in a file of type .huf 
# and outputs uncompressed file to disk

def decompress(file_name):
    (file_in,file_out) = helpers.start_decompress(file_name, ALG_NAME)
    
    # get dictionary of codes for given bytes
    codes = _add_codes(_build_tree(_build_freq_list(file_in)),{},'')
    
    
    
#citation: inspired by http://stackoverflow.com/questions/11587044
#/how-can-i-create-a-tree-for-huffman-encoding-and-decoding
#and http://stackoverflow.com/questions/6770925/
#huffman-encoding-how-to-write-binary-data-in-python

# build frequency list
def _build_freq_list (file_in):
    f = io.open(file_in, "r")
    freq_dict = {}
    byte = f.read(READ_IN_SIZE)
    while (byte != ''):
        if byte in freq_dict:
            freq_dict[byte] += 1
        else:
            freq_dict[byte] = 1 + (ord(byte)/1000.)
        byte = f.read(READ_IN_SIZE)
    freq_list = []        
    for key in freq_dict:
        freq_list.append((freq_dict[key],key))
    return freq_list
            

# builds huffman tree assuming frequency_list is a list of (f,val) tuples
def _build_tree(frequency_list):
    q = Queue.PriorityQueue()
    for val in frequency_list:
        q.put(val)
    while q.qsize() > 1:
        left, right = q.get(),q.get()
        new = (_new_freq(left[0],right[0]), (left,right))
        q.put(new)
    return q.get()   
    
# sum frequency and preserve decimal part with information about
# lowest ASCII character
def _new_freq(lfreq,rfreq) : 
    minimum = min ((lfreq - int(lfreq)), (rfreq - int(rfreq)))
    return (int(rfreq) + int(lfreq) + minimum)
    

# codes is a dictionary of bytes and corresponding encoded strings  
def _add_codes(huff_tree, dct, code) :
    (f, val) = huff_tree 
    print val
    if (type(val) != tuple) : 
         dct[val] = code
    else :
        (left, right) = val
        _add_codes(left, dct, (code + '0'))
        _add_codes(right, dct, (code + '1'))
    return dct

# l = huff._build_freq_list("../tests/ps7.py")
# tree = _huff_build_tree(l)
#             
    
    
  



