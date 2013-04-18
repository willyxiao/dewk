"""
CS51 Final Project
Eamon, David, Kevin, Willy

fib.py by Willy Xiao
willy@chenxiao.us

fib.py is a module that implements the fibonacci coding compression: 
[citation]

1. fib.compress compresses a file outputting FileName.fib to disk. 
2. fib.decompress takes in a file outputting FileName.FileType to disk. 
"""
import unittest 

# compress takes in a string of the file name to compress 
# and outputs a compressed file to disk
def compress(file_in_name):
  file_in = open(file_in_name, "r")
  while (str != EOF) : 
    str = file_in.read(1) 
    print (str);
  file_in.close(); 

# helper function which encodes a single integer less than or equal to 1 into a 
# fibonacci sequence. 
# This builds upon the function from http://en.wikipedia.org/wiki/Fibonacci_coding. 4/18/2013

def _encode_fib(n):
    assert n >= 1

    # Return string with Fibonacci encoding for n (n >= 1).
    result = ""
    if n >= 1:
        a = 1
        b = 1
        c = a + b   # next Fibonacci number
        fibs = [b]  # list of Fibonacci numbers, starting with F(2), each <= n
        while n >= c:
            fibs.append(c)  # add next Fibonacci number to end of list
            a = b
            b = c
            c = a + b
#        result = "1"  # extra "1" at end
        for fibnum in reversed(fibs):
            if n >= fibnum:
                n = n - fibnum
                result = "1" + result
            else:
                result = "0" + result
    return result

# decompress takes in a string of the file name to decompress 
# and outputs a decompressed file to disk 
def decompress(file):
  print file;
