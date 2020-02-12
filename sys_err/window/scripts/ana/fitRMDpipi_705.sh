#!/bin/sh
PATCH=$1
cat ECMS_Base_705 | while read line
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
    cd $HOME/bes/DDPIPI/v0.2/sys_err/window
    echo "Begininning of $PARAM_0!"
    thresh=4290
    if [ $PARAM_0 -ge $thresh ]; then
        python fit_rm_Dpipi.py $PARAM_0 data $PATCH
        python fit_rm_Dpipi.py $PARAM_0 D1_2420 $PATCH
        python fit_rm_Dpipi.py $PARAM_0 psipp $PATCH
        python fit_rm_Dpipi.py $PARAM_0 DDPIPI $PATCH
    else 
        python fit_rm_Dpipi.py $PARAM_0 data $PATCH
        python fit_rm_Dpipi.py $PARAM_0 psipp $PATCH
        python fit_rm_Dpipi.py $PARAM_0 DDPIPI $PATCH
    fi
    echo "$PARAM_0 is done!"
done
