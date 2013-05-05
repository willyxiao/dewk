'''
CS51 Final Project
Eamon, David, Kevin, Willy

huff.py by Kevin Eskici
keskici@college.harvard.edu
'''

import io
import helpers
import Queue

READ_IN_SIZE = 1
ALG_NAME = "huff"
BYTE_SIZE = 8

### COMPRESS ###

# compress(file_in_name) outputs a compressed .huf file to disk
def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)
    
    print "Constructing huffman tree..." 
    
    # get frequency list
    f_list = _build_freq_list(file_in_name)
    
    file_out.write((helpers.to_bin((len(f_list) -1), BYTE_SIZE)))
    
    for element in f_list :
        (f,val) = element
        file_out.write(helpers.to_bin(int(f), 4* BYTE_SIZE))
        file_out.write(helpers.to_bin(ord(val),BYTE_SIZE))
        
    # get dictionary of codes for given bytes
    codes = _add_codes(_build_tree(f_list),{},'')
    
    print "Done!"
    print "Writing codes..." 
    
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

    while padding > 0:
        file_out.write("0")
        padding -= 1 
    file_out.write(helpers.to_bin(padding_original, BYTE_SIZE))
    
    #now you're done!
    return helpers.end_compress(file_in,file_out)

####DECROMPRESS###

# decompress(file_name) takes in a file of type .huf 
# and outputs uncompressed file to disk

def decompress(file_name):
    
    (file_in,file_out) = helpers.start_decompress(file_name, ALG_NAME)
    
    p = file_in.tell()

    # go to last byte
    file_in.seek(-8,2)
    
    # store how much padding is in second to last byte
    pad = file_in.read(BYTE_SIZE)
    
    padding = int(pad,2)

    # set position to start of file
    file_in.seek(p,0)
    
    i = file_in.read(BYTE_SIZE)

    header_left = int(i,2) + 1
    header_left_original = header_left
    
    print "Constructing huffman tree ...."
    
    # get frequency list from header
    freq_list = [] 
    while (header_left > 0):
        freq = int(file_in.read(4*BYTE_SIZE),2)
        val = int(file_in.read(BYTE_SIZE),2)
        freq = freq + val/1000.
        header_left -= 1
        freq_list.append((freq,val))
        
    # get dictionary of codes for given bytes
    codes = _add_codes(_build_tree(freq_list),{},'')
    
    print "Done!"
    print "Writing file ..."
    
    # flip dictionary 
    inv_codes = helpers.inverse_dict(codes)

    i = file_in.read(READ_IN_SIZE)
    code = i
    counter = 0
    # take header, padding, and signature into account
    stop = (helpers.size(file_in.name) - ((2*BYTE_SIZE) + padding + p + \
        (header_left_original *5 * BYTE_SIZE) ))

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


### ESTIMATE ###
def estimate(file_name) : 

    #frequency list sample of the file
    freq_list = helpers.freq_list(file_name, "sample")
    
    freq_dict = {}
    
    if helpers.freq_list_sample_ratio(file_name) != 1 and len(freq_list) < 256: 

        for n in freq_list : 
            (fr, c) = n 
            freq_dict[c] = float(fr)
    
        i = 0 
        total_missing = 0
        while (i < 256) : 
            if chr(i) not in freq_dict : 
                freq_dict[i] = 1
                total_missing += 1
            i += 1
        
        prob_dict = {}
        
        for f in freq_dict : 
            prob_dict[f] = freq_dict[f] / (helpers.freq_list_sample_size(file_name) + total_missing)
        
        to_simulate = helpers.size(file_name) - helpers.freq_list_sample_size(file_name) 
        
        for f in prob_dict : 
            freq_dict[f] += (to_simulate * prob_dict[f]) 
        
        freq_list = []
        for key in freq_dict : 
            freq_list.append((freq_dict[key], key))

    # build dictionary
    codes = _add_codes(_build_tree(freq_list),{},'')
        
    # find total bits in first compressed sample_size bytes
    total_bits = 0
    for pair in freq_list:
        (freq, val) = pair
        total_bits += freq * len(codes[val])
        
    header_size = len(freq_list) * 5
        
    total_bytes = 2*BYTE_SIZE + header_size + total_bits / BYTE_SIZE     

    return total_bytes  
