/************************************************************
*
* huff.c
* 
* Willy Xiao
*
* Compresses a file using huffman
* 
*************************************************************/
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "huffile.h"
#include "forest.h"
#include "tree.h"

#define MAX_UNSIGNED 0xffffffff

// structure of a code which includes a list of bits and an integer displaying how many bits are relevant to the code
typedef struct
{
    uint32_t list;
    int extra;
}
code; 

// creates an array of codes for all of the symbols
code codes[SYMBOLS];

// orders the forest into a hierarchy of trees
void order(Forest* f); 

// makes the codes for all of the symbols in a huffman-tree, p must start as zero
void makecodes(Tree* t, int p, code* cbuffer);

// writes codes from one file to a huffile
void writecodes(FILE* f, Huffile* g);

/******************
*
* Let's go, baby
*
********************/
int main(int argc, char* argv[])
{
    // check to ensure proper usage
    if(argc != 3)
    {
        printf("Usage: Run FileName HuffileName\n");
        return 1;
    }

    // opens file to be read
    FILE* big = fopen(argv[1], "r");
    
    // check file is open
    if(big == NULL)
    {
        printf("Could not open: %s\n", argv[1]);
        return 1;
    }
    
    // declares all of the trees
    Tree* trees[SYMBOLS];
    
    // intializes all of the trees
    for(int i = 0; i < SYMBOLS; i++)
    {
        trees[i] = malloc(sizeof(Tree));

        // symbol is the ASCII symbol of int i
        trees[i]->symbol = (char) i;
        
        // frequency to zero and pointers to NULL
        trees[i]->frequency = 0;
        trees[i]->left = NULL;
        trees[i]->right = NULL;
    }    
   
    // increments the frequency of each symbol
    for(int i = fgetc(big); i != EOF; i = fgetc(big))
    {
            trees[(i + SYMBOLS) % SYMBOLS]->frequency++;
    }

    // puts the reader at the beginning of the stream again
    fseek(big, 0, SEEK_SET);

    // makes a forest
    Forest* jungle = mkforest();

    // johnny appleseeds all of the trees into the forest
    for(int i = 0; i < SYMBOLS; i++)
        plant(jungle, trees[i]);                    
     
    // creates header for the huffile
    Huffeader* header = malloc(sizeof(Huffeader));

    // initializes the magic number and the sum
    header->magic = MAGIC;
    header->checksum = 0;
    
    // copies all of the frequencies from the array of trees to the header and increments the checksum
    for(int i = 0; i < SYMBOLS; i++)
    {
        header->frequencies[i] = trees[i]->frequency;
        header->checksum += trees[i]->frequency;
    }

    // order the forest into a huffman-tree
    order(jungle);
    
    // creates a buffer to create the codes of each symbol
    code* cbuffer = malloc(sizeof(code));
    
    // makes the codes for all of the symbols, the depth starts at zero
    makecodes(jungle->first->tree, 0, cbuffer);
    
    // frees cbuffer's memory
    free(cbuffer);
    
    // opens huffile to be written
    Huffile* small = hfopen(argv[2], "w");
    
    // check file is open
    if(small == NULL)
    {
        // if not, yell and close everything
        printf("Could not write %s\n", argv[2]);
        fclose(big);
        for(int i = 0; i < SYMBOLS; i++)
        {
            if(trees[i]->frequency == 0)
                free(trees[i]);
        }
        rmforest(jungle);
        free(header);
        return 1;
    }

    // writes the header to the huffile
    hwrite(header, small);
    
    // writes the codes to the huffile
    writecodes(big, small);
    
    // closes everything and frees all memory
    fclose(big);
    for(int i = 0; i < SYMBOLS; i++)
    {
        if(trees[i]->frequency == 0)
            free(trees[i]);
    }
    rmforest(jungle);
    free(header);
    hfclose(small);
    
    // that's all David DiCurcio!
    return 0;
}

/******************
* Orders a forest into a huffman-tree
*******************/
void order(Forest* f)
{
    // declares two pointers to trees 
    Tree* a;
    Tree* b;

    // iterates until there is only one tree in the forest
    for(a = pick(f), b = pick(f); b != NULL; a = pick(f), b = pick(f))
    { 
        // creates a new tree so that the smaller trees can be combined
        Tree* c = mktree();
        
        // fills in information for new tree, symbol is NUL, frequency is the combination of the other frequencies
        c->symbol = '\0'; 
        c->frequency = a->frequency + b->frequency;
        
        // the left side points at first pick, the right side points at second
        c->left = a;
        c->right = b; 
                
        // plants the new tree back into the forest
        plant(f, c);
    }    
    
    // plant the only tree back into the forest
    plant(f, a);
}

/*********************
* Makes the codes for all of the symbols in the tree
**********************/
void makecodes(Tree* t, int p, code* cbuffer)
{
    // if the depth is at zero, set the buffer list to zero and extra to 1
    if(p == 0)
    {
        cbuffer->list = 0;
        cbuffer->extra = 1;
    } 
    
    // if it's at the end of a branch
    if(t->left == NULL)
    {
        // set the number of relevant bits as the depth of the tree
        cbuffer->extra = p;
        // set the code to equal buffer
        codes[(int) (t->symbol + SYMBOLS) % SYMBOLS] = *cbuffer;
        //reset buffer and return
        cbuffer->list = cbuffer->list & (MAX_UNSIGNED - (1 << (p -1)));
        return;
    }
    
    // recursion for left branch with incremented depth
    makecodes(t->left, p + 1, cbuffer);

    // change the value of cbuffer so that a 1 is recorded for moving right
    cbuffer->list = cbuffer->list | (1 << (p));

    // recursion for right branch with incremented depth
    makecodes(t->right, p + 1, cbuffer);
    
    // reset buffer and return
    cbuffer->list = cbuffer->list & (MAX_UNSIGNED - (1 << (p-1)));
    return;
}

/********************
*Writes all of the code from an original file to a huffile
********************/
void writecodes(FILE* f, Huffile* g)
{
    // iterates over all of the characters in the original file
    for(int i = fgetc(f); i != EOF; i = fgetc(f))
    {
        // iterates over the bits that are relevant
        for(int j = 0; j < codes[(int) (i + SYMBOLS) % SYMBOLS].extra; j++)
        {
            // if the bit in place "j" isn't zero, write a one
            if((codes[(int) (i + SYMBOLS) % SYMBOLS].list & (1 << j)) != 0)
                bwrite(1, g);                
            // else, write a zero
            else
                bwrite(0, g); 
        }           
    }
}
