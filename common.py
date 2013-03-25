import sys
import string
import math
import itertools
import gzip


def yieldFastqRecord( fh ):
    """ a generator to yield a fastq record  """

    record=''
    record+= fh.readline()
    record+= fh.readline()
    record+= fh.readline()
    record+= fh.readline().strip()

    yield record

def determineAltBases( genotypes, refbase):
    """ given a list of  genotypes and the ref base, determing the segregating alt base """

    alleles= [ list(tuple(g)) for g in genotypes ]
    observed_alleles=set( list(itertools.chain.from_iterable(alleles)) )

    alt='.'
    altbases= list( observed_alleles - set(refbase) )

    if len(altbases) == 0:
        alt='.'

    elif len(altbases) > 1:
        alt=",".join(altbases )
    else:
        alt=altbases[0]
    return alt



def numericalGenotypes( refbase,altstring, genostr):
    """ given refbase and comma-delimited string of alternate bases and n-character genotype string,
    return the numerical genotype where 1 is the reference and 2 and above be alternate.
    if the reference was G and alternate was C, GC genotype would be 1/2"""


    altbases=altstring.split(',')
    altbases.sort()

    segregating_alleles=[refbase] + altbases
    numerical_alleles=range(len(segregating_alleles))

    genotype_map=dict(zip(segregating_alleles, numerical_alleles))
    genotyped_alleles=tuple(genostr)
    try:
        nmapped=[ str(genotype_map[x]) for x in genotyped_alleles ]
    except KeyError:
        print 'allele in genotype not in list of ref or alt alleles!'
        return '-1/-1'

    return "/".join(nmapped)


def indexToGenotype( index,alleles='ACGT',ploidy=2 ):
    """ return genotype at a given index position after
    enumerating all possible genotypes given string of alleles and
    assigning to a list. By default the list contains all possible 10 genotypes"""


    genotypes= [ "".join(list(genotype))  for genotype in combinations_with_replacement(alleles, ploidy) ]

    try:
       return genotypes[index]
    except IndexError:
        print "Index out of bounds, not a valid index for list of genotypes"


def genotypeToIndex( geno, ploidy=2,alleles='ACGT'):
    """ given a genotype return its index in the enumerated list of possible genotypes
    given ploidy and alleles """


    genotypes= [ "".join(list(genotype))  for genotype in combinations_with_replacement(alleles, ploidy) ]
    

    try:
        return  genotypes.index(geno)
    except ValueError:
        print "genotype not in list of genotypes."


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
    return itertools.izip_longest(fillvalue=fillvalue, *args)

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


def ErrorProb(phredscore):
    """ given a phred-scaled score, return the error prob: 10^(-Q/10) """
    return pow(10,(-phredscore/10))

	
