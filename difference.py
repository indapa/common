#!/usr/bin/env python
import sys
import os
import argparse


def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='find difference  between lines in a file')
    parser.add_argument('-A',  type=str,help='file A')
    parser.add_argument('-B',  type=str,help='file B')
    parser.add_argument('-cardinality', dest='card', action='store_true')

    args = parser.parse_args()


    fhA=open(args.A,'r')
    fhB=open(args.B,'r')

    A=[]
    B=[]
    
    for line in fhA:
         A.append( line.strip() )
    for line in fhB:
        B.append( line.strip() )


    setA= set(A)
    setB = set(B)

    setdifference = setA.difference(setB)

    if args.card == False:
        for elem in list(setdifference):
            print elem

    else:
        print len(setdifference)    



if __name__ == "__main__":
    main()
