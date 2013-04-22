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
import subprocess
import string
import os

READ_IN_SIZE = 1 
ALG_NAME = "fib"
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
    subprocess.call(["rm", "-f", file_out_name])
    
'''for later        
        while(enc != ''): 
            #print enc
            leng = len(enc)
            
            if (leng + buffer_pos) < BYTE_SIZE : 
                (buffer, buffer_pos) = _update_buff(buffer, buffer_pos, enc, leng)
                enc = ''
                            
            elif (leng + buffer_pos) == BYTE_SIZE : 
                (buffer, buffer_pos) = _update_buff(buffer, buffer_pos, enc, leng)
                file_out.write(bytes(buffer))
                buffer = 0x00
                buffer_pos = 0 
                enc = ''
        
            else : #leng + buffer_pos > BYTE_SIZE : 
                (buffer, buffer_pos) = _update_buff(buffer, buffer_pos, enc, (BYTE_SIZE - buffer_pos))
fi                file_out.write(bytes(buffer))
                buffer = 0x00
                buffer_pos = 0
                enc = enc[(BYTE_SIZE - buffer_pos):]
    
        i = file_in.read(READ_IN_SIZE)
'''
# encodes a single integer less than or equal to 1 into a fibonacci sequence. 
# Note: this builds upon the algorithm from http://en.wikipedia.org/wiki/Fibonacci_coding. 4/18/2013
def _encode(n):
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

'''
might not need
def _update_buff(buffer, buffer_pos, enc, leng):
    j = 0
    while (j < leng) : 
        buffer = buffer | (int(enc[j]) << (leng - (j + 1)))
        j += 1
        buffer_pos += leng
    return (buffer, buffer_pos)
'''

###DECOMPRESS###

# decompress takes in a string of the file name to decompress 
# and outputs a decompressed file to disk 
def decompress(file):
  
  #get the signature and creat the temporary file name
  (alg, new_file_name) = helpers.unsign(file); 
  tmp_name = helpers.free_name(new_file_name + ".t")
  tmp_name2 = helpers.free_name(tmp_name + "t")

  #ensure that the compression algorithm was indeed fibonacci
  assert(alg == ALG_NAME)

  #convert binary file to string of 1's and 0's
  subprocess.call(["./reader", file, tmp_name, "e"])  
  
  file_out = open(tmp_name2, "w")
  file_in = open(tmp_name, "r") 
  
  #get rid of the signature at the front
  zero = 0 
  counter = 0 
  while(zero < 2) : 
    if(counter > TOO_MUCH) : 
        return "failure"
    elif (file_in.read(READ_IN_SIZE) == bytearray(1)) : 
        zero += 1
    counter += 1
  
  last = '0' 
  c = file_in.read(READ_IN_SIZE)  
  buffer = ""
  
  while (c != '') : 
    buffer = buffer + c    
    if ((c == '1') and (last == '1')) : 
        n = _decode(buffer)
        assert(n < (2 ** (BYTE_SIZE * READ_IN_SIZE)))
        b = bin(n)[2:]
        while(len(b) < BYTE_SIZE) : 
            b = '0' + b
        file_out.write(b)
        buffer = ""
        last = '0'
    else : 
        last = c
    c = file_in.read(READ_IN_SIZE)    
  
  file_in.close()
  file_out.close()
  
  subprocess.call(["./writer", tmp_name2, new_file_name, "no"])
  subprocess.call(["rm", "-f", tmp_name2])
  subprocess.call(["rm", "-f", tmp_name])

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

def test () : 
    compress("../tests/001.jpg")
    decompress("../tests/001.fib")
    compress("../tests/canon.mid")
    decompress("../tests/canon.fib")
    compress("../tests/ps7.txt")
    decompress("../tests/ps7.fib")
 
def del_tests () : 
    subprocess.call(["rm", "-f", "../tests/001.fib"])
    subprocess.call(["rm", "-f", "../tests/0010.jpg"])
    subprocess.call(["rm", "-f", "../tests/canon.fib"])
    subprocess.call(["rm", "-f", "../tests/canon0.mid"])
    subprocess.call(["rm", "-f", "../tests/ps7.fib"])
    subprocess.call(["rm", "-f", "../tests/ps70.txt"])
