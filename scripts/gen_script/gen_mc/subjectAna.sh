#!/bin/sh

ANA=$1
INPUT=0
ls $ANA* > temp
UPLIMIT=`wc -l temp | cut -d" " -f1`

echo "./subjectAna [NAME]"
echo "[NAME]: the name defined by makeJob.csh"

# subject jobs
echo "subject jobs"

until [[ $INPUT -gt $(($UPLIMIT-1)) ]]
do
    
    ANA_NAME=$ANA"_"$INPUT".txt"

    boss.condor $ANA_NAME

    echo $ANA_NAME" done!"

    INPUT=$(($INPUT+1))
  
done

rm -rf temp

echo "all done!"   
