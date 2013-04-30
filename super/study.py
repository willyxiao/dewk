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

# the algorithms listed
algos = {
    "none" : algs.none,
    
    "fib" : algs.fib,
    #"huff" : algs.huff,
    #"lzw" : algs.lzw, 
    #"seq" : algs.seq
}

# best_alg finds the best algorithm for compression based on the 
# first 500 bytes of the file
def best_alg(file_name): 
    
    # initialize the best algorithm to none
    best_estimate = algs.none.estimate(file_name)
    best_alg = algs.none

    # if any of the algorithms are better, then substitute it in for the best
    for alg_name in algos : 
        estimate = algos[alg_name].estimate(file_name)
        if best_estimate > estimate : 
            best_estimate = estimate
            best_alg = algos[alg_name]
    
    # return the best algorithm
    return best_alg

# get_alg returns the module used to compress the file 
# file_name must be the name of a compressed file
def get_alg(file_name): 
    alg_name = algs.helpers.which_alg(file_name)
    return algos[alg_name]
