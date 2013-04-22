'''
CS51 Final Project
Eamon, David, Kevin, Willy

huff.py by Kevin Eskici
keskici@college.harvard.edu
'''

import io
import helpers
import queue
# installed bitstream for this: 
# "sudo python setup.py install" after downloading from
# http://code.google.com/p/python-bitstring/
from bitstream import BitStream, BitArray

READ_IN_SIZE = 1
ALG_NAME = "huf"
BYTE_SIZE = 8

global buffer
buffer = 0x00

global buffer_pos
buffer_pos = 0

### COMPRESS ###

def compress(file_in_name):
    global buffer
    global buffer_pos

    #open output file and sign
    (file_out_name, sign) = helpers.ensign(file_in_name, ALG_NAME)
    file_out = io.open(file_out_name, "wb")
    file_out.write(sign)

    file_in = io.open(file_in_name, "r")
    i = file_in.read(READ_IN_SIZE)



#insert actual compression part


    file_in.close();
    file_out.close()



#citation-parts from http://stackoverflow.com/questions/11587044
#/how-can-i-create-a-tree-for-huffman-encoding-and-decoding
def _build_tree(frequency_list)
  q = queue.PriorityQueue()
  for val in frequency_list
      q.put(val)
  while q.qsize() > 1:
      smallest, next_smallest = q.get(),q.get()



