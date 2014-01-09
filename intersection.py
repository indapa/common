#!/usr/bin/env python
import sys
import os
import argparse
from common import intersect, difference

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='find intersection between lines in a file')
    parser.add_argument('fileA',  type=str,help='file A')
    parser.add_argument('fileB',  type=str,help='file B')

    args = parser.parse_args()


    fhA=open(args.fileA,'r')
    fhB=open(args.fileB,'r')

    A=[]
    B=[]
    
    for line in fhA:
         A.append( line.strip() )
    for line in fhB:
        B.append( line.strip() )

    

    for x in intersect(A,B):
        print x



if __name__ == "__main__":
    main()
