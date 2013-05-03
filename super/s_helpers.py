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

