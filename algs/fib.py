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
import helpers
import io

READ_IN_SIZE = 1 
ALG_NAME = "fib"
BYTE_SIZE = 8

global buffer
buffer = 0x00

global buffer_pos
buffer_pos = 0 
    
###COMPRESS###

# compress takes in a string of the file name to compress 
# and outputs a compressed file to disk
def compress(file_in_name):
    global buffer
    global buffer_pos

    # opens output file and signs it 
    (file_out_name, sign) = helpers.ensign(file_in_name, ALG_NAME)  
    file_out = io.open(file_out_name, "wb") 
    file_out.write(sign)
        
    file_in = io.FileIO(file_in_name, "r")
    i = file_in.read(READ_IN_SIZE)
    
    while (i != ''):
        enc = _encode_int(ord(i))
        leng = len(enc) 
        
        if (leng + buffer_pos) < BYTE_SIZE :            
            j = 0
            while (j < leng) : 
                buffer = buffer | (int(enc[j]) << (leng - (j + 1)))
                j += 1
                buffer_pos += leng
            
        elif (leng + buffer_pos) == BYTE_SIZE : 
            j = 0 
            while (j < leng) : 
                buffer = buffer | (int(enc[j]) << (leng - (j + 1)))
                j += 1
            file_out.write(unichr(buffer))
            buffer = 0x00
            buffer_pos = 0
        
        else : #leng + buffer_pos > BYTE_SIZE : 
            j = 0 
            while (j < (BYTE_SIZE - buffer_pos)) : 
                buffer = buffer | (int(enc[j]) << ((BYTE_SIZE - buffer_pos) - (j + 1)))
                j += 1
            file_out.write(unichr(buffer))
            buffer = 0x00
            buffer_pos = 0
    
        i = file_in.read(READ_IN_SIZE)

    file_in.close(); 
    file_out.close();

        
# encodes a single integer less than or equal to 1 into a fibonacci sequence. 
# Note: this builds upon the algorithm from http://en.wikipedia.org/wiki/Fibonacci_coding. 4/18/2013
def _encode_int(n):
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

# decompress takes in a string of the file name to decompress 
# and outputs a decompressed file to disk 
def decompress(file):
  print file;
