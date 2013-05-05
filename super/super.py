"""
CS51 Final Project
Eamon, David, Kevin, Willy

super.py by Willy Xiao and _
willy@chenxiao.us

super.compress first finds the best compression algorithm to be used on each file and then 
uses that algorithm to encode the file

super.decompress decompresses a file
"""
import study
import s_helpers

import subprocess
import sys
import os

DEWK = ".dewk"

def compress(file_name) :

    # ensure file_name is actually the name of a file
    s_helpers.check_file(file_name) 
    s_helpers.print_single_line() 
    print "Compressing File: \"" + file_name + \
        "\" (" + str(os.path.getsize(file_name)) + ")..."
    
    # best_algorithm based upon each alg's estimation
    alg = study.best_alg(file_name)
    
    # if the compression fails, then raise an error
    try : 
        intermediate = alg.compress(file_name) 
    except : 
        print "Unexpected error:", sys.exc_info()[0]
        raise
    # else remove the original file and return the name of the compressed file
    else : 
        compressed_file = os.path.splitext(intermediate)[0] + DEWK        
        os.rename(intermediate, compressed_file)
        os.remove(file_name)
    
        print "Compressed to: \"" + compressed_file + \
            "\" (" + str(os.path.getsize(compressed_file)) + ")"
        return compressed_file

def decompress(file_name) : 
    
    s_helpers.check_file(file_name)
    
    s_helpers.print_single_line()
    print "Decompressing File: \"" + file_name + \
        "\" (" + str(os.path.getsize(file_name)) + ")..."
    
    # return the algorithm used to compress the file
    alg = study.get_alg(file_name)
    
    ## same as compress except with decompress
    try : 
        decompressed_file = alg.decompress(file_name)
    except : 
        print "Unexpected error:", sys.exec_info()[0]
        raise
    else : 
        os.remove(file_name)
        print "Decompressed to: \"" + decompressed_file + \
            "\" (" + str(os.path.getsize(decompressed_file)) + ")\n"
        return decompressed_file
        
