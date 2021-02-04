#!/bin/sh
PATCH=$1
tac ECMS_Base | while read line
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
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    cd $HOME/bes/DDPIPI/v0.2/python/sys_err/scale_factor
    echo "Begininning of $PARAM_0!"
    thresh=4316
    if [ $PARAM_0 -gt $thresh ]; then
        python fit_rm_Dpipi.py $PARAM_0 D1_2420 $PATCH
        # python fit_rm_Dpipi_sideband.py $PARAM_0 D1_2420 $PATCH
    fi
    # python fit_rm_Dpipi.py $PARAM_0 data $PATCH
    python fit_rm_Dpipi.py $PARAM_0 psipp $PATCH
    python fit_rm_Dpipi.py $PARAM_0 DDPIPI $PATCH
    # python fit_rm_Dpipi_sideband.py $PARAM_0 data $PATCH
    # python fit_rm_Dpipi_sideband.py $PARAM_0 psipp $PATCH
    # python fit_rm_Dpipi_sideband.py $PARAM_0 DDPIPI $PATCH
    echo "$PARAM_0 is done!"
done
