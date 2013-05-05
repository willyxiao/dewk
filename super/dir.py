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
    
    old_size = dir_size(dir_name) 
    s_helpers.print_double_line()
    print "COMPRESSING DIRECTORY: \"" + dir_name + "\" " 
    print "Size: " + str(old_size) + " bytes"
    s_helpers.print_double_line()

    # compress all the files
    _dc_individuals(dir_name, "compress")

    # open the name of the final compressed_file name
    output_name = helpers.free_name(dir_name + DEWK)
    file_out = open(output_name, "w")
    
    # concatenates all compressed files together
    concat_files(dir_name, file_out)
    
    file_out.close()     
    shutil.rmtree(dir_name)           

    new_size = os.path.getsize(file_out.name)
    
    s_helpers.print_double_line()
    print "DIRECTORY COMPRESSED TO: \"" + file_out.name + "\" "
    print "Original Size: " + str(old_size) + " bytes" 
    print "New Size: " + str(new_size) + " bytes" 
    print "Compression Ratio: " + str(float(new_size) / old_size) 
    s_helpers.print_double_line()

    return file_out.name

# concat_files returns the concatenation of all the files within directory_name
def concat_files(dir_name, file_out) : 
    s_helpers.check_dir(dir_name)
    
    # write the signature at the beginning which is the "dir\00dir_name\00"
    file_out.write(ALG_NAME)
    file_out.write(chr(0))
    file_out.write(os.path.basename(dir_name))    
    file_out.write(chr(0))
    
    # add all of the sub-files into file_out too
    for f in os.listdir(dir_name) :
        f = os.path.join(dir_name, f)
         
        # if it's a directory, concatenate that first into a single file, then append it to concat_add
        if os.path.isdir(f) : 
            name = helpers.free_name(f + DEWK)
            file_inner = open(name, "w")
            done_inner = concat_files(f, file_inner)
            file_inner.close()
            concat_add(done_inner, file_out)
        else : # f is a file
            concat_add(f, file_out)            
    
    return file_out.name

# concat_add appends file to the end of file_out            
def concat_add(f_name, file_out) : 
    s_helpers.check_file(f_name) 
    
    # appends signature "file_name\x00file_size"
    file_out.write(os.path.basename(f_name))
    file_out.write(chr(0))    
    size = helpers.size(f_name)
    file_out.write(struct.pack("I", size))

    # copy file over
    copy = open(f_name, 'rb')
    shutil.copyfileobj(copy, file_out)
    copy.close()

### DECOMPRESS ###
def decompress(compressed_name) : 
    s_helpers.check_file(compressed_name)
    
    s_helpers.print_double_line()
    print "DECOMPRESSING DIRECTORY: \"" + compressed_name + "\" " 
    print "Size: " + str(os.path.getsize(compressed_name)) + " bytes"
    s_helpers.print_double_line()
    
    backup = s_helpers.free_dir_name(compressed_name)
    shutil.copyfile(compressed_name, backup)

    try : 
        compressed_file = open(compressed_name, "r") 
        path = os.path.dirname(compressed_name)
        
        # unpacks the directory tree from .dewk
        dir_name = unpack(path, compressed_file)     

        # then decompresses each individual file
        _dc_individuals(dir_name, "decompress")

        s_helpers.print_double_line()
        print "DIRECTORY DECOMPRESSED TO: \"" + dir_name + "\" "
        print "Size: " + str(dir_size(dir_name)) + " bytes"
        s_helpers.print_double_line()
    
    except : 
        try : 
            os.rename(backup, compressed_name) 
        except OSError: 
            if os.path.exists(backup) : 
                os.remove(compressed_name) 
                os.rename(backup, compressed_name) 
                os.remove(backup)
        else :
            raise

    else :  
        os.remove(backup)         
        
    return dir_name

# unpack(path, compressed_file) unpacks the directory tree from the .dewk file
def unpack(path, compressed_file) : 
    token = s_helpers.read_until(chr(0), compressed_file)
    
    # asserts that the token is dir
    if token != ALG_NAME : 
        raise TypeError(compressed_file.name + " is not a compressed directory")
    
    # makes the directory that it should be called
    basename = s_helpers.read_until(chr(0), compressed_file)
    dir_name = s_helpers.free_dir_name(os.path.join(path, basename))    
    os.mkdir(dir_name)

    is_eof = False 
    
    # read until the end_of_file
    while (not is_eof) : 
    
        try : 

            file_basename = s_helpers.read_until(chr(0), compressed_file)
            file_name = os.path.join(dir_name, file_basename)

        # RuntimeError indicates it's at the end of file
        except RuntimeError : 
            
            is_eof = True 
        
        # break the old file into the new file
        else : 
            tmp = struct.unpack("I", compressed_file.read(4)) # 4 is the size of an unsigned int
            size = tmp[0]
            file_out = open(file_name, "w")
            file_out.write(compressed_file.read(size))
            file_out.close () 

    # if any of the items are directories, unpack them
    for file_name in os.listdir(dir_name) : 
        file_name = os.path.join(dir_name, file_name) 
        
        f = open(file_name, "r") 
        
        try : 
            unpack(dir_name, f) 
        
        except TypeError : 
            f.close() 
    
    compressed_file.close()
    os.remove(compressed_file.name)
    return dir_name
            
# dc_individuals either decompresses or compresses all of the directories
# in place within a directory
def _dc_individuals(dir_name, mode) : 
    compress = (mode == "compress")
    decompress = (mode == "decompress")

    items = os.listdir(dir_name) 
    
    # go through all directories and items recursively, decompressing or compressing them
    for item in items : 
        name = os.path.join(dir_name, item)

        if os.path.isdir(name) : 
            _dc_individuals(name, mode)

        else : 
            if compress :         
                new_name = super.compress(name)

            elif decompress : 
                new_name = super.decompress(name) 

            else : 
                raise TypeError("dir.py : dc_individuals has incorrect [mode]")

# dir_size returns the size of the directory with all sub-files
def dir_size(dir_name) : 
    s_helpers.check_dir(dir_name) 
    total_size = 0 
    
    for f in os.listdir(dir_name) : 
        f = os.path.join(dir_name, f)
        
        if os.path.isdir(f) : 
            total_size += dir_size(f)
        else : 
            total_size += os.path.getsize(f)
    
    return total_size
