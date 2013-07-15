#/usr/bin/bash
#make a glf file with help of UMich modified samtools
#see this: http://genome.sph.umich.edu/wiki/Polymutt#Creation_of_GLF_files
EXPECTED_ARGS=1
E_BADARGS=65
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` {file.bam}"
  exit $E_BADARGS
fi

BAM=$1
BIN=/share/home/indapa/software/samtools-0.1.7a-hybrid
REFERENCE=/share/home/indapa/MySimulations/Simulation1/Reference/simref.1.fa

$BIN/samtools-hybrid view -bh $BAM simref.1:1-1000000 $BIN/samtools-hybrid calmd -Abr - $REFERENCE 2> /dev/null | $BIN/samtools-hybrid pileup - -g -f $REFERENCE  > $BAM.glf 2> glf.stderr

if [ $? -ne 0 ]; then
    echo "samtools-hybrid error"
fi
