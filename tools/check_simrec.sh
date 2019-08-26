#!/bin/bash

rm -rf badList
rm -rf goodList

#set +x
ANA_DIR=$1
echo "This is a script to check whether the job is successful or not"
echo "./check.sh [PATH]"
echo "[PATH]: job log path"

echo Current dir: $ANA_DIR
cd $ANA_DIR
ls *.0 > badList
total_num=`wc -l badList | cut -d" " -f1`
#ls *.txt > badList
grep -in 'survived event ' *.0 | cut -d "." -f1 > goodList
good_num=`wc -l goodList | cut -d" " -f1`

while read MY_LINE
do
	#echo $MY_LINE
	sed -i "/$MY_LINE/d" badList
done < goodList 
bad_num=`wc -l badList | cut -d" " -f1`
echo total: $total_num  success: $good_num jobs, failed $bad_num jobs
