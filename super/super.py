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

def compress(file_name) :
    alg = study.best_alg(file_name)
    return alg.compress(file_name)

def decompress(file_name) : 
    alg = study.get_alg(file_name)
    return alg.decompress(file_name)
