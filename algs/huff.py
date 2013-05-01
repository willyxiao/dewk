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
    
    # get frequency list
    f_list = _build_freq_list(file_in_name)
    
    file_out.write((helpers.to_bin((len(f_list) -1), BYTE_SIZE)))
    
    for element in f_list :
        (f,val) = element
        file_out.write(helpers.to_bin(int(f), 4* BYTE_SIZE))
        file_out.write(helpers.to_bin(ord(val),BYTE_SIZE))
        
    # get dictionary of codes for given bytes
    codes = _add_codes(_build_tree(f_list),{},'')
    
    # read the first integer into file
    i = file_in.read(READ_IN_SIZE)
    
    # initialize string to get total bits written
    # (needed to know how much padding is added)
    bit_string = 0
    
    # while the integer isn't end of file, encode and write to file
    while (i != ''):
        file_out.write(codes[i])
        bit_string = (bit_string + len(codes[i])) % 8
        i = file_in.read(READ_IN_SIZE)
    
    # write how many significant bits in last byte to end
    padding = (BYTE_SIZE - bit_string) % 8
    padding_original = padding
    print padding
    while padding > 0:
        file_out.write("0")
        padding -= 1 
    file_out.write(helpers.to_bin(padding_original, BYTE_SIZE))
    print helpers.to_bin(padding_original, BYTE_SIZE)
    
    #now you're done!
    return helpers.end_compress(file_in,file_out)

####DECROMPRESS###

# decompress(file_name) takes in a file of type .huf 
# and outputs uncompressed file to disk

def decompress(file_name):
    
    (file_in,file_out) = helpers.start_decompress(file_name, ALG_NAME)
    
    p = file_in.tell()
    print p

    # go to last byte
    file_in.seek(-8,2)
    
    # store how much padding is in second to last byte
    pad = file_in.read(BYTE_SIZE)
    print pad
    
    padding = int(pad,2)
    print padding
    # set position to start of file
    file_in.seek(p,0)
    
    i = file_in.read(BYTE_SIZE)

    header_left = int(i,2) + 1
    header_left_original = header_left

    freq_list = [] 
    while (header_left > 0):
        freq = int(file_in.read(4*BYTE_SIZE),2)
        val = int(file_in.read(BYTE_SIZE),2)
        freq = freq + val/1000.
        header_left -= 1
        freq_list.append((freq,val))
        
    # get dictionary of codes for given bytes
    codes = _add_codes(_build_tree(freq_list),{},'')
    
    # flip dictionary 
    inv_codes = {}
    for code in codes:
        inv_codes[codes[code]] = code

    i = file_in.read(READ_IN_SIZE)
    code = i
    counter = 0
    stop = (helpers.size(file_in.name) - ((2*BYTE_SIZE) + padding + p + (header_left_original *5 * BYTE_SIZE) ))
    print stop

    while (counter < stop):
        i = file_in.read(READ_IN_SIZE)
        counter += 1
        if (code in inv_codes):
            file_out.write(helpers.to_bin(inv_codes[code], BYTE_SIZE))
            code = i
        else:
            code = code + i
        
    return helpers.end_decompress(file_in,file_out)        

#citation: inspired by http://stackoverflow.com/questions/11587044
#/how-can-i-create-a-tree-for-huffman-encoding-and-decoding
#and http://stackoverflow.com/questions/6770925/
#huffman-encoding-how-to-write-binary-data-in-python

# build frequency list
def _build_freq_list (file_in):
    return helpers.freq_list(file_in, "specific")
''' 
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
'''         

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
    
    
  



