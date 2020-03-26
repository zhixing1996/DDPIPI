#!/bin/sh
PATCH=$1
mkdir -p /besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/psipp_shape
mkdir -p /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/psipp_shape
cat mix_Base_705 | while read line
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
    echo "Begininning of $PARAM_0!"
    cd $HOME/bes/DDPIPI/v0.2/sys_err/psipp_shape
    python mix_mc.py $PARAM_0 MC_signal psipp $PATCH
    python mix_mc.py $PARAM_0 MC_sideband psipp $PATCH
    python mix_mc.py $PARAM_0 MC_shape psipp $PATCH
    python mix_mc.py $PARAM_0 MC_mix none $PATCH
    echo "$PARAM_0 is done!"
done
