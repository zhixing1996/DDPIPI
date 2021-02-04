#!/bin/sh
cat incMC_Base | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # inc MC type
    PARAM_2=${arr[2]} # float energy point
    PARAM_3=${arr[3]} # path
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/$PARAM_1/$PARAM_0/rootfile
    cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/$PARAM_1/$PARAM_0/rootfile
    rm -rf incMC_$PARAM_1\_$PARAM_0\.root
    hadd incMC_$PARAM_1\_$PARAM_0\.root *.root
done
