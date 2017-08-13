#!/bin/bash
line=$(head -n 1 /tmp/rcpt_cd.csv)
/usr/bin/split -l 1000000 /tmp/rcpt_cd.csv /tmp/rcpt_cd_part
#Do a for 
FILES=/tmp/rcpt_cd_part*
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  #cat $f
  sed -i '1i\'"$line" $f
done
