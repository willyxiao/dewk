"""
CS51 Final Project
Eamon, David, Kevin, Willy

study.py by Willy Xiao and _
willy@chenxiao.us
"""
# allow the system path to be recognized
import sys
sys.path.append('../')

# import everything from algs that is needed
from algs import *
import algs

# rest of the necessary files
import random

def best_alg(file_name): 
    freq_list = algs.helpers.freq_list(file_name)
    for tup in freq_list : 
        (fr, ch) = tup 
        
    return algs.fib

def get_alg(file_name): 
    alg_name = algs.helpers.which_alg(file_name)

    if alg_name == "fib" : 
        return algs.fib
    else :
        print "Something went wrong! There ain't that alg yo..."
        raise Exception("Invariant Broken")
