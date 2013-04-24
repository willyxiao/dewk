"""
CS51 Final Project
Eamon, David, Kevin, Willy

super.py by Willy Xiao and _
willy@chenxiao.us

super.compress first finds the best compression algorithm to be used on each file and then 
uses that algorithm to encode the file

super.decompress decompresses a file
"""
# import all of the compression algorithms 
import sys
sys.path.append('../')
from algs import *

# rest of the necessary files
import random


def best_alg(file_name): 
    i = random.randint(1,2)
    if i == 1 :
        return "fib"
    else :
        return "sequiter"   
