#!/bin/sh
cat Data_Base_703p01 | while read line
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
    echo /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    rm -rf data_$PARAM_0\.root
    hadd data_$PARAM_0\.root *.root
    cd ..
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        dir=$(echo $PARAM_0 | sed 's/-1//g')
        mkdir -p $dir
        mv /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM_0\.root ./$dir
    elif [[ $PARAM_0 == *$shortbar2* ]]; then
        dir=$(echo $PARAM_0 | sed 's/-2//g')
        mkdir -p $dir
        mv /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM_0\.root ./$dir
        cd $dir
        rm -rf data_$dir\.root
        hadd data_$dir\.root data_$dir-1.root data_$dir-2.root
    else
        echo "No need to change for $PARAM_0"
    fi
done
