"""
CS51 Final Project
Eamon, David, Kevin, Willy

super.py by Willy Xiao and _
willy@chenxiao.us

super.compress first finds the best compression algorithm to be used on each file and then 
uses that algorithm to encode the file

super.decompress decompresses a file
"""

# this allows appending files from a different directory
import random

import sys
sys.path.append('../algs')
import fib
import sequiter

def best_alg(file_name): 
    i = random.int(1,2)
    if i = 1 :
        return "fib"
    else :
        return "sequiter"   
