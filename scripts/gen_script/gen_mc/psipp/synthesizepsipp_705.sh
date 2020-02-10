#!/bin/sh
cat psipp_Base_705 | while read line
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
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/rootfile
    cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/rootfile
    rm -rf sigMC_psipp_$PARAM_0\.root
    hadd sigMC_psipp_$PARAM_0\.root *.root
done
