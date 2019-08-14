#!/bin/sh

ANA=$1
RUNNO_LOW=$2
RUNNO_UP=$3
INPUT=0
ls $ANA* > temp
UPLIMIT=`wc -l temp | cut -d" " -f1`

echo "./subjectAna.sh [NAME] [RUNNO_LOW] [RUNNO_UP]"
echo "[NAME]: the name defined by makeJob.csh"
echo "[RUNNO_LOW]: the smallest runNo"
echo "[RUNNO_UP]: the largest runNo"

# subject jobs
echo "subject jobs"

until [[ $RUNNO_LOW -gt $RUNNO_UP ]]
do
    
    ANA_NAME=$ANA$RUNNO_LOW".txt"

    boss.condor $ANA_NAME

    echo $ANA_NAME" done!"

    RUNNO_LOW=$(($RUNNO_LOW+1))
  
done

rm -rf temp

echo "all done!"   
