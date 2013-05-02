"""
CS51 Final Project
Eamon, David, Kevin, Willy

lzw.py by Willy Xiao, Eamon Obrien, Kevin Eskici

1. fib.compress compresses a file outputting FileName.fib to disk. 
2. fib.decompress takes in a file outputting FileName.FileType to disk. 
"""
import unittest 
import subprocess
import string
import helpers


READ_IN_SIZE = 1 
ALG_NAME = "lzw"
BYTE_SIZE = 8
TOO_MUCH = 100
    
###COMPRESS###

def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)

    # initialize the file_in position, this is needed because file_in might not be "pure"
    init_pos = file_in.tell() # start of file (will need later)

    # STEP 1 : Create the code dictionary
    counter = _compress_run(file_in, file_out, 0, "none")
    
    # STEP 2 : Write out the length that each int will need
    # bit_len is the length required to represent each integer
    bit_len = len(bin(counter)) - 2

    # write the length
    file_out.write(helpers.to_bin(bit_len, BYTE_SIZE))
    
    # go back to beginning of file_in
    file_in.seek(init_pos, 0)
    
    # STEP 3 : Run again, writing out codes for the file
    _compress_run(file_in, file_out, bit_len, "write")
            
    return helpers.end_compress(file_in,file_out)

###DECOMPRESS###

# decompress(file_name) takes in a file of type .fib and outputs uncompressed file to disk
def decompress(file_name):

    (file_in, file_out) = helpers.start_decompress(file_name, ALG_NAME)  

    codes = helpers.inverse_dict(initial_dict()) 

    size = int(file_in.read(BYTE_SIZE), 2)
    
    n = file_in.read(size)
    string = chr(n)
    
    while (len(n) == size) : 
        helpers.write_string(file_out, string)
        
        string = codes[int(n, 2)]         
        

    return size #helpers.end_decompress(file_in, file_out) 

# initial dictionary used for compression and decompression    
def initial_dict () : 
    codes = {}
    i = 0 
    
    while i < 256 : 
        codes[chr(i)] = i 
        i += 1
    
    return codes

# create_codes takes in a file_in, a file_out, and a mode which determines if items should be writ
def _compress_run (file_in, file_out, bit_len, mode) : 

    codes = initial_dict() # initial dictionary for each unique char
    string = '' # empty string starting-off
    c = file_in.read(READ_IN_SIZE)
    counter = 255
    
    while c != '' : 
        string += c 

        if not (string in codes) : 
            codes[string] = counter

            if mode == "write" : 
                file_out.write(helpers.to_bin(codes[string[:-1]], bit_len))
                
            counter += 1            
            string = string[-1:]
        
        c = file_in.read(READ_IN_SIZE)
    
    return counter

### ESTIMATE ###
def estimate(file_name) : 

    ##TODO
    return "TODO"

### EXTRAS
'''    codes = initial_dict() # initial dictionary for each unique char
    string = '' # empty string starting-off
    c = file_in.read(READ_IN_SIZE)
    counter = 255
    
    while c != '' : 
        string += c 

        if not (string in codes) : 
            codes[string] = counter
            counter += 1            
            string = string[-1:]
        
        c = file_in.read(READ_IN_SIZE)
'''

