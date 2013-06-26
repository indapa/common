#!/usr/bin/env python
import sys
import os
import string
import re
import argparse
from common import yieldFastaRecord, writefasta_stdout

""" write out subsequence from fasta file to stdout """

def main():
    usage = "usage: %prog [options] file.fa "
    parser = argparse.ArgumentParser(description='filter records  based on genotypes')
    
    parser.add_argument('-start', type=int, help='zero based start index')
    parser.add_argument('-end', type=int, help='one-based end index')
    parser.add_argument('fasta',  type=str,help='file.fa file')
    

    args = parser.parse_args()
    
    fh=open(args.fasta,'r')
     
    for (header, sequence) in yieldFastaRecord(fh):
       
        writefasta_stdout(sequence[args.start:args.end], header+":"+str(args.start)+"-"+str(args.end))
if __name__ == "__main__":
    main()
