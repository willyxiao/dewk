"""
CS51 Final Project
Eamon, David, Kevin, Willy

fib.py by Willy Xiao
willy@chenxiao.us

fib.py is a module that implements the fibonacci coding compression: 
[citation]

1. fib.compress compresses a file outputting FileName.fib to disk. 
2. fib.decompress takes in a file outputting FileName.FileType to disk. 
"""
import unittest 
import subprocess
import string
import helpers


READ_IN_SIZE = 1 
ALG_NAME = "fib"
BYTE_SIZE = 8
TOO_MUCH = 100
    
###COMPRESS###

# compress(file_in_name) outputs a compressed .fib file to disk 
def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)
    
    # read the first integer into file
    i = file_in.read(READ_IN_SIZE)
    
    # while the integer isn't end of file, encode and write to file
    while (i != ''):
        enc = _encode(ord(i))
        file_out.write(enc)
        i = file_in.read(READ_IN_SIZE)
    
    #now you're done!
    return helpers.end_compress(file_in,file_out)

# encode(n) is a helper function that encodes a single 
# integer into a fibonacci sequence    
# Note: this builds upon the algorithm 
# from http://en.wikipedia.org/wiki/Fibonacci_coding. 4/18/2013
def _encode(n):
    # ensure n >= 1
    n += 1

    # Return string with Fibonacci encoding for n (n >= 1).
    a = 1
    b = 1
    c = a + b   # next Fibonacci number
    fibs = [b]  # list of Fibonacci numbers, starting with F(2), each <= n
    while n >= c:
        fibs.append(c)  # add next Fibonacci number to end of list
        a = b
        b = c
        c = a + b
    result = "1"  # extra "1" at end
    for fibnum in reversed(fibs):
        if n >= fibnum:
            n = n - fibnum
            result = "1" + result
        else:
            result = "0" + result
    return result

###DECOMPRESS###

# decompress(file_name) takes in a file of type .fib and 
# outputs uncompressed file to disk
def decompress(file_name):

    (file_in, file_out) = helpers.start_decompress(file_name, ALG_NAME)  

    # last will be used to check if two 1's are in a row
    last = '0' 
    
    # buffer will be the fibonacci sequence
    buffer = ""    
    
    # read first character from file (should be 1 or 0)
    c = file_in.read(READ_IN_SIZE)  
  
    # keep repeating until end of file
    while (c != '') : 

        # the buffer with the next 
        buffer = buffer + c    

        # if the current character and last are both 1 then buffer is done
        if ((c == '1') and (last == '1')) : 

            # n is the decoded int (n should be less than the max int inputted
            n = _decode(buffer)
            assert(n < (2 ** (BYTE_SIZE * READ_IN_SIZE)))
            
            # write it to file and reset buffer and last
            file_out.write(helpers.to_bin(n, BYTE_SIZE))
            buffer = ""
            last = '0'

        # otherwise last is character and repeat
        else : 
            last = c

        c = file_in.read(READ_IN_SIZE)    
  
    return helpers.end_decompress(file_in, file_out) 
  
# decode(code) takes in a binary fibonnaci string and returns
# the integer coded for
def _decode(code):
    assert(code[-2:] == "11")
    
    #initialize
    a = 1 
    b = 2 
    n = 0
    
    #run
    while (code != "1") : 
        n += (int(code[:1]) * a)
        tmp = a
        a = b
        b = tmp + b
        code = code[1:]
    
    #return
    return (n - 1)   

### ESTIMATE ###
def estimate(file_name) : 

    # frequency list sample of the file
    freq_list = helpers.freq_list(file_name, "sample") 
    
    # find the total number of bits of the first compressed sample_size bytes    
    total_bits = 0 
    for pair in freq_list : 
        (freq, char) = pair 
        total_bits += (len(_encode(ord(char))) * freq)
    
    total_bytes = total_bits / BYTE_SIZE
    
    # returns the total_bytes times the ration of the file_size / sample_size
    return (total_bytes * helpers.freq_list_sample_ratio(file_name))

