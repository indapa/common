for x in *.fa; 
do 
filename=$(basename $x); 
filename=${filename%.*}; 
echo $filename; 
faToTwoBit $x $filename.2bit;
done