"""
CS51 Final Project
Eamon, David, Kevin, Willy

helpers.py by Willy Xiao
willy@chenxiao.us

helpers.py is a module that includes helper functions for encoding. 
Also helps standardize everything. 
"""
import string
import os
import subprocess
import io

ZERO = bytearray(1)
TOO_MUCH = 100
READ_IN_SIZE = 1

# ensign(file_name, alg_name) returns the signature for the algorithm and file type, and a new file name
def ensign(file_name, alg_name) : 

    # the extension (e.g. "picture.jpg" becomes jpg)
    type_index = string.rfind(file_name, "."); 
    if type_index == -1 : 
        extension = ""
    else : 
        extension = file_name[(type_index + 1):]
    
    # signature is returned
    sign = alg_name + ZERO + extension + ZERO
    
    # the name of the new file is given 
    name = file_name[:type_index] + "." + alg_name + "t"

    return (free_name(name), sign)

# unsign(file_name) returns the compression algorithm used and a name of an
# uncompressed file that can be saved to disk
def unsign(file_name) : 
    try: 
        with open(file_name, "r") as file :     

            counter = 0 
            alg_name = "" 
            extension_name = ""

            # for the name of the algorithm
            i = file.read(1)
            while i != ZERO : 
                alg_name += i 
                i = file.read(1)

                # this checks if counter goes over the amount before giving up
                counter += counter
                if counter > TOO_MUCH :
                    raise IncorrectFileType
                    break
    
            # for the name of the extension
            i = file.read(1)
            while i != ZERO : 
                extension_name += i
                i = file.read(1)

                counter += counter
                if counter > TOO_MUCH :
                    raise IncorrectFileType
                    break
            
            # new file name
            period_at = string.rfind(file_name, "."); 
            
            new_file_name = file_name[:period_at] + "." + extension_name

            return (alg_name, free_name(new_file_name))
        
    except IOError : 
        print ("Error opening " + file_name);     

# returns a frequency list of all the bytes in a file,
# the "specific" mode also appends a decimal value to the 
# end of the frequency representing the byte, this is used for huff
def freq_list(file_in, mode) : 

    # initialize file, empty dictionary, and first byte
    f = io.FileIO(file_in, "r")
    freq_dict = {}
    byte = f.read(READ_IN_SIZE)

    # reads through the file, adding one to the frequency
    # of each byte read, if the mode is to sample, then only the first 500 bytes are returned
    counter = 0

    while (byte != ''):
        if byte in freq_dict:
            freq_dict[byte] += 1
        elif mode == "specific" :
            freq_dict[byte] = 1 + (ord(byte)/1000.)
        else :
            freq_dict[byte] = 1
        byte = f.read(READ_IN_SIZE)

        counter += 1
        if mode == "sample" and counter > 500 : 
            break 

    # converts the dictionary to a list and returns the list
    freq_list = []        
    for key in freq_dict:
        freq_list.append((freq_dict[key],key))
        
    return freq_list

# start_compress returns a file that python can read from and another it can write to
def start_compress(file_in_name, alg_name) : 
    (file_out_name, sign) = ensign(file_in_name, alg_name)  
    file_out = io.open(file_out_name, "wb") 
    file_out.write(sign)
    file_in = io.FileIO(file_in_name, "r")
    return (file_in,file_out)

# end_compress closes the files and calls the writer on the intermediate file, writes the result to disk
def end_compress(file_in,file_out) : 
    file_in.close()
    file_out.close()
    subprocess.call([abs_path("writer"), file_out.name, file_out.name[:-1], "e"])
    subprocess.call(["rm", "-f", file_out.name])
    return file_out.name[:-1]

# start_decompress returns a file that can be read in, one that can be string'd to, 
# and another name for the final output file
def start_decompress(file_name, alg_name) : 
  #get the signature and creat the temporary file name
  (alg, new_file_name) = unsign(file_name); 
  tmp_name = free_name(new_file_name + ".t")
  tmp_name2 = free_name(tmp_name + "t")

  #ensure that the compression algorithm was indeed fibonacci
  assert(alg == alg_name)

  #convert binary file to string of 1's and 0's
  subprocess.call([abs_path("reader"), file_name, tmp_name, "e"])  
  
  file_out = open(tmp_name2, "w")
  file_in = open(tmp_name, "r") 
  
  #get rid of the signature at the front
  zero = 0 
  counter = 0
  while(zero < 2) : 
    if(counter > TOO_MUCH) : 
        return "failure"
    elif (file_in.read(READ_IN_SIZE) == bytearray(1)) : 
        zero += 1
    counter += 1

  return (file_in, file_out)

# finishing decompression
def end_decompress(file_in, file_out) :   
    file_in.close()
    file_out.close()
    output = free_name(file_in.name[:-2])
    subprocess.call([abs_path("writer"), file_out.name, output, "no"])
#    subprocess.call(["rm", "-f", file_out.name])
#    subprocess.call(["rm", "-f", file_in.name])
    return output
    
# free_name takes in a name and returns a new_name that doesn't overwrite any 
# files
def free_name(name) : 
    c = 0 
    new_name = name; 
    
    # keep repeating until a new name is found that is free
    while(os.path.exists(new_name)) : 
        type_index = string.rfind(name, ".")
        new_name = name[:type_index] + str(c) + name[type_index:]
        c += 1
    return new_name

# this returns the name of the algorithm used
def which_alg(file_name) : 
    (alg_name, trash) = unsign(file_name)
    return alg_name

# converts an integer to its binary representation for the size wanted
def to_bin(n, size) : 
    b = bin(n)[2:]
    # append zeroes to the front of binary number if it isn't full
    while(len(b) < size) : 
        b = '0' + b
    return b
    
# returns the size of the file
def size(file_name) : 
    return os.path.getsize(file_name)

# returns the absolute path of a file/script inside the same directory as helpers
def abs_path(file_name) : 
    path = os.path.abspath(__file__)
    pos = string.rfind(path, "/")
    path = path[:(pos + 1)]
    return path + file_name

