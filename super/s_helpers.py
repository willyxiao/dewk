'''
CS51 Final Project
Eamon, David, Kevin, Willy

s_helpers.py by Willy Xiao
willy@chenxiao.us
'''
# for helpers
import sys
sys.path.append('../algs')
import helpers

import os

# assert that file_name is a file
def check_file(file_name) : 
    if not os.path.isfile(file_name) :         
        raise TypeError("super.py : \"" + file_name + "\" is not a file")
    else : 
        return 0

# assert that dir_name is a directory
def check_dir(dir_name) : 
    if not os.path.isdir(dir_name) :         
        raise TypeError("super.py : \"" + dir_name + "\" is not a directory")
    else : 
        return 0

# read_until will read a file until it hits c, if it hits EOF before that, returns error
def read_until(c, file_in) : 
    total_read = ''
    one_read = file_in.read(1)
    
    while ( one_read != c ) : 
        if one_read == '' : 
            raise RuntimeError(file_in.name + " does not have another " + c)
        total_read += one_read
        one_read = file_in.read(1)
    
    return total_read

# free_dir_name returns the free name of a directory
def free_dir_name(dir_name) : 
    counter = 0 
    new_name = dir_name
    
    while(os.path.exists(new_name)) : 
        new_name = dir_name + str(counter)
        counter += 1
   
    return new_name

def print_single_line() : 
    print "-------------------------" 
    
def print_double_line() : 
    print "=========================="
