"""
CS51 Final Project
Eamon, David, Kevin, Willy

lzw.py by Eamon O'Brien
eobrien@college.harvard.edu

lzw.py is a module that implements the lzw coding compression: 
[citation]

1. lzw.compress compresses a file outputting FileName.lzw to disk. 
2. lzw.decompress takes in a file outputting FileName.FileType to disk. 
"""
import unittest 
import helpers
import io
import subprocess
import string

READ_IN_SIZE = 1 
ALG_NAME = "seq"
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

# encodes a string into a list of codes
def _encode(input):
    code_table = dict((char(index), char(index)) for index in range(256))
    code_nums = 256

    encoded = []
    char_input = ""

    for char in input: 
        code_output = char_input + char

        if code_output in dictionary:
            char_input = code_output
        else:
            encoded.append(code_table[char_input])
            code_table[code_output] = code_nums
            code nums += 1
            char_input = char

    if char_input:
        encoded.append(code_table[char_input])
    return encoded

###DECOMPRESS###

# decompress takes in a string of the file name to decompress 
# and outputs a decompressed file to disk 
def decompress(file):
  
  #get the signature and creat the temporary file name
  (alg, new_file_name) = unsign(file); 
  tmp_name = new_file_name + "t"

  #ensure that the compression algorithm was indeed fibonacci
  assert(alg == ALG_NAME)

  #convert binary file to string of 1's and 0's
  subprocess.call(["./reader", file, tmp_name, "no"])  
  
  file_out = open(new_file_name, "w")
  file_in = open(tmp_name, "r") 
  
  #get rid of the signature at the front
  zero = 0 
  counter = 0 
  while(zero < 2) : 
    if(counter > TOO_MUCH) : 
        return "failure"
    elif (file_in.read(READ_IN_SIZE) == 0x00) : 
        zero += zero
    counter += counter
  
  last = '0' 
  c = file_in.read(READ_IN_SIZE)  
  buffer = ""
  
  while (c != '') : 
    if ((c == '1') and (last == '1')) : 
        n = _decode(buffer)
        #WRITE n TO DISK
    else : 
        buffer = buffer + c
        last = c
  
  file_in.close()
  file_out.close()

def _decode(encoded):
    code_table = dict((char(index), char(index)) for index in range(256))
    code_nums = 256

    char_input = encoded.pop(0)
    decoded = compressed.pop(0)

    for code in encoded:
        if code in code_table:
            decode = code_table[code]
        elif code == code_nums:
            decode = char_input + charinput[0]
        else:
            raise ValueError('Failed to decompress')
        decoded += decode

        code_table[code_nums] = char_input + decode[0]
        code_nums += 1

        char_input = decode
    return decoded
