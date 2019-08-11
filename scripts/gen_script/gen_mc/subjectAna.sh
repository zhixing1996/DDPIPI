#!/bin/sh

ANA=$1
INPUT=$2
UPLIMIT=$3

echo "./subjectAna [NAME] [NUM1] [NUM2]"
echo "[NAME]: the name defined by makeJob.csh"
echo "[NUM1]: the minimum number range of job subjected"
echo "[NUM1]: the maximum number range of job subjected"

# subject jobs
echo "subject jobs"

until [ $INPUT -gt $UPLIMIT ]
do
    
    ANA_NAME=$ANA"_"$INPUT".txt"

    boss.condor $ANA_NAME

    echo $ANA_NAME" done!"

    INPUT=$(($INPUT+1))
  
done

echo "all done!"   
