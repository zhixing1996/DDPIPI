#!/bin/bash

rm -rf totList
rm -rf badList
rm -rf goodList

#set +x
ANA_DIR=$1
echo "This is a script to check whether the job is successful or not"
echo "./check_simrec.sh [PATH]"
echo "[PATH]: job log path"

echo Current dir: $ANA_DIR
cd $ANA_DIR
ls *.0 | cut -d "." -f1 > totList
total_num=`wc -l totList | cut -d" " -f1`
grep -in 'DstHltMaker       SUCCESS' *.0 | cut -d "." -f1 > goodList
good_num=`wc -l goodList | cut -d" " -f1`

diff totList goodList > badList
bad_num=`wc -l badList | cut -d" " -f1`
let "bad_num = $bad_num - 1"
if [ $bad_num -lt 0 ]; then let "bad_num = 0"; fi
echo total: $total_num  success: $good_num jobs, failed $bad_num jobs
