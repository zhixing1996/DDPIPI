#!/bin/sh
PATCH=$1
mkdir -p /besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/BW
mkdir -p /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/BW
cat psipp_Base | while read line
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
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    echo "Begininning of $PARAM_0!"
    cd $HOME/bes/DDPIPI/v0.2/python/sys_err/BW
    threshold=4316
    if [[ $PARAM_0 -gt $threshold ]]; then
        python mix_mc.py $PARAM_0 MC_signal D1_2420 $PATCH
    fi
    python mix_mc.py $PARAM_0 MC_signal psipp $PATCH
    python mix_mc.py $PARAM_0 MC_signal DDPIPI $PATCH
    python mix_mc.py $PARAM_0 MC_mix none $PATCH
    python mix_mc.py $PARAM_0 raw none $PATCH
    echo "$PARAM_0 is done!"
done
