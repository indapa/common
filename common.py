import sys
import string
import math
from itertools import *

def writefasta(sequence, name, filename):
	fh=open(filename, 'w')
        l = len( sequence )
        c = 0
        fh.write( ">%s\n" % name )
        while c < l:
            b = min( c + 50, l )
            fh.write( "%s\n" % str( sequence[c:b] ) )
            c = b
def order(j,k): 
	return (k * (k + 1) / 2) + j


""" iterate through an utterable n values at a time
     http://stackoverflow.com/a/2990151         """
def grouper(n, iterable, fillvalue='x'):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

""" for reverse complementing a sequence """
def complement(s):
     """Return the complementary sequence string."""
     basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
     letters = list(s)
     letters = [basecomplement[base] for base in letters]
     return ''.join(letters)

def reversecomplement(s):
     """Return the reverse complement of the dna string."""
     s = s[::-1]
     s = complement(s)
     return s


def typeofGenotype(allele1, allele2):
    """ I really should be a python version of a typedef here, but dont know how
        hom_ref =0 het =1 hom_nonref=2 no_call=3                              """

    #print allele1, allele2


    if allele1== '.' or allele2 == '.': return 3

    if allele1 == '0' and allele2 == '0': return 0

    if allele1 == '0' and allele2 != '0': return 1
    if allele1 != '0' and allele2 == '0': return 1


    #if allele1 == '0' and allele2== '1': return 1
    #if allele1 =='1' and allele2 == '0': return 1

    if allele1 != '0' and allele2 != '0': return 2

def isTransition(allele1, allele2):
    
    if allele1 == 'A':
        if allele2 == 'G':
            return True
    elif allele1 == 'G':
        if allele2 == 'A':
            return True
    elif allele1 == 'C':
        if allele2 == 'T':
            return True
    elif allele1 == 'T':
        if allele2 == 'C':
            return True
    else:
        sys.stderr.write("skipping indel for transition/transversion classification\n")
        
    return False


def yield_bedcoordinate(fh):
    """ yield a tuple of (chr, start,end) from bed file """
    for line  in fh:
        if '@' in line: continue
        fields=line.strip().split("\t")
        (chr, start, end) = fields[0:3]
        yield(chr, int(start), int(end) )

def PhredScore(errorprob):
    """ given an error probbability, return the phred-scaled value: -10 * log_10(error) """
    return   -10 * math.log10(errorprob)


def ErrorProb(phredScore):
    """ given a phred-scaled score, return the error prob: 10^(-Q/10) """
    return pow(10,(-phredscore/10))

	
