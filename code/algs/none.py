"""
CS51 Final Project
Eamon, David, Kevin, Willy

none.py by Willy Xiao
willy@chenxiao.us

none.py is a module that does not compress the file
"""
import unittest 
import subprocess
import string
import helpers

ALG_NAME = "none"
BYTE_SIZE = 8
READ_IN_SIZE = 1
    
###COMPRESS###

def compress(file_in_name):
    
    (file_in,file_out) = helpers.start_compress(file_in_name, ALG_NAME)
    
    i = file_in.read(READ_IN_SIZE)
    
    while (i != ''):
        i = convert(i)
        file_out.write(i)
        i = file_in.read(READ_IN_SIZE)
    
    return helpers.end_compress(file_in,file_out)

def convert(n) : 
    return helpers.to_bin(ord(n), BYTE_SIZE)
    
###DECOMPRESS###

def decompress(file_name):

    (file_in, file_out) = helpers.start_decompress(file_name, ALG_NAME)  

    c = file_in.read(READ_IN_SIZE)  
  
    while (c != '') : 
        file_out.write(c)
        c = file_in.read(READ_IN_SIZE)    
  
    return helpers.end_decompress(file_in, file_out) 

###ESTIMATE###

def estimate(file_name) : 
    return helpers.size(file_name)
