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
import struct
import shutil
import s_helpers 
import subprocess

ALG_NAME = "dir"
BYTE_SIZE = 8
READ_IN_SIZE = 1
DEWK = ".dewk"

### COMPRESS ###
def compress(dir_name) : 
    s_helpers.check_dir(dir_name)

    # compress all the files
    _dc_individuals(dir_name, "compress")

    # open the name of the final compressed_file name
    output_name = helpers.free_name(dir_name + DEWK)
    file_out = open(output_name, "w")
    
    # concatenates all compressed files together
    concat_files(dir_name, file_out)
    
    compressed_name = file_out.name
    file_out.close() 
            
    return compressed_name

# concat_files returns the concatenation of all the files within directory_name
def concat_files(dir_name, file_out) : 
    s_helpers.check_dir(dir_name)
    
    file_out.write(ALG_NAME)
    file_out.write(chr(0))
    file_out.write(os.path.basename(dir_name))    
    file_out.write(chr(0))
#    number_of_items = len(os.path.listdir(dir_name))
#    file_out.write(struct.pack("I", number_of_items))
    
    for f in os.listdir(dir_name) :
        f = os.path.join(dir_name, f)
         
        if os.path.isdir(f) : 
            name = helpers.free_name(f + DEWK)
            file_inner = open(name, "w")
            done_inner = concat_files(f, file_inner)
            file_inner.close()
            concat_add(done_inner, file_out)
        else : # f is a file
            concat_add(f, file_out)            
    
    compressed_dir = file_out.name
    
    return compressed_dir
            
def concat_add(f_name, file_out) : 
    s_helpers.check_file(f_name) 
    
    file_out.write(os.path.basename(f_name))
    file_out.write(chr(0))
    
    size = helpers.size(f_name)
    file_out.write(struct.pack("I", size))
    copy = open(f_name, 'rb')
    shutil.copyfileobj(copy, file_out)
    copy.close()

### DECOMPRESS ###
def decompress(compressed_name) : 

    compressed_file = open(compressed_name, "r") 
    path = os.path.dirname(compressed_name)
    
    dir_name = unpack(path, compressed_file)     

    _dc_individuals(dir_name, "decompress")

    return dir_name

# unpack(path, compressed_file) unpacks the directory tree from the .dewk file
def unpack(path, compressed_file) : 
    token = s_helpers.read_until(chr(0), compressed_file)
    
    if token != ALG_NAME : 
        raise TypeError(compressed_file.name + " is not a compressed directory")
    
    basename = s_helpers.read_until(chr(0), compressed_file)
    dir_name = s_helpers.free_dir_name(os.path.join(path, basename))
        
    subprocess.call(["mkdir", dir_name])
    is_eof = False 
    
    while (not is_eof) : 
    
        try : 

            file_basename = s_helpers.read_until(chr(0), compressed_file)
            file_name = os.path.join(dir_name, file_basename)

        except RuntimeError : 
            
            is_eof = True 
        
        else : 
            tmp = struct.unpack("I", compressed_file.read(4)) # 4 is the size of an unsigned int
            size = tmp[0]
            file_out = open(file_name, "w")
            file_out.write(compressed_file.read(size))
            file_out.close () 

    for file_name in os.listdir(dir_name) : 
        file_name = os.path.join(dir_name, file_name) 
        
        f = open(file_name, "r") 
        
        try : 
            unpack(dir_name, f) 
        
        except TypeError : 
            f.close() 
    
    to_del = compressed_file.name            
    compressed_file.close()
    os.remove(to_del)

    return dir_name
            

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
                new_name = super.compress(name)
                print "Running compression: " + name + " ||>| " + new_name + "..."            
            elif decompress : 
                new_name = super.decompress(name) 
                print "Running decompression: " + name + " |>|| " + new_name + "..."
            else : 
                raise TypeError("dir.py : dc_individuals has incorrect [mode]")
