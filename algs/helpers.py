"""
CS51 Final Project
Eamon, David, Kevin, Willy

helpers.py by Willy Xiao
willy@chenxiao.us

helpers.py is a module that includes helper functions for encoding. 
Also helps standardize everything. 
"""
import string

ZERO = bytearray(1)
GIVE_UP = 100

# the signature at the beginning of each compressed file. 
# This consists of the name of the algorithm, followed by zero byte followed by old extension followed by zero
def ensign(file_name, alg_name) : 
    type_index = string.rfind(file_name, "."); 

    # uncompressed file type extension
    if type_index == -1 : 
        extension = ""
    else : 
        extension = file_name[(type_index + 1):]
    
    sign = alg_name + ZERO + extension + ZERO
    
    name = file_name[:type_index] + "." + alg_name

    return (name, sign)

#get types takes in a compressed file and returns
#[name of the compresson algorithm, name of extension]
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
                if counter > GIVE_UP :
                    raise IncorrectFileType
                    break
    
            # for the name of the extension
            i = file.read(1)
            while i != ZERO : 
                extension_name += i
                i = file.read(1)

                counter += counter
                if counter > GIVE_UP :
                    raise IncorrectFileType
                    break

        return (alg_name, extension_name)
        
    except IOError : 
        print ("Error opening " + file_name); 
        file.close();     


