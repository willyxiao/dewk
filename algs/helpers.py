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
        file.close();     

def start_compress(file_in_name, alg_name) : 
    (file_out_name, sign) = ensign(file_in_name, alg_name)  
    file_out = io.open(file_out_name, "wb") 
    file_out.write(sign)
    file_in = io.FileIO(file_in_name, "r")
    return (file_in,file_out)

def end_compress(file_in,file_out) : 
    file_in.close()
    file_out.close()
    subprocess.call(["./writer", file_out.name, file_out.name[:-1], "e"])
    subprocess.call(["rm", "-f", file_out.name])

def start_decompress(file_name, alg_name) : 
  #get the signature and creat the temporary file name
  (alg, new_file_name) = unsign(file_name); 
  tmp_name = free_name(new_file_name + ".t")
  tmp_name2 = free_name(tmp_name + "t")

  #ensure that the compression algorithm was indeed fibonacci
  assert(alg == alg_name)

  #convert binary file to string of 1's and 0's
  subprocess.call(["./reader", file_name, tmp_name, "e"])  
  
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

  return (file_in, file_out, new_file_name)

def end_decompress(file_in, file_out, new_file_name) :   
    file_in.close()
    file_out.close()
    subprocess.call(["./writer", file_out.name, new_file_name, "no"])
    subprocess.call(["rm", "-f", file_out.name])
    subprocess.call(["rm", "-f", file_in.name])

def free_name(name) : 
    c = 0 
    new_name = name; 
    while(os.path.exists(new_name)) : 
        type_index = string.rfind(name, ".")
        new_name = name[:type_index] + str(c) + name[type_index:]
        c += 1
    return new_name
