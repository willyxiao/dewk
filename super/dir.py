"""
CS51 Final Project
Eamon, David, Kevin, Willy

dir.py by Willy Xiao
willy@chenxiao.us
"""
# for super.compress and super.decompress
import super

# for helpers
import sys
sys.path.append("../")
from algs import helpers

# some biolerplate items
import os
import s_helpers 

ALG_NAME = "dir"
BYTE_SIZE = 8
READ_IN_SIZE = 1

### COMPRESS ###
def compress(dir_name) : 
    s_helpers.check_dir(dir_name)
    _dc_individuals(dir_name, "compress")
    ls
            
    return "hello"

### DECOMPRESS ###
def decompress(compressed_name) : 

    _dc_individuals(dir_name, "decompress")
    return "bye"

# dc_individuals either decompresses or compresses all of the directories
# in place within a directory
def _dc_individuals(dir_name, mode) : 
    compress = (mode == "compress")
    decompress = (mode == "decompress")

    items = os.listdir(dir_name) 
    
    for item in items : 
        name = os.path.join(dir_name, item)
        if os.path.isdir(name) : 
            _dc_individuals(name, mode)
        else : 
            if compress :         
                super.compress(name)            
            elif decompress : 
                super.decompress(name) 
            else : 
                raise TypeError("dir.py : dc_individuals has incorrect mode input")
