#!/bin/sh

rm -rf job.out
mkdir job.out
rm -rf job.err
mkdir job.err

INPUT=1
UPLIMIT=1

SIM="jobOptions_sim_sig_D1_2420_D_4360"
REC="jobOptions_rec_sig_D1_2420_D_4360"

SUB="jobOptions_sub_sig_D1_2420_D_4360"

# subject jobs
echo "subject jobs"

until [ $INPUT -gt $UPLIMIT ]
do

    
    SIM_NAME="boss.exe "$SIM"_"$INPUT".txt"
    REC_NAME="boss.exe "$REC"_"$INPUT".txt"
    SUB_NAME=$SUB"_"$INPUT".sh"
    touch $SUB_NAME
    chmod 700 $SUB_NAME

    echo "#!/bin/sh" > $SUB_NAME
    echo $SIM_NAME >> $SUB_NAME
    echo "sleep 300" >> $SUB_NAME
    echo $REC_NAME >> $SUB_NAME
    
    echo $SUB_NAME" done!"

    hep_sub -g physics $SUB_NAME -o ./job.out -e ./job.err

    INPUT=$(($INPUT+1))
  
done

echo "all done!"   
