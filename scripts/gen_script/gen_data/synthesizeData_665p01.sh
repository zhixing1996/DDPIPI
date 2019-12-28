#!/bin/sh
cat Data_Base_665p01 | while read line
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
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    PARAM_0=$(echo $PARAM_0 | sed 's/-Rscan//g')
    rm -rf data_$PARAM_0\.root
    hadd data_$PARAM_0\.root *.root
done
