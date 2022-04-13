#!/bin/sh
PATCH=$1
cat X_3842_Base_705 | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # ruNo low
    PARAM_2=${arr[2]} # ruNo up
    PARAM_3=${arr[3]} # float energy poit
    PARAM_4=${arr[4]} # luminosity
    PARAM_5=${arr[5]} # dst path
    WORKAREA=/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/$PARAM_0/jobs_sig/jobs.out
    SCPTPATH=$HOME/bes/DDPIPI/v0.2/python
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM=$(echo $PARAM_0 | sed 's/-1//g')
        for f in `ls $WORKAREA/subSimRec_X_3842_*_1*` 
        do
            cd $SCPTPATH
            python get_factor.py $f $PARAM X_3842 $PATCH
        done
        continue
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    for f in `ls $WORKAREA/subSimRec_X_3842_*_1*` 
    do
        cd $SCPTPATH
        python get_factor.py $f $PARAM_0 X_3842 $PATCH
    done
done
