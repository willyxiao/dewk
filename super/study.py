"""
CS51 Final Project
Eamon, David, Kevin, Willy

study.py by Willy Xiao
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
    "huff" : algs.huff,
    "lzw" : algs.lzw, 
    #"seq" : algs.seq
}

# NOTE: best_alg returns the best single alg. It doesn't, however, compress a compressed file

# best_alg finds the best algorithm for compression based on the 
# first sample_size bytes of the file (in helpers.py)
def best_alg(file_name): 
 
    # for testing
#    alg_name = random.choice(algos.keys())
#    best_alg = algos[alg_name]
#    best_estimate = best_alg.estimate(file_name)   
 
    # initialize the best algorithm to none
    best_estimate = algs.none.estimate(file_name)
    best_alg = algs.none

    # if any of the algorithms are better, then substitute it in for the best
    for alg_name in algos : 
        estimate = algos[alg_name].estimate(file_name)
        if best_estimate > estimate : 
            best_estimate = estimate
            best_alg = algos[alg_name]
    
    print "Best Algorithm: " + alg_name
    print "Estimated Size: " + str(best_estimate)

    # return the best algorithm
    return best_alg

# get_alg returns the module used to compress the file 
# file_name must be the name of a compressed file
def get_alg(file_name): 
    alg_name = algs.helpers.which_alg(file_name)
    print "Algorithm Used: " + alg_name
    return algos[alg_name]
