/************************************************************
*
* writer.c
* 
* Willy Xiao
*
* converts a compressed algorithm with strings of 1's and 0's to bytes
* 
*************************************************************/
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define ZEROES 2
#define TOO_MUCH 100
#define BYTE_SIZE 8

/******************
*
* writer
*
********************/
int main(int argc, char* argv[])
{
    // check to ensure proper usage
    if(argc != 4)
    {
        printf("Usage: Run FileInput FileOutput Mode");
        return 1;
    }

    // opens files to be read
    FILE* file_read = fopen(argv[1], "r");
    FILE* file_write = fopen(argv[2], "w"); 
    
    // check file is open
    if(file_read == NULL)
    {
        printf("writer.c 40\nCould not read file: %s\n", argv[1]);
        fclose(file_write);
        fclose(file_read);  
        return 1;
    }
    else if (file_write == NULL)
    {
        printf("writer.c 46\nCould not write file: %s\n", argv[2]); 
        fclose(file_read); 
        fclose(file_write); 
        return 1; 
    }

    int buffer; 
    uint8_t zero = 0x00; 
    char* e = malloc(sizeof(char));
    *e = 'e'; 
    
    if(strncmp(argv[3],e, 1) == 0)
    {    
        // copy the signature over
        int zeroes = 0; 
        int counter = 0; 
        
        while (zeroes < ZEROES && !feof(file_read))
        {
            if (counter < TOO_MUCH)
            {
                buffer = fgetc(file_read); 
                counter++; 
                if(buffer == 0x00) zeroes++; 
                fputc(buffer, file_write);
            } 
            else 
            {
                fclose(file_read);
                fclose(file_write); 
                printf("writer.c 75\nFile not of type dewk compressed_file\n"); 
                return 1; 
            }
        }
    }
    
    free(e); 
    
    uint8_t write_buffer = zero; 
    int just_wrote = 0; 
        
    while(!feof(file_read))
    {
        for(int i = 0; i < BYTE_SIZE; i++)
        {
            buffer = fgetc(file_read);
            if (buffer == EOF)
            {
                if(just_wrote != 1)
                {
                    fputc(write_buffer, file_write); 
                }
    
                fclose(file_write); 
                fclose(file_read);  
                return 0;
            }            
            else if (buffer == '1') 
            {
                write_buffer = write_buffer | (1 << (BYTE_SIZE - (i + 1)));
            }
            else if (buffer == '0')
            {
                // do nothing
            }
            else
            {
                fclose(file_read);
                fclose(file_write); 
                printf("writer.c\nRead this char: %c\n", buffer); 
                printf("Should have been either a 1 or a 0\n"); 
                return 1; 
            }

            just_wrote = 0;     
        }

        fputc(write_buffer, file_write);
        write_buffer = zero;  
        just_wrote = 1; 
    }

    fclose(file_read); 
    fclose(file_write); 
    return 0; 
}    

