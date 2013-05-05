"""
CS51 Final Project
Eamon, David, Kevin, Willy

test.py by Willy Xiao
willy@chenxiao.us
"""
import filecmp 
import unittest 
import os
import shutil
import time
import sys 
sys.path.append("../")

from algs import *
import algs
import super
import dir
import s_helpers

# the algorithms listed
algos = {
    "none" : algs.none,
    
    "fib" : algs.fib,
    "huff" : algs.huff,
    "lzw" : algs.lzw, 
    #"seq" : algs.seq
}

# tests all the individual algorithms
def test_algs (file_name) : 
    for alg_name in algos : 
        compressed = algos[alg_name].compress(file_name) 
        decompressed = algos[alg_name].decompress(compressed)
        assert(filecmp.cmp(file_name, decompressed))
        os.remove(compressed)
        os.remove(decompressed)

# tests super
def test_super (dir_name) : 
    for f in os.listdir(dir_name) : 
        f = os.path.join(dir_name, f)
        
        if os.path.isfile(f) :  
            tmp = algs.helpers.free_name(f + "tmp") 
            shutil.copyfile(f, f + "tmp") 
            assert(filecmp.cmp(super.decompress(super.compress(f)), tmp))
            os.remove(tmp)

# test dir_compress 
def test_dir (dir_name) : 
    # watch the printed statements to the output
    dir.decompress(dir.compress(dir_name))

# test all of 'em
def test_all(test_file_name, test_dir_name) : 
    
    print_with_sleep("Testing algs...") 
    test_algs(test_file_name)
    print_with_sleep("All algs passed!") 
    
    print_with_sleep("Testing super...")
    test_super(test_dir_name)
    print_with_sleep("Super passed!")
    
    print_with_sleep("Testing dir...") 
    test_dir(test_dir_name)
    print_with_sleep("Dir passed!")
    
    print "All tests passed! Yay!"  

# prints a message with a 2s delay
def print_with_sleep(message) : 
    s_helpers.print_single_line()
    print message
    s_helpers.print_single_line()
    time.sleep(2)
    
# to test everything from terminal
if len(sys.argv) != 3 : 
    print "Usage: python test.py test_file_name test_directory_name" 
else : 
    test_all(sys.argv[1], sys.argv[2])
