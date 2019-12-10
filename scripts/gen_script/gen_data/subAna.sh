#!/bin/sh

ANA=$1
ls $ANA*".txt" > temp

echo "./subjectAna.sh [NAME]"
echo "[NAME]: the name defined by makeJob.csh"

# subject jobs
echo "subject jobs"

for line in $(cat temp)
do

    boss.condor $line

    echo $line" done!"

done

rm -rf temp

echo "all done!"   
