import sys
import string

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
