/************************************************************
*
* reader.c
* 
* Willy Xiao
*
* converts a compressed file with bits to strings of 1's and 0's
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
        printf("Usage: Run FileInput FileOutput Mode\n");
        return 1;
    }

    // opens files to be read
    FILE* file_read = fopen(argv[1], "r");
    FILE* file_write = fopen(argv[2], "w"); 
    
    // check file is open
    if(file_read == NULL)
    {
        printf("Could not read: %s\n", argv[1]);
        fclose(file_write); 
        return 1;
    }
    else if (file_write == NULL)
    {
        printf("Could not write: %s\n", argv[2]); 
        fclose(file_read); 
        return 1; 
    }
    
    // copy the signature over
    int zeroes = 0; 
    int counter = 0; 
    char buffer; 
    
    char* e = malloc(sizeof(char));
    *e = 'e'; 

    if(strncmp(argv[3], e, 1) == 0)
    {
        while (zeroes < ZEROES && !feof(file_read))
        {
            if (counter < TOO_MUCH)
            {
                buffer = fgetc(file_read); 
                printf("%d\n", buffer); 
                counter++; 
                if(buffer == 0x00) zeroes++; 
                fputc(buffer, file_write);
            } 
            else 
            {
                fclose(file_read);
                fclose(file_write); 
                printf("Wrong file type"); 
                return 1; 
            }
        }
    }
    
    free(e); 

    while(!feof(file_read))
    {
        buffer = fgetc(file_read);
        
        if (buffer == EOF)
        {
            //printf("Read end of file \n"); 
            break;
        }

        for(int i = 0; i < BYTE_SIZE; i++)
        {
            if (buffer & (1 << (BYTE_SIZE - (i + 1))))
            {
                fputc('1', file_write); 
            }
            else
            {
                fputc('0', file_write); 
            }            
        }
    }
    
    fclose(file_write); 
    fclose(file_read);      
}    

