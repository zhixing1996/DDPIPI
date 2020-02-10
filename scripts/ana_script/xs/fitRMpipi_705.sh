#!/bin/sh
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
    cd $HOME/bes/DDPIPI/v0.2/python
    echo "Begininning of $PARAM_0!"
    python fit_rm_pipi.py $PARAM_0 sig 
    python fit_rm_pipi.py $PARAM_0 none_sig
    python fit_rm_pipi.py $PARAM_0 upper_limit
    echo "$PARAM_0 is done!"
done
