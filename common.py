import sys

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
