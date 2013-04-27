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

global buffer
buffer = 0x00

global buffer_pos
buffer_pos = 0

### COMPRESS ###

def compress(file_in_name):
    global buffer
    global buffer_pos

    #open output file and sign
    (file_out_name, sign) = helpers.ensign(file_in_name, ALG_NAME)
    file_out = io.open(file_out_name, "wb")
    file_out.write(sign)

    file_in = io.open(file_in_name, "r")
    i = file_in.read(READ_IN_SIZE)



#insert actual compression part


    file_in.close();
    file_out.close()



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
    
    
  



