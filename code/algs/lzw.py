"""
CS51 Final Project
Eamon, David, Kevin, Willy

lzw.py by Willy Xiao, Kevin Eskici, Eamon Obrien


lzw pseudo-code for compression: 

    initialize a code dictionary to contain all the ascii 
        integer-values of the characters
    initialize integer to 256
    initialize a string to '' 
    read a byte, attach the byte to the end of the string : 
        if string is in the code dictionary, move on
        else 
            add string to code dictionary
            increment integer
            write string without the last character to file
            string becomes the last character

**lots of help from : http://marknelson.us/2011/11/08/lzw-revisited/
"""
import subprocess
import sys
import string
import helpers

READ_IN_SIZE = 1 
ALG_NAME = "lzw"
BYTE_SIZE = 8
TOO_MUCH = 100
    
###COMPRESS###
def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)

    # initialize the file_in position, this is needed because 
    # file_in might not be "pure"
    init_pos = file_in.tell() # start of file (will need later)

    # STEP 1 : Create the code dictionary
    sys.stdout.write("Creating codes...")
    counter = _compress_run(file_in, file_out, 0, "none")
    print "Done!"

    # STEP 2 : Write out the length that each int will need
    # bit_len is the length required to represent each integer
    bit_len = len(bin(counter)) - 2

    # write the length
    file_out.write(helpers.to_bin(bit_len, BYTE_SIZE))
    
    # go back to beginning of file_in
    file_in.seek(init_pos, 0)
    
    # STEP 3 : Run again, writing out codes for the file
    sys.stdout.write("Writing codes...")
    _compress_run(file_in, file_out, bit_len, "write")
    print "Done!"
    
    return helpers.end_compress(file_in,file_out)

###DECOMPRESS###
def decompress(file_name):

    (file_in, file_out) = helpers.start_decompress(file_name, ALG_NAME)  

    # initial codes is the inverse of the original compression-codes
    codes = helpers.inverse_dict(initial_dict())

    # size is the number of bits needed to represent each int
    size = int(file_in.read(BYTE_SIZE), 2)
    
    # decompression!
    b = file_in.read(size)
    n = helpers.from_bin(b)
    string = codes[n]
    counter = 256
    
    while (len(b) == size) : 

        # write out current string
        helpers.write_string(file_out, string)

        # file_in.read might return '' in which case from_bin won't work, 
        # break the loop in that case
        try : 
            # read next integer from file
            b = file_in.read(size)
            n = helpers.from_bin(b)            
        except ValueError: 
            break 

        # otherwise continue with decoding
        else :        

            # create new string (if n is not yet in codes, 
            # that means there's repetition
            if (n in codes) : 
                string += codes[n][:1]
            else : 
                string += string[:1]

            codes[counter] = string
            counter += 1    

            # string to write out is the string taken in
            string = codes[n]

    return helpers.end_decompress(file_in, file_out) 

# initial dictionary used for compression and decompression    
def initial_dict () : 
    codes = {}
    i = 0 
    
    while i < 256 : 
        codes[chr(i)] = i 
        i += 1
    
    return codes

# compress_run takes in a file_in, a file_out, 
# and a mode which determines if items should be written
def _compress_run (file_in, file_out, bit_len, mode) : 

    writer = (mode == "write")
    
    # runs through the file and either creates the code, or 
    # creates the dictionary and writes to file
    codes = initial_dict() # initial dictionary for each unique char
    string = '' # empty string starting-off
    c = file_in.read(READ_IN_SIZE)
    counter = 256
    
    while c != '' : 
        string += c 

        if not (string in codes) : 
            codes[string] = counter

            if writer : 
                file_out.write(helpers.to_bin(codes[string[:-1]], bit_len))
                
            counter += 1            
            string = string[-1:]
        
        c = file_in.read(READ_IN_SIZE)
    
    if writer : 
        file_out.write(helpers.to_bin(codes[string], bit_len))
    
    return counter



### ESTIMATE ###
sample_size = 5000
import math

def estimate(file_name) : 
    # assuming compression ratio gets better by log( size of file / sample size) 
    return helpers.estimate_cr(file_name, compress, math.log, sample_size)
