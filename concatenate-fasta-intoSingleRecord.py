#!/usr/bin/env python
import sys
import os
import string
import re
import argparse
import itertools
from common import yieldFastaRecord, writefasta

def main():
    usage = "usage: %prog [options] file.fa "
    parser = argparse.ArgumentParser(description='concatenate records from seperate fasta files into a single fasta record ')
    parser.add_argument('fastafile', metavar='fastafile', type=str, nargs='+',
                   help='sample names to remove')
    
    parser.add_argument('-header',  type=str,help='header of new concatenated fasta record (header will also serve as the newfilename')
    
    
    

    args = parser.parse_args()

    print args


    fastafilehandles=list(itertools.imap(open, args.fastafile)) #list of filehandles for fastq files
    
    concatenateseq=''
    
    for fh in fastafilehandles:
         for (header, sequence) in yieldFastaRecord(fh):
             concatenateseq+=sequence
             
    
    writefasta(concatenateseq,args.header, args.header+".fa")

if __name__ == "__main__":
    main()
